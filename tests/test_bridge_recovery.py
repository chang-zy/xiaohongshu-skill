"""Bridge 自动恢复与连接交接测试。"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def _load_bridge_server_module():
    module_path = Path(__file__).parents[1] / "scripts" / "bridge_server.py"
    spec = importlib.util.spec_from_file_location("xhs_bridge_server", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeExtensionSocket:
    def __init__(self) -> None:
        self.incoming: asyncio.Queue[str | None] = asyncio.Queue()
        self.sent: list[dict] = []

    def __aiter__(self):
        return self

    async def __anext__(self) -> str:
        value = await self.incoming.get()
        if value is None:
            raise StopAsyncIteration
        return value

    async def send(self, raw: str) -> None:
        self.sent.append(json.loads(raw))

    async def close_stream(self) -> None:
        await self.incoming.put(None)


def test_old_extension_disconnect_does_not_clear_new_connection() -> None:
    async def scenario() -> None:
        module = _load_bridge_server_module()
        server = module.BridgeServer()
        old_socket = FakeExtensionSocket()
        new_socket = FakeExtensionSocket()

        old_task = asyncio.create_task(
            server._handle_extension(old_socket, {"version": "1.0.0"})
        )
        await asyncio.sleep(0)
        new_task = asyncio.create_task(
            server._handle_extension(
                new_socket, {"version": "1.1.0", "protocol_version": 1}
            )
        )
        await asyncio.sleep(0)

        await old_socket.close_stream()
        await old_task

        assert server._extension_ws is new_socket
        assert server._extension_info["version"] == "1.1.0"
        assert server._extension_info["protocol_version"] == 1

        await new_socket.close_stream()
        await new_task
        assert server._extension_ws is None

    asyncio.run(scenario())


def test_old_extension_disconnect_only_fails_its_own_requests() -> None:
    async def scenario() -> None:
        module = _load_bridge_server_module()
        server = module.BridgeServer()
        old_socket = FakeExtensionSocket()
        new_socket = FakeExtensionSocket()
        loop = asyncio.get_running_loop()
        old_future = loop.create_future()
        new_future = loop.create_future()
        old_task = asyncio.create_task(
            server._handle_extension(old_socket, {"version": "1.0.0"})
        )
        await asyncio.sleep(0)
        server._extension_ws = new_socket
        server._extension_info = {"version": "1.1.0"}
        server._pending = {
            "old": (old_future, old_socket),
            "new": (new_future, new_socket),
        }

        await old_socket.close_stream()
        await old_task

        assert old_future.done()
        assert isinstance(old_future.exception(), ConnectionError)
        assert not new_future.done()
        assert "new" in server._pending

        new_future.cancel()

    asyncio.run(scenario())


def test_extension_health_requires_live_extension_response(monkeypatch) -> None:
    from xhs import bridge as module

    class FakeConnection:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def send(self, raw: str) -> None:
            request = json.loads(raw)
            assert request["method"] == "ping_extension"

        def recv(self, timeout: float) -> str:
            assert timeout == 2
            return json.dumps({"result": {"ready": True, "version": "1.1.0"}})

    monkeypatch.setattr(module.ws_client, "connect", lambda *_args, **_kwargs: FakeConnection())

    page = module.BridgePage()
    assert page.is_extension_connected() is True
    assert page.get_extension_health()["version"] == "1.1.0"
