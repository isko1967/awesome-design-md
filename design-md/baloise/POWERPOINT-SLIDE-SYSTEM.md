# PowerPoint-Slide-System auf Basis des Baloise/Helvetia Design System

Übersetzung der Web-Tokens aus [`DESIGN.md`](./DESIGN.md) in ein pragmatisches
Foliensystem — plus die Vorgehensplanung für **Block 1 (Slides 7–14, Few-shot &
negative examples)**.

---

## Teil A — Warum das Mapping sauber aufgeht

PowerPoint rechnet in Punkt (1 Zoll = 72 pt). Eine 16:9-Folie im Standardformat
**13.333" × 7.5"** ist exakt **960 pt × 540 pt**.

Das Design System rastert auf **8 px**. Setzt man **1 pt = 1 px**, liegt das
komplette DS-Raster ohne Umrechnungsfehler auf der Folie:

| DS (Web) | Folie (PowerPoint) |
|---|---|
| 8 px Basisraster | 8 pt Basisraster |
| 12-Spalten-Grid | 12-Spalten-Grid |
| H1 = 40 px | Titel = 40 pt |
| Body = 16 px | Fliesstext = 16 pt |
| Radius large = 12 px | Kartenradius = 12 pt |

Das ist der eigentliche Gewinn: **kein eigenes Foliendesign erfinden**, sondern die
bestehenden Tokens 1:1 übernehmen. Die Grössen liegen zufällig genau im Bereich, den
Präsentationsdesign ohnehin fordert (Titel 36–44 pt, Body ≥ 14 pt).

---

## Teil B — Das Folienraster

```
960 pt breit × 540 pt hoch   (13.333" × 7.5", 16:9)

Aussenrand links/rechts : 64 pt
Inhaltsbreite           : 832 pt
Spalten                 : 12 × 40 pt
Rinne (Gutter)          : 32 pt
                          12×40 + 11×32 = 832  ✓
```

**Spaltenpositionen (x in pt):** Spalte *n* beginnt bei `64 + (n-1)·72`

| Aufteilung | Links | Rechts |
|---|---|---|
| 6 / 6 | x 64, w 400 | x 496, w 400 |
| 7 / 5 | x 64, w 472 | x 568, w 328 |
| 5 / 7 | x 64, w 328 | x 424, w 472 |
| 4 / 4 / 4 | x 64 / 352 / 640, w 256 |

**Vertikale Zonen (y in pt):**

| Zone | y | Höhe | Inhalt |
|---|---|---|---|
| Eyebrow | 40 | 20 | `LEARN` / `SEE` / `TRY` / `IMPROVE`, 14 pt Bold, Versalien, +1.5 Laufweite |
| Titel (Action Title) | 68 | 56 | 40 pt Bold, 1 Zeile |
| Lead | 132 | 32 | 20 pt Regular |
| **Inhalt** | **196** | **216** (mit Band) / **304** (ohne) | Karten, Spalten |
| Kernaussage-Band | 444 | 56 | volle Breite, getönte Fläche |
| Fusszeile | 508 | 16 | Blocklabel · Foliennummer, 12 pt `#747474` |

Abstände folgen den DS-Regeln: **Karte↔Karte 32 pt**, **innerhalb Karte 24 pt**,
**Heading→Inhalt 16 pt**, innere Untersektionen 8 pt.

---

## Teil C — Farb- und Typoregeln für Folien

### Farbe

| Rolle | HEX | Einsatz |
|---|---|---|
| Core Blue | `#000D6E` | Titel, Fliesstext, Icons, Divider-Fläche |
| Weiss | `#FFFFFF` | Default-Folienhintergrund, Text auf Blau |
| Grey 1 | `#F6F6F6` | neutrale Karte |
| Grey 5 | `#747474` | Fusszeile, Metatext |
| Primary Lighter | `#E5E7F0` | Kernaussage-Band, Hervorhebung |
| Sky Lighter | `#E5F1FE` | Akzentfläche Block 1 |
| Green Lighter / Green Dark | `#E9FBF7` / `#1B5951` | Positivbeispiel |
| Red Lighter / Red Dark | `#FFEEF1` / `#99172D` | Negativbeispiel |

**Drei Regeln, die aus dem DS kommen und hier wirklich greifen:**

1. **Kein Farbcoding.** Die vier Phasen `LEARN → SEE → TRY → IMPROVE` werden **nicht**
   über Farbe unterschieden, sondern über das Eyebrow-Label und einen Schrittindikator.
   Farbe markiert stattdessen den **Block** (= die Prompting-Technik). Genau das macht
   das Layout wiederverwendbar: Block 2 bekommt `Purple Lighter`, Block 3 `Yellow
   Lighter` usw. — gleiche Struktur, anderer Tint.
2. **Gleiches Farbspektrum je Element.** Eine grüne Karte trägt grüne Überschrift
   (`#1B5951` auf `#E9FBF7`), nie eine blaue.
3. **Positiv/Negativ über Brand-Grün/-Rot, nicht über Success/Danger.** Die Alert-Farben
   sind laut DS ausschliesslich für Zustände reserviert. Für "gutes Beispiel / schlechtes
   Beispiel" ist Brand Green/Red korrekt — und optisch ruhiger.

### Typografie

| Element | Grösse | Gewicht | Familie |
|---|---|---|---|
| Divider-Titel | 48 pt | Bold | Headline |
| Action Title | 40 pt | Bold | Headline |
| Statement / Frage | 32 pt | Light | Headline |
| Kartentitel | 24 pt | Bold | Headline |
| Sub-Header | 20 pt | Bold | Headline |
| Lead | 20 pt | Regular | Text |
| Fliesstext | 16 pt | Regular | Text |
| Beispieltext in Karten | 14 pt | Regular | Text |
| Eyebrow / Label | 14 pt | Bold, Versalien | Headline |
| Fusszeile / Quelle | 12 pt | Regular | Text |

**Schrift-Handling:** `BaloiseCreateHeadline` / `BaloiseCreateText` liegen im Repo nur
als `.woff/.woff2` — PowerPoint kann das nicht lesen. Vorgehen: die Schriftnamen trotzdem
setzen (auf Firmengeräten mit installierten Corporate Fonts rendert es korrekt), aber
**das Layout gegen Arial-Metriken absichern** — Arial ist der vom DS selbst definierte
Fallback. Alle Textboxen bekommen Reserve, damit nichts umbricht.

---

## Teil D — Was aus think-cell / Beratungspraxis übernommen wird

Das DS regelt *Look*. Es regelt nicht, wie eine Folie **argumentiert**. Dafür kommen
vier Prinzipien dazu:

1. **Action Titles.** Der Titel ist eine Aussage, kein Thema. think-cell formuliert es
   so: eine Folie = eine Idee, und diese Idee steht im Titel; alles auf der Folie stützt
   den Titel. → Konsequenz für Block 1: `WHAT` / `HOW` sind **Themen**, keine Aussagen.
   Sie wandern ins kleine Eyebrow-Label, der Aussagesatz wird zum H1.

2. **Horizontal Logic.** Liest man nur die Titel von 7 bis 14, muss die Geschichte
   stehen. Test für Block 1:

   > Show the model what good looks like. → Few-shot prompting gives the model examples
   > to learn from. → Negative examples show the model what to avoid. → Tell the model
   > what to learn from each example. → Can examples make a vague instruction more
   > precise? → Same task. Clearer guidance. → Use examples to guide your own output. →
   > Did the examples give you more control?

   Das trägt. Die Titelkette bleibt unverändert.

3. **Vertical Logic.** Jede Folie muss beweisen, was ihr Titel behauptet. Deshalb die
   feste **Kernaussage-Band**-Komponente unten: sie ist der "so what" und wiederholt
   sich auf jeder LEARN-Folie. Sie ist gleichzeitig das durchgehende visuelle Motiv.

4. **Vergleichslogik statt Dekoration** (Zelazny). Wo verglichen wird, bestimmt die
   Vergleichsart die Form: Positiv/Negativ (Slide 9) und Ohne/Mit (Slide 12) sind
   *Item Comparisons* → zwei gleich breite Spalten, identische innere Struktur, nur
   der Tint unterscheidet. Keine Pfeile, keine Diagramme — hier gibt es keine Daten.

**Bewusst nicht übernommen:** die Dekorationsempfehlungen aus generischen Slide-Guides
(Farbverläufe, Schatten, Akzentlinien unter Titeln, wechselnde Layouts pro Folie). Das
DS ist flächig und ruhig; Wiederholung ist hier ein Feature, kein Mangel — die Teilnehmenden
sollen die Struktur nach zwei Folien kennen.

---

## Teil E — Die sechs Folien-Archetypen

Bewusst **sechs**, nicht acht: Wiederverwendbarkeit über die weiteren Prompting-Blöcke
ist das Ziel. Jeder Archetyp wird als parametrisierte Layout-Funktion gebaut.

| # | Archetyp | Für Slide | Aufbau |
|---|---|---|---|
| **A** | **Divider** | 7 | Vollfläche `#000D6E`, Blocknummer `01` gross, Titel 48 pt Weiss, Subline, darunter der Zyklus `LEARN → SEE → TRY → IMPROVE` als Pill-Reihe |
| **B** | **Concept** | 8, 9, 10 | Eyebrow + Action Title + Lead, 7/5-Spalten: links Erklärung/Liste, rechts Beispielkarte(n) oder Aside, unten Kernaussage-Band |
| **C** | **Demo Setup** | 11 | Frage als Titel, Szenario-Karte, Ausgangsprompt als Code-Karte, 2 Tiles "Version 2 adds", rechts Checkliste "Watch for" |
| **D** | **Before / After** | 12 | Zwei 6/6-Spalten identischer Struktur: links neutral `#F6F6F6`, rechts akzentuiert; unten Band "What changed?" |
| **E** | **Practice** | 13 | 5 nummerierte Schritte im 4/4/4-Raster (3+2), Zeit-Badge als Pill, Disclaimer in der Fusszeile |
| **F** | **Reflection** | 14 | Frage 32 pt Light, 5 Antwortoptionen als Chips, Handlungsaufforderung "In the chat" |

Archetyp **B** trägt drei Folien und bekommt drei Ausprägungen:
- **B1 (Slide 8)** — Liste links, Beispiel-Gegenüberstellung rechts, Aside "Related concept"
- **B2 (Slide 9)** — zwei Kontrastkarten (Green/Red), darunter Synthese "Together"
- **B3 (Slide 10)** — Prompt-Template als hohe Code-Karte rechts, "Use when"-Band unten

---

## Teil F — Inhaltsbudget (der kritische Punkt)

Bei 16 pt Fliesstext und 24 pt Zeilenabstand fasst eine 400 pt breite Spalte
**ca. 55 Zeichen pro Zeile und 9 Zeilen** — zwei Spalten also grob **1'000 Zeichen**
Fliesstext plus Struktur.

Gemessen am gelieferten Text ist das für **Slide 8, 10 und 13** knapp. Vorschlag, in
dieser Reihenfolge:

1. **Aside-Spalte nutzen** — "Related concept" (8) und "Use when" (10) sind Randnotizen,
   nicht Hauptinhalt. Sie gehören in die schmale 5er-Spalte bzw. ins Band, bei 14 pt.
2. **Beispieltexte auf 14 pt** setzen — sie werden gezeigt, nicht vorgelesen.
3. Erst wenn beides nicht reicht: **Slide 13 splitten** (Schritte 1–3 / 4–5 + Zeitbadge).

Ich würde Slide 13 zunächst **nicht** splitten — fünf Schritte im 4/4/4-Raster
(3 oben, 2 unten) passen, wenn die Beispiel-Aufzählung unter Schritt 1 auf eine
Zeile zusammengezogen wird.

**Eine inhaltliche Anmerkung:** Der Disclaimer auf Slide 13 ("Keep all information
generic. Do not enter personal, customer or confidential information.") ist im
Versicherungskontext der wichtigste Satz der Folie. Er sollte nicht als 12-pt-Fusszeile
untergehen, sondern als eigene Warning-Fläche (`#FFF9E8` / `#7D4A0D`) direkt neben dem
Zeit-Badge stehen. Das ist der eine Ort, an dem eine Alert-Farbe DS-konform ist.

---

## Teil G — Vorgehen

### Schritt 1 — Theme- und Layout-Layer (der wiederverwendbare Teil)

```
slides/
  theme.js        Tokens: Farben, Type-Skala, Grid-Konstanten, Helpers
  layouts.js      Archetypen A–F als Funktionen (slide, data) => void
  components.js   Karte, Kernaussage-Band, Chip/Pill, Code-Karte, Eyebrow, Fusszeile
  content/
    block-01.js   Slides 7–14 als reine Daten
  build.js        pptxgenjs, 13.333"×7.5"
```

Technik: **pptxgenjs** (Node) über die vorhandene `pptx`-Skill. Der harte Schnitt
zwischen `content/` und `layouts.js` ist der Punkt, an dem sich die Arbeit für die
weiteren Blöcke auszahlt: Block 2 ist dann eine neue Datendatei plus ein Tint.

### Schritt 2 — Pilotfolie zuerst

Nicht alle acht Folien auf einmal. Zuerst **Slide 12 (Before/After)** bauen —
sie ist am dichtesten am Kern der Botschaft, nutzt Archetyp D und beweist Raster,
Typo und Farbregeln in einem Durchgang. Danach Slide 7 (Divider, Archetyp A), weil
er die Blockfarbe und den Zyklus etabliert.

Freigabe durch dich nach diesen zwei Folien — dann erst der Rest.

### Schritt 3 — Rest in Archetyp-Reihenfolge

B (8 → 9 → 10), dann C (11), E (13), F (14). Innerhalb eines Archetyps ist die
zweite Folie schnell.

### Schritt 4 — QA

- `markitdown output.pptx` → Textvollständigkeit, Tippfehler, Reihenfolge
- Rendern nach PNG → visuelle Prüfung auf Überlauf, Kollisionen, ungleiche Abstände
- **Arial-Test:** einmal ohne installierte Corporate Fonts rendern — das ist der
  realistische Worst Case
- Kontrastprüfung der Textfarben auf allen getönten Flächen gegen WCAG AA

### Schritt 5 — Übertragung auf die weiteren Blöcke

Ergebnis am Ende von Block 1: ein Layoutsystem, bei dem ein weiterer Block nur noch
**eine Datendatei + eine Blockfarbe** braucht. Die Farbreihenfolge für die Folgeblöcke
steht dann fest (Sky → Purple → Yellow → Green → Red), alle aus der DS-Primary-Palette,
alle gleichwertig — genau wie es das Design System verlangt.

---

## Offene Punkte

1. **Marke:** Baloise oder Helvetia? Das Repo ist mitten in der Umbenennung. Das
   betrifft Logo, Fusszeile und ggf. den Blauton.
2. **Corporate-Template:** Gibt es eine verbindliche `.potx`? Dann wird darauf
   aufgebaut statt from scratch — das ändert Schritt 1 erheblich.
3. **Sprache:** Der Inhalt ist Englisch, die Zielgruppe vermutlich gemischt.
   Folien Englisch belassen?
