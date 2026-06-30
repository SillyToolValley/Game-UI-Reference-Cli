# Example — Lucid Dawn: Dream Survivor (UX/UI spec)

A complete, generated UX/UI spec produced by the **`game-ui-spec`** skill from references harvested
with **`ui-ref`**. It shows, end to end, what this repo's output looks like.

## Contents
- **Spec** — `lucid_dawn_ui_ux_spec.en.md` / `.zh.md` / `.ko.md` / `.ja.md` (+ matching PDFs). 12 screens (out-game + in-game).
- **Wireframes** — `wireframes/*.svg` (+ rendered `*.png`): 13 annotated frames + `flow.svg`.
- **Design tokens** — `lucid_dawn_ui_ux_tokens.md` (color hex / type / motion / USS mapping).
- **Decision & number tracker** — `lucid_dawn_ui_ux_decisions.md` (each number tagged GDD-locked / standard / estimated).
- **References** — `references/ui/web-refs/` (harvested thumbnails; see `references/CITATIONS.md`).

## What it demonstrates
Every UI element is numbered, its region boxed/circled, a leader line pulled **outside** the frame to
a gutter label. Under each screen sit a legend, a state matrix, an input-parity table, a data-binding
table verified against the GDD, and a plain-language UX rationale. The spec also ships production-grade
companions: design tokens, a decision tracker, an engine-binding appendix (UI Toolkit × DOTS), and a
usability-test plan. (For a quick tour and captures, see the repo's main [README](../../README.md).)

## Languages
The spec is provided in four languages — read whichever you prefer:
[English](lucid_dawn_ui_ux_spec.en.md) ·
[Chinese](lucid_dawn_ui_ux_spec.zh.md) ·
[Korean](lucid_dawn_ui_ux_spec.ko.md) ·
[Japanese](lucid_dawn_ui_ux_spec.ja.md).
Design tokens and the decision tracker are shared (English).

## A note on the references
The spec embeds reference thumbnails inline. They are **low-resolution research citations** (source:
interfaceingame.com per-game pages) — not a redistributable asset pack. See `references/CITATIONS.md`
for sources and how to regenerate them with `ui-ref`.

## A note on the game
*Lucid Dawn: Dream Survivor* is a survivor-like/roguelite used here purely as a worked example. The
spec is derived from its GDD; every number cites a GDD section or is flagged in the decision tracker.
