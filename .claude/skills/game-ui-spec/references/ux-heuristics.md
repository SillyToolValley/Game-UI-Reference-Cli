# UX 고찰 엔진 — game UX heuristics & the considerations checklist

This is the most important reference in the skill — but it is the AI's **thinking tool, not
the reader's vocabulary**. Use this checklist to *decide* what the UI should do; then write
the spec in **plain language for a mixed meeting audience** (기획·아트·개발·PM). A spec stuffed
with "Hodent / Nielsen #1 / diegetic / juice budget / GWT / 역피라미드" is unreadable to the
people who have to build from it — that is a failing spec, even if every claim is "defensible."

> **OUTPUT STYLE (load-bearing).** Reason with the frameworks below; write the document
> WITHOUT naming them. Every UX claim in the body is a plain Korean sentence — the *decision*
> and a plain *why* ("적·아군 탄을 색과 모양으로 같이 구분해서 색약인 사람도 안전"), never the
> framework label ("P6 색 단독 금지(Nielsen #1; Beyond the HUD: meta)"). If you want the
> grounding on record, list the methodologies **once** in a short "설계 근거(방법론)" appendix —
> not per claim, not per cell. Cover BOTH halves (can they operate it / will they enjoy it),
> just say it plainly.

The backbone: **Celia Hodent's *The Gamer's Brain*** (depth, game-specific) +
**Nielsen's 10 heuristics** (breadth, HCI canon). Non-negotiable order in every UX 고찰:
**first USABILITY (can the player operate it), then ENGAGE-ABILITY (will they keep
playing).** Never ship a UX section covering only one half.

---

## Part 1 — USABILITY (cite the pillar/heuristic per claim)

1. **Signs & Feedback** (Hodent; Nielsen #1 visibility of status).
   For *every* player action and state change, specify the feedback = visual + audio +
   haptic where relevant. State explicitly: **no action occurs without feedback.** Cover
   hit confirmation, damage taken, pickup, level-up, cooldown ready, threshold reached.

2. **Clarity / visual hierarchy** (Hodent; Nielsen #1).
   Define a hierarchy ranking — default for action games: **player avatar > immediate
   threats > pickups > ambient.** Specify contrast, font legibility, minimum sizes, and
   **reserve a dedicated color/brightness band for the player character** so it's never
   lost in the crowd.

3. **Form follows function** (Hodent).
   Interactive objects, enemies, and pickups communicate their role through
   **silhouette / shape / color before any text.** Affordances readable at a glance.

4. **Consistency & standards** (Hodent; Nielsen #4).
   Lock controls, iconography, menu navigation, and world rules to be internally
   consistent and to follow genre/platform convention. **Flag and justify any deliberate
   deviation.**

5. **Minimize workload & errors** (Hodent; Nielsen #3/#5/#6/#9).
   Confirmation on irreversible actions; undo / exit / pause always reachable;
   **recognition over recall** (context-sensitive button prompts, not memorized combos);
   plain-language error messages stating **problem + solution** ("열쇠가 부족합니다 — 보스를
   처치해 봉인을 여세요").

6. **HUD type per element** (Fagerholt & Lorentzon, *Beyond the HUD*).
   For each HUD element, classify it **diegetic / meta / spatial / non-diegetic** and
   justify against the immersion-vs-readability tradeoff. (Diegetic = in world+fiction;
   Meta = fiction status w/o world object e.g. screen-edge damage vignette; Spatial = in
   3D space but not fiction e.g. floating waypoint; Non-diegetic = classic 2D overlay.)

7. **READABILITY UNDER CHAOS** — *mandatory for bullet-heaven / survivor-like / heavy-VFX*.
   (Swink *Game Feel*; Jonasson & Purho "Juice it or Lose it".)
   Define rules that guarantee the player can **always** parse: their character, incoming
   threats, **damage direction**, and pickups — even with hundreds of entities on screen.
   Require: telegraphs for dangerous attacks; elite/boss visual distinction; projectile
   contrast; layering/transparency rules; and a **cap on simultaneous screenshake/flash**
   so juice never buries critical signal.

## Part 2 — ENGAGE-ABILITY

8. **Juice / game feel + a juice budget** (Swink; Jonasson & Purho).
   Specify the feedback stack for core actions (hit-stop, screenshake, particles,
   squash/stretch, flashes, sound) **and a juice budget** so feedback scales with stakes
   without becoming noise. Tie it to the input→perception loop.

9. **Motivation & flow** (Hodent engage-ability).
   Address intrinsic motivation (competence / autonomy / relatedness) + the reward
   structure + a **flow curve** matching challenge to growing skill (no boredom, no
   anxiety). State the core loop and what makes minute-to-minute play satisfying.

10. **Emotion** (Hodent).
    Intended emotional beats; how presence / surprise / meaning are produced and
    reinforced through feedback and pacing.

## Part 3 — Cross-cutting (still part of every UX 고찰)

11. **Onboarding / FTUE & information layering** (Hodent GDC 2016; working-memory model).
    A sequenced first-session plan: which mechanics are taught, in what priority order, at
    what depth, via **teach-by-doing**, introduced **just-in-time**. Never overload one
    cognitive channel (don't force reading during a hard visuospatial task); don't fire
    many new inputs at once. (Phonological loop vs visuospatial sketchpad are separate,
    limited channels.)

12. **Accessibility** (Xbox XAG / IGDA GASIG Top Ten / Game Accessibility Guidelines).
    Never convey info by **color alone** — pair color with icon/shape/pattern; support
    deuteranopia/protanopia/tritanopia. Adjustable text size with adequate contrast;
    subtitles with speaker labels (~≤38 chars/line) + separate captions for non-speech
    audio. **Input & difficulty:** full remapping, sensitivity/invert/hold-vs-toggle,
    separate volume sliders (music/SFX/dialogue), broad difficulty **and** speed range,
    reduce-flashing / reduce-screenshake / photosensitivity toggles.

13. **Peer-reviewed game heuristics** (Pinelle CHI 2008; Desurvire PLAY/HEP).
    Pre-empt concrete failure modes: bad camera/FOV, unresponsive/unremappable controls,
    unskippable repeated content, hidden game status, micromanagement. Use PLAY to push
    beyond "usable" into fun/immersive (Game Play, Tutorial, Strategy/Challenge,
    Immersion, Coolness).

## Writing the "UX 설계 의도" section (plain language)

Use the 13 items above as a private checklist so you don't miss anything — then write the
section in plain Korean, grouped by reader-friendly themes, e.g.:
- **한눈에 읽히게** (what the player must see instantly; visual priority; 적·탄막이 많아도 보이게)
- **조작·실수 방지** (clear prompts, confirm/cancel, plain error messages)
- **재미·손맛** (feedback/연출 on key actions, kept from becoming noise)
- **첫 플레이 vs 반복** (teach a little at a time; efficient for veterans)
- **접근성** (색 단독 금지, 자막, 흔들림 토글, 리매핑)

Each point = the **decision + a plain why**, no framework names in the body. Cover BOTH
"can they operate it" and "will they keep playing." Close with **"이 화면에서 특히 조심할 점
top 3~5 + 대응"**, tied to the game's risk register *by description* (not by jargon). Mark a
genuinely N/A item with its reason rather than padding. Put the methodology names, if at all,
**once** in the document's "설계 근거(방법론)" appendix.

---

## Methodology table (for the AI's reasoning + the optional appendix — NEVER inline in the body)

| Framework | Use it for | Cite as |
| --- | --- | --- |
| **Celia Hodent — *The Gamer's Brain*** (CRC Press, 2017) | The spine of every UX 고찰: Usability pillars (Signs & Feedback, Clarity, Form-follows-function, Consistency, Minimize Workload, Error Prevention) + Engage-ability (Motivation, Emotion, Game Flow) | "Hodent, *The Gamer's Brain*, <pillar>" |
| **Nielsen's 10 Usability Heuristics for games** (NN/g) | Trusted HCI vocabulary for menu/HUD/settings flows | "Nielsen #\<n\>" |
| **Pinelle game usability heuristics** (CHI 2008) | Concrete failure modes (camera/FOV, unresponsive/unremappable controls, unskippable content, hidden status, micromanagement) | "Pinelle et al. 2008, #\<item\>" |
| **Desurvire PLAY / HEP** (HCII 2009 / CHI 2004) | Beyond usable → fun/immersive (Game Play, Tutorial, Strategy/Challenge, Immersion, Coolness) | "Desurvire PLAY: <category>" |
| **Fagerholt & Lorentzon, *Beyond the HUD*** (Chalmers, 2009) | Classifying each HUD element diegetic / non-diegetic / spatial / meta | "Beyond the HUD: <type>" |
| **Swink *Game Feel* (2008); Jonasson & Purho "Juice it or Lose it" (2012)** | Juice/feel stack + juice budget + readability-under-chaos | "Swink, *Game Feel*"; "Juice it or Lose it" |
| **Xbox XAG; IGDA GASIG Top Ten; Game Accessibility Guidelines** | Accessibility block (color-independence, text/contrast, subtitles, remapping, difficulty/speed, flashing/screenshake) | "Xbox XAG"; "IGDA GASIG"; "gameaccessibilityguidelines.com" |

**Default backbone:** Hodent (depth) + Nielsen (breadth). Reach for Pinelle/PLAY when
academic/portfolio credibility matters; *Beyond the HUD* whenever classifying a HUD element;
Swink/Juice + accessibility guidelines for every action-game screen.
