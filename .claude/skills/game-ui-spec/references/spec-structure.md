# Spec structure — document skeleton, per-screen anatomy, and the hard rules

The copy-paste blanks live in `../templates/spec-skeleton.md` and `../templates/per-screen.md`.
This file explains **what each part is for and the rules that make the spec implementable**.

The deliverable is an **annotated spec / redline** — a callout + legend + state + acceptance
**layer over the intended visual**. It is *not* a fresh fidelity level; it's an annotation
layer. Distinguish it from: wireframe (structure/hierarchy, low-fi) → mockup (visual, hi-fi)
→ prototype (interactive). This skill produces the annotated spec, built on a wireframe.

---

## Document skeleton (mandate this order)

The four non-negotiable wrappers (Kiess, *A Practical Guide to UX Specifications*): **Title,
Introduction, Annotated wireframes (the core), Version history.** Full order:

```
0. 표지 (Title)              문서명 / 기능 / 버전 / 날짜 / 작성자 / 상태(draft·review·approved)
1. 개요 및 목표               문제 / 측정가능 성공지표 / 포함·제외 범위
2. 사용자 및 맥락             페르소나 / 플랫폼·입력장치 / 진입 맥락 / 가정
3. 화면 흐름도 (wireflow)     화면=박스, 화살표=전이(이벤트 라벨), 분기=다이아몬드; 상태↔HUD 매핑
4. 글로벌 컴포넌트 인벤토리    재사용 컴포넌트 + variant + 토큰; 한 번 정의→화면별 코드 참조
5. 화면별 명세                per-screen 템플릿을 화면마다 (← 본문)
6. 공통 규칙                  내비 모델 / 글로벌 empty·loading·error / 접근성 글로벌
7. 미해결 질문                화면별 질문을 여기로 집계 (살아있는 섹션)
8. 버전 이력                  버전별 changelog
부록                         전체 흐름도 / references/ui 매니페스트 링크
```

Wireflow conventions (NN/g): explicit **entry trigger** + **success/error exits** on each
screen; label every arrow with the event/condition; tie each game state to HUD visibility
(combat-state → HUD shown / menu-state → HUD hidden).

---

## Per-screen anatomy (every screen gets all of this)

Order in `per-screen.md`: 목적 → 참조 → 와이어프레임 → 범례 → 상태 매트릭스 → 입력 패리티
→ 데이터 바인딩 → 내비게이션 → 엣지케이스 → 접근성 → **UX 설계 의도** → 미해결 질문.

### The legend table (annotation table)
Resolves every number in the SVG. Columns:
`# | 요소 | 위치 | 표시 조건 | 동작·상태 | 데이터 바인딩 | 동작 기준 | UX 의도 | 접근성`.
The **UX 의도** (a plain one-line reason, no framework names) and a measurable **동작 기준**
("…할 때 → …한다, 200ms 내") are required on every row.

### State matrix (per interactive element) — *the #1 spec gap is missing states*
`요소(코드) | default | hover | focus | pressed | selected | disabled/locked | loading | empty | error`.
For each non-default state give **exact microcopy + visual indicator (icon+color+text) +
recovery path**. **Never convey a state by color alone.** A spec missing empty/error/loading
is incomplete.

### Input parity table
`동작 | 마우스 | 키보드 | 패드 | 터치 | 스크린리더 안내`. Proves the screen is operable on
every input device — especially **gamepad focus** for a Steam/PC game.

### Data-binding table (event-driven, never polled)
`코드 | 데이터 필드 (GDD §) | 갱신 이벤트 (GDD §12-1/§4-3) | UI 제안 이벤트 (GDD 외) | 포맷 | 폴백`.
Bind each widget to a **named GDD event/dispatcher** (no frame polling). Keep **fields and
events in separate columns** — `level_reached` is a field, not an event. Any trigger the GDD
doesn't define goes in the **UI-proposed** column (flagged "§12-1 추가 필요"), never silently
in the canonical column. See hard rule #7.

---

## Hard rules (these make the spec traceable & testable)

1. **Immutable element codes.** Every annotated element gets a hierarchical code: UPPERCASE
   section letter + number + optional lowercase variant → `A1`, `D7`, `K4b`. Codes **never
   change**; a removed element's code is **retired permanently and never reused**; new
   elements **append at the end**. (UXMatters cascading specs.) The SVG badge carries the
   running number; the legend carries the immutable code.

2. **Given-When-Then acceptance criteria** on every element code AND every non-default
   state. Each criterion **atomic, independently yes/no testable, and measurable** — "결과는
   200ms 이내 로드", never "빠르게". (Parallel HQ / AltexSoft.)

3. **States are mandatory, not optional.** Force the full state matrix per interactive
   element. Missing empty/error/loading is the most common failure.

4. **Annotation marks use a distinct contrast color** so callouts are never mistaken for
   real UI (the kit uses blue `#5b8def` regions / `#1e3a8a` leaders; magenta is the
   canonical "documentation, not real UI" color).

5. **Inverted-pyramid information order:** critical real-time info most prominent → tactical
   → strategic (in menus) → meta settings deepest.

6. **Keep Open Questions live.** The spec is a talking-through artifact for devs, not a
   substitute for conversation.

7. **GDD vocabulary check (biggest reliability rule).** Every name in a data-binding
   trigger/field column MUST be **copy-verifiable to a GDD event table (e.g. §12-1) or
   field table (e.g. §12-2)**. Do NOT invent plausible handler names (`OnHealthChanged`,
   `XpGained`, …) and assert they're canonical — the model's strongest failure mode. Any
   UI-needed event/field the GDD lacks goes in a dedicated **"UI events/fields requiring
   GDD additions"** table as a tracked TDD-handoff item. Split the binding table into
   **field (GDD §) / event (GDD §) / UI-proposed (not in GDD)** columns, each carrying its
   section cite, so missing provenance is visible. Never write "bound to §12-1 events" when
   most names aren't in §12-1.

8. **Numeric values cite-or-flag.** Every numeric threshold or guarantee in a GWT/legend
   (a phase-split HP%, a latency budget, a "Rare ≥1" rule) either **cites the GDD line that
   fixes it** or is tagged **`[PLACEHOLDER — needs GDD confirmation]`**. Author-supplied
   numbers must never masquerade as design canon.

9. **GWT conditioned on state.** A GWT for an element whose behavior branches on game state
   (inventory full, first occurrence, co-op vs solo) MUST enumerate each branch — e.g.
   `Given 보유<6, Then 신규 1+강화 1 보장; Given 보유=6, Then 강화만`. A single unconditioned
   criterion that's only true in one branch is testably wrong in the others.

10. **No self-contradiction across sections.** The same element (keyed by its immutable
    code) must be described with **consistent position/behavior** across §1/§2/§3/§5/refs.
    If the wireframe geometry contradicts a prose convention claim (e.g. "timer top-center"
    while the clock is drawn top-left), fix one side — follow the GDD's explicit placement
    and **document the deviation explicitly** rather than asserting a convention you don't
    implement (see `screen-exemplars.md` deviation protocol).

## Sources
Kiess "A Practical Guide to UX Specifications"; NN/g wireflows; UXMatters cascading UX specs
(immutable codes, leader lines, legend); Stéphanie Walter (state matrix, a11y, interaction
parity); Material Design states; Parallel HQ / AltexSoft (Given-When-Then); Unreal
EventBasedUI / Unity UI Toolkit data-binding; UXPin / Balsamiq (artifact types).
