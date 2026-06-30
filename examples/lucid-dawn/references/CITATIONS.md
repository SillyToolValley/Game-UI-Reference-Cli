# Reference citations

The thumbnails under `ui/web-refs/` are **low-resolution research citations** gathered with this
repo's `ui-ref` CLI from **[interfaceingame.com](https://interfaceingame.com)** per-game pages.
They are included to make the example spec render and to study UI/UX patterns — **not** a
redistributable asset pack and **not** training data. All rights remain with the original games
and their publishers. If you are a rights holder and want a thumbnail removed, please open an issue.

## Sources (interfaceingame.com per-game pages)
- Hades — https://interfaceingame.com/games/hades/
- Risk of Rain 2 — https://interfaceingame.com/games/risk-of-rain-2/
- Honkai: Star Rail — https://interfaceingame.com/games/honkai-star-rail/
- Slay the Spire — https://interfaceingame.com/games/slay-the-spire/
- Returnal — https://interfaceingame.com/games/returnal/
- Hollow Knight — https://interfaceingame.com/games/hollow-knight/
- Moonlighter — https://interfaceingame.com/games/moonlighter/
- Destiny 2 — https://interfaceingame.com/games/destiny-2/

## Regenerate
```bash
# ui_research/urls.txt = the per-game URLs above
ui-ref collect --browser --site interfaceingame --scroll 8 --download-gallery-assets --download-asset-limit 10
ui-ref scan-local
# then curate into references/ui/web-refs/<category>/ by screen type
```

Direct survivor-like titles (Vampire Survivors / Brotato / 20 Minutes Till Dawn / Soulstone
Survivors) are not on interfaceingame; their patterns are described in words in the spec (Appendix B-2).
