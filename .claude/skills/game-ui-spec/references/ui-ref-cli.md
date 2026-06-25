# Reference harvesting with `ui-ref` (this repo's CLI)

The spec's reference images are gathered with **this repo's `ui-ref` CLI** and then linked
from the spec as **separate file links** (the user's hard requirement #1). Run this BEFORE
drawing wireframes — the wireframe is *derived from* the references.

> If `ui-ref` is unavailable in the current environment, the skill still produces the spec —
> it just notes that references must be gathered manually into the same
> `references/ui/<collection>/<category>/` layout so the links resolve.

## 1. Initialize the workspace (once per project)
```bash
ui-ref init --project-name "<게임명>"
```
Creates `references/ui/`, `ui_research/` (`cache/html`, `cache/assets`, `manifests`),
`ui_research/urls.txt`, and `ui_ref_config.json`.

**Local refs convention:** `references/ui/<collection>/<category>/*.png|jpg|webp|gif`
(e.g. `references/ui/survivor-like/hud/`, `references/ui/roguelite/level-up/`). The
`<collection>/<category>` folder names matter — `scan-local` derives `collection` +
`category` from them and infers coarse tags (`hud`, `combat`, `progression`, `inventory`,
`navigation`, `party`…) from the path.

## 2. Harvest references (per-screen-type URLs)
Put the Game UI Database deep-links from `screen-exemplars.md` into `ui_research/urls.txt`.
Game UI Database is JS-rendered, so the **browser path is required**:
```bash
# one-time browser setup
pip install -e ".[browser]" && playwright install chromium

# harvest; scroll loads lazy images; grab a couple of thumbnails per page
ui-ref collect --browser --scroll 6 --download-gallery-assets --download-asset-limit 2
```
Each run writes to `ui_research/manifests/`: `collected_pages_<run_id>.json` and a browsable
`contact_sheet_<run_id>.html`. Defaults are polite (8s delay, 20 pages/run, robots.txt
checked) — keep runs small. Login-walled sites (Mobbin) are out of scope. Unknown galleries
auto-pick `--mode images`; override with `--mode images` / `--gallery-class`.

## 3. Curate into `references/ui/<collection>/<category>/`
Review the contact sheet, then **manually save the chosen images** into the local refs tree
(the tool intentionally downloads only a few thumbnails — collected pages are citation
context, not a redistributable asset pack). Use stable, descriptive filenames the spec links
to, e.g. `references/ui/survivor-like/hud/001_vampire_survivors_hud.png`.

## 4. Index the curated set
```bash
ui-ref scan-local
```
Writes `ui_research/manifests/local_ui_refs_manifest.{json,md}` — link the `.md` from the
spec's appendix as the reference index.

## 5. Embed references INLINE in each screen's 참조 section (no separate files, no links)
**Do NOT put references in separate files and link to them.** In the final deliverable (PDF /
Word), a link to `references/hud.md` is **dead** — it opens nothing, and the recipient doesn't
have that file. So embed the curated images + "무엇을/왜" notes **directly inside each screen's
`#### 참조` subsection** in `spec.md`:
```markdown
#### 참조 — 이 화면이 참고한 실제 게임 UI
*출처: Game UI Database — Enemy Health & Damage (scrn=143).*

![적 체력 + 쿨다운 링](references/ui/survivor-like/hud/001_action-hud_enemy-health.jpg)
**무엇을.** 적 머리 위 체력 + 플레이어 쿨다운 링. **왜.** 시선 이동 없이 위협·자원을 읽게.
→ 본작 적용: 보스 HP(A6) · 스킬 라디얼(A8) · 궁극기(A9).

| 참조 포인트 | 본작 콜아웃 | 근거 |
| --- | --- | --- |
| 적 체력 수치/바 | A6 보스 HP | 위협 상태가 항상 보이게 |

> 추가 참고: Vampire Survivors / Dead Cells / RoR2. (전체 후보·절차: 부록 REFERENCE_BOARD)
```
> Image paths are relative to `spec.md` (which sits at the project root), so use
> `references/ui/<collection>/<category>/x.jpg` — NOT `ui/...` and NOT `../`. The image
> renders inline in the spec, the PDF, and the Word doc.

Derive the wireframe FROM these references: callouts trace the layout decisions visible in the
embedded shots, and the **UX 설계 의도** says which exemplar each decision follows (plainly). Keep
`REFERENCE_BOARD.md` as the harvest *plan/index* in the appendix. The collected thumbnails are
**personal study citations** (attribute the source; not a redistributable asset pack).

## When you cannot run a live harvest
Put a **reference BOARD** in the appendix instead — a table per screen of exemplar game +
source URL + intended local path + the `ui-ref` command to fetch it later — and in each
screen's `#### 참조` section, **state the intended image and describe the borrowed pattern
in words** (no image yet) with a one-line note that images are pending harvest. Put a visible
banner at the TOP of `spec.md` saying images aren't committed yet and where the recipe is.
Keep the intended paths exact so the moment you save real images, the inline `![]()` embeds
resolve. Never word it as if images are attached when they aren't.
