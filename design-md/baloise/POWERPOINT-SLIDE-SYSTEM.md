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

---

## Nachtrag — Entscheide vom 09.09.2026

**Marke:** Baloise (Status quo). **Sprache:** Englisch, Text unverändert.
**Vorlage:** Eine offizielle Corporate-`.potx` wird geliefert und ist die **primäre**
Quelle für die visuelle Sprache (Schriften, Farben, Typografie, Spacing, Formen,
Layoutkonventionen). Die Extraktion in `DESIGN.md` bleibt die Referenz für alles, was
die Vorlage offen lässt — sie ersetzt sie nicht.

### Geänderter Auftrag

Nicht das ganze Deck, sondern **zuerst 5 repräsentative Musterfolien** zur Abnahme.
Inhalt und didaktische Struktur bleiben unverändert — dieser Schritt ist reine
visuelle Übersetzung ins Corporate Design.

Prioritäten (in dieser Reihenfolge):
1. Corporate-Design-Konsistenz
2. Klare visuelle Hierarchie und Lesbarkeit
3. Einfache, robuste PowerPoint-Layouts
4. Kein Textüberlauf, keine Überlappungen, keine zu kleinen Schriften
5. Keine überflüssige Dekoration, kein Over-Engineering

Bestehende Corporate-Layouts werden genutzt, wo sie natürlich passen. Inhalt wird
**nicht** in unpassende Layouts gezwängt — dort entstehen einfache eigene
Kompositionen aus dem Design System.

### Vorschlag für die 5 Musterfolien

Ausgewählt nach Archetyp-Abdeckung, damit die Abnahme verallgemeinerbar ist:

| Slide | Archetyp | Warum in der Auswahl |
|---|---|---|
| **7** | Divider | Wiederholt sich in jedem Block; etabliert Blockfarbe und Zyklus |
| **10** | Concept (B3) | Textdichteste LEARN-Folie; enthält die Prompt-Template-Karte, die jeder Block braucht |
| **12** | Before/After | Grösstes Überlaufrisiko; zwei Spalten identischer Struktur |
| **13** | Practice | Nummeriertes Raster + Zeit-Badge + die Disclaimer-Entscheidung |
| **14** | Reflection | Das ruhige Ende der Bandbreite; Chips-Komponente |

Nicht in der Auswahl: 8 und 9 (Varianten von 10, leichter), 11 (strukturell nah an 10).

### Vorbereitet, unabhängig von der Vorlage

- `slides/inspect_template.py` — inventarisiert die `.potx`: Foliengrösse, Theme-Fonts,
  Farbschema, alle Master und Layouts mit Platzhalter-Geometrie in Punkt.
  Aufruf: `python3 inspect_template.py corporate.potx --slides`
- `slides/content/block-01.json` — der gesamte Inhalt der Slides 7–14 strukturiert und
  wortgleich, layoutunabhängig. Enthält für jede Folie Archetyp, Phase, Eyebrow,
  Action Title und die inhaltlichen Blöcke.
- Toolchain geprüft: Node 22, python-pptx, markitdown, LibreOffice für das Rendern
  nach PNG.

### Offen

Die `.potx` und `few_shot_prompting.pptx` sind noch nicht eingegangen.
Sobald sie vorliegen: Inventar fahren, Layout-Zuordnung je Musterfolie vorschlagen,
dann die 5 Folien bauen und rendern.

---

## Nachtrag 2 — Was die Vorlage tatsächlich vorgibt

Die `.potx` wurde inventarisiert (`inspect_template.py`) und visuell gerendert.
Ergebnis: **die Vorlage ist die Quelle, mein 960×540-Vorschlag oben war nur die
Notlösung ohne Vorlage.** Wo beide sich widersprechen, gilt die Vorlage.

### Bestätigt

- **Foliengrösse exakt 960 × 540 pt** — die 1 pt = 1 px-Annahme trägt.
- **Theme-Farben sind die Design-System-Tokens**: `dk1`/`dk2` = `#000D6E`,
  accent1 `#1B5951`, accent2 `#6C2273`, accent3 `#D9304C`, accent4 `#FA9319`,
  accent5 `#94E3D4`, accent6 `#B8B2FF`. Die Flächen der Layouts nutzen die
  Tints 2 und 3 derselben Familien. `DESIGN.md` ist damit die passende Referenz
  für alles, was die Vorlage offen lässt.
- **Marke: Helvetia.** Das Logo unten links ist das Helvetia-Wortmarke, das
  Kernblau bleibt `#000D6E`.

### Korrigiert

- **Theme-Schrift ist Arial**, major und minor. Die Frage nach den Corporate
  Fonts ist damit erledigt — kein Fallback-Risiko.
- **Titel ist 24 pt bold, nicht 40 pt.** Die Vorlage ist deutlich zurückhaltender
  als das Web-Design-System. Titelplatzhalter `x41 y38 w879 h60`.
- **Der Titel muss einzeilig bleiben.** Der Untertitel-Platzhalter (24 pt regular)
  beginnt bei `y=68` und überlappt eine zweite Titelzeile. Alle acht Action Titles
  von Block 1 passen einzeilig.
- **Ränder 41 pt**, Inhaltszone `y 120…480`, Fusszeilenband `y 497`.
  Spalten: 1×879 · 2×428 (Rinne 22) · 3×278 (Rinne 22) · Content-Box 653 + 203.
- **Fliesstext 16 pt** mit fixem 21-pt-Zeilenabstand. `Small_typo`-Varianten
  (12 pt) sind laut Vorlage „only for very much content" — für Block 1 nicht nötig.

### Genutzte Layouts

| Slide | Layout | Eigene Formen |
|---|---|---|
| 7 | `Chapter-green` | keine |
| 10 | `Content-Box-green` | 1 Karte (Prompt-Vorlage), 1 Fussnote |
| 12 | `2 Contents` | 2 Karten, 2 Spaltenlabels, 1 Fazit-Zeile |
| 13 | `Content-Box-green` | 10 Textboxen (5 Schritte) |
| 14 | `Headline-green` | 5 Chips, 2 Textboxen |

Blockfarbe für Block 1 ist **grün**. Die Vorlage bietet vier Akzentfamilien
(green · red · purple · tangerine) — bei mehr als vier Blöcken wiederholen sie sich.

### Zwei Entscheide, die eine Abnahme brauchen

1. **Phasenmarkierung im Fusszeilenband.** `LEARN` / `SEE` / `TRY` / `IMPROVE`
   steht in der Corporate-Fusszeile: `01  Few-shot & negative examples  ·  LEARN`.
   Kein zusätzliches Element, keine Farbcodierung — konform zur Regel „kein
   Farbcoding" des Design Systems. PowerPoint legt Fusszeilen-Platzhalter nicht
   automatisch auf neue Folien; das Skript kopiert sie aus dem Layout, damit
   Position und Formatierung aus der Vorlage kommen.
2. **Der Compliance-Hinweis auf Slide 13** steht fett in der grünen Corporate-Box,
   nicht auf einer eigenen Warnfläche. Begründung: eine gelbe Warnfläche direkt
   neben der grünen Box verletzt die Regel „gleiches Farbspektrum je Element",
   und das Design System reserviert Alert-Farben für Systemzustände. Die Prominenz
   kommt aus Position und Schriftschnitt. Wenn dir das zu leise ist, ist die
   Alternative eine `#FFF9E8`/`#7D4A0D`-Fläche über die volle Inhaltsbreite
   unterhalb der Schritte — dann muss die grüne Box weichen.

### Nicht im Repository

Die `.potx` und das erzeugte `.pptx` werden **nicht** eingecheckt: beide enthalten
Corporate Assets (Logo, Theme, Schriften). Eingecheckt sind nur das Build-Skript,
der Inventarisierer und die Inhaltsdaten.

---

## Nachtrag 3 — Eigene Komposition auf Corporate-Werten

Entscheid: **eigene Komposition, Corporate-Werte.** Die Content-Layouts der Vorlage
werden nicht mehr benutzt — ihre Boxen haben den Inhalt diktiert statt ihn zu tragen,
und das war der Grund für die leer wirkenden Folien. Alle Folien sitzen auf
`1 Content` (das schlichteste Layout, das die Master-Grafiken und damit das Logo
noch erbt); dessen eigene Inhaltsboxen werden entfernt, alles andere wird selbst
gesetzt.

### Aus der Vorlage, unverändert

- **Arial** als Theme-Schrift. Kein Run überschreibt den Schriftnamen, alles erbt.
- **Farbwerte direkt**: Text `#000D6E`; Akzente `#1B5951`, `#D9304C`; Flächen
  `#94E3D4`, `#CBF2EC`, `#FFD7D7`, `#FFECBC`. Einzige Ausnahme: `#F6F6F6` als
  neutrale Fläche — die Vorlage kennt keinen neutralen Tint, der Wert kommt aus
  dem Design System.
- **Geometrie**: Rand 41, Inhaltsbreite 879, Inhaltszone y 120–480, Fusszeilenband
  y 497. Spalten 428+428 (Rinne 22) und 278×3 (Rinne 22).

### Eigene Skala

Titel 32 pt (Mittelweg zwischen Vorlage 24 und meinem ursprünglichen 40),
Divider 48, Blocknummer 96, Statement 24, Kartentitel 20, Lead 18,
Fliesstext 16, Hinweis 13, Label/Fusszeile 12. Zeilenabstand durchgehend 1.3.

### Was die Leere behoben hat

| Slide | vorher | jetzt |
|---|---|---|
| 7 | untere Hälfte leer | vier Zyklus-Karten über die volle Breite bei y 376–460 |
| 10 | leere Seitenbox der Vorlage | zwei Spalten, drei Karten, Kernaussage-Band über die volle Breite |
| 12 | linke Karte kopflastig | beide Karten 290 hoch, Text vertikal zentriert, getöntes Fazit-Band |
| 13 | unteres Drittel leer | 3×2-Raster über die ganze Inhaltszone, Zeit-Badge oben rechts |
| 14 | untere Hälfte leer | Chips auf 163×110 vergrössert, Handlungsaufforderung als Band 326–450 |

Der Compliance-Hinweis auf Slide 13 hat jetzt eine eigene Zelle im Raster auf
`#FFECBC`. Das ist die Variante, die ich zuvor verworfen hatte — im eigenen Raster
steht sie nicht mehr neben der grünen Box, der Spektrum-Konflikt entfällt.
