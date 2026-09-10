"""Block 3 - Decomposition & plan-then-execute (slides 25-29).

LEARN -> SEE only; TRY and IMPROVE return in the Clinic. The two unused
cycle chips stay on the divider as outlines.
Content is verbatim from the source deck; only the layout is ours.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (icon, WHITE, CHOICE, ACTION, BLUE, COL2_W, COL2_X, CONTENT_W, GOOD, GREEN,
                      GREY_TEXT, GUARDRAIL, MARGIN, NEUTRAL, T_BODY, T_CARD,
                      T_DIVIDER, T_HINT, T_LEAD, T_META, T_NUMBER, T_STATEMENT,
                      arrow, band, blue_slide, card, divider, eyebrow,
                      flow_column, footer, lead, listing, new_slide, runs,
                      tangerine_slide, textbox, title, write)

LABEL = "03  Decomposition & plan-then-execute"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_25(prs):
    s = blue_slide(prs)
    divider(s, "03", ["Decomposition &", "plan-then-execute"],
            "Check the approach before creating the answer.",
            chips=("LEARN", "SEE", "TRY", "IMPROVE"),
            ghost=("TRY", "IMPROVE"))
    _foot(s, None, 25)


def slide_26(prs):
    s = new_slide(prs)
    title(s, "Decomposition breaks a complex task into manageable parts.")
    lead(s, "Example: plan a response to a surge in weather-related claims.")

    eyebrow(s, "One big task", x=COL2_X[0], w=COL2_W)
    big = card(s, COL2_X[0], 150, COL2_W, 258, NEUTRAL.surface, pad=18)
    write(big, [
        ("Analyse situation", T_BODY, True, GREY_TEXT, None),
        ("define response", T_BODY, False, BLUE, 6),
        ("plan operations", T_BODY, False, BLUE, 4),
        ("draft communication", T_BODY, False, BLUE, 4),
        ("prepare management view", T_BODY, False, BLUE, 4),
        ("All at once", T_HINT, False, GREY_TEXT, 14),
    ], anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Decomposed", x=COL2_X[1], w=COL2_W, colour=GREEN)
    steps = [
        ("1  Assess the situation", None),
        ("2  Identify affected groups", None),
        ("3  Define required actions", None),
        ("4  Plan communication", None),
        ("5  Prepare management view", None),
    ]
    top, pitch = 150, 51
    for i, (heading, _b) in enumerate(steps):
        cell = card(s, COL2_X[1], top + i * pitch, COL2_W, pitch - 9,
                    GOOD.surface, pad=10)
        write(cell, [(heading, T_BODY, True, GOOD.accent, None)],
              anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Key idea",
         "Smaller steps create more opportunities to steer the work.", GOOD)
    _foot(s, "LEARN", 26)


def slide_27(prs):
    """FLOW twin - two parallel flows. Known overflow risk (ARCHETYPES.md):
    both 5-step flows, both captions, the use-when line and the Chain-of-
    Thought related concept all have to share one slide, so the flow cells are
    compact and the two footnotes become slim full-width strips."""
    s = new_slide(prs)
    title(s, "One big task gives you one late control point.", has_lead=False)

    eyebrow(s, "Execute immediately", x=COL2_X[0], w=COL2_W, y=110)
    eyebrow(s, "Plan first", x=COL2_X[1], w=COL2_W, y=110, colour=GOOD.accent)

    flow_column(s, COL2_X[0], COL2_W, [
        ("Complex task", None),
        ("AI chooses an approach", None),
        ("AI makes assumptions", None),
        ("Full output", None),
        ("You review", None),
    ], top=132, cell_h=26, gap=16, role=NEUTRAL, size=T_HINT, pad=4)

    flow_column(s, COL2_X[1], COL2_W, [
        ("Complex task", None),
        ("AI proposes approach", None),
        ("You review", None),
        ("Adjust", None),
        ("AI executes", None),
    ], top=132, cell_h=26, gap=16, role=GOOD, size=T_HINT, pad=4)

    problem = card(s, COL2_X[0], 332, COL2_W, 40, NEUTRAL.surface, pad=10)
    runs(problem, [("Problem   ", True, GREY_TEXT),
                   ("Wrong direction becomes visible late.", False, BLUE)],
         size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)
    benefit = card(s, COL2_X[1], 332, COL2_W, 40, GOOD.surface, pad=10)
    runs(benefit, [("Benefit   ", True, GOOD.accent),
                   ("Correct the direction before producing everything.",
                    False, BLUE)],
         size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)

    use = card(s, MARGIN, 378, CONTENT_W, 34, GOOD.surface, pad=10)
    runs(use, [("Use when the task is   ", True, GOOD.accent),
               ("complex, multi-step, ambiguous or expensive to redo.",
                False, BLUE)], size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)
    cot = card(s, MARGIN, 416, CONTENT_W, 56, NEUTRAL.surface, pad=10)
    runs(cot, [("Related concept — chain of thought   ", True,
                BLUE),
               ("Models may reason step by step; for prompting, focus on "
                "reviewable intermediate outputs (plans, assumptions, "
                "criteria, decision points).", False, BLUE)],
         size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "LEARN", 27)


def slide_28(prs):
    s = new_slide(prs)
    title(s, "Ask for the plan before asking for the deliverable.")

    eyebrow(s, "Reusable prompt", w=COL2_W)
    prompt = card(s, MARGIN, 146, COL2_W, 296, NEUTRAL.surface, pad=18)
    write(prompt, [
        ("I need to complete the following task: [describe complex task].",
         T_BODY, False, BLUE, None),
        ("Do not execute the task yet. First:", T_BODY, True, BLUE, 10),
        ("1  Break it into 4–6 logical steps.", T_BODY, False, BLUE, 8),
        ("2  Explain the purpose of each step.", T_BODY, False, BLUE, 3),
        ("3  Identify dependencies and assumptions.", T_BODY, False, BLUE, 3),
        ("4  Flag missing information or open decisions.",
         T_BODY, False, BLUE, 3),
        ("5  Recommend the execution order.", T_BODY, False, BLUE, 3),
        ("Return the plan only. Wait for my feedback before proceeding.",
         T_HINT, False, GREY_TEXT, 12),
    ])

    eyebrow(s, "Use when", x=COL2_X[1], w=COL2_W, colour=GOOD.accent)
    use = card(s, COL2_X[1], 146, COL2_W, 132, GOOD.surface, pad=18)
    write(use, [("You want to review the approach before investing in the "
                 "full output.", T_LEAD, False, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Prompt chaining", x=COL2_X[1], w=COL2_W,
            y=294)
    chain = card(s, COL2_X[1], 316, COL2_W, 126, NEUTRAL.surface, pad=18)
    write(chain, [
        ("One output becomes the input to the next step.",
         T_BODY, False, BLUE, None),
        ("Analyse → Plan → Draft → Review → Finalise",
         T_BODY, True, BLUE, 10),
    ], anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "LEARN", 28)


def slide_29(prs):
    s = new_slide(prs)
    title(s, "Would you approve the approach before letting AI execute it?")
    lead(s, "You need an internal launch plan for a new customer feature.")

    eyebrow(s, "Version 1", x=COL2_X[0], w=COL2_W, y=128)
    v1 = card(s, COL2_X[0], 150, COL2_W, 108, NEUTRAL.surface, pad=16)
    write(v1, [("Create a complete internal launch plan for the new feature.",
                T_BODY, False, BLUE, None)], anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Version 2", x=COL2_X[1], w=COL2_W, colour=GOOD.accent)
    v2 = card(s, COL2_X[1], 150, COL2_W, 108, GOOD.surface, pad=16)
    write(v2, [("First propose the workplan and sequence. Identify audiences, "
                "dependencies, assumptions and open decisions. Do not create "
                "material yet.", T_HINT, False, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Review before execution", y=276)
    x = MARGIN
    for q in ("All audiences covered?", "Sequence realistic?",
              "Dependencies visible?", "Decisions unresolved?"):
        chip = card(s, x, 300, 205, 66, None, outline=CHOICE.surface, pad=10)
        write(chip, [(q, T_HINT, True, WHITE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += 205 + 19

    band(s, "Decision", "Approve → Adjust → Then execute", GOOD)
    _foot(s, "SEE", 29)


def slide_30(prs):
    """The break. It was three lines on an empty field; the clock time is the
    one thing people need to read from the back of the room."""
    s = blue_slide(prs)
    write(textbox(s, MARGIN, 120, CONTENT_W, 66),
          [("10-minute break", T_DIVIDER, True, WHITE, None)])

    clock = card(s, MARGIN, 208, 428, 120, WHITE, pad=24)
    icon(s, "clock", MARGIN + 28, 240, 30, BLUE)
    write(textbox(s, MARGIN + 76, 234, 330, 80),
          [("We continue at", T_BODY, False, BLUE, None),
           ("[CLOCK TIME]", T_STATEMENT, True, BLUE, 2)])

    open_note = card(s, 491, 208, 428, 120, WHITE, pad=24)
    icon(s, "message", 491 + 28, 240, 30, BLUE)
    write(textbox(s, 491 + 76, 234, 330, 80),
          [("Submitted a case?", T_CARD, True, BLUE, None),
           ("The trainers are reviewing the cases during the break.",
            T_BODY, False, BLUE, 4)])

    strip = card(s, MARGIN, 352, CONTENT_W, 48, WHITE, pad=14)
    runs(strip, [("Still open   ", True, BLUE),
                 ("Prompt Clinic submissions remain open until we restart.",
                  False, BLUE)], size=T_LEAD)
    footer(s, "Break", None, 30)


SLIDES = [slide_25, slide_26, slide_27, slide_28, slide_29, slide_30]
