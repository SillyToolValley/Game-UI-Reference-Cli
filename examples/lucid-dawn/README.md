# Example — Lucid Dawn: Dream Survivor (UX/UI design)

A complete, generated UX/UI design produced by the **`game-ux-ui-design`** skill from references harvested
with **`ui-ref`**. It shows, end to end, what this repo's output looks like.

## Contents
- **Design** — `lucid_dawn_ui_ux_design.en.md` / `.zh.md` / `.ko.md` / `.ja.md` (+ matching PDFs). 12 screens (out-game + in-game).
- **Wireframes** — `wireframes/*.svg` (+ rendered `*.png`): 13 annotated frames + `flow.svg`.
- **Art concept** — `art-concepts/levelup-ui-art-concept.png`: one optional imagegen pass from the
  level-up wireframe + GDD/design context + harvested reference notes.
- **Design tokens** — `lucid_dawn_ui_ux_tokens.md` (color hex / type / motion / USS mapping).
- **Decision & number tracker** — `lucid_dawn_ui_ux_decisions.md` (each number tagged GDD-locked / standard / estimated).
- **References** — `references/ui/web-refs/` (harvested thumbnails; see `references/CITATIONS.md`).

## What it demonstrates
Every UI element is numbered, its region boxed/circled, a leader line pulled **outside** the frame to
a gutter label. Under each screen sit a legend, a state matrix, an input-parity table, a data-binding
table verified against the GDD, and a plain-language UX rationale. The design also ships production-grade
companions: design tokens, a decision tracker, an engine-binding appendix (UI Toolkit × DOTS), and a
usability-test plan. (For a quick tour and captures, see the repo's main [README](../../README.md).)

## Optional art concept pass

The design can optionally include a small UI art-direction pass after the wireframes are stable. This
example includes one generated concept for the level-up / item-pick modal:

![Level-up UI art concept](art-concepts/levelup-ui-art-concept.png)

Treat it as mood/material direction only. Exact text, measurements, states, data binding, and
accessibility rules still come from the design document and tokens.

## Languages
The design is provided in four languages — read whichever you prefer:
[English](lucid_dawn_ui_ux_design.en.md) ·
[Chinese](lucid_dawn_ui_ux_design.zh.md) ·
[Korean](lucid_dawn_ui_ux_design.ko.md) ·
[Japanese](lucid_dawn_ui_ux_design.ja.md).
Design tokens and the decision tracker are shared (English).

## A note on the references
The design embeds reference thumbnails inline. They are **low-resolution research citations** (source:
interfaceingame.com per-game pages) — not a redistributable asset pack. See `references/CITATIONS.md`
for sources and how to regenerate them with `ui-ref`.

## A note on the game
*Lucid Dawn: Dream Survivor* is a survivor-like/roguelite used here purely as a worked example. The
design document is derived from its GDD; every number cites a GDD section or is flagged in the decision tracker.
