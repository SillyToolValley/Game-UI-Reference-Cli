# Game-UI-Reference-Cli

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Core deps](https://img.shields.io/badge/core%20dependencies-0-brightgreen)

[English](README.md) · **中文** · [한국어](README.ko.md) · [日本語](README.ja.md)

一个聚焦游戏 UI、依赖极轻的 **UI 参考研究** 命令行工具。它会索引你本地已有的 UI 参考图，并（可选）
从公开 UI 数据库收集参考页面——渲染页面、缓存其 HTML 与图片元数据、按需下载缩略图——以便研究 UI/UX 模式。

主要且结构化的来源是 **[Game UI Database](https://www.gameuidatabase.com)（gameuidatabase.com）**。
其他若干公开 UI/UX 图库也可通过通用图片抓取模式工作（见[支持的站点](#支持的站点)）。

它刻意保持保守、礼貌：

- 先索引本地参考；
- 外部 URL **仅在你列出时** 才抓取（不爬取）；
- 除非你要求，**不** 下载素材；
- 内置礼貌延迟、每次运行页数上限与 `robots.txt` 检查。

> **需登录的站点不在范围内。** 图库需要账号的站点（如 Mobbin 的应用截图）无法用本工具收集，且有意不支持。
> 这是个人研究助手，不是通用爬虫，也不用于再分发他人素材。请尊重各站点条款与 `robots.txt`。

## 成果示例

一个完整的实战示例位于 **[`examples/lucid-dawn/`](examples/lucid-dawn/)** —— 一款 survivor-like/roguelite
（*Lucid Dawn: Dream Survivor*）的完整 UX/UI 规格书，由 `game-ui-spec` 技能基于 `ui-ref` 收集的参考生成。
**12 个界面**（游戏外+游戏内）、**13 张带标注线框图**、设计令牌、决策追踪表、引擎绑定与可用性测试附录 ——
提供 **英文 / 中文 / 한국어** 三个版本。

| 带标注线框图（HUD） | 带标注线框图（升级） | 规格书（渲染） |
| --- | --- | --- |
| ![HUD wireframe](docs/captures/hud.png) | ![Level-up wireframe](docs/captures/levelup.png) | ![Spec cover](docs/captures/spec-cover.png) |

| Boss 奖励（技能树） | 结算（3 分支） | 角色选择 |
| --- | --- | --- |
| ![Skill tree](docs/captures/skilltree.png) | ![Result](docs/captures/results.png) | ![Character select](docs/captures/character-select.png) |

每个 UI 元素都编号，区域以方框/圆圈标注，引线拉到画面**之外**的侧栏标签，下方配有完整的图例+状态矩阵+
数据绑定。查看规格书：
[EN](examples/lucid-dawn/lucid_dawn_ui_ux_spec.en.md) ·
[中文](examples/lucid-dawn/lucid_dawn_ui_ux_spec.zh.md) ·
[한국어](examples/lucid-dawn/lucid_dawn_ui_ux_spec.ko.md) ·
[日本語](examples/lucid-dawn/lucid_dawn_ui_ux_spec.ja.md) ·
[PDF](examples/lucid-dawn/lucid_dawn_ui_ux_spec.en.pdf)。

## 安装

```bash
git clone https://github.com/SillyToolValley/Game-UI-Reference-Cli
cd Game-UI-Reference-Cli
pip install -e .
```

可选的浏览器支持（JavaScript 渲染的站点——即大多数——需要）：

```bash
pip install -e ".[browser]"
playwright install chromium     # 一次性：下载无头浏览器
```

| | `scan-local` | `collect`（静态） | `collect --browser` |
| --- | --- | --- | --- |
| 仅需 Python 标准库 | ✅ | ✅ | — |
| 需要 `playwright` + 浏览器 | — | — | ✅ |
| 适用于服务端渲染页面 | n/a | ✅ | ✅ |
| 适用于 JS 渲染的参考站点 | n/a | ✗（0 项） | ✅ |

浏览器路径直接使用 **Playwright**（真实的桌面 UA+视口，可选自动滚动以加载懒加载图片）。不含任何
反检测/反爬层——所支持的公开站点会把内容提供给普通无头浏览器；内置的礼貌机制让运行保持得体。

## 快速开始

在项目根目录：

```bash
ui-ref init --project-name "My Project"
# 将参考图放在 references/ui/<collection>/<category>/*.png|jpg|... 下
ui-ref scan-local
```

## 配套技能：`game-ui-spec`

本仓库附带一个 **Claude Code 技能**，把你在这里收集的参考转化为 **优秀的游戏 UX/UI 规格书** ——
专为 survivor-like / 弹幕天堂 / roguelite 游戏打造。位置：
[`.claude/skills/game-ui-spec/`](.claude/skills/game-ui-spec/)。

给定 GDD 或功能简报，它会产出这样的规格书：

- **参考图内联嵌入到每个界面正文**（用 `ui-ref` 收集）；
- **由这些参考推导出的线框图**——**每个 UI 元素都编号**、区域以方框/圆圈标注、**引线拉出画面外**做说明
  （SVG 标注引线套件——见
  [`templates/wireframe-kit.svg`](.claude/skills/game-ui-spec/templates/wireframe-kit.svg)）；
- 每个界面都有 **图例 / 状态矩阵 / 输入对等 / 数据绑定** 表；
- 每个界面都有通俗语言的 **「UX 设计意图」**（用游戏 UX 启发法思考，但正文不出现术语）；
- **出货级（可选）阶段**：设计令牌 · 数值/决策追踪表 · 引擎绑定 · 可用性测试计划；
- Markdown 源渲染为 **宽屏 16:9 横向 PDF**（`build_pdf.py` + `spec-pdf.css`），让密集表格便于分享。

完整生成示例见 **[`examples/lucid-dawn/`](examples/lucid-dawn/)**（12 界面、13 张线框图、令牌、追踪表、
英/中/韩）以及上方的[成果示例](#成果示例)截图。

要在你的游戏项目中使用，把技能文件夹复制到该项目的 `.claude/skills/`（或复制到 `~/.claude/skills/`
以对所有项目生效），然后让 Claude Code “画出〈某界面〉的 UX/UI 规格书”。

## 命令

### `scan-local` —— 索引本地参考

遍历 `references/ui/<collection>/<category>/<file>`，从文件字节读取图片尺寸（PNG/GIF/JPEG，无需 Pillow），
根据文件夹路径推断粗略标签，并在 `ui_research/manifests/` 下写出 JSON + Markdown 清单。

### `collect` —— 抓取显式列出的页面

把参考 URL（每行一个）放进 `ui_research/urls.txt`，然后：

```bash
# JS 渲染站点 → 用浏览器。会按每个 URL 的域名自动选择模式。
ui-ref collect --browser

# 每页下载几张图 + 滚动以加载懒加载图
ui-ref collect --browser --scroll 6 --download-gallery-assets --download-asset-limit 2

# 为未知站点强制指定模式或图库类名
ui-ref collect --browser --mode images
ui-ref collect --browser --gallery-class "thumb-card"
```

可在一个 `urls.txt` 中混合多个受支持站点的 URL——每个 URL 会自动选择各自的预设。

每次运行会在 `ui_research/manifests/` 下写出：

- `collected_pages_<run_id>.json` —— 每页状态、robots 备注、页面标题、链接/素材/图库元数据；
- `contact_sheet_<run_id>.html` —— **可浏览** 的联系表：已下载缩略图内联渲染，所有提取/抓取的图片都
  连同标题/尺寸与来源链接一并列出。用浏览器打开即可审阅收集结果。

> **站点实况提醒（亲测）：** Game UI Database 是 SPA + Cloudflare，无头收集不稳定 ——
> `index.php?&scrn=N` 的界面类型筛选在直接加载时不会生效（所有 scrn 得到同一默认图库），
> `gameData.php?id=N` 的单游戏页也可能超时。**interfaceingame.com 的单游戏页**（`/games/<slug>/`）
> 最稳定（每款游戏 30+ 张真实截图）。获取游戏 id/slug 时，用网页搜索比站内搜索（SPA）更快。
> 若收集站点没有直系品类（如弹幕幸存者类），用相邻作品 + 文字描述其模式来补充。

常用参数：`--site`、`--mode`、`--gallery-class`、`--scroll`、`--max-pages`、`--delay`、`--timeout`、
`--user-agent`、`--keep-*`、`--download-full-images`、`--download-title-contains`、`--no-headless`。

## 支持的站点

两种提取模式：

- **`gallery`** —— 结构化：读取图库锚点（锚点类名 + `data-title`/`data-imageid`/`data-thumb`），
  每项元数据丰富。
- **`images`** —— 通用：抓取渲染页面的 `<img>`/`srcset` 图片（过滤掉图标/头像/Logo 等明显的界面装饰）。
  适用于大多数站点。

模式/预设按每个 URL 的域名自动判定；可用 `--site`/`--mode`/`--gallery-class` 覆盖。

| 站点键 | 域名 | 模式 | 备注 |
| --- | --- | --- | --- |
| `gameuidatabase` | gameuidatabase.com | gallery | Game UI Database —— 结构化图库（需 `--browser`；注意 SPA+CF）。 |
| `interfaceingame` | interfaceingame.com | images | Interface In Game —— 游戏 UI 截图（推荐单游戏页）。 |
| `screenlane` | screenlane.com | images | 移动端 UI/UX 流程。 |
| `collectui` | collectui.com | images | 每日 UI 灵感。 |
| `landbook` | land-book.com | images | 落地页图库。 |
| `lapaninja` | lapa.ninja | images | 落地页示例。 |
| `refero` | refero.design | images | Web/iOS UI 灵感。 |
| `dribbble` | dribbble.com | images | 设计稿（公开页面）。 |
| `behance` | behance.net | images | 创意展示（公开页面）。 |

任何**没有预设**的站点默认走 `images` 模式（通用抓取）。需要登录的图库不受支持。

## 配置发现

不带 `--config` 时，CLI 会在以下位置查找 `ui_ref_config.json`：

```text
ui_ref_config.json
ui_research/ui_ref_config.json
docs/ui_research/ui_ref_config.json
```

用 `--project-root` 可从别处针对某个项目文件夹运行。

## 礼仪

运行要小而慢（默认 8 秒延迟、每次 20 页）。把收集到的页面当作引用/参考上下文 —— 不是可再分发的素材包，
也不是训练数据。

## 许可证

MIT —— 见 [LICENSE](LICENSE)。
