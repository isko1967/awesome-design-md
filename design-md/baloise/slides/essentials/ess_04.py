"""04 - Prompt Clinic (slides 25-29).

The six-step loop, the two live cases, the Prompt Gallery and the Q&A.
Case fields stay as placeholders - they are filled on the day.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, AVOID, BLUE, COL2_W, COL2_X, CONTENT_W, GOOD,
                      GREEN, MARGIN, NEUTRAL, T_BODY, T_CARD, T_HINT, T_LEAD,
                      T_META, T_STATEMENT, band, card, eyebrow, flow_column,
                      footer, lead, new_slide, runs, task_header, textbox,
                      title, write)
from essentials.ess_00 import slido

LABEL = "04  Prompt Clinic"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_25(prs):
    s = new_slide(prs)
    title(s, "Real situations. Better briefings.", width=729)
    task_header(s, "Prompt Clinic", "18 min")

    left = [
        ("1  Work situation", "What you submitted, generically"),
        ("2  Task & outcome", "What good would look like"),
        ("3  Prompt", "The briefing we write live"),
    ]
    right = [
        ("4  AI output", "Whatever we actually get"),
        ("5  Evaluation", "Useful? Accurate? Fits the audience?"),
        ("6  Improved prompt", "One change, then run again"),
    ]
    flow_column(s, COL2_X[0], COL2_W, left, top=150, cell_h=76, gap=22)
    flow_column(s, COL2_X[1], COL2_W, right, top=150, cell_h=76, gap=22)

    band(s, "Your job",
         "Call out in the chat what you would change — before I do.")
    _foot(s, None, 25)


def _field(slide, x, y, w, h, label, body, role=NEUTRAL, size=T_HINT):
    cell = card(slide, x, y, w, h, role.surface, pad=12)
    write(cell, [(label, T_META, True, role.accent, None),
                 (body, size, False, BLUE, 5)], anchor=MSO_ANCHOR.MIDDLE)
    return cell


def slide_26(prs):
    s = new_slide(prs)
    title(s, "From situation to better briefing.", width=729)
    task_header(s, "Clinic", "Case 1")

    _field(s, COL2_X[0], 150, COL2_W, 128, "The situation",
           "[SELECTED, SANITISED SLIDO CASE]")
    _field(s, COL2_X[0], 292, COL2_W, 128, "Task & desired outcome",
           "Written live with the group.")
    _field(s, COL2_X[1], 150, COL2_W, 128, "First prompt → first output",
           "Written and run live. Expect it to be fluent and to miss "
           "something.")
    _field(s, COL2_X[1], 292, COL2_W, 128, "One change → run again",
           "The group diagnoses; we change one instruction and compare.",
           role=GOOD)

    band(s, "Watch for",
         "Which building block was missing — and how small the change had "
         "to be.")
    _foot(s, "SEE", 26)


def slide_27(prs):
    s = new_slide(prs)
    title(s, "Same six steps, different situation.", width=729)
    task_header(s, "Clinic", "Case 2 — faster")

    _field(s, COL2_X[0], 150, COL2_W, 120, "The situation",
           "[SELECTED, SANITISED SLIDO CASE]")
    _field(s, COL2_X[0], 284, COL2_W, 120, "What we are watching for",
           "That the method transfers — different task, different "
           "department, same sequence.")
    _field(s, COL2_X[1], 150, COL2_W, 120, "Run it at speed",
           "Outcome stated, prompt written, output evaluated against the "
           "three questions, one change, run again.")
    _field(s, COL2_X[1], 284, COL2_W, 120, "Takeaway",
           "You are not taking away my prompts. You are taking away the "
           "sequence.", role=GOOD, size=T_BODY)
    _foot(s, "SEE", 27)


def slide_28(prs):
    s = new_slide(prs)
    title(s, "What you built today, reusable by someone else.", width=729)
    task_header(s, "Prompt Gallery")

    headers = ("Situation", "Use case", "Prompt", "Technique", "Key learning")
    rows = [
        ("Vendor delay affecting two teams", "Brief",
         "Audience named, status given, missing-data rule",
         "Output format + missing-data rule",
         "Naming the audience removed three guesses at once."),
        ("Meeting notes with unclear owners", "Extract",
         "Fixed columns, “not stated” instruction", "Missing-data rule",
         "“Not stated” beats an invented owner."),
    ]
    widths = (180, 110, 210, 179, 200)
    top, head_h, row_h = 150, 36, 100
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
            role = GOOD if i == 4 else NEUTRAL
            cell = card(s, x, y, widths[i] - 4, row_h, role.surface, pad=10)
            write(cell, [(value, T_HINT, False, BLUE, None)],
                  anchor=MSO_ANCHOR.MIDDLE)
            x += widths[i]

    band(s, "Where it lives",
         "[PROMPT GALLERY LOCATION] — entries are screened by a named owner "
         "before publication. Keep them generic.", y=422)
    _foot(s, None, 28)


def slide_29(prs):
    s = new_slide(prs)
    title(s, "What is still unclear?", has_lead=False)
    task_header(s, "Q&A", "8 min", y=140)

    how = card(s, MARGIN, 192, CONTENT_W, 94, NEUTRAL.surface, pad=18)
    write(how, [
        ("How this works", T_CARD, True, BLUE, None),
        ("Post in Slido and upvote — we work down the list by votes.",
         T_BODY, False, BLUE, 8),
    ], anchor=MSO_ANCHOR.MIDDLE)

    policy = card(s, MARGIN, 302, CONTENT_W, 116, AVOID.surface, pad=18)
    write(policy, [
        ("On policy questions", T_CARD, True, AVOID.accent, None),
        ("If it is about data handling or tool capability and the answer is "
         "not certain, we park it and follow up in writing. No guesses from "
         "the stage.", T_BODY, False, BLUE, 8),
    ], anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "INTERACT", 29)


SLIDES = [slide_25, slide_26, slide_27, slide_28, slide_29]
