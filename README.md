# 小红书 Skill for Codex

[English](README_EN.md) | 简体中文

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/chang-zy/xiaohongshu-skill?style=flat)](https://github.com/chang-zy/xiaohongshu-skill/stargazers)

**把小红书调研、评论区阅读和发帖准备，接进你与 Codex 的日常对话。**

这是一个以 **Codex** 为主要使用场景的小红书浏览器自动化技能。它连接本机 Chrome，复用你已登录的账号，让 Codex 搜笔记、看正文和配图、读评论与回复、研究账号，以及填写和发布图文、视频或长文。

平台也常被称为 **RedNote / Xiaohongshu / XHS / Little Red Book**。项目采用标准 `SKILL.md` 结构；其他兼容 Agent 也可接入。使用 Codex 时无需安装 OpenClaw。

## 能帮你做什么

| 你要完成的事 | 可以交给 Codex 的工作 | 得到什么 |
| --- | --- | --- |
| 选题调研 | 搜同类帖子，按点赞、收藏或时间筛选，打开正文和配图 | 带原帖出处的样本比较、选题与表达建议 |
| 阅读评论区 | 加载一级评论、展开子回复，检查加载状态 | 读者反复问的问题、争议点、后续选题线索 |
| 研究账号 | 读取主页、滚动加载并去重帖子 | 选题方向、更新习惯、标题和封面的样本观察 |
| 准备一篇帖子 | 结合你的资料与调研结果，整理标题、封面思路和正文 | 可修改的内容草稿与发布素材清单 |
| 填写与发布 | 上传本地配图或视频，填写正文，逐个选择正式话题 | 可在浏览器检查的发布页；确认后发布或保存草稿 |
| 日常互动 | 对指定笔记点赞、收藏，发送你授权的评论或回复 | 一次明确、可检查的互动操作 |

内容判断、写作与素材解读由 Codex 完成；本仓库提供页面操作和内容获取能力。外部数据核验、绘图等工作需要 Codex 的其他工具配合。它不会提供你账号的曝光或转化后台数据，也不保证任何笔记的传播效果。

## 一次实际使用：从市场研究到小红书帖子

我们用自己的市场走势研究准备了一篇帖子，工作顺序是：

1. **先搜样本**：查看同类市场观察笔记，比较点赞、收藏和内容呈现。
2. **再读内容**：打开候选笔记的正文、配图和评论，找出读者容易理解的写法。
3. **结合自己的资料**：整理标题、封面和正文，保留数据日期、来源与计算口径。
4. **填入发布页**：上传本地图片，填写文案，逐个选择话题。
5. **检查后发布**：在浏览器检查内容和话题，确认后执行发布。

这次实际验证了搜索、详情读取、图片素材获取和发布页填写，并确认五个话题都成为正式话题。最后点击发布是独立步骤，不包含在这次验证中。

你可以直接这样说：

> 搜一下“全球股市”相关图文笔记，挑几篇点赞和收藏较高的，读正文、配图和评论。比较它们怎么讲清楚数据，保留原帖链接，然后结合我的研究拟一篇平实的帖子。先给我看草稿。

> 读这条笔记的评论和子回复，告诉我读者最常问什么。说明加载是否完整，别把少量已加载评论当成整个评论区。

> 用这些本地图片和文案填写小红书发布页，添加这五个话题。每个都要选成正式话题，填好后让我检查。

## 为什么适合连续调研和发帖

- **评论采集有状态**：返回已加载回复数、声明回复数、剩余展开按钮等信息。`commentLoadStatus.complete` 表示已加载一级评论的子回复展开状态，不代表全站评论已被独立核验。
- **主页样本可追踪**：滚动加载、去重并报告停止原因，分析时能说明样本范围。
- **配图按原顺序获取**：保留本地路径和下载状态，方便 Codex 结合正文与配图阅读。视频可在明确确认后下载并提取关键帧、音轨。
- **话题成功有检查**：选择名称准确匹配的候选项，用实际鼠标点击，并以空格结束输入；随后检查带话题 ID 的正式节点。普通 `#文字`、漏选话题或点击未生效都会报错。
- **填写与发布可分开**：先准备发布页，再由你检查并确认，支持保存草稿。
- **复用本机浏览器**：通过本地 Bridge 连接 Chrome，支持断线恢复、失败诊断与任务收尾。

## 在 Codex 中安装

需要 **Python 3.11+、[uv](https://docs.astral.sh/uv/)、Google Chrome**。

### 1. 安装技能与依赖

以下使用 Codex 的用户级技能目录，供多个项目共用：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/chang-zy/xiaohongshu-skill.git ~/.agents/skills/xiaohongshu-skills
cd ~/.agents/skills/xiaohongshu-skills
uv sync
```

也可以将完整仓库放在项目的 `.agents/skills/xiaohongshu-skills/` 下。目录需要包含根 `SKILL.md`、`skills/`、`scripts/` 和 `extension/`，不要只复制一个技能文件。技能目录的说明见 [Codex 官方文档](https://developers.openai.com/codex/skills/)。

如果已经在现有 Codex 技能目录安装成功，可以沿用原路径；更新时进入原来的仓库，不要重复安装两份。

### 2. 加载 Chrome 扩展

1. 在 Chrome 打开 `chrome://extensions/`。
2. 开启右上角的 **开发者模式**。
3. 点击 **加载已解压的扩展程序**，选择刚才仓库的 `extension/` 目录。
4. 确认 **XHS Bridge** 已启用，保持 Chrome 可运行。

### 3. 检查登录并开始对话

在仓库目录运行：

```bash
uv run python scripts/cli.py check-login
```

未登录时，可在 Codex 中说“登录小红书”，按提示扫码。之后直接描述任务，根技能会路由到相应子技能。如果 Codex 没有发现新技能，重启 Codex 后再试。

## 更新与版本

- **main 分支**包含最近合入的修复；**[Releases](https://github.com/chang-zy/xiaohongshu-skill/releases)** 提供对应提交的打包文件，包含浏览器扩展。
- 发布标签使用 `v版本号-提交短哈希`，例如 `v0.1.1-9496f05`。同一基础版本可能有多个构建，以提交哈希区分。
- Git 安装可在原仓库目录执行 `git pull --ff-only`，然后 `uv sync`。若你自己修改过代码，先检查本地改动再更新。
- 更新了 `extension/` 后，去 `chrome://extensions/` 点击 XHS Bridge 的重新加载按钮。

## 命令行示例

在仓库根目录执行；统一使用 `uv run python`，避免系统 Python 缺少依赖。CLI 输出 JSON，可用于其他脚本。

```bash
# 按收藏量搜索图文样本
uv run python scripts/cli.py search-feeds --keyword "全球股市" --sort-by "最多收藏" --note-type "图文"

# 读取正文，并加载评论与子回复
uv run python scripts/cli.py get-feed-detail --feed-id FEED_ID --xsec-token XSEC_TOKEN --load-all-comments --load-all-replies

# 读取主页并滚动加载帖子
uv run python scripts/cli.py user-profile --user-id USER_ID --xsec-token XSEC_TOKEN --load-all-notes

# 填写图文发布页；标题、正文用 UTF-8 文件，文件路径使用绝对路径
uv run python scripts/cli.py fill-publish --title-file /abs/path/title.txt --content-file /abs/path/content.txt --images /abs/path/cover.png /abs/path/chart.png --tags "市场观察" "全球股市" "数据可视化"

# 检查发布页后，选择保存草稿，或在明确确认后发布
uv run python scripts/cli.py save-draft
# uv run python scripts/cli.py click-publish
```

`FEED_ID` 和 `XSEC_TOKEN` 取自搜索或详情结果，不需要手工编造。一次任务收尾可使用 `cleanup`；等待发布页确认时应保留页面。

### 主要命令

| 类型 | 命令 |
| --- | --- |
| 登录 | `check-login`、`login`、`phone-login`、`delete-cookies` |
| 调研 | `search-feeds`、`list-feeds`、`get-feed-detail`、`user-profile`、`browse-local` |
| 图文 / 视频 | `fill-publish`、`fill-publish-video`、`publish`、`publish-video` |
| 发布控制 | `click-publish`、`save-draft`；发布参数支持话题、定时与可见范围 |
| 长文 | `long-article`、`select-template`、`next-step` |
| 互动 | `post-comment`、`reply-comment`、`like-feed`、`favorite-feed` |
| 收尾 / 诊断 | `cleanup`、`check-risk`、`diagnose-404` |

用 `uv run python scripts/cli.py <命令> --help` 查看参数。退出码：`0` 成功、`1` 未登录、`2` 错误。发布、评论和回复等账号操作应基于你的明确指令。

## 常见问题

**话题看着有“#”，为什么没选成功？** 纯文本与正式话题是不同的编辑器节点。最新修复会准确选择候选项并检查话题 ID；人工预览时也可以确认每个话题都显示为蓝色。

**提示缺少 Python 模块？** 在仓库目录执行 `uv sync`，再使用 `uv run python scripts/cli.py ...`，不要混用系统 Python。

**Bridge 连接失败？** 检查 Chrome 是否运行、XHS Bridge 是否启用，以及扩展是否来自当前仓库。更新扩展后重新加载，再重试。

**必须用 OpenClaw 或 Claude Code 吗？** 不需要。本 README 的安装与使用以 Codex 为主。其他 Agent 的兼容信息不改变这一点。

**能保证读到所有评论吗？** 页面可能受删除、可见性、登录状态或加载限制影响。请结合返回的数量、剩余项和停止状态判断，报告中注明样本范围。

## 技能与结构

| 技能 | 职责 |
| --- | --- |
| `xhs-auth` | 登录与认证 |
| `xhs-explore` | 搜索、详情、主页与素材读取 |
| `xhs-publish` | 图文、视频、长文和分步发布 |
| `xhs-interact` | 评论、回复、点赞、收藏 |
| `xhs-content-ops` | 串联调研与内容运营流程 |

```text
xiaohongshu-skills/
├── SKILL.md              # Codex 技能入口
├── skills/               # 各任务的子技能指引
├── extension/            # Chrome XHS Bridge 扩展
├── scripts/cli.py        # JSON 命令行入口
├── scripts/xhs/          # 页面操作与内容获取
├── tests/                # 回归测试
├── README_EN.md          # 英文说明
└── pyproject.toml
```

## 开发

```bash
uv sync --extra dev
uv run pytest
uv run ruff check scripts/xhs/publish.py tests/test_publish_topics.py
uv run ruff format --check scripts/xhs/publish.py tests/test_publish_topics.py
```

按仓库约定在分支上开发，通过 PR 合入 main。请勿提交账号 Cookie、登录信息或个人发布素材。

## 上游与许可

本项目基于 [autoclaw-cc/xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills) 演进，保留原项目 MIT 许可与版权声明。感谢原作者和贡献者提供浏览器自动化基础。本仓库是独立下游版本，与原作者无隶属或维护关系。

[MIT License](LICENSE)
