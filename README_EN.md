# RedNote / Xiaohongshu Skill for Codex

English | [简体中文](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/chang-zy/xiaohongshu-skill?style=flat)](https://github.com/chang-zy/xiaohongshu-skill/stargazers)

**Bring RedNote research, comment reading and publishing preparation into your conversations with Codex.**

Built primarily for **Codex**, this skill connects to your local Chrome session to search Xiaohongshu (RedNote / XHS / Little Red Book), inspect posts and images, read comments and replies, study creator profiles, and prepare or publish image posts, videos and long-form content. It uses standard `SKILL.md` files and can work with other compatible agents. OpenClaw is not required.

## What you can do

| Workflow | Work delegated to Codex | Output |
| --- | --- | --- |
| Topic research | Search comparable posts, sort by likes, favorites or date, read text and images | Source-linked samples and editorial suggestions |
| Comment research | Load comments, expand replies, inspect collection status | Recurring questions, disagreements and follow-up ideas |
| Creator research | Load and deduplicate profile posts | Observations about topics, posting patterns and presentation |
| Post preparation | Combine your materials with research | Editable titles, cover concepts and body copy |
| Publishing | Upload local media, fill the form, select verified topics | A browser preview, followed by authorized publishing or draft saving |
| Interaction | Like, favorite, comment or reply on specified posts | Actions explicitly requested by you |

Codex handles writing and interpretation. This repository supplies browser operations and content retrieval; external fact-checking and chart generation need other tools. It does not provide private exposure/conversion analytics or promise reach.

## A workflow tested in practice

We prepared a market-observation post from our own research: search comparable posts → read candidate text, images and comments → draft plain-language copy and cover ideas → upload local images and fill the publishing form → verify five selected topics. The final publish click is supported as a separate action and was not performed in that validation.

Example requests:

> Search for global stock-market image posts with relatively high likes and favorites. Read the text, images and comments, compare how they explain data, and keep source links. Combine the findings with my research and show me a draft.

> Read this post's comments and replies. Summarize recurring reader questions and explain whether loading is complete.

> Fill the publishing form with these local images and copy. Select each requested topic as a real topic, then let me review the page.

## Reliability features

- **Collection status:** reports reply counts and remaining expansion buttons. `commentLoadStatus.complete` concerns replies under loaded top-level comments; it is not independent proof of complete platform-wide coverage.
- **Traceable profile samples:** scrolling, deduplication and stop reasons.
- **Media preparation:** ordered image downloads with local paths and status; video download, keyframes and audio extraction after explicit confirmation.
- **Verified topics:** selects an exact-name candidate through a real mouse click, ends input with a space, and checks official topic nodes with topic IDs. Plain hashtag text or failed selection raises an error.
- **Separate preparation and publishing:** review the browser form before publishing, or save a draft.
- **Local browser bridge:** reuses your login, supports reconnection, diagnostics and cleanup.

## Install in Codex

Requires Python 3.11+, [uv](https://docs.astral.sh/uv/) and Google Chrome.

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/chang-zy/xiaohongshu-skill.git ~/.agents/skills/xiaohongshu-skills
cd ~/.agents/skills/xiaohongshu-skills
uv sync
```

For a project-only installation, place the complete repository under `.agents/skills/xiaohongshu-skills/`. Keep the root `SKILL.md`, `skills/`, `scripts/` and `extension/` together. See [official Codex skill documentation](https://developers.openai.com/codex/skills/). Existing working installations can retain their original path; avoid installing duplicate copies.

1. Open `chrome://extensions/` in Chrome and enable **Developer mode**.
2. Choose **Load unpacked**, select the repository's `extension/`, and enable **XHS Bridge**.
3. From the repository directory, run `uv run python scripts/cli.py check-login`.
4. Ask Codex to log into RedNote if needed, then describe your task naturally. Restart Codex if it does not discover the newly installed skill.

## Updates and versions

`main` contains merged fixes. [Releases](https://github.com/chang-zy/xiaohongshu-skill/releases) include source and the browser extension. Tags use `vVERSION-SHORT_COMMIT`, so multiple builds can share a base version.

For a Git installation, run `git pull --ff-only` and `uv sync` in the original repository. Inspect your own local changes first. Reload XHS Bridge in Chrome after extension updates.

## CLI example

Run in the repository directory. Use `uv run python` consistently and absolute paths for your files.

```bash
uv run python scripts/cli.py search-feeds --keyword "global stock markets" --sort-by "最多收藏" --note-type "图文"
uv run python scripts/cli.py get-feed-detail --feed-id FEED_ID --xsec-token XSEC_TOKEN --load-all-comments --load-all-replies
uv run python scripts/cli.py fill-publish --title-file /abs/path/title.txt --content-file /abs/path/content.txt --images /abs/path/cover.png --tags "市场观察" "全球股市"
# Review the browser form before choosing either action:
# uv run python scripts/cli.py save-draft
# uv run python scripts/cli.py click-publish
```

Feed IDs and tokens come from search/detail results. `cleanup` closes task resources; preserve the page while waiting for publishing approval. Commands output JSON. Exit codes: `0` success, `1` not logged in, `2` error. See the [Chinese README](README.md) for the command table, troubleshooting and skill breakdown; use `<command> --help` for arguments.

## Development

```bash
uv sync --extra dev
uv run pytest
uv run ruff check scripts/xhs/publish.py tests/test_publish_topics.py
uv run ruff format --check scripts/xhs/publish.py tests/test_publish_topics.py
```

Develop on branches and merge through pull requests. Keep cookies, login information and personal publishing materials out of commits.

## Upstream and license

This independent downstream project evolved from [autoclaw-cc/xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills). It retains upstream MIT copyright notices and is not affiliated with or maintained by upstream authors.

[MIT License](LICENSE)
