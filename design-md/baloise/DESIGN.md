# Design System: Baloise / Helvetia

> Extrahiert aus dem öffentlichen Repository [`baloise/design-system`](https://github.com/baloise/design-system)
> (Design-Tokens: `packages/tokens/tokens/Base.tokens.json`, Foundation-Doku:
> `apps/storybook/src/foundation/*.mdx`, Docs-Site: https://design.baloise.dev).
>
> **Hinweis zur Marke:** Das Repository befindet sich in der Umbenennung von
> "Baloise Design System" zu **"Helvetia Design System"** (Zusammenschluss Baloise/Helvetia).
> Die Foundation-Texte sprechen bereits durchgängig von Helvetia, die Tokens und
> die Schriftfamilie tragen weiterhin die Baloise-Namen (`Primary = #000D6E`,
> `BaloiseCreateHeadline` / `BaloiseCreateText`). Vor externer Verwendung ist zu
> klären, welches Corporate Design verbindlich ist.

---

## 1. Gestaltungspersönlichkeit (Visual Theme & Atmosphere)

Die Persönlichkeit ist **sachlich-klar, geometrisch, ruhig und zugänglich** — nicht
verspielt, nicht dekorativ, nicht "tech-futuristisch". Das System beschreibt sich selbst
über vier Kernprinzipien: *Accessibility (WCAG 2.2 AA), Simplicity (HTML → CSS → JS),
Responsiveness, Standards Compliance*.

Der visuelle Anker ist **ein einziges, tiefes Blau** (`#000D6E`). Es trägt Logo, Fliesstext,
Überschriften, Buttons und Links. Alles andere ist Fläche: viel Weiss, dazu ein Set sehr
heller Tints als Hintergrundflächen. Farbe wird als *Atmosphäre* eingesetzt, nicht als
Bedeutungsträger — das System sagt ausdrücklich: **"There is no color coding within the
Helvetia appearance. All primary colors are equal and should be used as such."**

Die Hausschrift **Baloise Create** hat einen "solid geometric character" mit grosser
x-Höhe: elementare Formen, geringe Strichkontraste, nahezu perfekte Kreise. Die Headline-
Familie lebt von reiner Geometrie, die Text-Familie von Lesbarkeit in kleinen Graden.

**Kerncharakteristika:**
- Ein dominantes Blau `#000D6E` — Text, Titel, Icons, Interaktion
- Weiss als Default-Hintergrund; Farbflächen nur als sehr helle Tints (Tint 1/2)
- Kein Farbcoding — Farben tragen keine Bedeutung, sondern Rhythmus
- Farbkombinationen bleiben **im selben Farbspektrum** (Grün mit Grün-Light, nie Grün mit Lila)
- Geometrische Grotesk mit grosser x-Höhe, nur drei Gewichte (Light 300 / Regular 400 / Bold 700)
- 8pt-Raster über alle Viewports, 12-Spalten-Grid
- Radius als Vielfaches von 4; Schatten sparsam und flach
- Kontrast konsequent nach WCAG 2.2 AA

---

## 2. Farbpalette & Rollen

### Core / Primary

| Rolle | Token | HEX |
|---|---|---|
| **Core Blue** (Logo, Text, Buttons, Links) | `Primary.5` / `Surface.Primary` | `#000D6E` |
| Primary Hover | `Sky.5` | `#0014AA` |
| Primary Active / Dark | `Primary.6` | `#000739` |
| Primary Dark | `Primary.4` | `#293485` |
| Primary Light (Text auf Weiss, gedämpft) | `Primary.3` | `#656EA8` |
| Primary Lighter (Fläche, Highlight) | `Primary.1` | `#E5E7F0` |
| Selected | `Primary.1B` | `#CCCFE2` |

### Primary Colors (Brand-Akzente, gleichwertig, kein Coding)

Jede Familie hat Tints 1–6. Für Flächen gelten Tint 1/2, für Text auf diesen Flächen Tint 6.

| Familie | 1 (Lighter) | 2 (Light) | 3 (Base) | 4 | 5 | 6 (Dark) |
|---|---|---|---|---|---|---|
| **Sky** | `#E5F1FE` | `#A7D1FA` | `#56A7F5` | `#6672CC` | `#0014AA` | `#000A55` |
| **Green** | `#E9FBF7` | `#CBF2EC` | `#94E3D4` | `#21D9AC` | `#00B28F` | `#1B5951` |
| **Purple** | `#F9F3FF` | `#E1D9FF` | `#B8B2FF` | `#BE82FA` | `#9F52CC` | `#6C2273` |
| **Red** | `#FFEEF1` | `#FFD7D7` | `#FFACA6` | `#FF596F` | `#D9304C` | `#99172D` |
| **Yellow** | `#FFF9E8` | `#FFECBC` | `#FAE052` | `#FFBE19` | `#FA9319` | `#B24A00` |

### Neutrals

| Token | HEX | Verwendung |
|---|---|---|
| `White` | `#FFFFFF` | Default-Hintergrund |
| `Grey.0` | `#FAFAFA` | Hover-Fläche |
| `Grey.1` | `#F6F6F6` | Sehr helle Sektionsfläche |
| `Grey.2` | `#E8E8E8` | Disabled-Fläche, feine Trenner |
| `Grey.3` | `#D0D0D0` | Rahmen |
| `Grey.4` | `#B6B6B6` | Rahmen, kräftiger |
| `Grey.5` | `#747474` | Sekundärtext (`text-grey`) |
| `Grey.6` | `#313131` | Disabled-Text |

### Funktions- / Alert-Farben (nur für Zustände)

| Rolle | Fläche (Tint 1) | Text/Icon (Tint 5) |
|---|---|---|
| **Info** | `#E8F1FB` | `#155BA3` |
| **Success** | `#E8F3EC` | `#116B34` |
| **Warning** | `#FFF9E8` | `#7D4A0D` |
| **Danger** | `#FCE8E6` | `#CB1501` |

> Wichtig: Alert-Farben sind ausdrücklich *"a functional extension … meant to be used only
> for specific cases and situations"*. Für inhaltliche Gegenüberstellungen (gut/schlecht)
> gehören die **Brand**-Familien Green/Red, nicht Success/Danger.

### Textfarben

| Rolle | HEX |
|---|---|
| Primary (Default) | `#000D6E` |
| Inverted (auf dunkler Fläche) | `#FFFFFF` |
| Grey (sekundär) | `#747474` |
| Hint / Placeholder | `#656EA8` |

### On-Color-Regel

Das System definiert zu jeder Fläche eine `On*`-Textfarbe. Faustregel:
**Tint 1–3 → Text `#000D6E`. Tint 4–6 → Text `#FFFFFF`.**

---

## 3. Typografie

### Schriftfamilien

- **Headline:** `BaloiseCreateHeadline`, Fallback `Arial, sans-serif` — Titel, Bold-Leads
- **Text:** `BaloiseCreateText`, Fallback `Arial, sans-serif` — Fliesstext, UI
- Gewichte: **Light 300**, **Regular 400**, **Bold 700**
- Line-Height: Headings `1.3`, Text `1.5`, Single `1`, Double `2`

> Die Fontdateien liegen im Repo nur als `.woff`/`.woff2` (`packages/assets/src/fonts/`) —
> also nur für Web. Für Office-Dokumente ist **Arial der vom System selbst definierte
> Fallback**.

### Type Sets (Desktop / Tablet, Mobile abweichend)

| Rolle | Familie | Size (Desktop) | Line-Height | Weight |
|---|---|---|---|---|
| Display | Headline | 5rem / 80px | 6rem | 700 & 300 |
| Display 2 | Headline | 3rem / 48px | 3.5rem | 700 & 300 |
| H1 | Headline | 2.5rem / 40px | 3rem | 700 & 300 |
| H2 | Headline | 2rem / 32px | 2.5rem | 700 & 300 |
| H3 | Headline | 1.5rem / 24px | 2rem | 700 |
| H4 | Headline | 1.25rem / 20px | 2rem | 700 |
| H5 | Headline | 1rem / 16px | 1.5rem | 700 |
| Label | Headline | 0.875rem / 14px | 1.125rem | 700 |
| Body Large | Text | 1.25rem / 20px | 2rem | 400 / 700 |
| Body Medium | Text | 1.125rem / 18px | 1.625rem | 400 / 700 |
| Body Normal | Text | 1rem / 16px | 1.5rem | 400 / 700 |
| Body Small | Text | 0.875rem / 14px | 1.125rem | 400 / 700 |

Mobile-Stufen (relevant, wenn eng gesetzt wird): Display 48, Display 2 32, H1 28, H2 24,
H3 20, H4 18, H5 16.

Verfügbare Font-Sizes als Tokens: 12, 14, 16, 18, 20, 24, 28, 32, 40, 48, 80, 176 px.

---

## 4. Raster & Spacing

### Grid

- **12 Spalten**, vollständig responsiv
- **8pt-Basisraster** über alle Viewports (Ausnahme: 4pt für Kleinstelemente wie Icons)
- Begründung im System: die verbreitetsten Auflösungen sind auf mindestens einer Achse durch 8 teilbar

### Breakpoints

| Breakpoint | min-width |
|---|---|
| Mobile | 0px |
| Tablet | 769px |
| Desktop | 1024px |
| High-Definition | 1280px |
| Widescreen | 1440px |
| FullHD | 1920px |

### Container

| Container | max-width | Verwendung |
|---|---|---|
| default | 1496px | Standard |
| compact | 896px | Formulare, Funnels |
| fluid | 100% | Grossflächige Anwendungen |

### Spacing-Skala (px)

`0 · 1 · 2 · 4 · 8 · 12 · 14 · 16 · 20 · 24 · 32 · 40 · 48 · 56 · 64 · 72 · 96 · 128`

### Spacing-Regeln (aus der Foundation-Doku)

- **Heading → Inhalt:** 16px oder 8px
- **Sektion → Sektion:** 128px; bei inhaltlich zusammenhängenden Sektionen 64px
- **Karte → Karte:** 32px
- **Innerhalb einer Karte:** innere Sektionen 8px, Sektionen 24px

---

## 5. Border, Radius, Elevation

### Border
- Einheitliche Breite: **2px**
- Horizontale/vertikale Linien: `radius-rounded` an den Enden

### Radius (Vielfache von 4)

| Token | Wert | Verwendung |
|---|---|---|
| `none` | 0 | — |
| `normal` | 4px | Form-Controls, Buttons, Shapes |
| `md` | 6px | — |
| `large` | 12px | Karten, Notification, Sheet, Modal, Toast, Snackbar |
| `rounded` | 9999px | Pills, Linienenden |

### Elevation

| Token | Wert |
|---|---|
| `shadow` (Default: Karten, Snackbar, Toast) | `0 2px 5px 1px rgba(0,7,57,0.12)` |
| `shadow-2` | `0 4px 4px 0 rgba(0,7,57,0.15)` |
| `shadow-3` | `0 0 10px 0 rgba(0,7,57,0.15)` |
| `shadow-elevated` (nur Hover) | `0 0 30px 0 rgba(0,7,57,0.15)` |
| Text-Shadow | Nur bei Text über Bildern (Stage-Komponente) |

Opacity-Stufen: `0 · 0.3 · 0.4 · 0.5 · 0.6 · 0.8 · 1`

---

## 6. Iconografie & Brand Assets

- **~82 UI-Icons** in `packages/assets/src/icons/svg/` — Streamline "Core Solid Pro",
  klar, minimal, konsistent; in Primary `#000D6E` oder invertiert Weiss
- **Brand Icons** separat unter `packages/assets/src/brand-icons/`
- **Logo:** nur in Blau (positiv) oder Weiss (negativ) — keine weiteren Farbvarianten
- **Shapes:** Ausdruck des Logos, auf digitalen Touchpoints animiert; 6 Favicon-Farben,
  Blau ist Default

---

## 7. Verbindliche Gestaltungsregeln (Zitatnah)

1. **Kein Farbcoding.** *"There is no color coding within the Helvetia appearance.
   All Helvetia primary colors are equal and should be used as such."*
2. **Gleiches Farbspektrum je Element.** *"In a specific component, the same color spectrum
   must be applied. For example, if a green icon is used, a green background is required."*
3. **Icons brauchen Tint 1 oder Weiss als Hintergrund**, um den Kontrast zu sichern.
4. **Weiss ist der Default-Hintergrund**; andere Flächen nur, wenn der Kontext es zulässt.
5. **Blau ist auf jeder Seite präsent** — Logo, Text, Buttons, Links.
6. **WCAG 2.2 AA** ist gesetzt, nicht optional.

---

## 8. Quellen

| Thema | Pfad im Repo |
|---|---|
| Tokens (Single Source of Truth) | `packages/tokens/tokens/Base.tokens.json` |
| Farben | `apps/storybook/src/foundation/color.mdx` |
| Typografie | `apps/storybook/src/foundation/typography.mdx` |
| Grid & Breakpoints | `apps/storybook/src/foundation/grid.mdx` |
| Spacing | `apps/storybook/src/foundation/spacing.mdx` |
| Border & Radius | `apps/storybook/src/foundation/border-radius.mdx` |
| Elevation | `apps/storybook/src/foundation/elevation.mdx` |
| Iconografie | `apps/storybook/src/foundation/Iconography.mdx` |
| Brand Assets | `apps/storybook/src/foundation/brand-assets.mdx` |
| Fonts | `packages/assets/src/fonts/` (woff/woff2) |
| Icons | `packages/assets/src/icons/svg/` (82 SVG) |

Lizenz des Repositories: Apache-2.0. Schriften und Logos sind Corporate-Assets —
Verwendung nur im Unternehmenskontext, keine Weiterverbreitung.
