# Art Concept Imagegen Workflow

Use this only after the wireframe-level design document is coherent. The goal is to test visual
direction, not to replace the wireframe, legend, tokens, or accessibility rules.

## When to run

Run an art concept pass when the user asks to see the art direction, compare UI moods, prepare a
pitch/deck image, or validate that the design can carry the game's tone.

Pick **1-2 high-signal screens**:

- **Title/Main**: best for key art, tone, logo/menu placement.
- **HUD**: best for chaos readability and resource treatment.
- **Level-up / Item pick**: best for card language, rarity, reward feel.
- **Boss reward / Skill tree**: best for progression fantasy.
- **Result**: best for ending identity and emotional payoff.

Do not batch every screen by default. More concepts usually add noise before the art direction is
locked.

## Inputs

Before prompting, collect:

1. **GDD tone / fantasy / loop**: quote or summarize the core experience, genre, characters, stage,
   resources, and risk notes.
2. **Selected wireframe**: use the SVG/PNG as the layout authority. The concept must preserve its
   hierarchy: where panels, cards, meters, prompts, and safe areas live.
3. **Reference notes**: use the harvested reference screenshots and the per-screen "What/Why" notes
   for composition patterns only. Do not copy recognizable assets, characters, logos, or exact UI.
4. **Visual tokens**: colors, typography intent, rarity/resource rules, accessibility constraints.
5. **Art lock questions**: what should this image answer? Palette? Material language? Card frame?
   HUD icon style? Modal dim? Character key art?

## Prompt rules

Use Codex/imagegen if available. Otherwise write the prompt to
`art-concepts/<screen-id>-imagegen-prompt.md` for later use.

Prompt as a UI mockup:

- say **"high-fidelity UI art concept mockup"**, not "final screenshot";
- name the screen and exact layout hierarchy from the wireframe;
- describe the game's tone and resources from the GDD/design document;
- cite reference patterns in words only ("card choice grid", "reward card frame", "dark roguelite
  reward room"), not as "make it like Hades/Slay the Spire";
- specify the palette from tokens;
- ask for original art assets and no copied recognizable UI;
- constrain text heavily: exact text only for large labels, use abstract placeholder lines for small
  copy;
- preserve readability and safe space; avoid splash-art composition that breaks the UI.

## Output rules

Save project-bound generated images under:

```text
art-concepts/<screen-id>-ui-art-concept.png
```

Also save the prompt/brief when possible:

```text
art-concepts/<screen-id>-ui-art-concept.prompt.md
```

Add a short note in the design document or example README that the image is:

- art direction only;
- generated from the wireframe + GDD/design context + reference notes;
- not an implementation source for exact text, measurements, states, or accessibility.

## Review checklist

- Layout hierarchy still matches the wireframe.
- The screen's job is still obvious in 1 second.
- Art polish does not bury gameplay readability.
- Resource colors/rarity are paired with shape/icon/text, not color alone.
- It introduces a coherent material language (frames, panels, icon shape, glow, texture).
- It avoids copied third-party UI/characters/logos.
- Any generated text is either correct large text or intentionally treated as placeholder.

If the output fails layout or readability, iterate once with a narrower prompt. If it only fails small
text, keep the image as mood/art direction and note that exact text must be rebuilt in the UI tool.
