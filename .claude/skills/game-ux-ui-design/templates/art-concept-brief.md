# {Game} — UI Art Concept Brief: {screen-id}

> Optional downstream artifact. This image prompt tests art direction from the wireframe + GDD/design
> context. It does **not** replace the design document, tokens, exact UI text, states, measurements, or
> accessibility rules.

## 1. Screen

- Screen: `{screen-id}` / `{screen name}`
- Source wireframe: `wireframes/{screen-id}.svg`
- Design section: `{document}.md` §{section}
- Intended output: `art-concepts/{screen-id}-ui-art-concept.png`

## 2. GDD / Design Context

- Genre / camera / platform: {survivor-like, bullet-hell, PC/Steam, etc.}
- Core loop or fantasy: {pressure → read → dodge → reward...}
- Screen purpose: {what the player must understand/do in 1 second}
- Must preserve: {combat readability, pause state, card count, resource identity, etc.}

## 3. References Used

| reference | pattern borrowed | do not copy |
| --- | --- | --- |
| `{path}` | {card grid / reward frame / HUD meter / key art placement} | {characters, logos, exact UI, icon art} |
| `{path}` | {pattern} | {avoid} |

## 4. Visual Tokens

- Base / surface colors: `{tokens}`
- Accent/resource colors: `{tokens}`
- Rarity/state rules: {color + border + icon/text}
- Typography intent: {large labels only; small text rebuilt later}
- Accessibility: {no color-only state; focus contrast; reduced flash if relevant}

## 5. Imagegen Prompt

```text
Use case: ui-mockup
Asset type: game UI art concept mockup
Primary request: Create a polished 16:9 high-fidelity UI art concept for {screen}.
Context: {GDD/design tone and loop}
Layout: Preserve this wireframe hierarchy: {major regions and positions}.
Style/medium: {2D stylized / painterly / clean UI / etc.}
Color palette: {tokens}
UI details: {specific panels/cards/meters/icons}
Text: "{exact large text only}" and abstract placeholder lines for small copy.
Constraints: Art direction only, original assets, no copied third-party UI, no watermark, preserve readability.
Avoid: {known bad outputs}
```

## 6. Review Notes

- Pass/fail against wireframe hierarchy:
- Readability:
- Useful art decisions:
- Needs manual UI rebuild:
