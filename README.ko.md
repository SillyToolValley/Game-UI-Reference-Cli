# Game-UI-Reference-Cli

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Core deps](https://img.shields.io/badge/core%20dependencies-0-brightgreen)

[English](README.md) · [中文](README.zh.md) · **한국어** · [日本語](README.ja.md)

<img src="examples/lucid-dawn/art-concepts/levelup-ui-art-concept.png" alt="ui-ref 레퍼런스 기반으로 생성한 레벨업 UI 아트 컨셉" width="900">

<p align="center"><b>Concept art generated from UI references collected with this CLI</b></p>

게임 UI에 초점을 둔, 의존성 가벼운 **UI 레퍼런스 리서치** CLI. 로컬에 모아둔 UI 레퍼런스 이미지를
인덱싱하고, (선택적으로) 공개 UI 데이터베이스의 레퍼런스 페이지를 수집 — 렌더링하고, HTML·이미지
메타데이터를 캐시하고, 요청 시 썸네일을 받아 — UI/UX 패턴을 연구할 수 있게 해준다.

기본·구조화 소스는 **[Game UI Database](https://www.gameuidatabase.com) (gameuidatabase.com)**.
그 외 여러 공개 UI/UX 갤러리도 범용 이미지 수집 모드로 동작한다([지원 사이트](#지원-사이트) 참고).

의도적으로 보수적·예의 바르게 동작한다:

- 로컬 레퍼런스를 먼저 인덱싱하고,
- 외부 URL은 **사용자가 나열했을 때만** 가져오며(크롤링 없음),
- 에셋은 **요청하지 않으면** 받지 않고,
- 폴라이트 딜레이·런당 페이지 상한·`robots.txt` 확인이 내장돼 있다.

> **로그인 장벽이 있는 사이트는 범위 밖.** 계정이 필요한 갤러리(예: Mobbin 앱 화면)는 이 도구로
> 수집할 수 없으며 의도적으로 미지원이다. 이건 개인 연구 보조 도구지 범용 스크레이퍼가 아니며,
> 타인의 에셋을 재배포하기 위한 것도 아니다. 각 사이트의 약관과 `robots.txt`를 존중하라.

## 찾아내는 것 — UI 레퍼런스

이 도구의 핵심은 실제 게임 UI 스크린샷을 모아 패턴을 연구하게 하는 것이다. `ui-ref`에 레퍼런스 페이지를
가리키면 렌더링하고, 메타데이터를 캐시하고, 썸네일을 받아 —— 사용자가 **화면 유형별로** 정리한다. 아래는
샘플을 위해 `ui-ref collect --browser --site interfaceingame`로 per-game 페이지에서 수집한 레퍼런스다:

![ui-ref가 화면 유형별로 수집한 UI 레퍼런스](docs/captures/references-found.png)

각 실행은 받은 썸네일이 제목·크기·**출처 링크**와 함께 인라인 렌더되는 **콘택트 시트**
(`ui_research/manifests/contact_sheet_*.html`)와 **매니페스트**(`scan-local` →
`local_ui_refs_manifest.{json,md}`)도 쓴다. 이렇게 모은 레퍼런스가 아래 와이어프레임의 **출처**이며,
각 디자인 화면은 자기가 차용한 정확한 샷을 인용한다.

## 결과물 샘플

완성된 실제 예시가 **[`examples/lucid-dawn/`](examples/lucid-dawn/)** 에 있다 — survivor-like/로그라이트
(*Lucid Dawn: Dream Survivor*)의 완전한 UX/UI 디자인 문서로, `ui-ref`로 수집한 레퍼런스를 바탕으로
`game-ux-ui-design` 스킬이 생성했다. **12개 화면**(아웃게임+인게임)·**주석형 와이어프레임 13종**, 영어·중국어·한국어·일본어 제공.

**주석형 와이어프레임** — 모든 UI 요소에 번호, 영역을 네모/동그라미로, 리더 라인을 프레임 *밖* 거터 라벨로:

<img src="docs/captures/hud.png" alt="인게임 HUD 주석 와이어프레임" width="900">

### 디자인 문서는 얼마나 자세한가?

각 와이어프레임 아래에, **12개 화면 모두** 다음을 갖춘다:

- **목적** (진입 / 이탈 / 입력 컨텍스트 / 우선순위)
- **참조** — 차용한 실제 게임 UI를 "무엇을 / 왜" 메모와 함께 본문에 인라인 임베드
- **와이어프레임**(SVG) + **범례** — 요소별: 위치 · 표시 조건 · 동작/상태 · **데이터 바인딩** · **측정 가능한 동작 기준** · 평이한 UX 의도 · 접근성
- **상태 매트릭스** — default / hover / pressed / selected / disabled-locked / loading / empty / error
- **입력 패리티** — 마우스 · 키보드 · 게임패드 · 스크린리더
- **데이터 바인딩** — 모든 필드/이벤트를 **GDD와 대조 검증**; GDD에 없는 건 "GDD 추가 필요"로 표시(임의 발명 금지)
- **내비게이션 · 엣지 케이스 · 접근성 · UX 설계 의도(평이체) · 미해결 질문 · 수용 기준 체크리스트**

여기에 동반 문서: **디자인 토큰**(색 hex / 타이포 / 모션 / USS 변수), **수치·결정 트래커**(모든 수치를
GDD확정 / 표준 / 추정으로 분류), 그리고 **엔진 바인딩(UI Toolkit × DOTS)** · **사용성 테스트 플랜** 부록.

<details>
<summary><b>실제 발췌 보기 — 인게임 HUD 범례 + 상태 매트릭스</b></summary>

범례(9행 중 발췌):

| # | 코드 | 요소 | 위치 | 데이터 바인딩 | 동작 기준 | 접근성 |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | A2 | 알람 시계 | 좌상단 | `run.timer` 0–1200s (§4-1), `AlarmReached` (§12-1) | 어느 순간에도 남은 시간 1초 내 인지 | 시계+숫자, 최종 60초 소리+밝기 |
| 4 | A4 | HP / 실드 | 좌상단 | `Character.hp` (§12-2), 실드 (§12-2 추가) | 피격 100ms 내 반영; 저HP는 색+점멸+테두리 | 색+점멸+테두리+수치 |
| 7 | A7 | 정화도 바 | 하단 중앙 | 정화도 (§4-2), `PurgeGained` · `BossThresholdReached` (§12-1) | 획득 200ms 내; 임계치 → 보스 경고 | 채움+수치+소스 토스트 |

상태 매트릭스(발췌):

| 요소 | default | pressed/active | disabled/locked | error |
| --- | --- | --- | --- | --- |
| 스킬 (A8) | 라디얼 채움 | 눌림 + SFX, 라디얼 0 | 회색 + 자물쇠 + "미해금" | "쿨다운 오류 — 기본값" |
| 궁극기 (A9) | 충전 채움 | 발동 시네마틱 | <100이면 흐림 + 남은량 | 마지막값 + 경고 테두리 |

</details>

아래는 **실제 렌더된 디자인 페이지**다(인게임 HUD 화면 — 참조 스크린샷, 주석 와이어프레임, 10열 범례 표
전체, 산출물 그대로):

![디자인 페이지 샘플 — 인게임 HUD](docs/captures/design-page-hud.png)

**더 많은 화면** — 전체는 [`examples/lucid-dawn/wireframes/`](examples/lucid-dawn/wireframes/):

<img src="docs/captures/levelup.png" alt="레벨업/아이템 선택" width="440"> <img src="docs/captures/results.png" alt="결과 화면" width="440">
<img src="docs/captures/skilltree.png" alt="보스 보상 스킬트리" width="440"> <img src="docs/captures/character-select.png" alt="캐릭터 선택" width="440">

디자인 문서 전문 보기: [영어](examples/lucid-dawn/lucid_dawn_ui_ux_design.en.md) ·
[중국어](examples/lucid-dawn/lucid_dawn_ui_ux_design.zh.md) ·
[한국어](examples/lucid-dawn/lucid_dawn_ui_ux_design.ko.md) ·
[일본어](examples/lucid-dawn/lucid_dawn_ui_ux_design.ja.md) ·
[PDF](examples/lucid-dawn/lucid_dawn_ui_ux_design.en.pdf).

## 설치

```bash
git clone https://github.com/SillyToolValley/Game-UI-Reference-Cli
cd Game-UI-Reference-Cli
pip install -e .
```

선택적 브라우저 지원(JavaScript 렌더 사이트 — 즉 대부분 — 에 필요):

```bash
pip install -e ".[browser]"
playwright install chromium     # 1회: 헤드리스 브라우저 다운로드
```

| | `scan-local` | `collect` (정적) | `collect --browser` |
| --- | --- | --- | --- |
| Python 표준 라이브러리만 필요 | ✅ | ✅ | — |
| `playwright` + 브라우저 필요 | — | — | ✅ |
| 서버 렌더 페이지에서 동작 | n/a | ✅ | ✅ |
| JS 렌더 레퍼런스 사이트에서 동작 | n/a | ✗ (0건) | ✅ |

브라우저 경로는 **Playwright**를 직접 사용한다(현실적인 데스크톱 UA+뷰포트, 지연 이미지 로드를 위한
선택적 자동 스크롤). 스텔스/안티봇 레이어는 없다 — 지원하는 공개 사이트는 일반 헤드리스 브라우저에
콘텐츠를 제공하며, 내장된 예의(딜레이 등)가 런을 얌전하게 유지한다.

## 빠른 시작

프로젝트 루트에서:

```bash
ui-ref init --project-name "My Project"
# references/ui/<collection>/<category>/*.png|jpg|... 에 레퍼런스 이미지를 둔다
ui-ref scan-local
```

## 동반 스킬: `game-ux-ui-design`

이 repo는 여기서 모은 레퍼런스를 **모범적인 게임 UX/UI 디자인 문서**로 바꿔주는 **Claude Code 스킬**을
함께 제공한다 — survivor-like / 불릿헤븐 / 로그라이트 게임에 특화. 위치:
[`.claude/skills/game-ux-ui-design/`](.claude/skills/game-ux-ui-design/).

GDD나 기능 브리프가 주어지면 다음을 갖춘 디자인 문서를 만든다:

- **레퍼런스 이미지는 각 화면 본문에 인라인 임베드**(`ui-ref`로 수집);
- **그 레퍼런스에서 도출한 와이어프레임** — **모든 UI 요소를 번호로**, 영역을 네모/동그라미로,
  **프레임 밖으로 뽑은 리더 라인**으로 설명(SVG 주석 콜아웃 키트 —
  [`templates/wireframe-kit.svg`](.claude/skills/game-ux-ui-design/templates/wireframe-kit.svg));
- 각 화면에 **범례·상태 매트릭스·입력 패리티·데이터 바인딩** 표;
- 화면마다 평이한 우리말 **〈UX 설계 의도〉**(게임 UX 휴리스틱으로 사고하되 본문엔 용어를 쓰지 않음);
- **출하급 단계(선택)**: 디자인 토큰 · 수치/결정 트래커 · 엔진 바인딩 · 사용성 테스트 플랜;
- 마크다운 원본을 **16:9 가로 PDF**(`build_pdf.py` + `design-pdf.css`)로 렌더해 빽빽한 표도 공유하기 좋게;
- 선택한 와이어프레임을 Codex/imagegen 기반 **UI 아트 컨셉 목업**으로 뽑아 무드·재질·카드/HUD 처리를 검토.

전체 생성 샘플은 **[`examples/lucid-dawn/`](examples/lucid-dawn/)**(12화면, 와이어프레임 13종, 토큰,
트래커; 영어·중국어·한국어·일본어)과 위 [결과물 샘플](#결과물-샘플) 캡처를 참고.

내 게임 프로젝트에서 쓰려면 스킬 폴더를 그 프로젝트의 `.claude/skills/`(또는 모든 프로젝트용으로
`~/.claude/skills/`)에 복사한 뒤, Claude Code에 "〈화면〉의 UX/UI 디자인 문서 뽑아줘"라고 요청하면 된다.

## 명령어

### `scan-local` — 로컬 레퍼런스 인덱싱

`references/ui/<collection>/<category>/<file>`을 순회하며 파일 바이트에서 이미지 크기를 읽고
(PNG/GIF/JPEG, Pillow 불필요), 폴더 경로로부터 대략적 태그를 추론해 `ui_research/manifests/`에
JSON+Markdown 매니페스트를 쓴다.

### `collect` — 명시적으로 나열한 페이지 수집

`ui_research/urls.txt`에 레퍼런스 URL을 한 줄에 하나씩 넣고:

```bash
# JS 렌더 사이트 → 브라우저 사용. URL 도메인별로 모드가 자동 감지된다.
ui-ref collect --browser

# 페이지당 이미지 몇 장 + 지연 이미지 로드를 위한 스크롤
ui-ref collect --browser --scroll 6 --download-gallery-assets --download-asset-limit 2

# 알 수 없는 사이트에 모드/갤러리 클래스 강제
ui-ref collect --browser --mode images
ui-ref collect --browser --gallery-class "thumb-card"
```

한 `urls.txt`에 여러 지원 사이트의 URL을 섞어도 된다 — 각 URL이 자기 프리셋을 자동 선택한다.

각 런은 `ui_research/manifests/`에 다음을 쓴다:

- `collected_pages_<run_id>.json` — 페이지별 상태, robots 메모, 페이지 제목, 링크/에셋/갤러리 메타;
- `contact_sheet_<run_id>.html` — **브라우징 가능한** 시트: 받은 썸네일이 인라인 렌더되고, 추출/수집한
  모든 이미지가 제목/크기·출처 링크와 함께 나열된다. 브라우저로 열어 수집물을 검토하라.

> **사이트 현실 점검(겪어서 안다):** Game UI Database는 SPA + Cloudflare라 헤드리스 수집이
> 불안정하다 — `index.php?&scrn=N` 화면유형 필터가 직접 로드로는 적용되지 않고(모든 scrn이 같은
> 기본 갤러리), `gameData.php?id=N` per-game도 타임아웃될 수 있다. **interfaceingame.com per-game
> 페이지**(`/games/<slug>/`)가 가장 안정적(게임당 실제 스크린샷 30+장). 게임 id/슬러그는 사이트 내
> 검색(SPA)보다 웹 검색이 빠르다. 직계 장르(뱀서류 등)가 수집 사이트에 없으면 인접작 + 글 패턴으로 보강.

유용한 플래그: `--site`, `--mode`, `--gallery-class`, `--scroll`, `--max-pages`, `--delay`,
`--timeout`, `--user-agent`, `--keep-*`, `--download-full-images`, `--download-title-contains`, `--no-headless`.

## 지원 사이트

두 가지 추출 모드:

- **`gallery`** — 구조화: 갤러리 앵커(앵커 클래스 + `data-title`/`data-imageid`/`data-thumb`)를 읽는다.
  항목별 메타데이터가 풍부.
- **`images`** — 범용: 렌더된 페이지의 `<img>`/`srcset` 이미지를 수집(아이콘/아바타/로고 등 명백한
  크롬은 필터). 대부분 사이트에서 동작.

URL 도메인으로 모드/프리셋이 자동 감지되며 `--site`/`--mode`/`--gallery-class`로 재정의.

| 사이트 키 | 도메인 | 모드 | 비고 |
| --- | --- | --- | --- |
| `gameuidatabase` | gameuidatabase.com | gallery | Game UI Database — 구조화 갤러리(`--browser` 필요; SPA+CF 주의). |
| `interfaceingame` | interfaceingame.com | images | Interface In Game — 게임 UI 스크린샷(per-game 페이지 권장). |
| `screenlane` | screenlane.com | images | 모바일 UI/UX 플로우. |
| `collectui` | collectui.com | images | 데일리 UI. |
| `landbook` | land-book.com | images | 랜딩 페이지 갤러리. |
| `lapaninja` | lapa.ninja | images | 랜딩 페이지 예시. |
| `refero` | refero.design | images | 웹/iOS UI 영감. |
| `dribbble` | dribbble.com | images | 디자인 샷(공개 페이지). |
| `behance` | behance.net | images | 크리에이티브 쇼케이스(공개 페이지). |

프리셋이 없는 **다른** 사이트는 `images` 모드(범용 수집)로 기본 동작. 로그인이 필요한 갤러리는 미지원.

## 설정 탐색

`--config` 없이 CLI는 `ui_ref_config.json`을 다음에서 찾는다:

```text
ui_ref_config.json
ui_research/ui_ref_config.json
docs/ui_research/ui_ref_config.json
```

다른 위치에서 특정 프로젝트 폴더 대상으로 실행하려면 `--project-root` 사용.

## 에티켓

런은 작게·느리게(기본값 8s 딜레이, 런당 20페이지). 수집한 페이지는 인용/레퍼런스 컨텍스트로
취급 — 재배포 에셋 팩이나 학습 데이터가 아니다.

## 라이선스

MIT — [LICENSE](LICENSE) 참고.
