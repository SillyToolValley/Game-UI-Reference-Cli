<!-- Legend + state matrix header rows. Copy under each screen's wireframe. -->

<!-- Legend (resolves every SVG number). UX 근거 & 수용 기준 required on every row. -->
| # | 코드 | 요소 | 위치 | 표시 조건 | 동작·상태 | 데이터 바인딩 | 동작 기준 | UX 의도 | 접근성 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

<!-- State matrix (per interactive element). 색만으로 의미 전달 금지. 해당 없으면 — -->
| 요소(코드) | default | hover/focus | pressed/active | selected | disabled/locked | loading | empty | error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

<!-- Input parity -->
| 동작 | 마우스 | 키보드 | 패드 | 터치 | 스크린리더 안내 |
| --- | --- | --- | --- | --- | --- |

<!-- Data binding (event-driven, no polling). Names must be copy-verifiable to the GDD.
     Split field vs event; invented UI events go in the last column, never asserted as canonical. -->
| 코드 | 데이터 필드 (GDD §) | 갱신 이벤트 (GDD §12-1/§4-3) | UI 제안 이벤트 (GDD 외 — 추가 필요) | 포맷 | 폴백 |
| --- | --- | --- | --- | --- | --- |

<!-- Conditioned GWT example (state-branching element):
     Given 보유<6, Then 신규 1+강화 1 보장; Given 보유=6, Then 강화만(신규 보장 해제). -->
<!-- UI events requiring GDD §12-1 additions (TDD handoff) -->
| 제안 이벤트 | 발생 조건 (어떤 필드/임계치) | 대체 표시(현행 GDD 이벤트) |
| --- | --- | --- |
