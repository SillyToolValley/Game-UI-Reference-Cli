# Examples

A fully worked example (a real *Lucid Dawn* UX/UI 기획서 — HUD / 레벨업 / 결과 화면) was
produced with this skill to validate it end-to-end. **A published, polished sample will be
added here later**, once it's developed further. (The draft + its harvested reference
screenshots are kept local for now and not committed.)

## What a generated spec looks like

Running the skill on a GDD produces, under your project:

```
spec.md                      # the editable markdown source (§0 표지 → §8 + 부록)
spec.pdf / spec.docx         # rendered shares: wide 16:9 landscape (read / edit)
wireframes/<screen>.svg      # annotated wireframes — numbered callouts, region boxes,
                             #   leader lines pulled outside the frame to gutter labels
references/ui/<col>/<cat>/*   # reference screenshots harvested with `ui-ref`, embedded
                             #   INLINE in each screen's `#### 참조` section
references/REFERENCE_BOARD.md # the harvest plan/index (appendix)
```

## The bar this skill aims for

1. **References embedded inline** per screen (real image + the what/why) — no dead links.
2. **Every UI element numbered**, boxed/circled, with a leader line to a label outside the
   frame; full detail in the legend table beneath.
3. **Plain-language `UX 설계 의도`** a mixed team (기획·아트·개발·PM) can read — no framework
   jargon in the body (methodologies, if any, listed once in the appendix).
4. **Implementable:** immutable element codes, measurable 동작 기준, full state matrices,
   data-bindings tied to the GDD's fields/events.

To generate one: copy this skill into your game project's `.claude/skills/`, then ask for
the UX/UI 기획서 of the screens you want (see `../SKILL.md` for the process).
