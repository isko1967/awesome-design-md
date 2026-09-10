"""03 - Improving the result (slides 20-24).

The inspect-diagnose-change-run loop, the break, the missing-data demo,
the second practice round and its reflection.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, BLUE, CONTENT_W, GOOD, GREEN, MARGIN, NEUTRAL,
                      T_BODY, T_CARD, T_DIVIDER, T_HINT, T_LEAD, T_META,
                      T_STATEMENT, WHITE, band, blue_slide, card, divider,
                      eyebrow, flow_row, footer, lead, new_slide, runs,
                      task_header, textbox, title, write)
from essentials.ess_00 import option_chips

LABEL = "03  Improving the result"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_20(prs):
    s = new_slide(prs)
    title(s, "The first result is a draft, not a verdict.", has_lead=False)

    flow_row(s, [
        ("Inspect", "What specifically is wrong? Not “it is bad”."),
        ("Diagnose", "Which building block is missing?"),
        ("Change one", "One instruction. Not a rewrite."),
        ("Run", "Compare against the same task."),
    ], top=182, cell_h=196)

    band(s, "The rule that makes it work",
         "Change one thing so you can see what worked.")
    _foot(s, "LEARN", 20)


def slide_21(prs):
    """The break. A blue landmark, like the Session 2 break."""
    s = blue_slide(prs)
    write(textbox(s, MARGIN, 150, CONTENT_W, 70),
          [("Five-minute reset", T_DIVIDER, True, WHITE, None)])
    write(textbox(s, MARGIN, 232, CONTENT_W, 32),
          [("Vote for a Prompt Clinic case.", T_STATEMENT, False, WHITE,
            None)])

    note = card(s, MARGIN, 300, CONTENT_W, 118, WHITE, pad=20)
    write(note, [
        ("While you are away", T_CARD, True, BLUE, None),
        ("Vote in Slido for the situations you want worked through live. If "
         "your own submission is up and you would rather we did not use it, "
         "message the host.", T_BODY, False, BLUE, 8),
    ], anchor=MSO_ANCHOR.MIDDLE)
    footer(s, LABEL, None, 21)


def slide_22(prs):
    s = new_slide(prs)
    title(s, "Tell it what to do when something is missing.", width=729)
    task_header(s, "Demo 2 — notes into a table")

    headers = ("Decision", "Action", "Owner", "Due date")
    rows = [
        ("Release moves to 4 November", "Re-plan both team backlogs",
         "Team leads", "17 October"),
        ("Vendor defects to be re-tested", "Schedule a second test round",
         "not stated", "not stated"),
        ("Stakeholders to be informed", "Send the update", "Project lead",
         "18 October"),
    ]
    widths = (300, 279, 150, 150)
    gap = 0
    top, head_h, row_h = 148, 36, 46
    x = MARGIN
    for i, head in enumerate(headers):
        cell = card(s, x, top, widths[i] - 4, head_h, NEUTRAL.surface, pad=10)
        write(cell, [(head, T_HINT, True, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE)
        x += widths[i]
    for r, row in enumerate(rows):
        x = MARGIN
        y = top + head_h + 4 + r * (row_h + 4)
        for i, value in enumerate(row):
            cell = card(s, x, y, widths[i] - 4, row_h, NEUTRAL.surface,
                        pad=10)
            write(cell, [(value, T_HINT, False, BLUE, None)],
                  anchor=MSO_ANCHOR.MIDDLE)
            x += widths[i]

    instruction = card(s, MARGIN, 344, CONTENT_W, 86, GOOD.surface, pad=16)
    write(instruction, [
        ("The instruction that produced this", T_BODY, True, GOOD.accent,
         None),
        ("If a value is not in the notes, write “not stated”. Do not infer "
         "owners or dates.", T_BODY, False, BLUE, 6),
    ], anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Why it matters",
         "Without that line, a gap in your input becomes a confident "
         "sentence in your output.")
    _foot(s, "SEE", 22)


def slide_23(prs):
    s = new_slide(prs)
    title(s, "Improve your prompt with one change.", width=729)
    task_header(s, "Your task", "9 min")

    steps = [
        ("1", "Run your prompt from earlier."),
        ("2", "Judge it: useful? accurate? fits the audience?"),
        ("3", "Change one instruction to fix the worst one."),
        ("4", "Run again and compare."),
    ]
    top, pitch = 150, 62
    for i, (num, text) in enumerate(steps):
        cell = card(s, MARGIN, top + i * pitch, CONTENT_W, pitch - 10,
                    ACTION.surface, pad=12)
        runs(cell, [(f"{num}   ", True, GREEN), (text, True, BLUE)],
             size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "One change only",
         "Rewrite everything and you have learned nothing you can repeat.")
    _foot(s, "TRY", 23)


def slide_24(prs):
    s = new_slide(prs)
    title(s, "How much better was it after one change?", has_lead=False)
    task_header(s, "Reflect", "3 min", y=140)

    option_chips(s, ("1 — no change", "2", "3", "4", "5 — a lot"),
                 top=196, per_row=5, h=62)

    band(s, "In the chat", "One word: what did you change?")
    _foot(s, "IMPROVE", 24)


SLIDES = [slide_20, slide_21, slide_22, slide_23, slide_24]
