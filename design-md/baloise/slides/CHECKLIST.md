# Prüfliste

Jeder Punkt ist entweder **automatisch geprüft** (`check.py` bricht ab) oder
**durch Konstruktion erzwungen** (es gibt nur einen Weg, es zu bauen).
Nichts hier verlässt sich auf Hinschauen.

## Automatisch geprüft

| Regel | Wie |
|---|---|
| Kein Textüberlauf | Umbruch mit Arial-Metrik nachgerechnet, Lauf für Lauf bei gemischtem Schnitt |
| Keine Überlappung | Alle Textrahmen paarweise, Toleranz 4 pt |
| Nichts ausserhalb der Folie | Rahmen gegen 960 × 540 |
| Nichts unter 12 pt | Ausnahme: Fusszeile und Phasen-Chips bei 10 pt, wie im Corporate Master |
| Nur Grössen aus der Skala | 96 · 48 · 32 · 30 · 28 · 24 · 20 · 18 · 16 · 13 · 12 · 10 |
| Kontrast mindestens AA | Jeder Textlauf gegen seine Fläche, 4.5:1 bzw. 3:1 ab 24 pt |
| Icon sitzt auf der Textlinie | Optische Mitte des Glyphs gegen Mitte der Textzeile, Toleranz 4 pt |
| Nichts in der Chip-Zeile | Kein Objekt in y 16–46 rechts von x 500 ausser den Chips |
| Eckenradius einheitlich | Jede Form 4 pt ± 1.5 |
| Höchstens zwei Rollenfarben je Folie | Grau und Weiss zählen nicht mit |
| Kein Violett | Die Rolle existiert nicht mehr |
| Label höchstens 24 Zeichen | `eyebrow()` bricht sonst ab |
| Titel einzeilig, mindestens 28 pt | Sonst nennt der Build die Folie zum Umformulieren |

## Durch Konstruktion erzwungen

| Regel | Komponente |
|---|---|
| Label hängt an seinem Feld | `snap_labels()` setzt es 10 pt darüber, Icon wandert mit |
| Gleicher Kopfabstand auf jeder Folie | `settle()` |
| Abschlussband immer neutral, immer gleiche Höhe | `band()` |
| Abschnittstitel fett, Badge rechts daneben | `task_header()` |
| Icon vor Text immer auf der Linie | `icon_inline()` |
| Aufzählung mit Marker, nie kahle Wörter | `bullet_list()` |
| Chips gefüllt, nie Kontur | `card()` ignoriert `outline` |
| Divider zeigt nur die Phasen des Blocks | `divider()` |

## Farbrollen

| Rolle | Fläche | Akzent | Nur für |
|---|---|---|---|
| GOOD | `#CBF2EC` | `#1B5951` | Positivbeispiel, verbessertes Ergebnis, Empfehlung |
| AVOID | `#FFD7D7` | `#99172D` | Negativbeispiel, Don't, Compliance-Hinweis |
| NEUTRAL | `#F6F6F6` | `#000D6E` | Info-Kästen, Rohmaterial, Prompt-Leinwand, Nebeninfo |
| CHOICE | `#000D6E` | `#FFFFFF` | Was der Teilnehmer auswählt, Badges |
| Divider | `#000D6E` | `#FFFFFF` | Blocktrenner, Pause, Clinic, Abschluss |

Grün nur mit Gegenpol. Wo alles auf der Folie „das Gute" ist, bleibt es neutral.
Kein Grau für Text. Kein Tangerine. Kein Violett.

## Raster

Rand 41 · Inhaltsbreite 879 · Titel y 48 (voll: 38) · Abschnittszeile y 104 ·
Inhalt ab 132 · Band y 448 · Fusszeile y 497 · Phasen-Chips y 22.
Spalten 428+428, 278×3, 203×4, 653+203, Rinne 22.

## Was der Checker nicht sieht

Ob eine Folie inhaltlich etwas aussagt. Ob die Phase stimmt — das wird gegen
die Slide-Spezifikation abgeglichen, nicht abgeleitet. Ob eine Formulierung
für Teilnehmende verständlich ist. Diese drei bleiben Handarbeit.
