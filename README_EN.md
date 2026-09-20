# RedNote / Xiaohongshu Skill for AI Agents

English | [简体中文](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/chang-zy/xiaohongshu-skill?style=flat)](https://github.com/chang-zy/xiaohongshu-skill/stargazers)

Browser automation skills for **RedNote (Xiaohongshu / XHS / RED / Little Red Book)**, built for **Codex, Claude Code, OpenClaw, and other AI agents**. Search and inspect posts, collect verifiable comment threads, analyze creator profiles, prepare image and video content for multimodal understanding, publish posts, and interact through a real local Chrome session.

Unlike a typical Xiaohongshu MCP or RedNote MCP server, this project uses an **Agent Skill + Chrome extension + Python CLI** architecture. It reuses your existing browser login and emphasizes complete, auditable research results and reliable multi-step workflows.

## Why this project

- **Verifiable comment collection** — expands top-level comments and nested replies, then reports loaded counts, remaining items, and completeness instead of silently returning partial data.
- **Complete creator-profile reading** — scrolls, loads, and deduplicates profile posts while returning a stop reason and completeness status.
- **Multimodal research preparation** — downloads post images in their original order; with explicit confirmation, it can also download videos and extract keyframes and audio.
- **Session-based local discovery** — uses RedNote's own nearby/local filters without reading a precise address or inferring a creator's identity.
- **Resilient browser workflows** — includes bridge reconnection, actionable failure diagnostics, safe task cleanup, and minimal disruption to existing Chrome windows.
- **One skill set for the full workflow** — login, search, profile analysis, publishing, comments, replies, likes, favorites, and compound content-operations tasks.

## Included skills

| Skill | Purpose | Main capabilities |
|---|---|---|
| `xhs-auth` | Authentication | Login status, QR-code login, phone-code login |
| `xhs-explore` | Discovery and research | Search, post details, creator profiles, home feed |
| `xhs-publish` | Publishing | Image posts, videos, long-form posts, scheduling and preview |
| `xhs-interact` | Interaction | Comments, replies, likes and favorites |
| `xhs-content-ops` | Compound workflows | Competitor research, trend tracking and content operations |

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- Google Chrome

## Installation

Clone the repository into your agent's skills directory:

```bash
cd <your-agent-project>/skills/
git clone https://github.com/chang-zy/xiaohongshu-skill.git xiaohongshu-skills
cd xiaohongshu-skills
uv sync
```

Then install the local browser bridge:

1. Open `chrome://extensions/` in Chrome.
2. Enable **Developer mode**.
3. Choose **Load unpacked** and select this repository's `extension/` directory.
4. Confirm that **XHS Bridge** is enabled.

## Use with an AI agent

After installing the repository as a skill, ask your agent in natural language:

```text
Search RedNote for the most-liked image post about camping and summarize it.
Collect all loaded comments and nested replies, and tell me whether the result is complete.
Analyze this Xiaohongshu creator's recent posts and identify recurring topics.
Prepare this XHS video for content analysis.
Publish this image post after showing me a preview.
```

The root `SKILL.md` routes requests to the appropriate specialized skill. All functions are also available through `python scripts/cli.py`; see the [Chinese README](README.md) for the complete command reference.

## Search aliases

The same platform or ecosystem may be searched as **RedNote, Xiaohongshu, XHS, RED, Little Red Book, Red Book, RedNote automation, Xiaohongshu automation, XHS bot, RedNote Skill, Xiaohongshu Skill, AI Agent Skill, browser automation, Claude Code Skill, Codex Skill,** or **OpenClaw Skill**.

`RedNote` is the preferred English brand name and `Little Red Book` is a common translation. `RedBook` and `Small Red Book` are less precise, so they are included only as secondary search aliases.

## Upstream and license

This independent downstream project evolved from [autoclaw-cc/xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills). It retains the upstream MIT license and copyright notices and is not affiliated with or maintained by the upstream authors.

Use automation conservatively. High-frequency actions may trigger platform risk controls or account restrictions.

Licensed under the [MIT License](LICENSE).
