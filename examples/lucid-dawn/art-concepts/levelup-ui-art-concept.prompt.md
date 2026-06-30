# Level-up UI Art Concept Prompt

Generated with the built-in Codex/imagegen path as an art-direction test.

Input context:

- Wireframe: `../wireframes/levelup.png`
- Design section: `../lucid_dawn_ui_ux_design.en.md` §5.I3
- References: `../references/ui/web-refs/levelup-reward/slay-the-spire-choose-a-card-500x281.png`,
  `../references/ui/web-refs/levelup-reward/hades-well-of-charon-500x281.jpg`
- Tokens: `../lucid_dawn_ui_ux_tokens.md`

Prompt:

```text
Use case: ui-mockup
Asset type: game UI art concept mockup for a UX/UI design skill example
Primary request: Create a polished 16:9 game UI art concept for the "Lucid Dawn: Dream Survivor" Level-up / Item pick paused modal. It should transform a wireframe into a high-fidelity art direction sample, not a final production screenshot.
Context: The game is a survivor-like / bullet-hell / action roguelite about pressure, split-second reads, perfect dodges, lucid rush, purify/grow, and waking up by your own hand. Tone is cute nightmare / dream-depth / dark roguelite, with readable combat UI.
Layout: Keep this exact composition: dark dimmed combat backdrop; top-center level-up header; left current-build panel; three large reward choice cards centered; bottom-center pick prompt. The three cards must be the visual focus and be readable in one second.
Style/medium: high-fidelity stylized 2D game UI mockup, original assets, not copied from any existing game. Dark dreamlike fantasy with soft nightmare motifs, crisp UI panels, card frames, subtle gem/sigil accents, light particle flourishes.
Color palette: base void #0B0F1A, raised panels #16203A, lucid blue #4AA6FF, dream gold #FFC24A, purify violet #B58CFF, HP rose #FF5D6C. Rarity states use border + corner icon + text-like badge shape, not color alone.
UI details: left build panel has six small owned item slots with icons; center has three reward cards with icon art at top, name band, short stat-effect area, rarity corner marker; selected middle card has a clear focus ring and slight glow; bottom prompt uses keyboard/gamepad glyph shapes. Header reads "LEVEL UP" only. Avoid tiny body copy; use abstract placeholder lines for card text.
Composition/framing: 1920x1080 landscape, orthographic UI screenshot, no perspective skew, no phone frame, no browser chrome. Keep generous combat-safe negative space behind the modal.
Constraints: Preserve the wireframe hierarchy and locations. No copyrighted characters or recognizable UI from Hades, Slay the Spire, Returnal, or other games. No watermarks, logos, real brand names, or clutter. Do not make it a marketing splash screen; it must look like an in-game UI mockup.
```

Review:

- Useful: preserves the left build panel + three reward cards + selected-card focus hierarchy.
- Useful: establishes a coherent dream/nightmare material language for card frames, glow, sigils, and item icons.
- Caveat: exact UI text and small copy should be rebuilt manually in the UI/tooling layer; this image is not an implementation source.
