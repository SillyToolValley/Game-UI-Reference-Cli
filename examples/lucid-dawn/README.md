# Example — Lucid Dawn: Dream Survivor (UX/UI spec)

A complete, generated UX/UI spec produced by the **`game-ui-spec`** skill from references harvested
with **`ui-ref`**. It shows what this repo's output looks like end to end.

*由 `game-ui-spec` 技能基于 `ui-ref` 收集的参考生成的完整 UX/UI 规格书示例。*
*`ui-ref`로 수집한 레퍼런스를 바탕으로 `game-ui-spec` 스킬이 생성한 완전한 UX/UI 기획서 예시.*
*`ui-ref` で収集したリファレンスをもとに `game-ui-spec` スキルが生成した完全な UX/UI 仕様書のサンプル。*

## Contents
- **Spec** (12 screens, out-game + in-game) — `lucid_dawn_ui_ux_spec.en.md` / `.zh.md` / `.ko.md` / `.ja.md` (+ PDFs)
- **Wireframes** — `wireframes/*.svg` (+ rendered `*.png`), 13 annotated frames + `flow.svg`
- **Design tokens** — `lucid_dawn_ui_ux_tokens.md` (color hex / type / motion / USS mapping)
- **Decision & number tracker** — `lucid_dawn_ui_ux_decisions.md` (GDD-locked / standard / estimated)
- **References** — `references/ui/web-refs/` (harvested thumbnails; see `references/CITATIONS.md`)

## What it demonstrates
Every UI element is numbered, its region boxed/circled, a leader line pulled **outside** the frame
to a gutter label; underneath each screen sits a legend + state matrix + input parity + GDD-verified
data binding + a plain-language UX rationale. Plus production-grade companions: design tokens, a
decision tracker, an engine-binding appendix (UI Toolkit × DOTS), and a usability-test plan.

> The spec embeds reference thumbnails inline. They are **low-res research citations** (source:
> interfaceingame.com per-game pages) — not a redistributable asset pack. See `references/CITATIONS.md`.
> To regenerate them: `ui-ref collect --browser --site interfaceingame` over the URLs in
> `references/CITATIONS.md`, then `ui-ref scan-local`.

## Note on the game
*Lucid Dawn: Dream Survivor* is a survivor-like/roguelite used here purely as a worked example.
The spec is derived from its GDD; numbers cite GDD sections or are flagged in the decision tracker.
