# Annotated wireframe kit (SVG) — how to draw numbered callouts with leader lines

This is the heart of the deliverable. Every screen in the design document gets ONE annotated
wireframe: a 16:9 screen drawn as boxes, with **each UI element numbered, its region
marked by a rectangle or circle, and a leader line pulled OUTSIDE the frame to a short
label**. The full description for each number lives in a **legend table** beneath the
image — never crammed into the picture.

Pair this file with `../templates/wireframe-kit.svg` (copy it per screen).

---

## Why SVG (and not ASCII / Mermaid / a screenshot)

| Need | SVG | ASCII | Mermaid | screenshot |
| --- | --- | --- | --- | --- |
| Boxes + circles for regions | ✅ | rough | ✗ | n/a |
| **Leader line pulled outside the frame** | ✅ | ✗ | ✗ | ✗ |
| Numbered badges on regions | ✅ | rough | ✗ | manual |
| Renders in GitHub / VS Code preview as a file | ✅ | ✅ | ✅* | ✅ |
| Editable in text by an AI, diff-able | ✅ | ✅ | ✅ | ✗ |

SVG is the only text format that does the user's exact ask — **번호 + 동그라미/네모 영역표시
+ 밖으로 뽑은 선 + 설명**. Always ship an SVG. Optionally add a tiny ASCII layout map
(below) as a fast-scan companion, but the SVG is the source of truth.

> Rendering note: link the `.svg` as a **file** — `![HUD](wireframes/hud.svg)` — so its
> internal `<style>` applies. Do **not** paste raw `<svg>` inline into the `.md`: GitHub
> sanitizes inline SVG and the CSS classes won't apply. A standalone `.svg` file renders
> correctly in GitHub, VS Code preview, and browsers.

> **Two silent failures to avoid** (both make the diagram look broken in review):
> 1. **No background rect → labels vanish.** The gutter labels are light text. With a
>    transparent canvas they render on the page background and disappear in GitHub light
>    mode. The kit's **first drawn element is a full-canvas `<rect ... fill="#0b0f1a"/>`** —
>    keep it.
> 2. **Inline `<svg>` in markdown → renders nothing.** GitHub strips raw inline SVG
>    (XSS sanitization). Always a separate `.svg` file + `![]()`. Also avoid `<script>`,
>    CSS animation, and `<foreignObject>` (sanitized away).

---

## The coordinate contract (memorize this)

```
viewBox: 0 0 1760 820
┌─ left gutter ─┐┌──────────── SCREEN FRAME 16:9 ────────────┐┌── right gutter ──┐
 x: 0 .. 190      x: 200 .. 1480  (w=1280)  y: 50 .. 770       x: 1490 .. 1760
 labels live      the game screen you are speccing             labels live here
 here                                                          (270px ≈ 12 Hangul)
```

- **Frame**: `x=200 y=50 w=1280 h=720`. This is the playable 16:9 screen (1920×1080 ref).
- **Gutters**: left `0–190`, right `1490–1760`. Callout labels go in the gutter **nearest**
  the element they describe. (The canvas is 1760 wide — widened from 1680 — so CJK
  right-gutter labels don't clip off-canvas.)
- **Label length is a PIXEL budget, not a char count (CJK-aware).** A Hangul/CJK glyph at
  font-size 18 is ~18px — roughly **2× a Latin char**. Right gutter is 270px, so keep
  right-gutter label text ≤ **~12 Hangul** (or ~22 Latin). Text must never pass `x=1760`
  (it is dropped, not just tight). If it would, shorten the label and move detail to the
  legend, or right-anchor it (`text-anchor:end` at x=1742) so it grows leftward.
- **Stagger** labels vertically — keep label rows ≥ 44px apart so leader lines never
  collide.
- **Balance the two gutters.** Do NOT dump most callouts on one side. Aim for a roughly
  even split, **≤ 6 labels per gutter**. With 10 callouts, target ~5 left / ~5 right. If
  one side would exceed 6, push the lowest-priority callouts to the other gutter even if
  it's slightly farther — a balanced board with one longer leader beats a crowded stack of
  near-parallel leaders. (Left-gutter crowding is the most common first-draft mistake.)
- A leader line **bends at most once** (out horizontally, then up/down to the label row).
  Leader lines **must not cross** each other.

---

## The five reusable pieces

Copy these from `wireframe-kit.svg`. Each callout is one `<g id="cN">` containing:

1. **Region** — `rect` (panels, bars, areas) or `circle` (single icon/button/dot):
   ```svg
   <rect x".." y".." width".." height".." rx="6" class="region"/>
   <circle cx".." cy".." r".." class="regionC"/>
   ```
2. **Numbered badge** on the region (so the eye links picture→number):
   ```svg
   <g transform="translate(X,Y)"><circle r="15" class="badge"/><text class="badgeT">N</text></g>
   ```
3. **Leader line** from the region edge out to the gutter. **Exactly ONE vertical bend
   between two horizontal runs** (a single staircase step): start horizontal from the
   region edge, one vertical move in the gutter channel, then horizontal to the label.
   That is the 4-point pattern below — **two axis-changes count as "one bend"; do not add
   an extra stub** (a 5-point leader that first escapes up through the mock is disallowed):
   ```svg
   <polyline class="lead" points="REGION_EDGE_X,Y  OUT_X,Y  OUT_X,LABEL_Y  GUTTER_X,LABEL_Y"/>
   ```
4. **Gutter label** — badge + short name + tiny meta (position · condition):
   ```svg
   <g transform="translate(GUTTER_X,LABEL_Y)">
     <circle cx="14" cy="0" r="13" class="badge"/><text x="14" y="0" class="badgeT">N</text>
     <text x="34" y="0"  class="callTb">짧은 이름</text>
     <text x="34" y="20" class="callT">top-left · 항상</text>
   </g>
   ```
5. **Layout zones** (optional, drawn first) — faint boxes so the wireframe reads like a
   real screen before callouts go on top (`class="zone"`).

Numbering order: **top→bottom, then left→right** (reading order). Keep numbers sequential
with no gaps; the legend table uses the same numbers.

**Cap 8–10 callouts per frame.** If a screen has more elements, split it into two
diagrams (e.g. `hud.svg` + `hud-boss.svg`) rather than crowding leaders. A frame with
15 crossing leaders is unreadable — and unreviewable.

**Anti-patterns (these survive only when the frame is sparse, then fail on a dense one):**

- **Never route a leader across the open play-center.** A central element (boss bar,
  on-player combo) that can't reach a gutter without a long traversal of the empty middle
  is a sign to **split into a second diagram** — e.g. put the boss-fight HUD in its own
  `hud-boss.svg`. Two long near-parallel leaders crossing the play zone are the "spaghetti"
  the kit exists to avoid; they read fine only because the center happens to be empty.
- **Stagger the vertical channels — don't share one.** If every left leader runs through
  `x=150` and every right through `x=1300`, a leader's horizontal run lands exactly on a
  neighbor's vertical trunk (coincident segments that degrade into crossings as density
  grows). Offset channels slightly (`x=150 / 158 / 166`) **or** order callouts so a label
  row never falls inside a neighbor trunk's y-span.
- **The left-gutter "x=60 sweep" trap (most common real crossing).** A left callout's FINAL
  horizontal run goes from its channel all the way to the label at `x≈60`, so it sweeps the
  whole `60..channel` band at the label's y. If another callout's vertical channel sits in that
  band (e.g. `x=148/158`) and spans that y, they CROSS. Fix: route the crossing callout's label
  **above/below** the other's exit y (so its vertical channel's y-range doesn't include the
  sweep), or move its channel left of the other's terminus. Re-run `validate_wireframe.py` after
  each move — it reports the exact crossing point. (Mirror on the right gutter toward `x=1530`.)

**Convention conformance (geometry must match the prose).** If the design's text promises a
layout convention (e.g. "timer top-center, boss bar takes over that slot"), the wireframe's
geometry must actually implement it: the boss bar must occupy the **same screen region** the
timer occupied. If your timer is in a corner, you are NOT implementing the takeover pattern —
either center it or **drop the claim and document the deviation** (see `screen-exemplars.md`).
Mismatched prose-vs-geometry is the #1 way a wireframe silently contradicts its own design document.

**Immutable element codes (for multi-version design documents).** When the design document will live across
versions, give each element a stable hierarchical code in the legend — UPPERCASE section
letter + number + optional variant letter (`A1`, `D7`, `K4b`). Codes **never change** and
a removed element's code is **retired, never reused**; new elements append at the end. The
SVG badge shows the running number; the legend table carries the immutable code. This is
what keeps a callout traceable when the wireframe is redrawn. (Convention: UXMatters
cascading UX design documents.)

---

## Rectangle vs circle — when to use which

- **Rectangle** (`class="region"`): panels, bars, meters, card rows, lists, multi-element
  clusters, anything with area (HP bar, XP bar, ability tray, boss bar, card grid).
- **Circle/ellipse** (`class="regionC"`): a single point element — one icon, one button,
  a status dot, an avatar, a single resource pip.

---

## Legibility do / don't

| ✅ Do | ❌ Don't |
| --- | --- |
| Keep gutter label text ≤ ~22 chars; real design document goes in the legend table | Write paragraphs inside the SVG |
| Group every callout in `<g id="cN">` | Leave loose elements ungrouped |
| Use dashed strokes + `rx` so regions read as overlays | Solid fills that hide the wireframe |
| Stagger labels; one bend per leader; no crossings | Spaghetti leaders that cross |
| Font ≥ 16px; badges r=13–15 | Tiny text, micro badges |
| Reuse the palette classes from the kit | Re-style every element ad hoc |

---

## The legend table (always directly under the SVG)

Every number in the SVG resolves here. This is where the real design document lives.

```markdown
| # | 요소 | 위치 | 표시 조건 | 동작 / 상태 | 데이터 바인딩 | UX 근거 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 알람 시계 | 좌상단 | 항상 | 초침 회전; 잔여 60s 펄스 | run.timer 0–1200s | 최상위 룰 가시성 — 7시 목표를 항상 인지(가독성/피드백) |
| 2 | … | … | … | … | … | … |
```

- **UX 근거** is mandatory for every row — tie it to a heuristic (see
  `ux-heuristics.md`). A callout with no rationale is decoration, not a design document.
- **데이터 바인딩** ties the element to a game state/event/field so it is implementable
  (e.g. `RunTelemetry.minute_purge`, `BossPattern.telegraph_time`).

---

## Optional ASCII layout map (fast-scan companion)

Put this in a fenced block above the SVG link for readers skimming in plain text. It is
NOT a replacement for the SVG.

```text
┌───────────────────────────── 16:9 ─────────────────────────────┐
│ (1)알람시계  (2)봉인게이지            (9)보스 HP 바              │
│ (3)HP/실드                                                      │
│ (5)드림에너지                                                   │
│                          · 플레이어 ·                           │
│                        (8)루시드 콤보                           │
│                                                                 │
│            (4)정화도 바        (6)스킬슬롯  (7)궁극기 게이지     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Authoring loop (per screen)

1. Decide the layout zones from the reference exemplars + GDD (positions are often given).
2. Copy `wireframe-kit.svg` → `wireframes/<screen>.svg`; lay the zone boxes.
3. For each UI element: draw region → badge → leader → gutter label. Keep reading order.
4. Verify: run the SVG through an XML parse (well-formed), eyeball that no leaders cross,
   labels don't overlap, every number has a legend row.
5. Write the legend table with a **UX 근거** per row.

### Validation — run BOTH on every wireframe (not optional)

**1. Structural lint (dependency-free).** Ship & run `validate_wireframe.py` (in `templates/`).
It checks: XML well-formed, background rect present, ≤10 callouts, every number appears
exactly twice (badge + label), leaders ≤4 points (one bend) and non-crossing, gutter balance
(≤6/side, imbalance ≤2), and off-canvas text clipping:
```bash
python templates/validate_wireframe.py wireframes/hud.svg wireframes/levelup.svg wireframes/results.svg
```
Fix every FAIL before embedding. (The badge↔legend-row mapping still needs an eyeball against
the .md table — the SVG alone can't see the legend.)

**2. Visual render — MANDATORY whenever a headless browser exists** (Edge & Chrome ship on
Windows). The structural lint can't see *how it looks*; the render catches clipped CJK labels
and visual crowding. Do not mark a wireframe done without it. The SVG has no intrinsic size,
so wrap it in an HTML shell sized to the viewBox (1760×820):
```bash
printf '<!doctype html><body style="margin:0"><img src="file:///%s" width="1760" height="820">' "$PWD/wireframes/<screen>.svg" > _v.html
chrome --headless=new --window-size=1760,820 --screenshot=_v.png _v.html   # or msedge
```
Open `_v.png` and confirm: no leader crosses, no gutter label is clipped at the right edge,
labels are legible, and the geometry matches the design's prose (convention conformance).
