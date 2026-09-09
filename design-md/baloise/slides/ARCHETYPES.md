# Archetypen und Slide-Zuordnung

Acht Archetypen decken alle 54 Slides. Jeder neue Block ist damit eine
Inhaltsdatei, kein neues Layout.

## Grundflächen-Regel

| Slide-Art | Grundfläche |
|---|---|
| Technik-Divider (7, 15, 25, 31, 41) | Vollflächig `#000D6E`, Text und Chips weiss |
| Titelfolie (1) | Vollflächig `#000D6E` |
| Teilnahme-Landmarken: Pause (30), Clinic-Opener (46), Abschluss (54) | Vollflächig Tangerine `#FFECBC` |
| Alle Inhaltsfolien | Weiss, Farbe nur in Karten und Bändern |

Begründung: Blau ist im Corporate Design die Strukturfarbe und auf jeder Seite
präsent. Grün als Divider-Grund würde bedeuten „dieses Kapitel ist der
gute Zustand" — Grün ist aber im ganzen Deck für den Zielzustand reserviert.

## Farbrollen

| Rolle | Fläche | Akzent | Bedeutung |
|---|---|---|---|
| GOOD | `#CBF2EC` | `#1B5951` | Zielzustand: Positivbeispiel, verbessertes Ergebnis, „so sieht gut aus" |
| AVOID | `#FFD7D7` | `#D9304C` | Der Don't: Negativbeispiel, zu vermeidendes Muster, Gegenteil vom Ziel |
| GUARDRAIL | `#E1D9FF` | `#6C2273` | Grenzen und Regeln: Compliance-Hinweis, „nicht tun", Stopp-Bedingung |
| NEUTRAL | `#F6F6F6` | `#747474` | Rohmaterial: schwaches „Vorher", Prompt-Leinwand, Nebenspalte |
| ACTION | `#FFECBC` | `#B24A00` | Der Teilnehmer ist dran: Übung, Slido, Chat, Clinic, Transfer |
| BLUE | — | `#000D6E` | Text und Struktur |

Zwei Regeln zur Farbe:

- **Farbe markiert das Artefakt, nicht den Satz darüber.** Eine Karte mit „A
  positive example answers…" ist neutral; die Rolle trägt nur das Beispiel selbst.
- **Rot (AVOID) und Violett (GUARDRAIL) sind getrennt.** Rot ist das schlechte
  Beispiel, das man nachahmen könnte und nicht soll; Violett ist eine Regel oder
  Grenze („keine Kundendaten eingeben"). Tangerine bleibt der Teilnahme-Farbe
  vorbehalten und wird nie für Warnungen benutzt.

## Die acht Archetypen

| Archetyp | Einsatz |
|---|---|
| **DIVIDER** | Blocktrenner; Varianten: Cover, Pause, Opener, Abschluss |
| **CONCEPT** | Zweiseitige Gegenüberstellung, zwei getönte Karten, Kernaussage-Band |
| **BEFORE/AFTER** | Ein Vergleich, zwei gleich hohe 428-Karten, Fazit-Band |
| **PRACTICE** | 3×2-Raster aus 278-Zellen, Badge oben rechts |
| **REFLECTION** | Frage, Chip-Reihe, Handlungs-Band |
| **PROMPT** | Prompt-Leinwand in einer Spalte, Nebenspalte 203, „Use when"-Band |
| **LIST** | 3–7 gleichrangige Einträge, Nummer + Aussage + Hinweis |
| **FLOW** | Ablauf, bei dem die Reihenfolge die Botschaft ist; Varianten: horizontal, Schleife, Doppelspalte |

## Zeilenraster für LIST

Mit Band (Spanne 294 pt ab y 146):

| Einträge | Zeilenhöhe | Abstand |
|---|---|---|
| 3 | 91 | 101 |
| 4 | 66 | 76 |
| 5 | 50 | 60 |
| 6 | 40 | 50 |
| 7 | 34 | 43 |

## Zuordnung aller 54 Slides

| # | Archetyp | # | Archetyp | # | Archetyp |
|---|---|---|---|---|---|
| 1 | DIVIDER cover | 19 | PROMPT | 37 | PROMPT demo |
| 2 | LIST 4 | 20 | BEFORE/AFTER | 38 | BEFORE/AFTER |
| 3 | LIST 5 caution | 21 | PROMPT demo | 39 | PRACTICE |
| 4 | LIST 5 | 22 | BEFORE/AFTER | 40 | REFLECTION |
| 5 | REFLECTION 7 | 23 | PRACTICE | 41 | DIVIDER |
| 6 | REFLECTION 4 | 24 | REFLECTION | 42 | CONCEPT |
| 7 | DIVIDER | 25 | DIVIDER | 43 | LIST 4 + aside |
| 8 | CONCEPT | 26 | CONCEPT | 44 | PROMPT |
| 9 | CONCEPT | 27 | FLOW twin | 45 | PROMPT demo |
| 10 | PROMPT | 28 | PROMPT | 46 | DIVIDER opener |
| 11 | PROMPT demo | 29 | PROMPT demo | 47 | FLOW loop |
| 12 | BEFORE/AFTER | 30 | DIVIDER break | 48 | PRACTICE |
| 13 | PRACTICE | 31 | DIVIDER | 49 | PRACTICE |
| 14 | REFLECTION | 32 | LIST 4 + aside | 50 | PRACTICE |
| 15 | DIVIDER | 33 | FLOW horizontal | 51 | LIST 5 |
| 16 | CONCEPT | 34 | LIST 5 caution | 52 | LIST 5 |
| 17 | LIST 4 + aside | 35 | CONCEPT | 53 | LIST 5 matrix |
| 18 | LIST 5 | 36 | PROMPT | 54 | DIVIDER close |

## Überlauf-Leiter

Wenn Inhalt nicht passt, in dieser Reihenfolge:

1. Randmaterial in die 203-Nebenspalte bei 13 pt
2. Hinweise und Beispieltexte auf 13 pt
3. Eine Aufzählung von 4–6 kurzen Einträgen zu einer Zeile mit „·" verdichten
4. Das Fazit ins Band, das Szenario hoch in den 18-pt-Lead
5. Splitten — letzte Wahl, die Deck-Länge ist auf 54 festgelegt

Slides mit bekanntem Überlaufrisiko: 17, 27, 29, 32, 36, 43, 45, 47 — je mit
festgelegter Behandlung. Die Messung übernimmt `check.py`, nicht das Auge.

## Zyklus-Chips

Blöcke 3 und 5 durchlaufen nur LEARN und SEE. Alle vier Chips bleiben stehen,
TRY und IMPROVE werden als Umriss ohne Füllung gesetzt: der Zyklus bleibt
visuelle Konstante, die Verkürzung wird gezeigt statt verschwiegen.
