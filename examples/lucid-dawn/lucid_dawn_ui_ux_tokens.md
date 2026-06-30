# Lucid Dawn — Design Tokens (UI design system v0.1)

> Brings the wireframes/components of `lucid_dawn_ui_ux_spec.*.md` down to **implementable visual tokens**.
> Colors (hex) / type / spacing / radius / motion all map 1:1 to **Unity 6 UI Toolkit USS variables** (`--ld-*`).
> Shared across the EN / 中文 / 한글 spec versions. Status: draft; `[TBD]` = pending art lock.
> **Rule: color never carries meaning alone (P6)** — every color token ships with an icon/shape/position/label. Colorblind palette in §7.

## 1. Color — surfaces / text
| token | hex | use | contrast |
| --- | --- | --- | --- |
| `ld.color.bg.void` | `#0B0F1A` | base background (dream depth) | — |
| `ld.color.bg.surface` | `#0F1422` | panels / modals | — |
| `ld.color.bg.raised` | `#16203A` | cards / list items | — |
| `ld.color.bg.dim` | `#070A12` @55% | pause/modal dim | — |
| `ld.color.text.hi` | `#EAF0FB` | titles / emphasis | ≥12:1 on void |
| `ld.color.text.mid` | `#9FB3D6` | secondary | ≥4.5:1 |
| `ld.color.text.lo` | `#6B7796` | disabled/placeholder (not body) | ≥3:1 |
| `ld.color.line.subtle` / `.strong` | `#2C3A57` / `#3B4A6B` | dividers / frame |

## 2. Color — functional/resource (each a distinct hue, paired with icon+position)
| token | hex | meaning | shape/icon |
| --- | --- | --- | --- |
| `ld.color.lucid` | `#4AA6FF` | lucid accent (evade/counter/combo) — project energy-wave palette (0.29,0.65,1.0) | blue afterimage |
| `ld.color.hp` | `#FF5D6C` | HP | heart |
| `ld.color.shield` | `#8FD6FF` | shield | shield |
| `ld.color.dream` | `#FFC24A` | Dream Energy (ult resource) | star/spark |
| `ld.color.purge` | `#B58CFF` | Purify / seal | seal |
| `ld.color.xp` | `#6EA8FF` | XP (top strip — distinct by position) | (strip) |
| `ld.color.boss` | `#E5484D` | boss HP | skull/segments |
| `ld.color.dawn` | `#FFD37A` | alarm / time warning / Dawn ending | alarm clock |
| `ld.color.danger` | `#FF3B5C` | lethal hazard / enemy bullet | warning spike |
| `ld.color.success` | `#5BCF9E` | success / unlock / Dream Break | check/whiteout |

> HP (rose) vs Boss (crimson) are close in hue — separated by **position (top-left vs top-center) + size + icon** (P4/P6). Colorblind mode widens the hues (§7).

## 3. Color — rarity (C-CARD/C-NODE) · states
| rarity | token | hex | shape backup |
| --- | --- | --- | --- |
| Common | `ld.color.rarity.common` | `#C2C9D6` | 1px border, ○ corner |
| Uncommon | `ld.color.rarity.uncommon` | `#6BD968` | 2px border, ◇ corner |
| Rare | `ld.color.rarity.rare` | `#49A6FF` | 3px border, ◆ corner |
| Lucid | `ld.color.rarity.lucid` | `#FFD24A`→`#B58CFF` gradient | 3px + glow, ✦ corner |

| state | token | value | rule |
| --- | --- | --- | --- |
| focus | `ld.color.state.focus` | `#7AA2E8` | ring ≥3:1, 2.5px + slight scale |
| disabled | `ld.color.state.disabled` | text.lo @40% | + lock icon / reason text |
| error | `ld.color.state.error` | `#FF6B6B` | + "problem + fix" text |
| new/upgrade | `ld.color.state.new` | `ld.color.dawn` | "NEW"/"+" text badge |

## 4. Typography
| token | family (proposed) | note |
| --- | --- | --- |
| `ld.type.display` | `[TBD display font]` | logo / ending badge (license-check) |
| `ld.type.ui` | Latin: Inter/Segoe · KR: Pretendard/Malgun · CN: Noto Sans SC/思源黑体 | body/labels |
| `ld.type.num` | **tabular digits** (Roboto/JetBrains Mono) | timer/HP/damage — stop digit jitter |

Sizes (px): `timer 40 · h1 32 · h2 24 · body 16 · sub 14 · cap 12` (no smaller). Line-height 1.4 body / 1.2 heads. CJK `word-break:keep-all`. User text scale 80–150% (§9-3) multiplies the scale.

## 5. Spacing / radius / elevation
- `ld.space.1..7` = 4/8/12/16/24/32/48 · `ld.radius.sm/md/lg/pill` = 4/8/12/999 · `ld.elev.panel` = y2 blur8 #000@40% · `ld.elev.modal` = y8 blur24 #000@55% · `ld.safe.tv` = 5% edge safe.

## 6. Motion / timing (GDD-locked values cited; others proposed → tracker)
| token | value | source | use |
| --- | ---: | --- | --- |
| `ld.motion.instant` | 100ms | proposed (input budget) | button/input reaction |
| `ld.motion.quick` | 200ms | proposed (value-reflect budget) | bar fill / value update |
| `ld.motion.lucidStop` | 450ms | **GDD §4-3 (0.45s)** | lucid time-stop feel |
| `ld.motion.lucidICD` | 400ms | **GDD §4-3 (0.40s)** | lucid reward internal cd |
| `ld.motion.counter` | 700ms | **GDD §4-3 (0.7s)** | counter window (A12) |
| `ld.motion.combo` | 6000ms | **GDD §4-3 (6.0s)** | lucid combo hold (A6) |
| `ld.motion.bossWarn` | 5000ms | **GDD §4-1 (5s)** | boss warning |
| `ld.motion.groggy` | 4000ms | **GDD §7-1 (4.0s)** | boss groggy |
| `ld.motion.reward` | 8000ms | **GDD §7-1 (8s)** | boss reward protect (I4) |
| `ld.motion.alarm60` | 60000ms | **GDD §4-1** | final-60s warning |

> **Juice budget (P3):** cap simultaneous screenshake/flash so feedback never buries critical signal. All motion → 0/short under reduce-motion / shake / flash toggles (§9-3).

## 7. Accessibility — colorblind palette + contrast
| item | rule |
| --- | --- |
| body text contrast | ≥ 4.5:1 |
| large text / UI / focus ring | ≥ 3:1 + non-color marker |
| colorblind (deuter/prot/trit) | enemy bullet = `danger` + spike shape; ally = `lucid` + round; hazard zone = hatch pattern — **shape first** |
| state | color + (icon/shape + text) always |

## 8. Component tokens (spec §4 inventory → values)
| component | mapping |
| --- | --- |
| C-BAR | height 16–22px, `radius.sm`, per-type color (§2)+icon; danger = `color.hp`+blink(`motion.quick`)+border |
| C-CARD | `bg.raised`, `radius.lg`, rarity border/corner (§3), confirm = gem + i-frame (`motion.quick`) |
| C-RADIAL | radial fill `color.lucid`/`color.dream`, ready = 1 flash (`motion.instant`) + keycap glyph |
| C-NODE | locked = `state.disabled`+lock, available = `state.focus` border, owned = filled (rarity) |
| C-LIST/PANEL | `bg.surface`, hover = `bg.raised`, selected = `state.focus` border + check |
| C-PROMPT | auto input-device glyph (mouse/key/pad), `size.sub` |
| C-BADGE | ending/rarity/combo — color + **text label required** |

## 9. USS mapping (Unity 6 UI Toolkit)
```css
.ld-root { --ld-color-lucid:#4AA6FF; --ld-color-hp:#FF5D6C; --ld-color-dream:#FFC24A; --ld-color-purge:#B58CFF; --ld-color-boss:#E5484D; --ld-color-dawn:#FFD37A; --ld-space-3:12px; --ld-radius-lg:12px; --ld-type-size-timer:40px; }
.ld-bar-hp { background-color: var(--ld-color-hp); height:20px; border-radius: var(--ld-radius-sm); }
.ld-timer { font-size: var(--ld-type-size-timer); }
```
> UI Toolkit supports USS custom props (`--var`). Collect tokens in one `.uss`; components reference via `var()` → theme/colorblind swap = root class swap.

## 10. Open (art lock needed)
`[TBD]` display font + license (§13-3 #1) · HP/Boss colorblind final hues · Lucid rarity gradient · per-character theme color (Kohaku stable / Toko agile).
