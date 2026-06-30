# {게임명} — 디자인 토큰 (UI 디자인 시스템) — TEMPLATE

> 와이어프레임/컴포넌트를 **구현 가능한 시각 토큰**으로 내리는 문서(Process 8). 색 hex·타이포·간격·반경·
> 모션을 엔진 변수로 매핑(UI Toolkit `--var` USS / Unreal Slate style / CSS custom props).
> **이 문서가 있어야 산출물이 "와이어프레임 디자인 문서"에서 "구현 가능한 디자인 시스템"으로 올라간다.**
> 규칙: 색은 단독으로 의미를 전달하지 않는다(항상 아이콘/모양/위치/글자 동반). 색약 대체 팔레트 필수.

## 0. 명명 규칙
`--<ns>-<범주>-<의미>[-<상태>]`. 범주: `color · type · space · radius · elev · motion · z · comp`.

## 1. 색 — 표면/텍스트
| 토큰 | hex | 용도 | 대비 |
| --- | --- | --- | --- |
| `color.bg.base` | `{#}` | 최하단 배경 | — |
| `color.bg.surface` | `{#}` | 패널/모달 | — |
| `color.bg.raised` | `{#}` | 카드/항목 | — |
| `color.text.hi` | `{#}` | 제목/강조 | ≥ 4.5:1 |
| `color.text.mid` | `{#}` | 보조 | ≥ 4.5:1 |
| `color.text.lo` | `{#}` | 비활성(본문 금지) | ≥ 3:1 |

## 2. 색 — 기능/자원 (서로 다른 hue로 고정, 위치+아이콘 동반)
| 토큰 | hex | 의미 | 동반 형태 |
| --- | --- | --- | --- |
| `color.accent` | `{#}` | 브랜드/핵심 액센트 | {아이콘} |
| `color.hp` / `color.resourceN` | `{#}` | 각 자원 | {아이콘} |
| `color.danger` | `{#}` | 위험/즉사 | 경고형 |
| `color.success` | `{#}` | 성공/해금 | 체크 |
> 게임별 자원(체력/자원/진행도/적 위협)마다 **다른 색상**을 배정. hue가 가까운 둘은 위치/크기/아이콘으로 분리.

## 3. 색 — 등급/상태
| 등급/상태 | 토큰 | hex | 형태 백업 |
| --- | --- | --- | --- |
| {common…} | `color.rarity.*` | `{#}` | 테두리/꼭지 모양 |
| focus | `color.state.focus` | `{#}` | 링 ≥3:1 + 확대 |
| disabled | `color.state.disabled` | `{#}` | 자물쇠+사유 |
| error | `color.state.error` | `{#}` | 문제+해결 글자 |

## 4. 타이포
| 토큰 | 패밀리 | 비고 |
| --- | --- | --- |
| `type.display` | `{확정 필요}` | 표제(라이선스 확인) |
| `type.ui` | Latin: {…} · KR/CJK: {Pretendard/Malgun…} | 본문/라벨 |
| `type.num` | **탭ular 숫자**({mono}) | 타이머/HP/데미지 자릿수 흔들림 방지 |

스케일(px): `{key}` 40/32/24/16/14/12 … 줄높이 1.4(본문)/1.2(제목). CJK `word-break:keep-all`. 사용자 텍스트 배율 80~150%.

## 5. 간격/반경/고도/모션
- `space.1..7` = 4/8/12/16/24/32/48 · `radius.sm/md/lg/pill` = 4/8/12/999 · `elev.*` = 그림자.
- **모션 토큰은 GDD 타이밍을 인용**(예: 시간정지 0.45s, 보호 8s…). 추정 모션값은 트래커(`decisions-tracker.md`)에 등록. `reduce-motion`/흔들림·플래시 토글에서 0/축약.

## 6. 접근성 팔레트
색약(deuter/prot/trit) 대체 hue + 형태 1차 구분. 텍스트 ≥4.5:1, UI/포커스 ≥3:1 + 색 외 표식.

## 7. 컴포넌트 토큰
디자인 문서 §4 인벤토리의 각 컴포넌트(C-BAR/C-CARD/…)를 실제 값(높이/색/반경/모션)으로 매핑.

## 8. 엔진 매핑 예 (UI Toolkit USS)
```css
.{ns}-root { --{ns}-color-accent: {#}; --{ns}-space-3: 12px; --{ns}-radius-lg: 12px; }
.{ns}-bar-hp { background-color: var(--{ns}-color-hp); }
```
> 토큰을 한 `.uss`/스타일 에셋에 모으고 컴포넌트가 `var()`로 참조 → 테마/색약 팔레트는 루트 클래스 스왑.

## 9. 미해결(아트 확정 필요)
{디스플레이 폰트/색약 최종값/캐릭터 테마색 …}
