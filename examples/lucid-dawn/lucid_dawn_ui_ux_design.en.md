# Lucid Dawn: Dream Survivor — Full UI/UX Design (out-game + in-game)

> **Annotated-wireframe design document.** Each screen has ① the real game UI it references (web-harvested with
> `ui-ref`, embedded inline), ② a wireframe derived from it (`wireframes/*.svg`), ③ a numbered legend
> (every element boxed/circled with a leader line pulled outside the frame), ④ state matrix · input
> parity · data binding, ⑤ a plain-language **UX rationale**. Editable source = this `.md`; shareables =
> wide 16:9 PDF/DOCX (Appendix C). Companion docs: **design tokens** `lucid_dawn_ui_ux_tokens.md`,
> **decision/number tracker** `lucid_dawn_ui_ux_decisions.md` (shared by the EN/中文/한글 versions).

> **Reference sources.** Images were harvested with **Game UI Reference CLI (`ui-ref`)** from
> **interfaceingame.com** per-game pages (Hades · Risk of Rain 2 · Honkai: Star Rail · Slay the Spire ·
> Returnal · Hollow Knight · Moonlighter · Destiny 2). Personal research citations, not a redistributable
> asset pack. Index/recipe: Appendix B. Direct survivor-like patterns (Vampire Survivors/Brotato/20MTD)
> are described in words in §B-2 (not on the harvest site).

---

## 0. Cover

| field | value |
| --- | --- |
| Document | Lucid Dawn: Dream Survivor — Full UI/UX Design (out-game + in-game) |
| Game / build | Lucid Dawn: Dream Survivor / Vertical Slice (v0.8 scope, v0.9 GDD) |
| Version / date / author | v1.0 (EN master) / 2026-06-30 / UX |
| Status | draft |
| Source GDD | `GameDesign/lucid_dawn_design_docs/lucid_dawn_gdd.md` (§2 loop, §4 systems, §5 chars, §6 stage, §7 boss, §9 UI/UX, §10 BM/records, §12 TDD handoff) |
| Wireframes | out-game `title-mainmenu/character-select/stage-select/settings/meta-progress/leaderboard.svg`; in-game `hud/hud-boss/levelup/skilltree/results/pause.svg`; `flow.svg` |

---

## 1. Overview & goals

- **Problem this solves**: GDD §9-1 (screen flow) and §9-2 (HUD table) only fix "what goes where". To build it you need every screen's states, inputs, data binding, edge cases, accessibility, and the *why* — from the menus (out-game) through combat/reward/result (in-game).
- **Core experience (GDD §1-1)**: "pressure → split-second read → perfect dodge → lucid rush → purify/grow → waking up by your own hand". The UI must never hide that loop.
- **Measurable success**
  - Out-game: a first-time player starts a run within **3 minutes** (menu depth + label clarity).
  - In-game: at any instant the player reads **time left until 7:00** within 1s (§3-2); at the 180-enemy hard cap (§6-4) the player, lethal bullets, hazard fields and pickups stay distinguishable by **color + shape** (§13-3 #5).
  - Reward flow follows GDD §12-3: **skill point grant → skill tree → separate 4-item pick**.
  - BM (§10): no paid power, no gacha → the meta screen is **play-unlock only (no purchase UI)**.
- **In scope**: out-game O1 Title/Main, O2 Character select, O3 Stage/Difficulty, O4 Options, O5 Meta progress (unlock/codex), O6 Leaderboard; in-game I1 HUD, I2 HUD (boss/hidden), I3 Level-up/item pick, I4 Boss reward (tree + 4-pick), I5 Pause, I6 Result (3 branches).
- **Out of scope (this doc)**: co-op-only UI (lobby/team gauge/ghost/joint ult — GDD §8) is unbuilt in VS → tracked as risk in §6-1; tutorial screens, shop (none per BM), cutscene polish are later.

---

## 2. Users & context

- **Persona**: survivor-like / 20-min-survival / bullet-hell / action-roguelite / co-op-PvE players (GDD §1). Novice (first Dawn Wake) through veteran (Dream Break / no-damage records) coexist.
- **Platform / input**: PC/Steam first. Keyboard+mouse and gamepad both (GDD §2-5). Touch out of scope (design stays pad-parity-extensible).
- **Entry context**: out-game = non-combat, focus-driven; in-game = real-time combat, except level-up/reward picked under pause/protection (§4-5, §7-1). One run = 6:40→7:00 (20 min, internal 0–1200s). HUD only in-run; hidden in menus/result. VS roster = Kohaku, Toko (4 others locked); stage = LD-001 (§3, §5, §6-2).

### 2-1. Design principles (every screen)
| # | principle | meaning here | if broken |
| --- | --- | --- | --- |
| P1 | instant feedback | every action/state change answers at once (sound + display) | weak feel/awareness |
| P2 | hazard legibility | player > immediate threats (bullets/zones/charges) > pickups > ambient | danger unseen |
| P3 | legible in chaos | at 180 enemies the core stays color+shape+sound; cap juice | one-shot patterns buried |
| P4 | consistency | lock position/color/icon/control/bar shape across screens; flag deliberate exceptions | constant confusion |
| P5 | progressive disclosure | core first, rest when needed (lucid/purify/boss taught on first occurrence) | novice overload |
| P6 | accessibility | no color-only (color+shape+text), subtitles, shake/flash/cut-in toggles, remap | colorblind/sensitive excluded |

---

## 3. Wireflow

```text
[Title/Main O1] --any key/single--> ┬ [Character O2] --confirm--> [Stage/Difficulty O3] --start--> (in-run)
                                     ├ [Options O4] · [Meta O5] · [Leaderboard O6] · Quit
(in-run, HUD shown)
[RunStart] --1s--> [NormalRun I1]
   [NormalRun] --level-up--> [Level-up I3] --confirm--> [NormalRun]   (paused)
   [NormalRun] --ESC--> [Pause I5] --resume--> [NormalRun]
   [NormalRun] --purify threshold--> [BossWarning] --appear--> [BossFight I2]
   [BossFight] --defeat--> [BossReward I4: tree→4-pick] --> [NormalRun]
   [4 seals broken] --> [HiddenBossAttempt I2]  (boss HP + time left)
(ending → result)
[HP0]→FailedWake ┐  [7:00]→DawnWake ├─> [Result I6]   [kill hidden boss before 7:00]→DreamBreak ┘
```

![Wireflow](wireframes/flow.svg)

| transition | trigger (event/condition) | to | state ↔ HUD |
| --- | --- | --- | --- |
| Title → Main | any key | Main | HUD hidden |
| Main → Character → Stage → run | single → confirm → start | in-run | HUD shown |
| NormalRun → Level-up | `RunTelemetry.level_reached` ++ | I3 modal | combat **paused** |
| NormalRun → Pause | ESC/Start | I5 | combat **paused** |
| NormalRun → BossWarning | `BossThresholdReached` (§12-1) | warning 5s | HUD kept |
| BossWarning → BossFight | `BossSpawned` (§12-1) | I2 | top-center boss HP takeover |
| BossFight → BossReward | `BossDefeated` (§12-1) | I4 | reward flow, **8s protect** |
| 4 seals → hidden boss | `HiddenBossSpawned` (§12-1) | I2 hidden | boss HP + time left |
| in-run → result | `AlarmReached`/HP0/`DreamBreakAchieved` (§12-1) | I6 | HUD hidden |

### 3-1. Reference overview
Real game UI the wireframes draw from (web-harvested). **Actual images + notes are embedded inline in each screen's `#### References`.** Direct survivor-likes (Vampire Survivors/Brotato/20MTD) aren't on interfaceingame, so patterns come from roguelites (Hades·Slay the Spire·Returnal·RoR2), action (Hollow Knight·Destiny 2), anime (Honkai: Star Rail), with direct-genre patterns in words (§B-2).

## 4. Global component inventory

> **Visual tokens (color hex / type / spacing / motion / USS mapping) live in [`lucid_dawn_ui_ux_tokens.md`](lucid_dawn_ui_ux_tokens.md).** The "tokens" column below points to that file's concrete values (`ld.color.*`). Number-lock status: [`lucid_dawn_ui_ux_decisions.md`](lucid_dawn_ui_ux_decisions.md).

| code | component | variants | tokens (color/shape/rule) | used in |
| --- | --- | --- | --- | --- |
| C-BAR | horizontal meter | hp·shield·xp·purge·dream·boss | horizontal only; per-type color+icon+position; danger = color+blink+border | I1·I2 |
| C-CARD | choice card | common·uncommon·rare·lucid | rarity = color+border+corner icon; new/upgrade text badge; 1s read | I3·I4 |
| C-RADIAL | cooldown radial | skill Q·E·ult R | radial fill + keycap glyph; ready = 1 flash + sound | I1 |
| C-NODE | skill node | locked·available·owned | lock=lock+gray, available=focus border, owned=filled; never color-only | I4·O5 |
| C-LIST | list/grid | menu·roster·stage·option·record | item = icon+label, selected = border+check, locked = lock+condition | O1·O2·O3·O4·O5·O6·I5 |
| C-PANEL | info panel | char·stage·node·item·option·record | title+summary+detail; empty/error microcopy | O2·O3·O4·O5·I4 |
| C-PROMPT | input prompt | mouse·key·pad | auto glyph for current device (no memorization) | all bottom |
| C-BADGE | status badge | rarity·ending·combo·new | color + **text label required** | I3·I4·I6 |

## 5. Screen designs

> Order per screen: Purpose → References → Wireframe → Legend → State matrix → Input parity → Data binding → Navigation → Edge cases → Accessibility → UX rationale → Open questions → Acceptance. Out-game O1–O6, in-game I1–I6.

---

### 5.O1 TITLE — Title / Main Menu · state: menu (HUD hidden)

#### Purpose
First impression and hub to play / options / meta / leaderboard. Convey the "cute nightmare" tone and let a first-timer drop straight into single-player.

| field | value |
| --- | --- |
| Enter | launch / Result "to Main" |
| Exit | single→O2 / co-op (out of scope) / O4·O5·O6 / quit |
| Input context | non-combat, focus |
| Priority | core |

#### References — real game UI this screen draws from
*Source: ui-ref harvest — interfaceingame (main menu).*

![Hades main menu](references/ui/web-refs/title-mainmenu/hades-main-menu-500x281.jpg)
**What.** Logo top-left, vertical menu (Play/Options/…) center-left, character key art right, version top-right, platform/social bottom-left. **Why.** The eye flows "logo→menu" in one column and the art sells the tone. → applied: logo(1)·menu(2)·key art(4)·version(5)·platform/license(6).

![Slay the Spire main menu](references/ui/web-refs/title-mainmenu/slay-the-spire-main-menu-500x281.jpg)
**What.** Few menu items over a large backdrop. **Why.** Minimal items lower first-entry load. → applied: keep menu(2) short.

> Words: GDD §13-3 #1 (license/official-confusion) → reserve an explicit **platform/license line (6)** on the main screen.

#### Wireframe
![TITLE wireframe](wireframes/title-mainmenu.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | T1 | Game logo | top-left | always | static / small motion | static asset | shown on enter | identity/tone | logo+text name |
| 2 | T2 | Menu list | center-left | always | single/co-op/codex·unlock/leaderboard/options/quit; co-op locked (VS) | menu def (static) | select reacts ≤100ms | core path in one column | label text + focus |
| 3 | T3 | Select highlight | menu item | always | focus emphasis + SFX | input focus | highlight on move | where am I | border+color+sound |
| 4 | T4 | Key art | right | always | character illustration | static asset | — | tone/character | decorative (alt text) |
| 5 | T5 | Version | top-right | always | build/version | build meta | — | build id | text |
| 6 | T6 | Platform·license | bottom-left | always | platform/social/license line | static | — | prevent license confusion (§13-3 #1) | text+icon |
| 7 | T7 | Input prompt | bottom | always | current-device prompt | input map (§2-5) | swaps on device change | how to operate | device glyph+text |

#### State matrix (menu item T2/T3)
| element | default | hover/focus | pressed | disabled/locked | error |
| --- | --- | --- | --- | --- | --- |
| Menu item (T2) | normal | emphasis+SFX, ring ≥3:1 | pressed | co-op = "Coming soon" (VS lock) | "menu load error — retry" |
| Highlight (T3) | first item default focus | tracks | — | skips locked items | — |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| move | hover | ↑/↓ | D-Pad/stick | "Single Play, 1/6" |
| run | click | Enter | A/○ | "Single Play activate" |
| quit | click | — | — | "Quit, confirm required" |

#### Data binding
| code | field (GDD §) | event (GDD §12-1) | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| T2 | menu/modes (static), co-op lock (§3 VS) | — | `MenuFocusChanged` | items | default menu |
| T5 | build meta (static) | — | — | vX.Y | empty |

#### Navigation
single→O2 / options→O4 / codex·unlock→O5 / leaderboard→O6 / co-op→(VS lock) / quit→confirm modal. Default focus **Single Play**.

#### Edge cases
Quit = irreversible → confirm modal. No save (first launch): meta/codex empty but enterable. Co-op locked: "Coming soon", not startable.

#### Accessibility
Focus = color+border+sound; locked = lock+text. Subtitles/text scale. License line readable contrast (§13-3 #1).

#### UX rationale
- **See at a glance**: logo→vertical menu in one line; only 6 items so a first-timer finds "Single Play" instantly.
- **Operate / avoid mistakes**: default focus on single; quit confirms; co-op grayed "Coming soon" prevents dead clicks.
- **Feel**: key art on the right carries the "cute nightmare" tone from the first screen.
- **First vs repeat**: novice goes single; veteran jumps to meta/leaderboard.
- **Accessibility**: lock/select not by color alone; license line legible.
- **Watch (top 3)**: ① official/license confusion (§13-3 #1) → reserved license line (legal review separate); ② menu overload → few items + default focus; ③ co-op dead click → lock label.

#### Open questions
Hide co-op in VS vs gray it (currently gray). Title motion/sound toggle location.

#### Acceptance
- [ ] First launch focuses Single Play by default.
- [ ] Co-op is shown locked and never starts.
- [ ] Pad-only can move & run the menu.
- [ ] License line is present.

---

### 5.O2 CHARSEL — Character Select · state: menu

#### Purpose
Show how each character "wakes from the dream" differs (§5) and let the player choose. VS: Kohaku/Toko active, 4 locked. Put the evade feel up front.

| field | value |
| --- | --- |
| Enter | Main→single / Result→Retry |
| Exit | confirm→O3 / back→Main |
| Input context | non-combat, focus |
| Priority | core |

#### References
*Source: ui-ref harvest — interfaceingame (character).*

![Honkai: Star Rail / Destiny 2 character screens](references/ui/web-refs/character-select/destiny-2-character-500x281.jpg)
**What.** Portrait grid/list with rarity & lock state, a focused 3D character, a right info card (name/desc/stats). **Why.** Grid+lock/rarity shows ownership & playstyle at a glance; left/center/right makes "browse + compare" natural. → applied: list(2)·lock(3)·3D preview(4)·name/archetype(5)·core stats(6)·weapon/passive/ult(7).

![Slay the Spire choose your character](references/ui/web-refs/character-select/slay-the-spire-choose-your-character-500x281.jpg)
**What.** Few characters as large cards with a one-line playstyle. **Why.** With a small roster, a big preview + summary aids choice. → applied: VS 2-character big preview.

> Words: the key difference here is **evade feel**, so dash distance/cooldown/safe-time/lucid-window go to the front of the stats (§4-3).

#### Wireframe
![CHARSEL wireframe](wireframes/character-select.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | E1 | Screen title | top-left | always | "Character Select" | static | shown on enter | where am I | text |
| 2 | E2 | Character list | left | always | 6; Kohaku/Toko active, 4 locked (§3,§5) | `Character.id`(§12-2), roster(§5) | focus syncs right ≤instant | choices in one column | icon+name |
| 3 | E3 | Select/lock mark | list item | always | select=border, lock=lock+gray+condition | unlock (§2-3 meta) | locked not startable | can I pick it | color+border+lock |
| 4 | E4 | 3D preview | center | always | model rotate/idle | `Character.id`(§12-2) | swaps ≤200ms on focus | see the look | alt text (name·playstyle) |
| 5 | E5 | Name·archetype | top-right | always | name+archetype+recommended (§5) | `Character`(§5) | syncs on focus | identity one line | text |
| 6 | E6 | Core stats | mid-right | always | HP·move·dash(dist/cd/safe)·lucid window | `Character.hp`·`move_speed`·`dash_*`·`lucid_window`(§12-2) | exact per-char values (§4-3,§5) | the evade difference | bars/radar + numbers |
| 7 | E7 | Weapon·passive·ult | low-right | always | base weapon·passive·ult mod | `CombatWeapon`·`passive`·`ultimate_modifier`(§12-2) | exact per-char (§4-4,§4-6,§5) | how it fights | icon+text |
| 8 | E8 | Start button | bottom | active pick | confirm → O3 | routing | disabled if locked char | next step | button+prompt |

#### Kohaku vs Toko (E6·E7 data, GDD §4-3/§5)
| item | Kohaku (standard) | Toko (agile) |
| --- | --- | --- |
| HP / move | 110 / 6.0 | 90 / 6.8 |
| dash dist/cd/safe | 4.8m / 1.25s / 0.28s | 4.1m / 0.85s / 0.20s |
| lucid window | 0.10s | 0.08s |
| base weapon | Star Pulse (single) | Phantom Needle (3-burst) |
| passive | Steady Waking (+10% evade reward) | Fleeting Mischief (+20% combo purify) |
| ult mod | Cannon +10% width | dash cd -35% after cannon |
| recommended | first players, stable | skilled / speedrun |

#### State matrix (E2/E3, E8)
| element | default | hover/focus | selected | disabled/locked | loading | error |
| --- | --- | --- | --- | --- | --- |
| List item (E2/E3) | normal | emphasis+right sync | border+check | locked=lock+gray+"unlock cond" (§2-3) | enter fade | "char load error" |
| Start (E8) | active | emphasis+ring | — | disabled+"locked character" if locked pick | — | "transition fail — retry" |
| 3D preview (E4) | idle | — | — | — | "loading…" (≠ no-data) | model fail = portrait fallback |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| focus char | hover | ↑/↓ | D-Pad/stick | "Kohaku, standard, unlocked" |
| confirm | click | Enter | A/○ | "Kohaku selected, start" |
| back | click | Esc | B | "Main menu" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| E2/E3 | `Character.id`(§12-2), roster(§5), unlock(§2-3) | — | `CharacterFocused`, `RosterLoaded` | list | default 2 |
| E4 | `Character.id`(§12-2) | — | `PreviewLoaded` | 3D | portrait |
| E6 | `Character.hp`·`move_speed`·`dash_*`·`lucid_window`(§12-2) | — | — | numbers/radar | "—" |
| E7 | `CombatWeapon`·`passive`·`ultimate_modifier`(§12-2) | — | — | summary | "—" |

#### Navigation
confirm(E8) → O3 → run(I1). back → Main. Result(I6) "Retry" enters here.

#### Edge cases
Locked char: focusable but E8 disabled + unlock condition. Default focus Kohaku (first-player rec, §5). Preview fail → portrait. Co-op (out of scope): per-player select / duplicates allowed (§8) unbuilt in VS.

#### Accessibility
Lock/select via color+border+lock; stats show numbers alongside any radar; focus announces "name·playstyle·unlock"; 3D alt text.

#### UX rationale
- **See at a glance**: pick on the left → center look + right performance update instantly. The core difference is evade feel, so dash/lucid-window lead the stats → Kohaku (stable) vs Toko (fast/risky) reads immediately.
- **Operate / avoid mistakes**: locked = lock+condition+disabled start; default focus on the recommended starter.
- **Feel**: 3D preview + one-line weapon/passive/ult lets you imagine the playstyle.
- **First vs repeat**: rec guides novices to stable; veterans pick Toko for speedrun builds.
- **Accessibility**: not color-only; numbers beside radar.
- **Watch**: ① choosing blind → evade stats up front + one-line summary; ② lock confusion (colorblind) → lock+text; ③ radar imprecise → numbers; ④ license/official confusion (§13-3 #1) → name-display guideline (legal separate).

#### Open questions
Unlock-condition text exposure. Stats radar vs bars (bars are precise for the 4 evade stats).

#### Acceptance
- [ ] Kohaku/Toko active, 4 locked, distinguishable.
- [ ] Preview & stats sync ≤200ms on focus.
- [ ] Dash dist/cd/safe/lucid-window shown per GDD values.
- [ ] Colorblind mode distinguishes lock/select.
- [ ] Locked char disables Start.

---

### 5.O3 STAGESEL — Stage / Difficulty Select · state: menu

#### Purpose
Pick the stage (VS: LD-001 Sleeping Room) and difficulty (Sleepy–Lucid), and show what each choice changes (foes/boss/reward/purify requirement).

| field | value |
| --- | --- |
| Enter | after O2 confirm |
| Exit | start→run(I1) / back→O2 |
| Input context | non-combat, focus |
| Priority | core |

#### References
*Source: ui-ref harvest — interfaceingame (map/level).*

![Hades map (node path)](references/ui/web-refs/stage-map/hades-map-500x281.jpg)
**What.** Progress nodes/paths + a reward preview per node. **Why.** Show what's coming (foes/reward) before choosing. → applied: stage list(2)·info(4).

![Hollow Knight map](references/ui/web-refs/stage-map/hollow-knight-map-500x281.jpg)
**What.** Current vs locked regions on a map. **Why.** Convey unlock state spatially. → applied: lock/select mark(3).

> Words: difficulty(5) changes not just HP but purify requirement · threat · reward multipliers (§2-4) → info panel updates with difficulty.

#### Wireframe
![STAGESEL wireframe](wireframes/stage-select.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | G1 | Screen title | top-left | always | "Stage Select" | static | instant | where | text |
| 2 | G2 | Stage list | left | always | LD-001 active + 4 locked (§6-1) | stage def(§6-1), unlock | focus syncs right | where I fight | thumb+name |
| 3 | G3 | Lock/select mark | item | always | select=border, lock=lock+condition | unlock cond(§6-1) | locked not startable | can I go | color+lock+text |
| 4 | G4 | Stage info | top-right | always | theme·foes·boss·reward (§6-2) | stage(§6-2), diff mult(§2-4) | updates on focus/difficulty | what shows up | text+icon |
| 5 | G5 | Difficulty | mid-right | always | Sleepy/Normal/Nightmare/Lucid + multipliers | diff mult(§2-4) | changing G5 updates G4 | choose challenge | segmented+numbers+color |
| 6 | G6 | Mode summary | right | always | Core Dream Run·20min·goal(survive/Dream Break) | mode(§2-4) | — | what I do | text |
| 7 | G7 | Start button | bottom | active pick | confirm → run | routing | disabled if locked | start | button+prompt |

#### Difficulty data (§2-4)
| difficulty | purify req | enemy HP | enemy threat | reward |
| --- | ---: | ---: | ---: | ---: |
| Sleepy | 0.85x | 0.85x | 0.80x | 0.90x |
| Normal | 1.00x | 1.00x | 1.00x | 1.00x |
| Nightmare | 1.18x | 1.20x | 1.25x | 1.15x |
| Lucid | 1.35x | 1.35x | 1.45x | 1.30x |

#### State matrix (G3, G5, G7)
| element | default | hover/focus | selected | disabled/locked | error |
| --- | --- | --- | --- | --- | --- |
| Stage (G3) | normal | emphasis+sync | border | locked=lock+"unlock cond"(§6-1) | "stage load error" |
| Difficulty (G5) | Normal default | emphasis | selected+multipliers | Lucid etc. may be meta-locked | — |
| Start (G7) | active | emphasis+ring | — | disabled if locked stage | "transition fail" |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| focus stage | hover | arrows | D-Pad | "Sleeping Room, unlocked" |
| change difficulty | click | ←/→ | LB/RB | "Normal, reward 1.0x" |
| start | click | Enter | A/○ | "Sleeping Room, Normal start" |
| back | click | Esc | B | "Character select" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| G2/G3 | stage(§6-1), unlock | — | `StageFocused`, `StagesLoaded` | list | LD-001 |
| G4 | stage(§6-2), diff mult(§2-4) | — | `StageInfoUpdated` | text/icon | default |
| G5 | diff mult(§2-4) | — | `DifficultyChanged` | multipliers | Normal |

#### Navigation
start(G7) → run(I1, RunStart). back → O2. Non-LD-001 stages active only when §6-1 unlock met.

#### Edge cases
VS plays LD-001 only; others locked preview. Lucid difficulty may be meta-locked (lock+condition). Changing difficulty must update info numbers immediately (avoid false expectation).

#### Accessibility
Difficulty difference via multiplier numbers + bars, not color only; locked = lock+condition; info text scalable.

#### UX rationale
- **See at a glance**: pick stage left → theme/foes/boss/reward right; changing difficulty updates those numbers so "what gets harder" is visible.
- **Operate / avoid mistakes**: locked stage/difficulty = lock+condition + disabled start.
- **Feel**: locked stages still preview as a "next goal".
- **First vs repeat**: Normal·LD-001 default for novices; veterans push Nightmare/Lucid for reward.
- **Accessibility**: difficulty conveyed as numbers too.
- **Watch**: ① not knowing what difficulty changes → multipliers in info (§2-4); ② lock confusion → lock+condition; ③ late-game tedium (§13-3 #3) → mode summary states the Dream Break goal for motivation.

#### Open questions
Difficulty lock condition (meta). Stage list map vs cards (VS = 1 stage → cards fine).

#### Acceptance
- [ ] LD-001 active, others locked preview.
- [ ] Difficulty change updates info multipliers immediately.
- [ ] Colorblind mode distinguishes difficulty/lock.
- [ ] Pad-only stage/difficulty select & start.

---

### 5.O4 SETTINGS — Options / Settings · state: menu (or from Pause)

#### Purpose
Group gameplay/display/audio/UI-accessibility/controls options (incl. GDD §9-3 accessibility) and explain what each changes. **Accessibility is a first-class citizen.**

| field | value |
| --- | --- |
| Enter | Main(O1) / Pause(I5) |
| Exit | back → caller |
| Input context | non-combat, focus |
| Priority | core (accessibility) |

#### References
*Source: ui-ref harvest — interfaceingame (settings).*

![Risk of Rain 2 audio settings](references/ui/web-refs/settings/risk-of-rain-2-audio-500x281.jpg)
**What.** Top tabs (Gameplay/Keyboard/Controller/Audio/Video/Graphics), left sliders/toggles, right description, bottom Back/Revert. **Why.** Tabs + left control + right description is the low-learning standard. → applied: tabs(1)·options(2·3)·description(4)·bottom(6).

![Hades display settings](references/ui/web-refs/settings/hades-display-500x281.jpg)
**What.** Per-item current value + left/right adjust. **Why.** Slider/stepper makes value changes clear. → applied: option control(3).

> Words: highlight a dedicated **accessibility group(5)** — colorblind palette · screenshake · flash · post-processing · hit-judgment display · cut-in simplify · auto-aim bias · lucid-evade assist · subtitles (§9-3).

#### Wireframe
![SETTINGS wireframe](wireframes/settings.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S1 | Tab row | top | always | Gameplay·Display·Audio·UI/Access·Controls | categories (static) | tab swaps options instantly | group to find | tab label + selected |
| 2 | S2 | Option list | left | always | per-tab sliders/toggles/steppers | settings (saved) | change reflects/previews | all in one place | label+value text |
| 3 | S3 | Option control | row | always | slider/toggle; current value | settings (saved) | adjust ≤100ms reflect | clear value change | value text+steps |
| 4 | S4 | Description panel | right | focus option | effect of the focused option | option meta (static) | desc updates on focus | what it changes | text |
| 5 | S5 | Accessibility group | left (section) | UI/Access tab | colorblind·shake·flash·cut-in·subs·aim·assist (§9-3) | a11y settings (saved) | toggle applies at once | a11y front and center | toggle+state text |
| 6 | S6 | Apply·revert·back | bottom | always | apply/cancel/exit | — | apply confirms save | safe changes | button+prompt |

#### State matrix (S3)
| element | default | hover/focus | active | disabled | error |
| --- | --- | --- | --- | --- | --- |
| Option control (S3) | current value | emphasis+description | dragging/toggling | dependent disabled+reason ("fullscreen only") | "settings save failed — retry" |
| Tab (S1) | first tab | emphasis | pressed | — | — |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| switch tab | click | Q/E·Tab | LB/RB | "Audio tab" |
| focus option | hover | ↑/↓ | D-Pad | "Music volume, 80%" |
| adjust value | drag/click | ←/→ | stick/D-Pad | "Music volume 75%" |
| apply/back | click | Enter/Esc | A/B | "Applied" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| S2/S3 | settings (saved; §9-3 a11y items) | — | `SettingChanged`, `SettingsLoaded` | value | default |
| S5 | a11y settings (§9-3) | — | `AccessibilityChanged` | toggle/value | default off/standard |
| S6 | — | — | `SettingsApplied`, `SettingsReverted` | — | — |

#### Navigation
back → caller (Main or Pause). From Pause, combat stays paused.

#### Edge cases
Dependent options (fullscreen↔resolution) disabled+reason. Unapplied change on back: "unsaved changes — apply/cancel". Remap conflict: same-key warning + resolution.

#### Accessibility
This screen is the gateway to all of it: colorblind palette, shake/flash/post-processing/cut-in toggles, hit-judgment display, auto-aim bias, lucid-evade assist, subtitles (size/bg/speed) — all §9-3. Toggle state = color + text (ON/OFF).

#### UX rationale
- **See at a glance**: tabs group options; the focused option's description on the right answers "what does this do?".
- **Operate / avoid mistakes**: apply/revert make changes safe; dependent options disable with a reason; remap conflicts warn.
- **Feel**: clarity over flourish; volume/shake preview immediately.
- **First vs repeat**: accessibility/controls up front for those who need them; veterans go to graphics/gameplay.
- **Accessibility**: this screen exposes all of §9-3; toggle = color+text.
- **Watch**: ① excluding colorblind/sensitive users (§13-3 #5) → colorblind/shake/flash/cut-in toggles first-class; ② lost changes → unsaved-change confirm; ③ key conflict → warn+resolve.

#### Open questions
Accessibility presets (colorblind/low-stim bundle). Which options apply live in-game (shake etc.).

#### Acceptance
- [ ] All §9-3 accessibility items exposed; toggles shown by color+text.
- [ ] Focusing an option updates the description.
- [ ] Back with unsaved changes shows a confirm modal.
- [ ] Pad-only tab/value/apply works.

---

### 5.O5 META — Meta Progress (permanent unlocks / codex) · state: menu

#### Purpose
Between runs, spend currency (dream shards/stardust/lucid core, §2-3) to **unlock by play only** (characters/skill trees/ult/relics/difficulty) and view a codex. **GDD §10 BM: no paid power, no gacha → no purchase UI.**

| field | value |
| --- | --- |
| Enter | Main(O1) "Codex/Unlock" |
| Exit | back → Main |
| Input context | non-combat, focus |
| Priority | core (repeat motivation) |

#### References
*Source: ui-ref harvest — interfaceingame (skill tree / collection).*

![Hades Mirror of Night (permanent upgrades)](references/ui/web-refs/skill-tree/hades-mirror-of-night-500x281.jpg)
**What.** Upgrade rows (name+effect+level pips+MAX), currency top-right, selected item desc bottom-right. **Why.** Rows+currency+desc make "what costs what" clear. → applied: unlock list(3)·item(4)·currency(2)·desc(5)·unlock button(6).

![Slay the Spire collection (codex)](references/ui/web-refs/inventory/slay-the-spire-collection-500x281.jpg)
**What.** Collected items/cards grid. **Why.** Codex collection progress. → applied: codex tab (C-LIST).

> Words: **no cash purchase button/price** — every unlock spends play-earned currency only (§10). This is the deliberate difference from a typical shop screen.

#### Wireframe
![META wireframe](wireframes/meta-progress.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | K1 | Title·tabs | top-left | always | Permanent upgrades / Codex / Records | categories (static) | tab swaps instantly | grouping | tab label |
| 2 | K2 | Currency | top-right | always | dream shards·stardust·lucid core (§2-3) | meta currency (§2-3) | reflects on change | what I can spend | icon+number |
| 3 | K3 | Unlock list | center | upgrade tab | rows: name·effect·state(owned/locked) | unlock items(§2-3), `Item`/`SkillNode`(§12-2) | focus syncs desc | what can I open | row label+state |
| 4 | K4 | Item state | row | always | locked / available / owned | cost·prereq(§2-3) | "available" when currency met | can I open now | lock/check+color |
| 5 | K5 | Item desc·cond | right | on focus | effect·cost·unlock condition | item meta | updates on focus | confirm before unlock | text |
| 6 | K6 | Unlock button | low-right | available | spend currency to unlock (no cash) | cost(§2-3) | click deducts+confirm | confirm unlock | button+prompt |
| 7 | K7 | Back·input | bottom-left | always | exit | — | — | leave | button |

#### State matrix (K4, K6)
| element | default | hover/focus | selected | disabled/locked | error |
| --- | --- | --- | --- | --- | --- |
| Item (K4) | owned=check / not=outline | emphasis+desc | just-unlocked mark | prereq unmet=lock+condition / low currency="N short" | "load error — retry" |
| Unlock (K6) | active when available | emphasis+ring | — | disabled+reason if short/unmet | "unlock failed — retry" |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| switch tab | click | Q/E | LB/RB | "Codex tab" |
| focus item | hover | arrows | D-Pad/stick | "Lucid Sense, cost 50 shards, lock: clear boss once" |
| unlock | click | Enter | A/○ | "unlocked, 50 shards spent" |
| back | click | Esc | B | "Main" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| K2 | meta currency(§2-3) | — | `CurrencyChanged` | number | 0 |
| K3/K4 | unlock items(§2-3), `SkillNode`/`Item`(§12-2) | — | `UnlockablesLoaded`, `UnlockStateChanged` | list | locked |
| K5 | item meta·cost(§2-3) | — | `UnlockableFocused` | text | "select" |
| K6 | cost(§2-3) | — | `UnlockPurchased` (currency) | — | — |

> No cash-payment event is defined (§10 BM).

#### Navigation
back → Main(O1). Unlocked characters/difficulty become active in O2/O3 at once. Codex tab shows enemy/boss/item collection (§6-3, §4-5, §10).

#### Edge cases
Currency short: button disabled+amount. Prereq unmet: lock+condition ("clear boss once"). Unlock confirm (currency spend is irreversible). Empty codex entry: "undiscovered" (minimize spoilers).

#### Accessibility
Unlock state (locked/available/owned) via color+lock/check; currency/cost numbers explicit; description scalable; no time pressure.

#### UX rationale
- **See at a glance**: center unlock list, right shows the focused item's effect/cost/condition; currency top-right tells "what I can open for how much".
- **Operate / avoid mistakes**: short currency or unmet prereq disables with a reason; unlock confirms.
- **Feel**: unlocking fills items and the codex grows — long-term repeat motivation.
- **First vs repeat**: highlight 1–2 next unlocks for novices; veterans optimize the tree.
- **Accessibility**: state not color-only.
- **Watch**: ① **monetization confusion (§10 BM)** → never any cash UI, currency unlocks only; ② late-game tedium (§13-3 #3) → codex/unlock as long-term goals; ③ colorblind lock confusion → lock+condition.

#### Open questions
Codex spoiler policy (silhouette vs hidden). Visual distinction between permanent tree and in-run tree (I4).

#### Acceptance
- [ ] No cash-purchase UI; all unlocks spend currency.
- [ ] Short/unmet items show disabled+reason.
- [ ] Unlock deducts currency and reflects in O2/O3.
- [ ] Colorblind mode distinguishes locked/owned.

---

### 5.O6 LEADER — Leaderboard / Records · state: menu

#### Purpose
Show GDD §10 records (Dream Break Time, boss splits, hidden-boss unlock time, no-damage, highest purify, co-op, character clears) split by stage/difficulty/character/solo·co-op/condition, and highlight **my rank** to drive competition.

| field | value |
| --- | --- |
| Enter | Main(O1) "Leaderboard" |
| Exit | back → Main |
| Input context | non-combat, focus, network-dependent |
| Priority | extended (competition) |

#### References
*Source: no direct leaderboard capture on the harvest games; rank-table composition derived from a result stats panel.*

![Risk of Rain 2 result (stats table composition)](references/ui/web-refs/results/risk-of-rain-2-defeat-500x281.jpg)
**What.** A left stats panel listing per-item numbers line-aligned. **Why.** Line-aligned tables compare many numbers fastest. → applied: rank table(4)·my-rank highlight(5) row structure.

> Words: a real leaderboard capture can be added later from Game UI Database `Leaderboards & Ranking` (scrn=55) — see Appendix B (note the GUIDB headless limit). Filter(2)·record type(3)·my-rank(5) are derived from common leaderboard patterns in words.

#### Wireframe
![LEADER wireframe](wireframes/leaderboard.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | L1 | Screen title | top-left | always | "Leaderboard" | static | instant | where | text |
| 2 | L2 | Filter tabs | top | always | stage·difficulty·character·solo/co-op·condition (§10) | filters (§10 axes) | change refreshes table | compare like-for-like | tab label+selected |
| 3 | L3 | Record type | left | always | DB time·boss split·hidden unlock·no-damage·highest purify (§10) | record types (§10) | select refreshes table | what we compete | label+selected |
| 4 | L4 | Rank table | center | always | rank·player·record·character | record data (§10) | sorted after load | rank compare | table header+values |
| 5 | L5 | My-rank highlight | table row | my record exists | highlight + jump-to | my record (§10) | scrolls to my row on enter | my position | color+border+"YOU" |
| 6 | L6 | Back·input | bottom | always | exit | — | — | leave | button |

#### State matrix (L4, L5)
| element | default | hover/focus | disabled | loading | empty | error |
| --- | --- | --- | --- | --- | --- | --- |
| Table (L4) | sorted | row emphasis | offline = local-only + "Offline" | "loading ranks…" (network) | "no records — be the first" | "load failed — retry" |
| My rank (L5) | highlight | — | no record = hidden + "no record" | — | — | — |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| filter/type | click | Q/E·arrows | LB/RB·D-Pad | "Difficulty: Normal, record: Dream Break Time" |
| scroll | wheel/drag | ↑/↓ | stick | "1st 9:12 Toko" |
| to my rank | button | Home | Y | "jump to my rank 14th" |
| back | click | Esc | B | "Main" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| L2/L3 | axes·record types(§10) | — | `LeaderboardFilterChanged` | tabs | default |
| L4 | records(§10), `dream_break_stage_times`(§12-2) | — | `LeaderboardLoaded` | table | empty/error |
| L5 | my record(§10) | `DreamBreakAchieved`(§12-1) | `MyRankResolved` | row | hidden |

#### Navigation
back → Main(O1). Result(I6) "Leaderboard" enters here with the matching record filter.

#### Edge cases
Offline: local-only + "Offline" badge, resync on reconnect. No records: "be the first". Loading: skeleton + "loading…" (≠ enter anim). Cheat-report/filters later.

#### Accessibility
My rank via color + "YOU" label + border; sticky table header; network state in words; scalable text.

#### UX rationale
- **See at a glance**: filter first (so comparisons are like-for-like), then record type, then table; on enter it scrolls to my rank.
- **Operate / avoid mistakes**: offline/loading/empty stated in words so "why is it blank?" never happens.
- **Feel**: my-rank highlight + new-record markers drive the next attempt.
- **First vs repeat**: "be the first" lowers novice pressure; veterans chase Dream Break Time/no-damage.
- **Accessibility**: my row marked beyond color.
- **Watch**: ① blank-on-network-fail confusion → offline/error/loading distinct copy; ② unfair mixed comparison → force filter first; ③ colorblind my-rank id → "YOU" label.

#### Open questions
Co-op record exposure (VS = solo). Cheat-report/verification policy. Season/weekly reset.

#### Acceptance
- [ ] Filter/record change refreshes the table immediately.
- [ ] On enter, scrolls to and highlights my rank.
- [ ] Offline/loading/empty shown with distinct copy.
- [ ] Colorblind mode identifies my rank by label.

---

### 5.I1 HUD-IN — In-game HUD (combat) · state: `NormalRun`

#### Purpose
Let the player read **time left · survival · resources · progress** without moving their eyes, and judge move/dodge/skill/ult. Priority #1: the HUD never hides bullets/telegraphs even in chaos.

| field | value |
| --- | --- |
| Enter | `RunStart` +1s → `NormalRun` (§4-1) |
| Exit | level-up(I3)/reward(I4)/pause(I5) overlay / ending → I6 |
| Input context | real-time combat |
| Priority | all core (lucid combo extended) — §9-2 |

#### References
*Source: ui-ref harvest — interfaceingame (HUD).*

![Hades combat HUD](references/ui/web-refs/hud/hades-fight-500x281.jpg)
**What.** Minimal chrome, top-left HP/resource, bottom-right ability. **Why.** Push HUD to the edges and keep center clear for combat legibility. → applied: clear center, minimal chrome; vitals top-left (2·3·4·5), skills/ult bottom (8·9).

![Hades in-game](references/ui/web-refs/hud/hades-in-game-500x281.jpg)
**What.** Resource/cooldown shown as radials/gauges. **Why.** Read resource/cooldown without text. → applied: skill radial(8)·ult gauge(9).

> Words: timers usually sit **top-center/top-right**, but here it's an **alarm clock (diegetic) fixed top-left** (deliberate exception — see UX rationale). XP = a thin full-width strip at the very top.

#### Wireframe
![HUD-IN wireframe](wireframes/hud.svg)

```text
┌──────────────────── 16:9 ────────────────────┐
│ (1)──── XP strip ─────────────────────────────│
│ (2)Alarm  (3)Seal  (4)HP/Shield (5)DreamEnergy│
│                   · Player ·                   │
│ (6)Lucid combo                                 │
│      (7)Purify bar     (8)Skills Q·E  (9)Ult R │
└────────────────────────────────────────────────┘
```

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A1 | XP bar | top full-width | always | fill 0→100%; flash+reset on level-up | XP (§4-5), `RunTelemetry.level_reached`(§12-2); event UI-proposed | reflects ≤200ms | progress to next growth | fill+number, not color-only |
| 2 | A2 | Alarm clock | top-left | always | hand sweep; 1140–1200s edge brighten + hand emphasis (§4-1) | `run.timer` 0–1200s(§4-1), `AlarmReached`(§12-1) | time-left read ≤1s anytime (§3-2) | top rule visibility | clock+digits, final-60s sound+brightness |
| 3 | A3 | Seal gauge | below clock | always | 4 seals; lights on boss kill | seal slot(§4-2), `BossDefeated`(§12-1) | lights ≤300ms on break | progress to early clear | pips+lock/unlock icon |
| 4 | A4 | HP/Shield | top-left | always | drop+red blink on hit; shield distinct color; low-HP border | `Character.hp`(§12-2), shield (§12-2 add) | hit reflects ≤100ms; low-HP (≤25% [TBD]) color+blink+border | near-death by shape too | color+blink+border+number |
| 5 | A5 | Dream Energy | near HP | always | charges via evade/kill; full = ult ready signal | dream energy(§4-3·§4-6; field §12-2 add), `EvasionLucid`/`EvasionNearMiss`(§4-3) | full → signal with A9 at once | foreshadow ult timing | fill+number+icon |
| 6 | A6 | Lucid combo | low-left | 6s after evade | combo 1→3 + multiplier; fades if no streak in 6s | `LucidComboStep`(§4-3), max 3(§4-3) | updates ≤0.2s; holds 6.0s (§4-3) | reward the dodge rhythm | step+color+sound |
| 7 | A7 | Purify bar | bottom-center | always | fills to slot threshold; boss warning at threshold | purify(§4-2 thr 260/620/1080/1640), `PurgeGained`·`BossThresholdReached`(§12-1) | gain ≤200ms; threshold→warning at once | distance to next boss | fill+number+source toast |
| 8 | A8 | Skills Q·E | bottom | always | cooldown radial; ready flash; pressed+SFX | skill cd(§2-5; field §12-2 add) | ready flash ≤200ms after cd | usable? how long? | radial+keycap+sound |
| 9 | A9 | Ult gauge R | low-right | always | lit at dream energy 100; cinematic on use | dream/100(§4-6), R(§2-5) | lit at 100 at once; input ≤100ms | finisher resource apart | fill+number+lit |

#### State matrix (key dynamic elements)
| element | default | pressed/active | disabled/locked | loading | empty | error |
| --- | --- | --- | --- | --- | --- | --- |
| Skill (A8) | radial fill | pressed+SFX, radial 0 | gray+lock+"unlocked later" (pre-tree) | enter fade | N/A | "cd error — default" |
| Ult (A9) | charging fill | cinematic on fire | dim+remaining if <100 | enter fade | N/A | resource missing = last value+border |
| HP/Shield (A4) | current | red blink on hit | N/A | enter fill | HP0 = FailedWake transition | missing = last value+border |
| Lucid combo (A6) | hidden | appears+increments on evade | N/A | appear anim | fades after 6s | N/A |
| Alarm (A2) | normal | 60s warning: brightness+hand | N/A | enter set | N/A | missing = "syncing…" + last |

#### Input parity
| action | key | pad | screen reader |
| --- | --- | --- | --- |
| move | WASD | left stick | "move" |
| dash/dodge | Space | A/○ | "dodge, cd n s" |
| skill 1·2 | Q·E | LB·RB | "skill1 ready/cd" |
| ultimate | R | Y/△ | "ult ready/charge n%" |
| camera/ping | hotkey | right stick/D-Pad | "ping" |

#### Data binding (event-driven)
| code | field (GDD §) | event (GDD §12-1/§4-3) | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| A1 | XP(§4-5); `level_reached`(§12-2) | — | `XpChanged`, `LevelReached` | 0–100%+Lv | 0% |
| A2 | `run.timer` 0–1200s(§4-1) | `AlarmReached`(§12-1) | `RunTimerTick` | mm:ss left | 0:00 |
| A3 | seal(§4-2); `Boss.seal_slot`(§12-2) | `BossDefeated`·`BossThresholdReached`(§12-1) | `SealStateChanged` | 4 pips | 0 |
| A4 | `Character.hp`(§12-2); shield (§12-2 add) | — | `HpChanged`, `ShieldChanged` | n/max | last |
| A5 | dream energy(§4-3·§4-6; field §12-2 add) | `EvasionLucid`·`EvasionNearMiss`(§4-3) | `DreamEnergyChanged` | n/100 | 0 |
| A6 | combo step(§4-3; field §12-2 add) | `LucidComboStep`(§4-3) | — | x1–x3 | hidden |
| A7 | purify(§4-2; field §12-2 add) | `PurgeGained`·`BossThresholdReached`(§12-1) | `PurgeGaugeChanged` | n/thr | 0 |
| A8 | skill cd(§2-5; field §12-2 add) | — | `SkillCooldownChanged`, `SkillReady` | s left | ready |
| A9 | dream/100(§4-6) | — | `UltimateChargeChanged`, `UltimateReady` | n/100 | 0 |

> **UI events/fields — GDD additions needed:** runtime state `RunState{timer, purge_current, seal_slot_index}`, `PlayerRuntime{hp_current, shield_current, dream_energy, ultimate_charge, lucid_combo_step}`, `SkillSlot{cooldown_remaining}` are not in §12-2. **XP bar isn't in §9-2 either** → UI-proposed. We do not claim these are bound to §12-1 events.

#### Navigation
No routing (display only). State transitions only: `NormalRun`→I3/I5/I2/I6.

#### Edge cases
Concurrent ends (§4-1): 7:00 + boss kill → `DawnWake` priority (no boss reward); level-up open at 7:00 → close window then `DawnWake`. Ult cinematic at 7:00 → cut/fade then `DawnWake`. Data flood: toasts merge/throttle. Missing value: last value + border.

#### Accessibility
Colorblind palette distinguishes enemy bullets / ally bullets / hazard zones by shape+color (§9-3). Shake/post-processing strength, hit-judgment display (§9-3). Low-HP/threshold = color+blink+sound (triple).

#### UX rationale
- **See at a glance**: first read ① time to 7:00 (top-left alarm), ② HP (top-left), ③ purify to next boss (bottom). Action resources sit bottom/low-right where the hand is. Center is empty so bullets/telegraphs/character stay visible.
- **Operate / avoid mistakes**: skills/ult show "usable now?" as radial fill + key glyph — no memorization. Low resource = dim + remaining.
- **Feel**: lucid evade pops the combo instantly; full dream energy signals on both the resource bar and the ult slot. Juice is capped so it never buries info.
- **First vs repeat**: unfamiliar info (combo/purify) appears on first occurrence (combo hidden otherwise); veterans read fixed positions fast.
- **Accessibility**: hazard/low-HP/threshold never color-only.
- **Watch**: ① danger buried in volume (§13-3 #5) → HUD to edges, center clear, hazards by shape too; ② missing time because alarm is top-left → final-60s edge brighten+sound (boss-fight handling in I2); ③ juice hiding info → caps+toggles; ④ purify/seal/dream confusion → distinct color+position+icon, labeled meaning.

#### Open questions
Low-HP threshold % (currently 25%). Promote XP bar to §9-2. Verify purify(A7) vs seal(A3) meaning overlap.

#### Acceptance
- [ ] A random screenshot lets you read time-to-7:00 within 1s.
- [ ] At 180 enemies, player/lethal bullets/zones stay distinct in colorblind mode.
- [ ] Hit reflects HP drop within 100ms via color+blink+border.
- [ ] At dream 100 the resource bar and ult slot signal together.
- [ ] Pad-only performs all combat actions.

---

### 5.I2 HUD-BOSS — In-game HUD (boss / hidden boss) · state: `BossFight` · `HiddenBossAttempt`

#### Purpose
Add **boss HP · phase · shield-crack/groggy · counter window** without losing survival/time info. Key: the **top-center slot is taken over by the boss HP bar**.

| field | value |
| --- | --- |
| Enter | `BossSpawned`/`HiddenBossSpawned`(§12-1) |
| Exit | `BossDefeated`→I4 / `AlarmReached`→DawnWake / `DreamBreakAchieved`→I6 |
| Input context | real-time (boss + weakened waves 45%/hidden 25% — §6-4) |
| Priority | core |

#### References
*Source: ui-ref harvest — interfaceingame; boss-bar takeover from words (no clean boss-bar capture this run).*

![Returnal status / threat display](references/ui/web-refs/hud/returnal-status-500x281.png)
**What.** Enemy/threat status emphasized separately from the player HUD. **Why.** Surface "the chance to break it". → applied: shield-crack/groggy(11)·counter window(12).

> **Deliberate exception (important):** the survivor-like standard is "timer top-center → boss HP takes that slot". Here the timer is an **alarm clock (a world object), fixed top-left**. Instead the **top-center slot is left empty in normal play and owned by the boss HP bar in a fight** (same physical slot shared over time). Safeguards: ① the alarm clock stays top-left during boss fights; ② in a hidden-boss fight, per §4-1 the **time-left is inset into the boss bar**. Boss-bar = top-center, segmented at HP55% phase (§7-1), with the boss NAME (LoL Swarm / GUIDB pattern, §B-2).

#### Wireframe
![HUD-BOSS wireframe](wireframes/hud-boss.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | A10 | Boss HP bar | top-center | boss/hidden | horizontal fill; HP55% phase segment (§7-1); boss name | `Boss.hp`·`phase_rules`(§12-2), `BossSpawned`(§12-1) | hit ≤100ms; phase flips at 55% | threat/remaining always on top | fill+segment line+number |
| 2 | A2 | Alarm clock | top-left | kept in boss fight | as I1 | `run.timer`(§4-1) | time read ≤1s kept | time pressure kept | as I1 |
| 3 | A3 | Seal→Hidden | below clock | always | at 4 seals the gauge becomes the hidden-boss gauge (§4-2) | seal/hidden(§4-2), `HiddenBossSpawned`(§12-1) | converts at 4 seals | stage transition clear | shape change+label |
| 11 | A11 | Shield-crack/Groggy | under boss HP | boss | crack accrues; 100→4s groggy (×1.35 dmg)(§7-1) | `BossPattern.shield_crack_value`·`groggy_interaction`(§12-2), `EvasionBossLucid`(§4-3) | crack ++ on boss-lucid counter; 100→groggy 4.0s | the chance to break it | separate bar+groggy icon+sound |
| 12 | A12 | Counter window | near player | 0.7s after lucid evade | brief lit; invites counter | `LucidCounterWindowOpen`(§12-1), 0.7s(§4-3) | lit at once on evade, 0.7s | counter timing feel | lit+sound+color/shape |
| 13 | A13 | Time inset | inside boss HP | hidden boss only | time-left inset in boss bar | `run.timer`(§4-1), `HiddenBossSpawned`(§12-1) | inset shown at once on hidden | time+HP at once | digits+bar, dual with top-left clock |
| 14 | A14 | Seal-trial banner | mid-bottom | during trial(§7-2) | trial name·time limit·goal; countdown | `DreamBreakTrial.id`·`duration_limit`·`success_condition`(§12-2) | shown at trial start; 1s ticks | trial goal/time clear | text+countdown+color |
| 7 | A7 | Purify bar | bottom-center | boss | only 30% of normal-enemy purify (§4-2 BossActive) | purify(§4-2), `PurgeGained`(§12-1) | 30% ratio in boss | keep progress context | fill+number |

#### State matrix (boss additions)
| element | default | active | groggy/special | locked | loading | error |
| --- | --- | --- | --- | --- | --- | --- |
| Boss HP (A10) | fill+name | hit flash | groggy: contrast+icon+×1.35 mark | hidden when not boss (empty slot) | enter slide | missing = last+border |
| Shield-crack (A11) | 0 | ++ on counter | 100→groggy flip | N/A | — | missing = last |
| Counter window (A12) | hidden | 0.7s lit after evade | — | no judgment during ult i-frames (§4-3) | — | N/A |
| Time inset (A13) | hidden (normal boss) | shown in hidden fight | 60s warning emphasis | — | enter | missing = fall back to top-left clock |

#### Input parity
As I1 (shared combat). Additionally **counter** fires within 0.7s after a lucid evade (§4-4 lucid counter 28). Same pad/key.

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| A10 | `Boss.hp`·`phase_rules`·`pattern_list`(§12-2) | `BossSpawned`(§12-1) | `BossHpChanged`, `BossPhaseChanged` | n/max+phase | last |
| A11 | `BossPattern.shield_crack_value`·`groggy_interaction`(§12-2) | `EvasionBossLucid`(§4-3) | `ShieldCrackChanged`, `GroggyChanged` | n/100 | 0 |
| A12 | 0.7s window(§4-3) | `LucidCounterWindowOpen`(§12-1) | — | on/off | off |
| A13 | `run.timer`(§4-1) | `HiddenBossSpawned`(§12-1) | `RunTimerTick` | mm:ss | top-left clock |
| A14 | `DreamBreakTrial.*`(§12-2) | — | `TrialStarted`, `TrialTick`, `TrialResult` | name+countdown | hidden |

#### Navigation
`BossFight`→(kill)→I4 / (HP0)→FailedWake(I6) / (7:00)→DawnWake(I6). `HiddenBossAttempt`→(kill)→DreamBreak(I6) / (7:00)→DawnWake.

#### Edge cases
Dream Break cutscene started then 7:00: if the kill event is already locked, keep `DreamBreak` (§4-1). No off-screen attacks (§4-3): telegraphs only on-screen. No elites during boss/hidden (§6-4).

#### Accessibility
Boss telegraphs multiplexed by color+shape+lead time (§4-3). Groggy/counter via sound+icon. Cut-in simplify toggle (§9-3). Hidden-boss time dual-shown with the top-left clock.

#### UX rationale
- **See at a glance**: in a fight a big boss bar appears top-center so "who I'm fighting" is clear — that's why the slot was kept empty. Time (top-left) and HP (top-left) stay put.
- **Operate / avoid mistakes**: the path to break the boss (crack→groggy) and the counter moment (0.7s) are shown separately, so "when to be greedy" is unambiguous.
- **Feel**: lucid counter → crack fills → groggy → harder hits: the "risk into reward" core amplified in the boss fight.
- **First vs repeat**: the trial banner spells out goal/time for newcomers; veterans hunt groggy to cut kill time.
- **Accessibility**: telegraphs by color+shape+time; cut-ins toggleable; time dual-shown.
- **Watch**: ① missing time because alarm is top-left → clock kept + hidden-boss time inset (dual); ② boss bar+crack+counter clutter → split top(HP)–below(crack)–near-player(counter); ③ effects hiding telegraphs → cut-in toggle, telegraph on top layer; ④ concurrent-end confusion → §4-1 priority, only a locked Dream Break keeps the cutscene.

#### Open questions
Boss HP segment count (currently 55% only). Counter window (A12) world-space vs HUD.

#### Acceptance
- [ ] On boss spawn the boss HP takes top-center while the top-left clock stays visible.
- [ ] In a hidden-boss fight the boss bar shows the inset time-left simultaneously.
- [ ] A successful boss-lucid counter increments crack; at 100 it flips to groggy.
- [ ] Colorblind mode distinguishes boss bar / crack / counter window by shape.

---

### 5.I3 LVLUP — Level-up / Item pick · state: `NormalRun` (paused) overlay modal

#### Purpose
At level-up, **freeze combat** and pick one of 3 cards to grow the build — read a card in ~1s and decide **while seeing the current build/synergies**.

| field | value |
| --- | --- |
| Enter | `RunTelemetry.level_reached` ++ (§4-5) |
| Exit | card confirm → `NormalRun` / 7:00 → close then `DawnWake`(§4-1) |
| Input context | **paused** |
| Priority | core |

#### References
*Source: ui-ref harvest — interfaceingame (boon/card pick).*

![Slay the Spire choose a card](references/ui/web-refs/levelup-reward/slay-the-spire-choose-a-card-500x281.png)
**What.** Card grid, hover tooltip with effect, "Choose a Card" prompt, currency top. **Why.** Card = icon+name+effect reads in 1s; hover gives detail. → applied: cards(4)·rarity(5)·delta/desc(6)·prompt(7).

![Hades reward room (Well of Charon)](references/ui/web-refs/levelup-reward/hades-well-of-charon-500x281.jpg)
**What.** Reward candidates as cards/icons with short effects. **Why.** Reward clarity. → applied: concise card effects.

> Words: **pause + 3–4 cards** (Vampire Survivors), **choice clarity + rarity color** (Hades), **review current build while choosing** (the 20MTD gap) → current-build panel (3).

#### Wireframe
![LVLUP wireframe](wireframes/levelup.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | B1 | Pause dim | full | modal | combat freeze + dim | combat freeze (level-up) | freeze at once (0 input loss) | remove time pressure/strain | dim + input-block notice |
| 2 | B2 | Level-up header | top-center | modal | "Level n reached" + flourish | `level_reached`(§12-2) | updates on level-up | what happened in one line | text+icon+sound |
| 3 | B3 | Current build | left | modal | owned items (≤6)·level·synergy (read-only) | `Item.*`(§12-2), max 6(§4-5) | always visible before pick | choose by synergy | icon+name+level |
| 4 | B4 | Choice cards ×3 | center | modal | 3 cards; icon+name+effect; focus emphasis; confirm | `RewardScreenRule.item_offer_count`(§12-2); 3 normal(§4-5) | 1 card read ≤1s; pick ≤100ms | pick a direction fast | focus ring ≥3:1, labels |
| 5 | B5 | Rarity·new/upgrade | on card | modal | rarity = color+border+corner; new/upgrade badge | `Item.rarity`(§12-2); odds(§4-5) | rarity by shape/text too | rarity & new-effect at once | color+shape+text |
| 6 | B6 | Stat delta·desc | card bottom | modal | +/- numbers + level effect | `Item.effect`(§12-2); table(§4-5) | sign+value | what improves | sign+number |
| 7 | B7 | Pick prompt | bottom | modal | device glyph + action | input(§2-5) | swaps on device change | no memorization | device glyph |

#### State matrix (card B4)
| element | default | hover/focus | selected | disabled/locked | loading | empty | error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Card (B4) | normal | emphasis+scale, ring ≥3:1 | confirm + gem + short i-frame | Lucid card: lock+"lucid condition" pre-condition (§4-5) | dealing anim (≠ no-data) | "no choices" fallback | "gen error — retry" |
| Build panel (B3) | owned | item tooltip | N/A | owned 0 = "none yet" | enter fade | "no items" | "build load error" |
| Rarity (B5) | rarity color+shape | — | — | maxed item removed from pool (§4-5) | — | — | — |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| focus card | hover | ←/→ | D-Pad/stick | "card 2/3, Moonlit Ribbon" |
| confirm | click | Enter | A/○ | "Moonlit Ribbon, move +8%" |
| review build | hover | Tab | RB | "owned: Blue Pillow Lv.1" |

> No reroll (§4-5) — no reroll control.

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| B2 | `level_reached`(§12-2) | — | `LevelReached` | "Level n" | last |
| B3 | `Item.*`(§12-2), ≤6(§4-5) | — | `InventoryChanged` | icon+Lv | "none" |
| B4 | `RewardScreenRule.item_offer_count`·`rarity_guarantee`(§12-2), `ItemPoolRule.*`(§12-2) | — | `LevelUpOffer` | 3 cards | edge |
| B5 | `Item.rarity`(§12-2), `ItemPoolRule.base_weight`(§12-2) | — | — | rarity+badge | Common |
| B6 | `Item.effect`(§12-2), table(§4-5) | — | — | ±value | "effect TBD" |

> Needs add: `LevelReached`, `InventoryChanged`, `LevelUpOffer`, `ItemPicked` (confirm; `stacking_rule`/`category_limit` per §12-2).

#### Navigation
Modal only. Confirm → `NormalRun`(I1). Multiple level-ups queue.

#### Edge cases
Pick rules (§4-5): first level-up = Common/Uncommon + ≥1 defense guaranteed / normal = ≥1 upgrade + ≥1 new / owned 6 = upgrades only / category-3 limit, maxed removed. Empty pool: 1 fallback reward `[TBD]`. 7:00 mid-pick (§4-1): close then `DawnWake` (no reward if unpicked). Rapid multi level-up: queue.

#### Accessibility
Rarity/new via color+border+corner icon+text (§9-3). Focus ring ≥3:1. Paused = no time pressure. Scalable text.

#### UX rationale
- **See at a glance**: freeze + dim focuses three cards; icon=type, color/border=rarity, short number=effect → reads in 1s.
- **Operate / avoid mistakes**: the left current-build lets you pick by synergy (the gap many survivor-likes miss); input glyphs at the bottom.
- **Feel**: confirm pops a gem + brief i-frames — the "I grew" beat; higher rarity = more flourish.
- **First vs repeat**: first level-up seeds defense so novices don't collapse; veterans build fast within the guarantee rules.
- **Accessibility**: rarity not color-only.
- **Watch**: ① picking without knowing synergy → build panel always on; ② colorblind rarity → color+border+icon+text; ③ 7:00 overlap loss → rule-based close then Dawn Wake; ④ maxed/category misclick → removed from pool / shown as upgrade.

#### Open questions
Empty-pool fallback type. Card-confirm i-frame length.

#### Acceptance
- [ ] Level-up freezes combat at once and shows 3 cards.
- [ ] owned<6 guarantees ≥1 new + ≥1 upgrade; owned=6 upgrades only.
- [ ] First level-up includes ≥1 defense item.
- [ ] Colorblind mode distinguishes rarity by shape/text.
- [ ] Pad-only focus & confirm.

---

### 5.I4 BOSSRWD — Boss reward (skill tree → 4-item pick) · state: `BossReward` (8s protect)

#### Purpose
Right after a boss/seal-trial kill, **grant the skill point**, then run **① skill-tree node pick → ② a separate 4-item pick**. GDD §12-3: SP grant and item-pick UI are **separated**; skill nodes are not mixed into the 4-pick.

| field | value |
| --- | --- |
| Enter | `BossDefeated`(§12-1) → SP +1 (§7-1) |
| Exit | step-2 (4-pick) confirm → `NormalRun`(I1) |
| Input context | **8s protect** (§7-1) |
| Priority | core |

#### References
*Source: ui-ref harvest — interfaceingame (skill tree / reward).*

![Hades Mirror of Night (nodes + description)](references/ui/web-refs/skill-tree/hades-mirror-of-night-500x281.jpg)
**What.** Upgrade rows/nodes, currency top-right, selected-item desc bottom-right. **Why.** Nodes+desc confirm effect/cost/prereq. → applied: node graph(4)·node state(5)·node info(6)·skill point(2).

![Slay the Spire rewards](references/ui/web-refs/levelup-reward/slay-the-spire-rewards-500x281.jpg)
**What.** Reward items as a card/list to pick. **Why.** Reuse the same card grammar for the 4-item pick. → applied: 4-pick (C-CARD, 4 cards, Rare guaranteed).

> Words: separate permanent growth (tree) from run reward (items) **by step** (§12-3); no nodes in the 4-pick.

#### Wireframe (step 1: skill tree)
![BOSSRWD wireframe](wireframes/skilltree.svg)
> Step-2 4-item pick reuses §I3 cards (C-CARD) as **4 cards, Rare guaranteed** (table below).

#### Legend (step 1 skill tree)
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C1 | Char·tree name | top-left | always | the character's dedicated tree | `Character.id`·`SkillNode.character_scope`(§12-2) | shown on enter | whose tree | text+portrait |
| 2 | C2 | Skill point | top-right | always | remaining SP; decrements on use | `RewardScreenRule.skill_point_delta`(§12-2), boss +1(§7-1) | +1 at once on kill | what I can spend | number+icon |
| 3 | C3 | Protect 8s | top | enter 8s | "take your time" + remaining | `RewardScreenRule.timeout_rule`(§12-2), 8s(§7-1) | 8.0s protect | unhurried choice | text+countdown+sound |
| 4 | C4 | Node graph | center | always | nodes + prereq edges; 4 nodes per char (§5) | `SkillNode.id`·`prerequisite`·`offered_after_boss`(§12-2) | pickable after kill (§4-5) | growth path | nodes+edges |
| 5 | C5 | Node state | graph | always | locked/available/owned | `SkillNode.prerequisite`·`cost`(§12-2) | "available" when prereq+SP met | what can I take | lock/border/fill |
| 6 | C6 | Node info | low-right | on focus | effect·cost·prereq | `SkillNode.effect`·`cost`·`prerequisite`(§12-2) | updates on focus | confirm before take | title+detail |
| 7 | C7 | Next: 4-item pick | bottom | after SP use/skip | go to step 2 | `RewardScreenRule.step_order`(§12-2/§12-3) | tree → 4-pick transition | reward order clear | button+prompt |

#### Step 2: 4-item pick (reuse C-CARD)
After the tree, a **separate screen** for the 4-pick (§7-1, §12-3). Card component/states/a11y as I3 B4–B6, except:
| item | value (GDD §) |
| --- | --- |
| cards | **4** (`RewardScreenRule.item_offer_count`, §4-5) |
| guarantee | **≥1 Rare**, no skill nodes (§4-5, §12-3) |
| Dream Break route | Blue Second-Hand · Starlight Lens · lucid-line weighting (§4-5) |
| elite reward (ref) | 3 cards, ≥1 Uncommon (§4-5) |

#### State matrix (node C5 / 4-pick card)
| element | default | hover/focus | selected | disabled/locked | loading | empty | error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Node (C5) | owned=fill/else=outline | emphasis+info | just-taken | prereq unmet=lock+"need prereq" / low SP="point short" | enter fade | N/A: 4 nodes | "tree load error" |
| 4-pick card | normal | emphasis+ring | confirm+gem | maxed hidden (§4-5) | dealing anim | "no choices" | "gen error" |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| focus node | hover | arrows | D-Pad/stick | "Steady Counter, cost 1" |
| confirm node | click | Enter | A/○ | "Steady Counter taken, SP 0" |
| next/skip | click | Esc/Enter | B/A | "to 4-item pick" |
| pick item | click | Enter | A | "Starlight Lens selected" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| C2 | `RewardScreenRule.skill_point_delta`(§12-2) | `BossDefeated`(§12-1) | `SkillPointChanged` | int | 0 |
| C4·C5 | `SkillNode.*`(§12-2) | `BossDefeated`(§12-1) | `SkillTreeOpened`, `NodeStateChanged` | graph | read-only |
| C6 | `SkillNode.effect`·`cost`·`prerequisite`(§12-2) | — | `NodeFocused` | detail | "select node" |
| C7/4-pick | `RewardScreenRule.step_order`·`item_offer_count`·`rarity_guarantee`(§12-2) | `BossDefeated`(§12-1) | `RewardStepAdvanced`, `BossItemOffer` | 4 cards | edge |

> Needs add: `SkillPointChanged/SkillTreeOpened/NodeStateChanged/NodeFocused/NodePicked/RewardStepAdvanced/BossItemOffer/ItemPicked`.

#### Navigation
step 1 (tree) → C7 → step 2 (4-pick) → confirm → `NormalRun`(I1). Seal-trial rewards reuse this in shortened form (§7-2: Seal 3 Trial = Rare pick).

#### Edge cases
Reward order fixed (§7-1): on HP0, `BossDefeated` grants SP+1 & purify bonus first → during 8s protect, tree → then 4-pick. SP 0/skip: proceed without taking (SP carries). 8s end: auto-advance, unspent SP kept (assumed) `[TBD]`. Dream Break route weighting (§4-5).

#### Accessibility
Node state via color+lock/border/fill (§9-3). 8s protect = no time pressure. Info panel scalable; focus order numbered; 4-pick inherits I3 a11y.

#### UX rationale
- **See at a glance**: separate permanent growth (tree) from run reward (4-pick) by step so they don't blur. The tree draws nodes+edges to show "what I can take now / what opens next".
- **Operate / avoid mistakes**: focusing a node shows effect/cost/prereq before confirm; the 8s protect cuts misclicks and unspent points carry.
- **Feel**: granting the skill point up front cements "I beat the boss".
- **First vs repeat**: protect lets novices read; veterans take recommended nodes (§7-1) fast then go to the 4-pick.
- **Accessibility**: node state not color-only.
- **Watch**: ① node/item confusion → step separation, no nodes in the 4-pick; ② prereq/point misclick → color+lock+text; ③ reward-order tangle → SP first, order enforced; ④ 8s feeling rushed → "take your time" + points kept.

#### Open questions
Unspent SP/items at 8s end. Per-character tree as separate screen vs shared frame (currently shared).

#### Acceptance
- [ ] On kill, SP+1 is granted first, then tree → 4-pick in order.
- [ ] The 4-pick is 4 cards with ≥1 Rare and no skill nodes.
- [ ] Prereq-unmet/point-short nodes show color+lock+text.
- [ ] During 8s protect you can choose slowly; skipping keeps points.
- [ ] Pad-only node & 4-pick selection.

---

### 5.I5 PAUSE — Pause menu · state: `NormalRun`/`BossFight` paused

#### Purpose
Mid-combat ESC/Start freezes the field; choose resume/settings/controls/main/quit. Show a run summary to re-orient.

| field | value |
| --- | --- |
| Enter | ESC / Start (in combat) |
| Exit | resume → combat / settings → O4 / main·quit → after confirm |
| Input context | **paused** |
| Priority | core |

#### References
*Source: ui-ref harvest — interfaceingame (pause).*

![Risk of Rain 2 paused](references/ui/web-refs/pause/risk-of-rain-2-paused-500x281.jpg)
**What.** A dimmed field with a center vertical menu (Resume/Settings/Quit to Menu/Quit to Desktop). **Why.** Pause is best as a short center vertical menu — resume fast or leave. → applied: dim(1)·center menu(2)·highlight(3)·input(5).

> Words: add a **run summary(4)** (time/purify/seal) to re-orient on resume; main/quit lose progress → confirm.

#### Wireframe
![PAUSE wireframe](wireframes/pause.svg)

#### Legend
| # | code | element | position | shown | behavior/state | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Z1 | Pause dim | full | menu | combat freeze + dim | freeze (ESC) | freeze at once | clearly stopped | dim + input-block notice |
| 2 | Z2 | Menu list | center | menu | resume/settings/controls/to main/quit | menu (static) | select ≤100ms | fast resume/leave | label+focus |
| 3 | Z3 | Select highlight | item | menu | focus emphasis + SFX | input focus | emphasis on move | where am I | border+color+sound |
| 4 | Z4 | Run summary | top-left | menu | time-left·purify·seal progress | `run.timer`(§4-1)·purify(§4-2)·seal(§4-2) | snapshot at open | re-orient | text+numbers |
| 5 | Z5 | Input prompt | bottom | menu | device prompt | input(§2-5) | swaps on device | how to operate | device glyph |

#### State matrix (Z2/Z3)
| element | default | hover/focus | pressed | disabled | loading | error |
| --- | --- | --- | --- | --- | --- | --- |
| Menu item (Z2) | normal | emphasis+SFX, ring ≥3:1 | pressed | — | N/A | "menu error" |
| Highlight (Z3) | Resume default focus | tracks | — | — | — | — |
| Run summary (Z4) | values | — | — | — | snapshot at open | missing = "—" |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| open/close | — | ESC | Start | "paused" |
| move | hover | ↑/↓ | D-Pad | "Resume, 1/5" |
| run | click | Enter | A/○ | "Resume activate" |
| main/quit | click | — | — | "To main, confirm progress loss" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| Z2 | menu (static) | — | `PauseFocusChanged` | items | default |
| Z4 | `run.timer`(§4-1)·purify(§4-2)·seal(§4-2) | `PurgeGained`(§12-1) | `RunSummarySnapshot` | numbers | "—" |

> Needs add: `PauseOpened/PauseClosed`, `RunSummarySnapshot`.

#### Navigation
Resume → combat. Settings → O4 (re-paused on return). To main/quit → confirm modal then leave (no I6, progress forfeit). Controls → control overlay.

#### Edge cases
Main/quit forfeit progress (irreversible) → confirm. Pause allowed in boss fight (solo); co-op (out of scope) differs. 7:00 arriving while paused: on unpause, apply §4-1 priority.

#### Accessibility
Focus = color+border+sound; main/quit confirm states the outcome in words; summary shows numbers; subtitles/text scale.

#### UX rationale
- **See at a glance**: a short center vertical menu, Resume on top and default-focused; the left run summary re-orients "how far am I".
- **Operate / avoid mistakes**: to-main/quit forfeit progress, so they confirm.
- **Feel**: clarity over flourish; resume fast.
- **First vs repeat**: a controls entry lets novices check inputs anytime.
- **Accessibility**: outcome (loss) stated in words.
- **Watch**: ① accidental quit losing progress → confirm modal; ② default focus on a dangerous item → default Resume; ③ 7:00 handling confusion → §4-1 priority on unpause.

#### Open questions
Showing 7:00 arrival while paused (instant result vs on-unpause). Controls overlay vs separate screen.

#### Acceptance
- [ ] ESC/Start freezes the field and shows the center menu.
- [ ] Default focus is Resume.
- [ ] To-main/quit show a progress-loss confirm.
- [ ] Run summary (time/purify/seal) is shown.

---

### 5.I6 RESULT — Result / Summary (3 branches) · state: `DawnWake` · `DreamBreak` · `FailedWake`

#### Purpose
Close the run with the **emotion matching how it ended**, show **final build and run stats separately**, then meta rewards/unlocks. Even on failure, show the next goal.

| field | value |
| --- | --- |
| Enter | `AlarmReached`→DawnWake / `DreamBreakAchieved`→DreamBreak / HP0→FailedWake (§4-1) |
| Exit | Retry→O2 / Main / Leaderboard(O6) |
| Input context | non-combat, focus |
| Priority | core |

#### References
*Source: ui-ref harvest — interfaceingame (results).*

![Risk of Rain 2 defeat](references/ui/web-refs/results/risk-of-rain-2-defeat-500x281.jpg)
**What.** "Defeat!" title, left Stats panel (time/kills/damage…), right Info (class/killed-by/Items Collected/Unlocked), Continue. **Why.** Separate build (items/unlocks) from stats (records) so neither cramps. → applied: ending badge(1)·final build(3)·run stats(4)·currency/unlock(6).

![Hades game over](references/ui/web-refs/results/hades-game-over-500x281.jpg)
**What.** A failure screen with reached records. **Why.** Even failure closes with a reached point / next goal. → applied: FailedWake branch (2) + next goal.

> Words: **results must partition build vs stats** (Brotato). Dream Break = triumphant, Dawn Wake = relief, Failed = calm — same screen, different emotion.

#### Wireframe
![RESULT wireframe](wireframes/results.svg)

#### Legend
| # | code | element | position | shown | behavior/state (per branch) | data binding | criterion | UX intent | a11y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | D1 | Ending badge | top-center | always | DawnWake/DreamBreak/FailedWake — text+color+icon | branch(§4-1), `AlarmReached`·`DreamBreakAchieved`(§12-1) | branch badge on enter | how it ended | text label required |
| 2 | D2 | Ending pose | left | always | per-branch pose+line(§9-4) | `Character.id`(§12-2), lines(§9-4) | branch pose/line sync | character close | subtitle+voice, cut-in toggle |
| 3 | D3 | Final build (A) | top-right | always | weapon level + items(≤6) + level | `CombatWeapon`·`Item`·`weapon_level`·`level_reached`(§12-2) | accurate at end | this run's build | icon+name+level |
| 4 | D4 | Run stats (B) | mid-right | always | time·kills·purify·lucid evades·boss time | `RunTelemetry.*`(§12-2) | telemetry accurate | performance numbers | line-aligned+numbers |
| 5 | D5 | Records·splits | low-right | by branch | DB Time·boss splits·hidden unlock·no-damage·highest purify(§10) | `dream_break_stage_times`(§12-2), records(§10) | achieved only, else "—" | competition/PB | text+number+PB badge |
| 6 | D6 | Currency·unlock | low-left | always | dream shards/stardust/lucid core + unlocks(§2-3) | meta currency(§2-3) | shown at once on end | repeat motivation | icon+number+unlock text |
| 7 | D7 | Action buttons | low-right | always | Retry/Main/Leaderboard | routing | ≤100ms, default focus | next action | button+prompt |

#### Per-branch differences
| branch | D1 badge/color | D2 line (§9-4) | D5 emphasis | special |
| --- | --- | --- | --- | --- |
| `DawnWake` | dawn color, "Dawn Wake" | "…it was a dream. *phew*." | survival·purify | 7:00 + boss kill = no boss reward (§4-1) |
| `DreamBreak` | whiteout, "Dream Break" | "wait, I really thought I shot it…" | DB Time·splits·no-damage | true-ending emphasis, lucid core |
| `FailedWake` | cool color, "Failed Wake" | cold sweat | reached point·next goal | failure motivation (§13-3 #8) |

#### State matrix (D7 / D5)
| element | default | hover/focus | selected | disabled | loading | empty | error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Action button (D7) | normal | emphasis+ring | default focus (Retry) | leaderboard offline = dim+"Offline" | enter fade | N/A: 3 buttons | "transition fail — retry" |
| Records (D5) | values | item detail | new record = badge | not achieved = "—" (branch n/a) | "calculating" | "no records" | "record load error" |
| Currency (D6) | shown | — | new unlock = emphasis | — | settle anim | "none" | "settle error" |

#### Input parity
| action | mouse | key | pad | screen reader |
| --- | --- | --- | --- | --- |
| focus button | hover | Tab/arrows | D-Pad | "Retry (default)" |
| run | click | Enter | A/○ | "Retry activate" |
| record detail | hover | arrows | RB | "Dream Break Time 9:12, new record" |
| main | click | Esc | B | "Main menu" |

#### Data binding
| code | field (GDD §) | event | UI-proposed (needs add) | format | fallback |
| --- | --- | --- | --- | --- | --- |
| D1 | branch(§4-1) | `AlarmReached`·`DreamBreakAchieved`(§12-1) | `RunEnded{result}` | badge | "result TBD" |
| D2 | `Character.id`(§12-2), lines(§9-4) | (above) | — | pose+subtitle | default |
| D3 | `CombatWeapon`·`Item`·`weapon_level`·`level_reached`(§12-2) | — | `RunBuildSnapshot` | icon+Lv | "none" |
| D4 | `RunTelemetry.*`(§12-2) | — | `RunStatsSnapshot` | numbers | 0 |
| D5 | `dream_break_stage_times`(§12-2), records(§10) | `DreamBreakAchieved`(§12-1) | `RecordSplits` | time/number | "—" |
| D6 | meta currency(§2-3) | — | `RewardsGranted`, `UnlocksGranted` | number+unlock | 0 |

> Needs add: `RunEnded{result}/RunBuildSnapshot/RunStatsSnapshot/RecordSplits/RewardsGranted/UnlocksGranted`.

#### Navigation
Retry→O2 / Main / Leaderboard(O6, matching filter). Default focus **Retry**. Pad B/Esc = Main.

#### Edge cases
Concurrent ends (§4-1): 7:00 + kill → DawnWake priority. Dream Break cutscene entered then 7:00 → keep DreamBreak. Offline: leaderboard button dim+reason, records cached. New record: D5 badge+sound. FailedWake: still grants some reward (§2-3) + next goal.

#### Accessibility
Ending branch via text label + icon, not color only (§9-3). Cut-in/ending toggle. Subtitle size/bg. Unachieved records as "—" (no blanks). Default focus/order clear.

#### UX rationale
- **See at a glance**: a big top badge conveys "how it ended" with emotion; below, this-run's build (weapon/items) and play record (time/kills/evades) split left/right so neither cramps.
- **Operate / avoid mistakes**: three buttons, default focus on Retry for one-tap replay; leaderboard unavailable = dim+reason.
- **Feel**: Dream Break = triumphant whiteout + true-ending line; Dawn Wake = relief; failure = calm — per-branch emotion. New record = badge.
- **First vs repeat**: failure shows reached point + next goal so you want another go; veterans chase DB Time/splits/no-damage.
- **Accessibility**: branch stated in text; effects toggleable.
- **Watch**: ① build/stats blur → partition (Brotato); ② failure feeling like a dead end → reached/next-goal/partial reward (§13-3 #8); ③ colorblind branch → badge text; ④ concurrent-end confusion → §4-1 priority.

#### Open questions
FailedWake meta reward ratio. Leaderboard axis exposure.

#### Acceptance
- [ ] Each branch shows the right badge/pose/line.
- [ ] Final build and run stats are shown in separate areas.
- [ ] Dream Break shows DB Time·splits·no-damage records.
- [ ] Colorblind mode distinguishes the ending branch by text/icon.
- [ ] Default focus is Retry; pad-only restart works.

---

## 6. Cross-cutting rules

- **Navigation model**
  - Out-game (O1–O6): focus-driven. Always set a default focus (Main=Single, Character=Kohaku, Stage=LD-001/Normal, Result=Retry, Pause=Resume). Back/cancel = Esc/B. Irreversible (quit/to-main/unlock/run-start loss) confirms.
  - In-game (I1–I2): real-time. Only modals (level-up I3) / protection (reward I4) / pause (I5) overlay; combat freezes during them.
  - Switching input device swaps every C-PROMPT glyph at once (no memorization).
- **Global empty / loading / error**: `loading` distinguishes **enter-anim** from **no-data** ("loading…/syncing…" vs fade-in). `error` states **problem + fix** ("record load error — retry"); missing value = last value + warning border. `empty` is never blank — give a reason ("—", "undiscovered").
- **Accessibility (GDD §9-3)**: colorblind palette (enemy/ally bullets, hazard zones by shape+color), shake/flash/post-processing strength, hit-judgment display, ult cut-in simplify, auto-aim bias, lucid-evade assist, subtitles (size/bg/speed). **No screen conveys state by color alone.** Settings (O4) is the gateway to all of it.
- **BM consistency (GDD §10)**: no paid power / no gacha → **no cash-purchase UI on any screen.** Meta (O5) unlocks via play-earned currency only.
- **Layout / safe area**: 16:9 (1920×1080). HUD at edges/top/bottom, center clear. Top-left (status) / bottom (resources) / top-center (boss) slots have fixed meaning across screens (P4). 21:9·4:3 scale within safe area (later).

### 6-1. UX synthesis (GDD §13-3 risk linkage)
| UX risk (GDD §13-3) | screens | decision / mitigation | verification |
| --- | --- | --- | --- |
| danger unseen in volume (#5) | I1, I2 | HUD to edges, center clear; hazards color+shape+sound | 180-enemy + colorblind playtest |
| time awareness vs top-left diegetic timer | I1, I2 | alarm fixed top-left + final-60s edge/sound + hidden-boss time dual | 1s read from any screenshot |
| late-game tedium (#3) | O3, I1, I6, O5 | purify/seal visualize early boss spawn; Dream Break goal in stage/result; meta long-term goals | progress awareness · retry rate |
| lucid evade too hard/spammy (#4) | I1, I2 | combo + near/lucid reward tiers; counter window visible | novice accidental · veteran intentional |
| Dream Break too hard (#8) | I2, I6 | seal progress · hidden-boss approach; failure → next goal | reach rate · retry rate |
| survivor-like clone look (#2) | all | lucid evade · alarm clock · Dream Break · per-character tree front-and-center | differentiation survey |
| scope creep (#7) | O2, O3 | VS Kohaku/Toko/LD-001 active, rest locked | out-of-scope unbuilt check |
| monetization confusion (BM §10) | O5, all | no cash UI, currency unlocks only | no purchase screen |
| license/official confusion (#1) | O1, O2 | character-name/display license area — **layout only, legal separate** | display-guideline review |
| co-op time-stop disturbing others (#6) | (out of scope) | unbuilt in VS; per-player/team/joint effect split at co-op build | — (out of UX scope) |

> #1 and #6 are partly outside UX (legal / co-op build) and flagged as such. The rest are handled by this design's layout/state/feedback rules.

## 7. Open questions (aggregate)
| # | screen | question |
| --- | --- | --- |
| Q1 | I1 | low-HP warning threshold (% — currently 25%) |
| Q2 | I1 | promote XP bar to a §9-2 HUD element? |
| Q3 | I1 | purify(A7) vs seal(A3) meaning overlap |
| Q4 | I2 | boss HP phase segment count / counter-window placement |
| Q5 | I3 | empty-pool fallback reward / card i-frame length |
| Q6 | I4 | unspent SP/items at 8s protect end |
| Q7 | I6 | FailedWake meta reward ratio / leaderboard axis exposure |
| Q8 | O2/O3 | unlock-condition text / stats radar vs bars / difficulty lock |
| Q9 | O4 | accessibility presets / live-apply option scope |
| Q10 | O5 | codex spoiler policy / permanent tree vs run tree visual split |
| Q11 | O6 | co-op record exposure / cheat policy / season reset |
| Q12 | global | 21:9·4:3 safe area · HUD scale |
| Q13 | global | **data contract**: add §5 "UI-proposed" events / runtime state to GDD §12-1/§12-2 |

> Full list of needed runtime fields/events in the decision tracker (`lucid_dawn_ui_ux_decisions.md` §4). No cash-payment events (§10).

## 8. Version history
| version | date | change |
| --- | --- | --- |
| v1.0 (EN master) | 2026-06-30 | Full out-game(O1–O6)+in-game(I1–I6) annotated-wireframe design document, web-harvested refs (interfaceingame, 8 games), design tokens + decision tracker, engine binding (App. D), usability test plan (App. E). 13 wireframes lint+render pass. Korean/Chinese versions derived from this master. |

## Appendix A. Methodology (rationale)
The UX rationale sections reason with the frameworks below but never name them in the body (plain-language rule).
| framework | used for |
| --- | --- |
| Celia Hodent, *The Gamer's Brain* | spine of every UX rationale (feedback/clarity/form-follows-function/consistency/error prevention + motivation/emotion/flow) |
| Nielsen's 10 heuristics | status visibility, consistency, error messages (problem+fix), recognition over recall |
| Pinelle game usability heuristics (CHI 2008) | camera/control/hidden-status/micromanagement failure modes |
| Desurvire PLAY / HEP | fun/immersion lens |
| Fagerholt & Lorentzon, *Beyond the HUD* | HUD element classification (diegetic alarm clock vs meta/non-diegetic bars) |
| Swink *Game Feel*; Jonasson & Purho "Juice it or Lose it" | feel stack + juice budget + readability under chaos |
| Xbox XAG; IGDA GASIG Top Ten; Game Accessibility Guidelines | color-independence, subtitles, shake/flash toggles, remap, difficulty/speed |

## Appendix B. Reference index / harvest recipe
- Harvested with **Game UI Reference CLI (`ui-ref`)** from **interfaceingame.com** per-game pages: Hades · Risk of Rain 2 · Honkai: Star Rail · Slay the Spire · Returnal · Hollow Knight · Moonlighter · Destiny 2. Curated by screen type into `references/ui/web-refs/<category>/`. Personal research citations, not a redistributable asset pack. Manifest: `ui_research/manifests/local_ui_refs_manifest.md`.

```bash
# one-time: pip install playwright && playwright install chromium
# put interfaceingame per-game URLs in ui_research/urls.txt, then
ui-ref collect --browser --site interfaceingame --scroll 8 --download-gallery-assets --download-asset-limit 10
# gap-fill specific screens:
ui-ref collect --browser --site interfaceingame --download-title-contains defeat --download-title-contains paused --download-title-contains audio
ui-ref scan-local
```
> Game UI Database is SPA + Cloudflare → headless harvest blocked (both the `scrn=` filter and `gameData.php?id=` per-game time out). We used interfaceingame per-game; direct survivor-likes are described in words in §B-2.

### B-2. Direct survivor-like patterns (words — not captured)
The harvested games are adjacent roguelites, so direct **bullet-heaven / survivor-like** conventions are noted here. (Capture later from GUIDB Soulstone Survivors = `gameData.php?id=2403`, etc., subject to the headless limit above.)
| screen | direct title | pattern to adopt / contrast | our callout |
| --- | --- | --- | --- |
| HUD | Vampire Survivors | **timer top-center**, **XP = top full-width strip**, HP near player, ability icons in one corner, minimal chrome | I1: XP A1 adopted; alarm top-left (deliberate exception) |
| HUD | 20 Minutes Till Dawn | **manual aim** (not auto-target) → aim feedback/reticle, active abilities | I1: auto-aim bias option (§9-3) + skill slots A8 |
| Level-up | Vampire Survivors / Brotato | **pause + 3–4 cards**, rarity color, instant read, brief i-frame on confirm | I3: paused cards B4, rarity B5 |
| Level-up | 20 Minutes Till Dawn | **review current build/synergy while choosing** (the gap modders fix) | I3: current-build panel B3 |
| Result | Brotato | **partition build vs stats**, meta currency/unlock surfaced | I6: D3 build / D4 stats split |
| Inventory/build | Soulstone Survivors / Halls of Torment | many stacked items **scale-down + stack count**, rarity color, full build panel on pause | I3 B3, I6 D3 |
| Boss | LoL Swarm (survivor mode) | top horizontal boss bar **takes the timer slot**, phase segments | I2: boss HP A10 (ours takes the empty top-center slot) |

> Deliberate differentiation (avoid clone look, §13-3 #2): lucid evade (counter window A12) · alarm clock (diegetic top-left) · Dream Break (hidden boss + time dual A13) · per-character skill tree (I4). We foreground what the direct titles don't.

## Appendix C. Build (shareables) + wireframe validation
```bash
pip install markdown python-docx
python <skill>/templates/build_pdf.py  lucid_dawn_ui_ux_design.en.md --css <skill>/templates/design-pdf.css
python <skill>/templates/build_docx.py lucid_dawn_ui_ux_design.en.md   # render wireframes/*.png first
```
All 13 wireframes pass `validate_wireframe.py` (XML, background rect, ≤10 callouts, badges twice, leaders ≤4 pts non-crossing, gutter ≤6/side, no off-canvas) + headless-Chrome render eyeball. flow.svg is a wireflow (exempt from the callout linter).

## Appendix D. Implementation binding — Unity 6 UI Toolkit × DOTS/ECS
> Implements §5 data binding **event-driven, no-GC** on the chosen stack (Unity 6 · DOTS · UI Toolkit). Authoritative refs: `unity-dots-manual`, bullet-hell rendering recipe. Final decisions = TDD.

- **Roles**: ECS (sim, jobs/Burst) is the single source of runtime state (`RunState`, `PlayerRuntime`, boss/trial runtime — §7 add). UI Toolkit (managed, main thread) renders. A **bridge `SystemBase`** (main thread) reads ECS and pushes to UI **only on change** — the real implementation of "event-driven".
- **No-GC / no per-frame rebuild** (HUD must not cost at 180 enemies, P3): state as `IComponentData` singletons; bridge checks ECS **ChangeVersion** and updates only changed labels; cache `VisualElement` refs (no per-frame `Q<>()`); no LINQ/boxing in the loop; timer text updates per **second**, not per frame.
- **World vs screen space**: fixed HUD = screen overlay (UIDocument/PanelSettings); player/enemy-anchored (lucid combo A6, counter window A12, **damage numbers**) = world anchors — **heavy world text (damage numbers) goes through the project's mass render path, not UI Toolkit**; UI Toolkit only for the few HUD-anchored ones.
- **Events ↔ ECS**: §5 "UI-proposed" events implemented as bridge change-detection (DOTS-friendly); GDD §12-1 events (`BossDefeated`, etc.) received as ECS events/singleton flags driving UI transitions. Modals/reward = sim pause synced (system-group stop).
- **Multi-res / input / localization**: PanelSettings scale mode + safe area (tracker D-18); gamepad via UI Toolkit focus navigation (ring ≥3:1) + Input System; Unity Localization string tables (KR/EN/CN length, subtitle ~≤38/line, locale number format).
- **Checklist**: [ ] 0 alloc / minimal reflow at high density · [ ] update only on change (profiled) · [ ] mass world text off UI framework · [ ] sim pause synced during modals · [ ] pad focus nav on every screen.

## Appendix E. Usability test plan (core loop)
> The UX rationale is heuristic reasoning; this is how it gets validated. Wireframe-only claims (readability-under-chaos) MUST be re-validated in an engine build.

- **Goal/hypotheses**: pass the core loop (menu→combat→level-up→boss→reward→result) without getting lost; key legibility: ① read time-to-7:00 ≤1s, ② identify hazard/player/pickups at 180 enemies, ③ read a card ≤1s, ④ understand reward order (SP→tree→4-pick).
- **Method/participants**: moderated think-aloud, 6–8 — survivor-like novice 3 + veteran 3 + colorblind 1–2 (separate session). Build: VS scope.
- **Task scenarios ↔ acceptance**:
  | # | task | success | links |
  | --- | --- | --- | --- |
  | T1 | from start to run begin | ≤3 min, unguided, pick char+stage→start | O1/O2/O3 |
  | T2 | (random pause) "how long until 7:00?" | correct ≤1s | I1 A2 (§3-2) |
  | T3 | pick one level-up card | read ≤1s, **observe build-panel use** | I3 B3/B4 |
  | T4 | attempt lucid evade | novice accidental + combo seen / veteran intentional | I1 A6 (§3-2) |
  | T5 | boss fight | boss bar seen, crack→groggy & counter **used** | I2 A10/A11/A12 |
  | T6 | boss reward | **understand SP→tree→4-pick order**, node/item distinct | I4 |
  | T7 | result | recognize branch, build vs stats split, Retry restarts | I6 |
- **Metrics**: per-task success/time/errors · SUS · fun/engagement survey · **readability-under-chaos** (frozen high-density screenshot id accuracy, separate colorblind session) · accessibility (colorblind id / toggle behavior).
- **Pass bar / iteration**: core tasks (T1·T2·T3·T6) success ≥85%, T2 1s-read ≥90%, colorblind lethal id =100%. Misses → adjust the corresponding number in the tracker and re-test; reflect in §8.
- **Limit**: this is the *test design*. A real clickable prototype / sessions / SUS tally need build + people — not performed here.





