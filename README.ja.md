# Game-UI-Reference-Cli

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Core deps](https://img.shields.io/badge/core%20dependencies-0-brightgreen)

[English](README.md) · [中文](README.zh.md) · [한국어](README.ko.md) · **日本語**

<img src="examples/lucid-dawn/art-concepts/levelup-ui-art-concept.png" alt="ui-ref リファレンスを基に生成したレベルアップ UI アートコンセプト" width="900">

**この CLI で収集した UI リファレンスを基に生成したコンセプトアート。** `game-ux-ui-design`
スキルは、安定したワイヤーフレーム、GDD/デザイン文脈、収集済みリファレンスメモを Codex/imagegen に渡し、
UI アート方向性 mockup を生成できる。この画像はムード/素材感の方向確認用であり、正確な文言・寸法・状態・
アクセシビリティ規則はデザインドキュメントとトークンを基準にする。

ゲーム UI に特化した、依存の軽い **UI リファレンス調査** CLI。ローカルに保管している UI リファレンス画像を
インデックス化し、（任意で）公開 UI データベースからリファレンスページを収集 —— レンダリングし、HTML と
画像メタデータをキャッシュし、要求に応じてサムネイルをダウンロード —— して UI/UX パターンを研究できる。

主要かつ構造化されたソースは **[Game UI Database](https://www.gameuidatabase.com)（gameuidatabase.com）**。
他のいくつかの公開 UI/UX ギャラリーも汎用の画像収集モードで動作する（[対応サイト](#対応サイト)参照）。

意図的に控えめで礼儀正しく動作する:

- まずローカルリファレンスをインデックス化し、
- 外部 URL は **あなたが列挙したときだけ** 取得（クロールしない）、
- アセットは **要求しない限り** ダウンロードしない、
- ポライトネス遅延・実行ごとのページ上限・`robots.txt` チェックを内蔵。

> **ログイン必須サイトは対象外。** ギャラリーにアカウントが必要なサイト（例: Mobbin のアプリ画面）は本ツールでは
> 収集できず、意図的に非対応。これは個人研究の補助ツールであり、汎用スクレイパーでも、他者のアセットを
> 再配布するためのものでもない。各サイトの規約と `robots.txt` を尊重すること。

## 何を見つけるか —— UI リファレンス

中核の仕事は、実際のゲーム UI スクリーンショットを集めてパターンを研究できるようにすること。`ui-ref` に
リファレンスページを指定すると、レンダリングし、メタデータをキャッシュし、サムネイルをダウンロードする
—— それを **画面タイプ別** に整理する。以下はサンプル用に `ui-ref collect --browser --site interfaceingame`
で作品別ページから収集したリファレンス:

![ui-ref が画面タイプ別に収集した UI リファレンス](docs/captures/references-found.png)

各実行は、ダウンロードしたサムネイルがタイトル・サイズ・**ソースリンク** と共にインライン表示される
閲覧可能な **コンタクトシート**（`ui_research/manifests/contact_sheet_*.html`）と、**マニフェスト**
（`scan-local` → `local_ui_refs_manifest.{json,md}`）も書き出す。こうして集めたリファレンスが下の
ワイヤーフレームの **出典** であり、各デザイン画面は借用した具体的なショットを明記している。

## 成果物サンプル

完全な実例が **[`examples/lucid-dawn/`](examples/lucid-dawn/)** にある —— survivor-like/ローグライト
（*Lucid Dawn: Dream Survivor*）の完全な UX/UI デザインドキュメントで、`ui-ref` で収集したリファレンスをもとに
`game-ux-ui-design` スキルが生成した。**12 画面**（ゲーム外+ゲーム内）・**注釈付きワイヤーフレーム 13 点**、英語・中国語・韓国語・日本語で提供。

**注釈付きワイヤーフレーム** —— すべての UI 要素に番号、領域を矩形/円で、引き出し線をフレームの *外* のガターのラベルへ:

<img src="docs/captures/hud.png" alt="ゲーム内 HUD の注釈付きワイヤーフレーム" width="900">

### デザインドキュメントはどこまで書かれている？

各ワイヤーフレームの下に、**12 画面すべて** が次を備える:

- **目的**（進入 / 退出 / 入力コンテキスト / 優先度）
- **参考** —— 借用した実際のゲーム UI を「何を / なぜ」のメモ付きで本文にインライン埋め込み
- **ワイヤーフレーム**（SVG）+ **凡例** —— 要素ごとに: 位置 · 表示条件 · 挙動/状態 · **データバインディング** · **測定可能な判定基準** · 平易な UX 意図 · アクセシビリティ
- **状態マトリクス** —— default / hover / pressed / selected / disabled-locked / loading / empty / error
- **入力パリティ** —— マウス · キーボード · ゲームパッド · スクリーンリーダー
- **データバインディング** —— すべてのフィールド/イベントを **GDD と照合検証**；GDD に無いものは「GDD への追加が必要」と明示（勝手に捏造しない）
- **ナビゲーション · エッジケース · アクセシビリティ · UX 設計意図（平易な言葉）· 未解決の質問 · 受入チェックリスト**

さらに付随ドキュメント: **デザイントークン**（色 hex / 書体 / モーション / USS 変数）、**数値・意思決定トラッカー**
（各数値を GDD 確定 / 標準 / 推定 で分類）、そして **エンジンバインディング（UI Toolkit × DOTS）** ·
**ユーザビリティテスト計画** の付録。

<details>
<summary><b>実際の抜粋を見る —— ゲーム内 HUD の凡例 + 状態マトリクス</b></summary>

凡例（9 行のうち抜粋）:

| # | コード | 要素 | 位置 | データバインディング | 判定基準 | アクセシビリティ |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | A2 | アラーム時計 | 左上 | `run.timer` 0–1200s (§4-1), `AlarmReached` (§12-1) | いつでも残り時間を ≤1s で読める | 時計+数字、最後の 60 秒は 音+明るさ |
| 4 | A4 | HP / シールド | 左上 | `Character.hp` (§12-2), シールド (§12-2 追加) | 被弾 ≤100ms 反映；低 HP は 色+点滅+枠 | 色+点滅+枠+数値 |
| 7 | A7 | 浄化バー | 下部中央 | 浄化 (§4-2), `PurgeGained` · `BossThresholdReached` (§12-1) | 獲得 ≤200ms 反映；閾値 → ボス警告 | 充填+数値+ソースのトースト |

状態マトリクス（抜粋）:

| 要素 | default | pressed/active | disabled/locked | error |
| --- | --- | --- | --- | --- |
| スキル (A8) | リング充填 | 押下 + SFX、リング 0 | グレー + 錠 + 「未解放」 | 「CD エラー —— 既定値」 |
| 必殺 (A9) | チャージ充填 | 発動カットシーン | <100 なら淡色 + 残量 | 直前値 + 警告枠 |

</details>

以下は **実際にレンダリングしたデザインドキュメントのページ**（ゲーム内 HUD 画面 —— 参考スクショ、注釈付きワイヤー
フレーム、10 列の凡例表すべて、納品そのまま）:

![デザインドキュメントページのサンプル —— ゲーム内 HUD](docs/captures/design-page-hud.png)

**その他の画面** —— 全点は [`examples/lucid-dawn/wireframes/`](examples/lucid-dawn/wireframes/):

<img src="docs/captures/levelup.png" alt="レベルアップ/アイテム選択" width="440"> <img src="docs/captures/results.png" alt="リザルト画面" width="440">
<img src="docs/captures/skilltree.png" alt="ボス報酬スキルツリー" width="440"> <img src="docs/captures/character-select.png" alt="キャラクター選択" width="440">

デザインドキュメントの全文を読む: [英語](examples/lucid-dawn/lucid_dawn_ui_ux_design.en.md) ·
[中国語](examples/lucid-dawn/lucid_dawn_ui_ux_design.zh.md) ·
[韓国語](examples/lucid-dawn/lucid_dawn_ui_ux_design.ko.md) ·
[日本語](examples/lucid-dawn/lucid_dawn_ui_ux_design.ja.md) ·
[PDF](examples/lucid-dawn/lucid_dawn_ui_ux_design.en.pdf)。

## インストール

```bash
git clone https://github.com/SillyToolValley/Game-UI-Reference-Cli
cd Game-UI-Reference-Cli
pip install -e .
```

任意のブラウザ対応（JavaScript レンダリングのサイト —— つまり大半 —— に必要）:

```bash
pip install -e ".[browser]"
playwright install chromium     # 一度だけ: ヘッドレスブラウザをダウンロード
```

| | `scan-local` | `collect`（静的） | `collect --browser` |
| --- | --- | --- | --- |
| Python 標準ライブラリのみ | ✅ | ✅ | — |
| `playwright` + ブラウザが必要 | — | — | ✅ |
| サーバーレンダリングのページで動作 | n/a | ✅ | ✅ |
| JS レンダリングのリファレンスサイトで動作 | n/a | ✗（0 件） | ✅ |

ブラウザ経路は **Playwright** を直接使う（現実的なデスクトップ UA+ビューポート、遅延読み込み画像のための
任意の自動スクロール）。ステルス/アンチボット層は同梱しない —— 対応する公開サイトは通常のヘッドレス
ブラウザにコンテンツを提供し、内蔵のポライトネスが実行を行儀よく保つ。

## クイックスタート

プロジェクトルートで:

```bash
ui-ref init --project-name "My Project"
# references/ui/<collection>/<category>/*.png|jpg|... にリファレンス画像を置く
ui-ref scan-local
```

## 同梱スキル: `game-ux-ui-design`

このリポジトリは、ここで集めたリファレンスを **優れたゲーム UX/UI デザインドキュメント** に変える **Claude Code スキル** を
同梱する —— survivor-like / 弾幕天国 / ローグライト向けに作られている。場所:
[`.claude/skills/game-ux-ui-design/`](.claude/skills/game-ux-ui-design/)。

GDD や機能ブリーフを与えると、次を備えたデザインドキュメントを生成する:

- **リファレンス画像を各画面の本文にインライン埋め込み**（`ui-ref` で収集）;
- **そのリファレンスから導いたワイヤーフレーム** —— **すべての UI 要素に番号**、領域を矩形/円で、
  **フレーム外へ伸ばす引き出し線** で説明（SVG 注釈引き出しキット ——
  [`templates/wireframe-kit.svg`](.claude/skills/game-ux-ui-design/templates/wireframe-kit.svg)）;
- 各画面に **凡例 / 状態マトリクス / 入力パリティ / データバインディング** 表;
- 画面ごとに平易な言葉の **「UX 設計意図」**（ゲーム UX ヒューリスティクスで考えるが、本文に用語は出さない）;
- **出荷級（任意）ステージ**: デザイントークン · 数値/意思決定トラッカー · エンジンバインディング · ユーザビリティテスト計画;
- Markdown ソースを **ワイド 16:9 横向き PDF**（`build_pdf.py` + `design-pdf.css`）にレンダリングし、密な表も共有しやすく;
- 選定したワイヤーフレームを **UI アートコンセプト mockup** にして、ムード・素材言語・カード/HUD 処理を確認できる。

完全な生成サンプルは **[`examples/lucid-dawn/`](examples/lucid-dawn/)**（12 画面、ワイヤーフレーム 13 点、トークン、
トラッカー、英/中/韓/日）と上の[成果物サンプル](#成果物サンプル)のキャプチャを参照。

自分のゲームプロジェクトで使うには、スキルフォルダをそのプロジェクトの `.claude/skills/`（または全プロジェクト
共通なら `~/.claude/skills/`）にコピーし、Claude Code に「〈画面〉の UX/UI デザインドキュメントを作って」と頼む。

## コマンド

### `scan-local` —— ローカルリファレンスをインデックス化

`references/ui/<collection>/<category>/<file>` を走査し、ファイルバイトから画像サイズを読み取り
（PNG/GIF/JPEG、Pillow 不要）、フォルダパスから粗いタグを推論して `ui_research/manifests/` に
JSON + Markdown マニフェストを書き出す。

### `collect` —— 明示的に列挙したページを取得

`ui_research/urls.txt` にリファレンス URL を 1 行ずつ入れて:

```bash
# JS レンダリングのサイト → ブラウザを使う。URL のドメインごとにモードが自動判定される。
ui-ref collect --browser

# ページごとに画像を数枚 + 遅延読み込みのためのスクロール
ui-ref collect --browser --scroll 6 --download-gallery-assets --download-asset-limit 2

# 未知のサイトにモード/ギャラリークラスを強制
ui-ref collect --browser --mode images
ui-ref collect --browser --gallery-class "thumb-card"
```

1 つの `urls.txt` に複数の対応サイトの URL を混在させてよい —— 各 URL が自分のプリセットを自動選択する。

各実行は `ui_research/manifests/` に次を書き出す:

- `collected_pages_<run_id>.json` —— ページごとの状態、robots メモ、ページタイトル、リンク/アセット/ギャラリーメタ;
- `contact_sheet_<run_id>.html` —— **閲覧可能** なシート: ダウンロード済みサムネイルがインライン表示され、抽出/収集した
  すべての画像がタイトル/サイズ・ソースリンクと共に列挙される。ブラウザで開いて収集物を確認する。

> **サイトの実情（経験則）:** Game UI Database は SPA + Cloudflare のため、ヘッドレス収集が不安定 ——
> `index.php?&scrn=N` の画面種別フィルタは直接ロードでは効かず（どの scrn でも同じデフォルトギャラリー）、
> `gameData.php?id=N` の作品別ページもタイムアウトしうる。**interfaceingame.com の作品別ページ**
> （`/games/<slug>/`）が最も安定（1 作品あたり実スクリーンショット 30 枚以上）。ゲーム id/slug の取得は
> サイト内検索（SPA）よりウェブ検索が速い。直系ジャンル（Vampire Survivors 系など）が収集サイトに無ければ、
> 近接作品 + そのパターンを文章で補う。

便利なフラグ: `--site`、`--mode`、`--gallery-class`、`--scroll`、`--max-pages`、`--delay`、`--timeout`、
`--user-agent`、`--keep-*`、`--download-full-images`、`--download-title-contains`、`--no-headless`。

## 対応サイト

2 つの抽出モード:

- **`gallery`** —— 構造化: ギャラリーアンカー（アンカークラス + `data-title`/`data-imageid`/`data-thumb`）を読む。
  項目ごとのメタデータが豊富。
- **`images`** —— 汎用: レンダリング後のページの `<img>`/`srcset` 画像を収集（アイコン/アバター/ロゴ等の
  明らかな装飾はフィルタ）。大半のサイトで動作。

モード/プリセットは各 URL のドメインから自動判定され、`--site`/`--mode`/`--gallery-class` で上書き可能。

| サイトキー | ドメイン | モード | 備考 |
| --- | --- | --- | --- |
| `gameuidatabase` | gameuidatabase.com | gallery | Game UI Database —— 構造化ギャラリー（`--browser` 必須；SPA+CF 注意）。 |
| `interfaceingame` | interfaceingame.com | images | Interface In Game —— ゲーム UI スクショ（作品別ページ推奨）。 |
| `screenlane` | screenlane.com | images | モバイル UI/UX フロー。 |
| `collectui` | collectui.com | images | デイリー UI インスピレーション。 |
| `landbook` | land-book.com | images | ランディングページギャラリー。 |
| `lapaninja` | lapa.ninja | images | ランディングページ事例。 |
| `refero` | refero.design | images | Web/iOS UI インスピレーション。 |
| `dribbble` | dribbble.com | images | デザインショット（公開ページ）。 |
| `behance` | behance.net | images | クリエイティブショーケース（公開ページ）。 |

プリセットの無い **その他** のサイトは `images` モード（汎用収集）が既定。ログインが必要なギャラリーは非対応。

## 設定の探索

`--config` なしの場合、CLI は `ui_ref_config.json` を次の順で探す:

```text
ui_ref_config.json
ui_research/ui_ref_config.json
docs/ui_research/ui_ref_config.json
```

別の場所から特定のプロジェクトフォルダを対象に実行するには `--project-root` を使う。

## エチケット

実行は小さく・ゆっくり（既定は 8 秒遅延・実行ごと 20 ページ）。収集したページは引用/参照のコンテキストとして
扱う —— 再配布用のアセットパックでも、学習データでもない。

## ライセンス

MIT —— [LICENSE](LICENSE) を参照。
