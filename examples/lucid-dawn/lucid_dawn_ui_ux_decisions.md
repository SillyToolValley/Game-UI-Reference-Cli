# Lucid Dawn — UI/UX Decision & Number Tracker (living doc)

> Every number / open decision in `lucid_dawn_ui_ux_design.*.md`, classified by **source** so it gets locked before ship.
> Source: **`GDD`** (cite line) · **`STD`** (WCAG/platform/a11y) · **`EST`** (author proposal — confirm via design/playtest).
> Status: `OPEN` · `PROPOSED` (has default) · `LOCKED`. Shared across EN/中文/한글 design versions.

## 1. GDD-locked values (use as-is)
| value | GDD § | UI use |
| --- | --- | --- |
| Run timer 0–1200s (6:40→7:00), final-60s warning | §4-1 | alarm A2, time inset A13 |
| Boss warning 5s | §4-1 | BossWarning |
| Lucid time-stop 0.45s / ICD 0.40s / combo 6.0s / counter window 0.7s | §4-3 | combo A6, counter A12, motion tokens |
| Boss reward protect 8s / groggy 4.0s / phase HP55% | §7-1 | reward I4, groggy A11, boss bar A10 |
| Seal thresholds 260/620/1080/1640 | §4-2 | purify A7, seal A3 |
| Char stats (HP/move/dash dist·cd·safe/lucid window) | §4-3·§5 | char select E6 |
| Enemy hard cap 180 | §6-4 | HUD readability goal (P3) |
| Difficulty multipliers (Sleepy–Lucid) | §2-4 | stage/difficulty G5 |
| Pick counts (3 / elite 3 / boss 4), Rare guarantee, owned 6, category 3, no reroll | §4-5 | level-up I3, reward I4 |
| Reward order (SP-grant → tree → 4-pick) | §12-3 | I4 |

## 2. Standard values (industry/a11y — locked, cite)
| value | std | use | status |
| --- | --- | --- | --- |
| body text contrast ≥ 4.5:1 | WCAG 2.2 AA | all text | LOCKED |
| large text/UI/focus ring ≥ 3:1 | WCAG 2.2 AA / Game A11y | focus·bars | LOCKED |
| no color-only state (color+shape+text) | Game Accessibility Guidelines | all states | LOCKED |
| subtitle ~≤38 chars/line | Game A11y | subtitles | PROPOSED |
| TV-safe 5% | console cert | layout | PROPOSED |

## 3. Estimated — needs design/playtest (proposed defaults)
| # | item | screen | now (proposed) | source | status | how to confirm |
| --- | --- | --- | --- | --- | --- | --- |
| D-01 | low-HP warning threshold | I1 A4 | **25%** | EST | OPEN | playtest (near-death recognition); GDD lacks → consider adding |
| D-02 | UI input reaction budget | global | **100ms** | EST/HCI | PROPOSED | measure input latency |
| D-03 | value-reflect (bar fill) budget | I1 | **200ms** | EST | PROPOSED | readability test |
| D-04 | seal light-up motion | I1 A3 | **300ms** | EST | PROPOSED | art/motion lock |
| D-05 | character preview swap | O2 E4 | **200ms** | EST | PROPOSED | load measure |
| D-06 | card read time | I3 B4 | **≤1s** | EST | PROPOSED | usability test |
| D-07 | card-confirm i-frame | I3 B4 | **[TBD]** | EST | OPEN | VS convention + balance |
| D-08 | empty-pool fallback reward | I3 | **[TBD]** (small heal?) | EST | OPEN | GDD decision |
| D-09 | unspent SP at 8s protect end | I4 | **keep (assumed)** | EST | OPEN | GDD decision |
| D-10 | FailedWake meta reward ratio | I6 | **[TBD]** | EST | OPEN | economy balance |
| D-11 | toast merge/throttle threshold | I1 | **[TBD]** | EST | PROPOSED | 180-enemy stress test |
| D-12 | boss HP phase segments | I2 A10 | **1 boundary (55%)** | GDD-derived/EST | PROPOSED | expand if more phases |
| D-13 | counter-window placement | I2 A12 | **[TBD]** (world vs HUD) | EST | OPEN | readability test |
| D-14 | promote XP bar to §9-2 HUD list | I1 A1 | **UI-proposed** | EST | OPEN | GDD §9-2 revision |
| D-15 | difficulty lock (meta condition) | O3 G5 | **[TBD]** | EST | OPEN | meta design |
| D-16 | codex spoiler policy | O5 | **"undiscovered" (assumed)** | EST | OPEN | direction |
| D-17 | text scale range | O4 | **80–150%** | EST/STD | PROPOSED | a11y QA |
| D-18 | 21:9 / 4:3 HUD scale rule | global | **[TBD]** | EST | OPEN | multi-resolution pass |

## 4. GDD additions needed (data contract) — design document §7 Q13
Runtime state fields (`RunState`/`PlayerRuntime`/`SkillSlot`/boss·trial runtime) + UI events (`RunTimerTick`, `HpChanged`, `DreamEnergyChanged`, `PurgeGaugeChanged`, `BossHpChanged`, `TrialStarted` …) are absent from GDD §12-1/§12-2 → **add at TDD handoff**. No cash-purchase events (§10 BM).

## 5. Rules
- Every `OPEN` must be `LOCKED` before ship. Change estimated numbers here only; the design document references this doc.
- New design document numbers must carry a source label (GDD/STD/EST) and be registered here.
