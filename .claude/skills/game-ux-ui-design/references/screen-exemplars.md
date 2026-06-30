# Screen exemplars — recognized game UI templates to derive wireframes from

Before drawing a screen, study the recognized exemplars for that screen type and bake the
named pattern into the wireframe + the UX 설계 의도. **Cite which exemplar each layout decision
follows** (e.g. "timer top-center per Vampire Survivors; pause-on-level-up per VS").

## Reference galleries (cite both, with roles)

- **Game UI Database — `gameuidatabase.com`** — primary. 1,300+ games, 55,000+ shots, free,
  searchable **by screen type** + attributes (art style, camera, control scheme, color,
  layout, font size). Has video + colorblind filters. **JS-rendered → harvest with
  `ui-ref collect --browser`.**
- **Interface In Game — `interfaceingame.com`** — curated whole-screen + per-game pages
  (e.g. `/games/risk-of-rain-2/`). Use for clean composition refs and single-title deep dives.

### Game UI Database deep-links (paste into `ui_research/urls.txt`)

| Screen type | URL |
| --- | --- |
| Choose Boon/Upgrade (level-up) | `https://www.gameuidatabase.com/index.php?tag=86` |
| Results Screen | `https://www.gameuidatabase.com/index.php?scrn=53` |
| Rewards & Experience | `https://www.gameuidatabase.com/index.php?scrn=54` |
| Enemy Health & Damage (boss bars) | `https://www.gameuidatabase.com/index.php?scrn=143` |
| Hades (per-game) | `https://www.gameuidatabase.com/gameData.php?id=534` |
| Dead Cells (per-game) | `https://www.gameuidatabase.com/gameData.php?id=1780` |

---

## Per-screen exemplars + the pattern to emulate

### In-run HUD
- **Exemplars:** Vampire Survivors (baseline), Dead Cells (readability under chaos, 4-slot
  loadout), Halls of Torment (ARPG/Diablo variant with stats panel).
- **Pattern:** survival **timer top-CENTER** (the core stake — readable from one
  screenshot); **XP bar = thin full-width strip across the very top**; health on/near the
  player; ability/weapon icons + cooldowns **clustered in one corner**; minimal chrome so
  the HUD never competes with projectiles/telegraphs.

### Level-up / item-pick modal
- **Exemplars:** Vampire Survivors (**pause** + 3–4 cards), Hades boon UI (choice-clarity
  gold standard).
- **Pattern:** **PAUSE the game on level-up** (removes time pressure + visual strain); 3–4
  choice cards; **distinct icon family per source/type** + color/border for rarity AND for
  permanent-vs-run (Hades gold vs blue laurels); concise stat deltas so a card reads in
  **<1s**; **CRITICAL — let the player review their current build/synergies while choosing**
  (the gap 20 Minutes Till Dawn modders fix); reward feedback on confirm (gem animation +
  brief i-frames, à la VS).

### Character select
- **Exemplars:** VS / Brotato roster grids; Halls of Torment (stat-rich).
- **Pattern:** portrait grid; per character show starting weapon/passive + key stat mods +
  unlock state; clear locked/unlocked affordance; scannable so playstyle reads at a glance.

### Results / summary
- **Exemplars:** Brotato win/loss recap, Hades run recap; GUIDB Results (`scrn=53`).
- **Pattern:** **partition** into (a) final build (weapons + passives — RoR2 scaling-icon
  idea) and (b) run stats (time, level, kills, damage, currency); surface unlocks/meta
  progression; **don't cramp either** (the Brotato community pain point).

### Boss HUD variant
- **Exemplars:** GUIDB Enemy Health & Damage (`scrn=143`); LoL Swarm behavior.
- **Pattern:** long horizontal bar at **TOP, taking over the top-center timer slot during
  the fight**; show the boss **NAME**; **SEGMENT** the bar to telegraph phases; optional
  green→yellow→red shift.

### Pause / inventory
- **Exemplars:** **Risk of Rain 2** scaling item bar (best for many stacked upgrades), Dead
  Cells loadout, Halls of Torment stats panel.
- **Pattern:** single item strip where icons **SCALE DOWN** as the collection grows so the
  full build stays visible; **STACK** identical items with a count; color-code rarity
  (white→green→blue→purple→orange); on pause expose a full stats/build panel + per-item
  inspection.

---

## Cross-cutting conventions (apply to all screens)

1. **Minimal clutter:** only show what the player checks often; **group by when/why it's
   read** (the Hades grouping principle).
2. **Horizontal bars read faster than vertical bubbles** — prefer horizontal HP/XP.
3. **Readability / telegraph first:** HUD + pickups stay legible amid bullet-heaven chaos;
   use universally-understood codes (timer, damage numbers, glowing XP gems).
4. **Repurpose the top-center slot contextually:** timer normally → boss HP in boss fights
   → countdown on selection screens (the LoL Swarm pattern).

## Geometric invariant — the top-center slot (don't satisfy the prose while breaking the layout)

The takeover pattern is a **single physical slot** shared over time. The boss bar MUST
occupy the **identical screen region** the timer occupied. **If your timer is in a corner,
you are NOT implementing this pattern** — either center the timer, or **drop the takeover
claim**. A wireframe that draws the clock top-left while the prose promises "timer
top-center → boss HP takeover" is self-contradictory (this exact error is easy to ship).
Verify in the render: the element sitting in the top-center band IS the timer (default) and
the boss bar (boss state), and they share one x-band.

## Deviation protocol (mirror the "cite every borrow" rule for every departure)

The skill already requires citing which exemplar each decision follows. **Symmetrically:
when you DEVIATE from an exemplar placement** — e.g. corner HP instead of near-player, or a
top-left diegetic clock instead of a top-center timer because the GDD or fiction demands it —
you MUST **name it as a deliberate deviation, cite the alternative convention you're following
instead, and state the mitigation** for whatever the original pattern protected (e.g. if the
timer stays in a corner during a boss fight, mandate that it remains visible / is inset into
the boss bar so remaining-time visibility isn't lost). Unannounced deviations read as mistakes.

## Two do/don't lessons to bake in

- **Results screens must partition build vs stats** (Brotato).
- **The level-up screen MUST let players review their current build/synergies while
  choosing** (20 Minutes Till Dawn gap).

## Sources
- gameuidatabase.com · creativebloq "Game UI Database 2.0" · interfaceingame.com
- jboger.substack.com "The secret sauce of Vampire Survivors" · vampire.survivors.wiki "Level up"
- LoL Swarm (leagueoflegends.fandom.com) · Hades HUD redesign (medium @bramhadalvi)
- RoR2 inventory (blog.rwittmann.com) · Halls of Torment review (rogueliker.com)
- Dead Cells (gameuidatabase id=1780; kokutech flow-state) · Brotato & 20MTD (Steam community)
