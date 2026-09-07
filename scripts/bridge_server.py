"""XHS Extension Bridge Server

Extension 连接到这里（WebSocket），CLI 命令通过同一端口发送（role=cli），
Bridge 将命令路由给 Extension 并把结果返回给 CLI。

启动方式：
    python scripts/bridge_server.py

端口：9333（可通过 --port 覆盖）
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import uuid
from typing import Any

import websockets
from websockets.server import ServerConnection

logger = logging.getLogger("xhs-bridge")


class BridgeServer:
    def __init__(self) -> None:
        self._extension_ws: ServerConnection | None = None
        self._extension_info: dict[str, Any] = {}
        self._pending: dict[str, tuple[asyncio.Future[Any], ServerConnection]] = {}

    async def handle(self, ws: ServerConnection) -> None:
        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=10)
        except Exception as e:
            logger.warning("握手超时或失败: %s", e)
            return

        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            return

        role = msg.get("role")
        if role == "extension":
            await self._handle_extension(ws, msg)
        elif role == "cli":
            await self._handle_cli(ws, msg)
        else:
            logger.warning("未知 role: %s", role)

    # ─── Extension 端（长连接） ───────────────────────────────────────

    async def _handle_extension(self, ws: ServerConnection, handshake: dict[str, Any]) -> None:
        logger.info("Extension 已连接: version=%s", handshake.get("version", "unknown"))
        self._extension_ws = ws
        self._extension_info = {
            "version": handshake.get("version"),
            "protocol_version": handshake.get("protocol_version"),
            "extension_id": handshake.get("extension_id"),
            "connected_at": handshake.get("connected_at"),
        }
        try:
            async for raw in ws:
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if msg.get("type") == "heartbeat":
                    continue
                msg_id = msg.get("id")
                pending = self._pending.get(msg_id) if msg_id else None
                if pending and pending[1] is ws:
                    future, _ = self._pending.pop(msg_id)
                    if not future.done():
                        future.set_result(msg)
        finally:
            if self._extension_ws is ws:
                self._extension_ws = None
                self._extension_info = {}
                logger.info("当前 Extension 已断开")
            else:
                logger.info("旧 Extension 连接已退出，保留当前新连接")

            # 只唤醒由这个连接承接的请求，不能影响后来建立的新连接。
            stale_ids = [msg_id for msg_id, (_, owner) in self._pending.items() if owner is ws]
            for msg_id in stale_ids:
                future, _ = self._pending.pop(msg_id)
                if not future.done():
                    future.set_exception(ConnectionError("Extension 断开连接"))

    # ─── CLI 端（短连接，发一条命令，收一条回复） ─────────────────────

    async def _handle_cli(self, ws: ServerConnection, msg: dict) -> None:
        # 特殊命令：查询 server/extension 状态，无需转发
        if msg.get("method") == "ping_server":
            await ws.send(json.dumps({
                "result": {
                    "extension_connected": self._extension_ws is not None,
                    "extension": self._extension_info,
                }
            }))
            return

        if not self._extension_ws:
            error = "Extension 未连接，请确认浏览器已安装并启用 XHS Bridge 扩展"
            await ws.send(json.dumps({"error": error}))
            return

        msg_id = str(uuid.uuid4())
        msg["id"] = msg_id

        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()
        extension_ws = self._extension_ws
        self._pending[msg_id] = (future, extension_ws)

        try:
            await extension_ws.send(json.dumps(msg))
        except Exception as exc:
            self._pending.pop(msg_id, None)
            await ws.send(json.dumps({"error": f"Extension 连接已失效: {exc}"}))
            return

        try:
            result = await asyncio.wait_for(future, timeout=90.0)
            await ws.send(json.dumps(result))
        except TimeoutError:
            self._pending.pop(msg_id, None)
            await ws.send(json.dumps({"error": "命令执行超时（90s）"}))
        except ConnectionError as e:
            await ws.send(json.dumps({"error": str(e)}))


async def main(port: int) -> None:
    server = BridgeServer()
    async with websockets.serve(server.handle, "localhost", port):
        logger.info("Bridge server 已启动: ws://localhost:%d", port)
        logger.info("等待浏览器扩展连接...")
        await asyncio.Future()  # 永久运行


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="XHS Extension Bridge Server")
    parser.add_argument("--port", type=int, default=9333, help="监听端口（默认 9333）")
    args = parser.parse_args()

    asyncio.run(main(args.port))
