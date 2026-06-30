---
name: game-ui-spec
description: >-
  Produce an exemplary game UX/UI design spec (UI/UX 기획서) from a GDD or feature
  brief — especially for survivor-like / bullet-heaven / roguelite games. Use when the
  user wants a UI spec, screen spec, HUD design doc, annotated wireframes, 화면 기획서,
  or "design the UI/UX for <screen>". Output is an annotated-wireframe spec: reference
  images linked as separate files, wireframes derived from them, every UI element
  numbered with a circle/rectangle region and a leader line pulled outside the frame to
  a description, plus a plain-language "UX 설계 의도" for every screen that a mixed team can read.
---

# game-ui-spec — exemplary game UX/UI specs (기획서)

A generic "make me a UI/UX spec" prompt yields vague prose. This skill produces a
**traceable, implementable, annotated-wireframe spec** in the format the user expects:

1. **Reference images linked as separate files** (never embedded) — harvested with this
   repo's `ui-ref` CLI from recognized galleries.
2. **Wireframes derived from those references.**
3. **Every UI element numbered**, its region marked with a **rectangle or circle**, a
   **leader line pulled outside the frame** to a short label, with full detail in a
   numbered **legend table**.
4. **A plain-language `UX 설계 의도`** per screen — the *why* behind the design, written for a
   mixed meeting audience (no framework names / academic jargon in the body; reason with the
   heuristics privately). This is the part most often done badly — make it readable, not an
   afterthought.
5. **Recognized game-UI templates** (survivor-like / roguelite) baked into every screen.

## When to use
Triggered when the user asks to design or spec the UI/UX of a game: a HUD, a screen, a
flow, a 화면 기획서 / UI 기획서, or "뽑아줘" a UX/UI spec from a GDD. Works best with a
GDD or feature brief in hand; if none exists, ask for the screen list and core loop first.

## Process (follow in order)

**0. Scope.** Read the GDD/brief. List the screens to spec and the game state each maps to.
Identify genre conventions (survivor-like? roguelite? — see `references/screen-exemplars.md`).

**1. Gather references → embed them inline.** Run the harvest in `references/ui-ref-cli.md`
(`ui-ref init` → Game UI Database deep-links in `ui_research/urls.txt` →
`ui-ref collect --browser --download-gallery-assets` → curate into
`references/ui/<collection>/<category>/` → `ui-ref scan-local`). Then **embed the curated
images inline** in each screen's `#### 참조` section with the 무엇을/왜 notes (§5 of
ui-ref-cli.md) — not as separate files. The browser path needs `pip install -e ".[browser]"
&& playwright install chromium`; if you can't harvest, describe the pattern in words inline +
a top banner. Pick exemplars from `references/screen-exemplars.md`.

**2. Lay out the document.** Copy `templates/spec-skeleton.md`. Fill §0–4 (표지, 개요·목표,
사용자·맥락 + 디자인 원칙, 화면 흐름도 + 레퍼런스 보드, 컴포넌트 인벤토리). Rules:
`references/spec-structure.md`.

**3. Draw each screen's annotated wireframe.** Copy `templates/wireframe-kit.svg` →
`wireframes/<screen-id>.svg`. Lay layout zones from the references, then add per element:
region (rect/circle) → numbered badge → leader line out to a gutter label. Conventions and
the anti-crossing rules: `references/annotated-wireframe-svg.md`.

**4. Write each per-screen section.** Copy `templates/per-screen.md`. Fill the legend table,
state matrix, input parity, data-binding, navigation, edge cases, accessibility — then the
**UX 설계 의도** in plain Korean (reason with `references/ux-heuristics.md`, but **don't name
frameworks in the body**). When you fill the data-binding table, **verify every field/event
name against the GDD** (§12-1/§12-2) and shunt any invented name to the "UI events requiring
GDD additions" table — don't fabricate.

**5. Cross-cutting + close.** Fill §6 공통 규칙 + UX 설계 의도 종합 (cross-screen risks in plain
language, tied to the GDD risks by description), §7 미해결 질문, §8 버전 이력, appendix (link the
`scan-local` manifest + the optional "설계 근거(방법론)" note).

**6. Validate (run the checklist; don't mark done until all pass).**
- **SVG lint:** `python templates/validate_wireframe.py wireframes/*.svg` (XML well-formed,
  background rect, ≤10 callouts, badges appear twice, leaders ≤4 pts & non-crossing, gutter
  balance ≤6/side, no off-canvas clipping).
- **Visual render (mandatory when a browser exists):** render each SVG to PNG and eyeball —
  no clipped CJK labels, no crossings, and **geometry matches the prose** (the top-center
  element really is the timer/boss bar the spec claims).
- **Legend↔badge:** every SVG number maps 1:1 to a legend row (same code).
- **Vocabulary:** no data-binding cell asserts an invented event as a GDD §12-1 event.
- **UX 설계 의도:** each section is plain Korean (no framework names / jargon in the body),
  covers both "can they operate it" and "will they keep playing," and closes with the screen's
  top things-to-watch + mitigation. Methodology names appear only in the appendix, if at all.
- **Consistency:** no element (by code) is described with conflicting positions across
  sections; every number is cite-or-flagged; state-branching GWTs enumerate branches.
- **Refs:** if no images committed, the top-of-spec board banner is present.

**7. Render the shareable deliverables.** The raw `.md` is the editable source, but a
10-column legend table wraps to mush in a narrow markdown view. Produce two wide 16:9
landscape outputs from the same source:
```bash
pip install markdown python-docx
python templates/build_pdf.py  spec.md     # read-only share: wide 16:9 PDF (+ spec.html)
python templates/build_docx.py spec.md     # editable share: landscape .docx (Word/Google Docs)
```
(References are embedded inline in the spec now, so no `--append` is needed. `--append` still
exists for stitching in extra sections if you ever want them.)
- **`spec.pdf`** (+ `spec.html`) — 16:9 page (`spec-pdf.css`, JetBrains Mono): tables across
  the full width with Korean `word-break:keep-all` (no mid-word wrap), repeated headers, each
  screen on its own page, wireframes + inline reference images embedded. Headless Chrome/Edge.
- **`spec.docx`** — landscape Word doc anyone on the team can edit (wireframes embedded as
  their PNG renders, so run the PDF/SVG render first). `.md` = source, PDF = read, DOCX = edit.
- **Render gotcha:** `chrome --headless --screenshot=wireframes/x.png` sometimes writes nothing
  to a project subfolder (profile/permission). Render to a temp dir then copy into `wireframes/`.

## Process — OPTIONAL downstream stages (steps 8–11): lift the spec to production-grade

The base spec (steps 0–7) is an **annotated-wireframe spec, not a hi-fi mockup**. When the user
wants it "production-grade / 출하급", add these. Each has a template; fill it as a companion doc
and link it from the spec's §4 + appendix.

**8. Design tokens** (`templates/design-tokens.md` → `<spec>_tokens.md`). Color hex / typography /
spacing / radius / **motion tokens (cite GDD timings)** / colorblind palette + **engine variable
mapping** (UI Toolkit USS `--var`, Unreal Slate, CSS props). This is the single biggest gap — without
it the "component inventory" is empty name-tags. Color never carries meaning alone.

**9. Decisions/number tracker** (`templates/decisions-tracker.md` → `<spec>_decisions.md`). Classify
EVERY number as `GDD확정 / 표준 / 추정` with status `OPEN/PROPOSED/LOCKED`, proposed default + how to
confirm. Collect all `[확정 필요]` here. Keeps author-guessed timings from masquerading as canon.

**10. Engine binding** (`references/engine-binding.md` → a spec appendix). Tie §5 data-binding to the
chosen engine (UI Toolkit×DOTS, Unreal UMG×Mass…): no-GC event-driven updates, world vs screen space,
heavy world text off the UI framework, localization. Grounds the spec in the real stack.

**11. Usability test plan** (`templates/usability-test.md` → a spec appendix). Task scenarios ↔
acceptance criteria, metrics (success rate / SUS / readability-under-chaos / colorblind), pass bar,
iteration loop. The UX 고찰 is heuristic reasoning — this is how it gets validated. (Wireframe-only
claims like readability-under-chaos MUST be re-validated in an engine build.)

## Load-bearing rules (do not skip — these are the silent failures)

- **Positioning: this is a wireframe-level spec, not a hi-fi mockup.** Say so. Tokens (step 8),
  mockups, clickable prototypes, and playtests (step 11) are downstream. Don't let "exemplary"
  read as "finished UI."
- **Number-source labels.** Every numeric in a GWT/legend carries its provenance — cite the GDD
  line, mark `표준` (WCAG/platform), or tag `[PLACEHOLDER — needs GDD/playtest]`. Author-supplied
  timings (animation ms, thresholds) go to the decisions tracker (step 9), never as silent canon.

- **Embed references INLINE — never as separate files/links.** Each screen's `#### 참조`
  subsection embeds the curated reference images + the 무엇을/왜 notes **directly in the
  spec body** (`![](references/ui/<collection>/<category>/x.jpg)`), so they show in the PDF
  and the Word doc. Do **not** put references in `references/<screen>.md` and link to them —
  in a PDF/Word a link to a local `.md` is **dead** and the recipient doesn't have the file.
  See `references/ui-ref-cli.md` §5. Derive the wireframe FROM these references. If you can't
  harvest images, describe the borrowed pattern in words inline + a top-of-spec banner that
  images are pending — but prefer running the `ui-ref` harvest so real images embed.
- **One `.svg` file per wireframe; never inline `<svg>` in markdown** (GitHub strips it →
  renders nothing). Embed with `![<screen> wireframe](../wireframes/<id>.svg)`.
- **First drawn element of every SVG is a full-canvas background `<rect>`** (else light
  gutter labels vanish in GitHub light mode). Canvas is **1760×820** (right gutter widened
  so CJK labels don't clip). The kit has it — keep it.
- **SVG label length is a PIXEL budget (CJK ≈ 2× Latin): ≤ ~12 Hangul / ~22 Latin per
  gutter line; never let text pass x=1760.** All detail lives in the legend table. Cap
  8–10 callouts per frame; split otherwise. Leaders make exactly one vertical bend and
  never cross; never route a leader across the open play-center.
- **Geometry must match the prose.** If the spec claims a layout convention, the wireframe
  must implement it (e.g. boss bar occupies the *same* slot the timer occupied). Otherwise
  follow the GDD's explicit placement and **document the deviation** — don't assert a
  convention you don't draw.
- **GDD vocabulary check (most important).** Every data-binding field/event name must be
  copy-verifiable to a GDD table (§12-1 events / §12-2 fields). **Never invent `OnX`/`XChanged`
  event names and claim they're canonical.** Split the binding table into field / GDD-event /
  UI-proposed columns; list invented events in a "UI events requiring GDD additions" table.
- **Immutable element codes** (`A1`, `D7`, `K4b`): never change, retired-never-reused, new
  ones appended. The badge shows the running number; the legend carries the code.
- **States are mandatory.** Every interactive element gets the full state matrix
  (default/hover/focus/pressed/selected/disabled/loading/empty/error). Distinguish a
  loading=entry-animation from loading=data-unavailable. Justify every `—`. Never convey a
  state by color alone.
- **Given-When-Then acceptance criteria** on every element and non-default state —
  measurable ("200ms 이내"), never "빠르게"; **enumerate each branch** when behavior depends
  on game state. **Cite-or-flag every number** (HP%, latency, guarantee): cite the GDD line
  or tag `[PLACEHOLDER — needs GDD confirmation]`.
- **Shareable deliverables are wide landscape PDF + editable DOCX, not the raw `.md`.**
  Markdown is the source; render a 16:9 **PDF** (`build_pdf.py`) for clean reading and a
  landscape **.docx** (`build_docx.py`) for teammates to edit in Word/Google Docs, so the
  wide legend/state tables stay readable. Keep cells concise (the page is wide, not infinite).
  See Process step 7.
- **The "UX 설계 의도" section is the core deliverable — write it in PLAIN language.** The UX
  frameworks in `ux-heuristics.md` are the AI's *thinking tool*, not the reader's vocabulary:
  reason with them, but the document NEVER names them. No "Hodent / Nielsen #1 / diegetic /
  juice budget / GWT / 역피라미드 / FTUE" in the body — each point is the decision + a plain
  Korean why. Group by reader themes (한눈에 읽히게 / 조작·실수 방지 / 재미·손맛 / 첫 플레이 vs
  반복 / 접근성), cover both "can they use it" and "will they enjoy it", and close with the
  screen's top-3–5 things-to-watch + mitigation. Put methodology names, if at all, ONCE in a
  "설계 근거(방법론)" appendix.

## Files in this skill
- `references/ux-heuristics.md` — the UX reasoning checklist (the AI's *thinking tool*) +
  the methodology table for the optional appendix. **Reason with it, then write plainly.**
- `references/screen-exemplars.md` — recognized templates per screen type + Game UI
  Database deep-links. (Covers survivor-like / roguelite screens. **If the target genre
  isn't listed, harvest 3+ exemplars per screen and derive the pattern explicitly** before
  drawing — don't force survivor-like conventions onto a strategy/card/sim game.)
- `references/annotated-wireframe-svg.md` — the SVG callout kit conventions + anti-crossing
  rules + the validation step.
- `references/spec-structure.md` — document skeleton, per-screen anatomy, and the hard rules.
- `references/ui-ref-cli.md` — the `ui-ref` reference-harvesting workflow.
- `templates/` — `spec-skeleton.md`, `per-screen.md`, `wireframe-kit.svg`, `legend-table.md`,
  `validate_wireframe.py` (SVG lint, step 6), `spec-pdf.css` + `build_pdf.py` (landscape PDF,
  step 7), `build_docx.py` (editable landscape Word, step 7).
- `examples/` — a worked example spec (see `examples/README.md`).
