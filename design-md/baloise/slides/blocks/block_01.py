"""Block 1 - Few-shot & negative examples (slides 7-14).

Content is verbatim from the source deck; only the layout is ours.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, blue_slide, divider, BAND_TOP, BLUE, CAUTION, COL2_W, COL2_X, COL3_W,
                      COL3_X, CONTENT_TOP, CONTENT_W, GOOD, GREY_TEXT, MARGIN,
                      NEUTRAL, T_BODY, T_CARD, T_DIVIDER, T_HINT, T_LEAD,
                      T_META, T_NUMBER, T_STATEMENT, WHITE, badge, band, card,
                      eyebrow, footer, lead, new_slide, runs, textbox, title,
                      write)

LABEL = "01  Few-shot & negative examples"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_07(prs):
    s = blue_slide(prs)
    divider(s, "01", ["Few-shot &", "negative examples"],
            "Show the model what good looks like.",
            chips=("LEARN", "SEE", "TRY", "IMPROVE"))
    _foot(s, None, 7)


def slide_08(prs):
    s = new_slide(prs)
    title(s, "Few-shot prompting gives the model examples to learn from.")
    lead(s, "Instead of only describing what you want, provide one or more "
            "examples of the desired output.")

    eyebrow(s, "What the model infers")
    infer = card(s, MARGIN, 142, CONTENT_W, 64, NEUTRAL.surface, pad=14)
    write(infer, [
        ("tone and level of formality · structure and formatting · "
         "length and level of detail · wording and style",
         T_BODY, True, BLUE, None),
    ], anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Example", y=216)
    plain = card(s, COL2_X[0], 238, COL2_W, 172, NEUTRAL.surface)
    write(plain, [
        ("Instruction only", T_LEAD, True, GREY_TEXT, None),
        ("Summarise this claims update for senior management.",
         14, False, BLUE, 10),
    ])
    guided = card(s, COL2_X[1], 238, COL2_W, 172, GOOD.surface)
    write(guided, [
        ("With an example", T_LEAD, True, GOOD.accent, None),
        ("Summarise this claims update for senior management.",
         14, False, BLUE, 10),
        ("Use the example below as a reference for tone, structure and level "
         "of detail.", 14, False, BLUE, 6),
        ("Example: [insert strong previous update]", 14, True, BLUE, 8),
    ])

    related = textbox(s, MARGIN, 418, CONTENT_W, 20)
    runs(related, [("RELATED CONCEPT   ", True, GREY_TEXT),
                   ("Zero-shot: instructions without examples   ·   "
                    "Few-shot: one or more examples provided as guidance",
                    False, BLUE)], size=T_HINT, anchor=MSO_ANCHOR.TOP)

    band(s, "Key idea",
         "Examples reduce how much the model has to interpret.", GOOD)
    _foot(s, "LEARN", 8)


def slide_09(prs):
    s = new_slide(prs)
    title(s, "Negative examples show the model what to avoid.")
    lead(s, "Imagine you regularly create management updates about claims "
            "performance.")

    for x, question, answer, role in (
            (COL2_X[0], "A positive example answers",
             "What should the output look like?", GOOD),
            (COL2_X[1], "A negative example answers",
             "What should the output not look like?", CAUTION)):
        ask = card(s, x, CONTENT_TOP, COL2_W, 84, role.surface)
        write(ask, [(question, T_BODY, True, role.accent, None),
                    (answer, T_LEAD, True, BLUE, 4)])

    positive = card(s, COL2_X[0], 220, COL2_W, 216, GOOD.surface)
    write(positive, [
        ("Positive example", T_CARD, True, GOOD.accent, None),
        ("Status: Claims volumes increased by 12%.", T_BODY, False, BLUE, 12),
        ("Impact: Processing time is temporarily above target.",
         T_BODY, False, BLUE, 2),
        ("Action: Additional capacity has been activated.",
         T_BODY, False, BLUE, 2),
        ("→ gives direction", T_BODY, True, GOOD.accent, 14),
    ])
    negative = card(s, COL2_X[1], 220, COL2_W, 216, CAUTION.surface)
    write(negative, [
        ("Negative example", T_CARD, True, CAUTION.accent, None),
        ("We would like to provide an update regarding various developments "
         "that have taken place within claims operations over the past "
         "reporting period…", T_BODY, False, BLUE, 12),
        ("→ sets a boundary", T_BODY, True, CAUTION.accent, 14),
    ])

    band(s, "Key idea",
         "You do not always need both. Add a negative example when avoiding "
         "a specific pattern matters.", GOOD)
    _foot(s, "LEARN", 9)


def slide_10(prs):
    s = new_slide(prs)
    title(s, "Tell the model what to learn from each example.")

    eyebrow(s, "What to specify", w=COL2_W)
    positive = card(s, MARGIN, 146, COL2_W, 140, GOOD.surface)
    write(positive, [
        ("Positive example", T_CARD, True, GOOD.accent, None),
        ("Follow its", T_BODY, True, BLUE, 10),
        ("tone · structure · level of detail", T_BODY, False, BLUE, 2),
    ])
    negative = card(s, MARGIN, 302, COL2_W, 140, CAUTION.surface)
    write(negative, [
        ("Negative example", T_CARD, True, CAUTION.accent, None),
        ("Avoid its", T_BODY, True, BLUE, 10),
        ("unnecessary background · vague wording · lack of clear actions",
         T_BODY, False, BLUE, 2),
    ])

    eyebrow(s, "The prompt", x=COL2_X[1], w=COL2_W)
    prompt = card(s, COL2_X[1], 146, COL2_W, 296, NEUTRAL.surface)
    write(prompt, [
        ("Use the examples below as guidance for the new output.",
         T_BODY, False, BLUE, None),
        ("Positive example:", T_BODY, True, BLUE, 12),
        ("[insert example]", T_BODY, False, GREY_TEXT, 0),
        ("Negative example:", T_BODY, True, BLUE, 12),
        ("[insert example]", T_BODY, False, GREY_TEXT, 0),
        ("Now complete this task:", T_BODY, True, BLUE, 12),
        ("[insert task]", T_BODY, False, GREY_TEXT, 0),
        ("Do not copy the content of the examples. Use them only as guidance "
         "for how the new output should be written.",
         T_HINT, False, GREY_TEXT, 14),
    ])

    band(s, "Use when",
         "The desired quality is easier to demonstrate than to describe.",
         GOOD)
    _foot(s, "LEARN", 10)


def slide_11(prs):
    s = new_slide(prs)
    title(s, "Can examples make a vague instruction more precise?")
    lead(s, "Severe weather has increased claims volumes. Management needs a "
            "short update.")

    eyebrow(s, "Starting prompt")
    start = card(s, MARGIN, 146, CONTENT_W, 62, NEUTRAL.surface)
    write(start, [("Turn these notes into a short update for senior "
                   "management.", T_LEAD, False, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Version 2 adds", y=226)
    for x, count, kind, purpose, role in (
            (COL2_X[0], "1", "positive example",
             "to show the desired style", GOOD),
            (COL2_X[1], "1", "negative example",
             "to show what to avoid", CAUTION)):
        tile = card(s, x, 252, COL2_W, 176, role.surface, pad=20)
        write(tile, [
            (count, T_NUMBER // 2, True, role.accent, None),
            (kind, T_CARD, True, BLUE, 4),
            (purpose, T_BODY, False, BLUE, 6),
        ])

    band(s, "Watch for",
         "prioritisation · structure · level of detail · tone · "
         "action orientation", GOOD)
    _foot(s, "SEE", 11)


def slide_12(prs):
    s = new_slide(prs)
    title(s, "Same task. Clearer guidance.")

    eyebrow(s, "Without examples", x=COL2_X[0], w=COL2_W)
    eyebrow(s, "With examples", x=COL2_X[1], w=COL2_W, colour=GOOD.accent)

    before = card(s, COL2_X[0], 146, COL2_W, 296, NEUTRAL.surface, pad=20)
    write(before, [
        ("Recent severe weather events have led to an increase in claims "
         "volumes. The claims organisation is currently taking several "
         "actions to manage the situation. Additional capacity has been made "
         "available, and developments will continue to be monitored.",
         T_BODY, False, BLUE, None),
    ], anchor=MSO_ANCHOR.MIDDLE)

    after = card(s, COL2_X[1], 146, COL2_W, 296, GOOD.surface, pad=20)
    rows = []
    for i, (heading, text) in enumerate([
            ("Status — Attention required",
             "Severe-weather claims increased volumes and processing times."),
            ("Response", "Additional external capacity has been activated."),
            ("Customer impact",
             "No change to current customer communication is required."),
            ("Next watchpoint",
             "Reassess processing times at the end of the week.")]):
        rows.append((heading, T_BODY, True, GOOD.accent, None if i == 0 else 12))
        rows.append((text, T_BODY, False, BLUE, 0))
    write(after, rows, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "What changed?",
         "More specific · more structured · more actionable", GOOD)
    _foot(s, "SEE", 12)


def slide_13(prs):
    s = new_slide(prs)
    title(s, "Use examples to guide your own output.", width=729)
    lead(s, "Your task")
    badge(s, "TIME  5 MIN")

    steps = [
        ("1", "Choose a recurring text-based task.",
         "stakeholder update · meeting summary · decision note · "
         "internal announcement"),
        ("2", "Add one positive example.",
         "Choose something that represents the quality you want."),
        ("3", "Optional: add one negative example.",
         "Use it if there is a recurring pattern you want to avoid."),
        ("4", "Tell AI what to learn from the examples.",
         "Tone? Structure? Length? Level of detail?"),
        ("5", "Run the prompt and compare the result.", None),
    ]
    for i, (number, text, hint) in enumerate(steps):
        cell = card(s, COL3_X[i % 3], 150 if i < 3 else 325, COL3_W, 155,
                    ACTION.surface)
        rows = [(number, T_STATEMENT, True, ACTION.accent, None),
                (text, T_LEAD, True, BLUE, 6)]
        if hint:
            rows.append((hint, T_HINT, False, GREY_TEXT, 6))
        write(cell, rows)

    # the compliance note takes the sixth cell and the caution colour, the
    # same colour that marks what to avoid everywhere else in the deck
    note = card(s, COL3_X[2], 325, COL3_W, 155, CAUTION.surface)
    write(note, [
        ("Before you start", T_LEAD, True, CAUTION.accent, None),
        ("Keep all information generic. Do not enter personal, customer or "
         "confidential information.", T_BODY, False, BLUE, 8),
    ])
    _foot(s, "TRY", 13)


def slide_14(prs):
    s = new_slide(prs)
    title(s, "Did the examples give you more control?")
    lead(s, "Compare the result with what you would normally receive.")

    write(textbox(s, MARGIN, 140, 500, 28),
          [("What changed most?", T_CARD, True, BLUE, None)])

    x = MARGIN
    for text in ("Tone", "Structure", "Level of detail", "Wording",
                 "Nothing meaningful"):
        chip = card(s, x, 180, 163, 110, ACTION.surface)
        write(chip, [(text, T_LEAD, False, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += 163 + 16

    cta = card(s, MARGIN, 326, CONTENT_W, 124, ACTION.surface, pad=24)
    write(cta, [
        ("In the chat", T_BODY, True, ACTION.accent, None),
        ("Share the one thing that changed most.", T_STATEMENT, False, BLUE, 8),
    ], anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "IMPROVE", 14)


SLIDES = [slide_07, slide_08, slide_09, slide_10, slide_11, slide_12,
          slide_13, slide_14]
