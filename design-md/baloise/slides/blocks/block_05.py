"""Block 5 - Debugging loop (slides 41-45).

LEARN -> SEE only; TRY and IMPROVE return in the Clinic, so the divider keeps
their chips as outlines. The distinction that carries the block: self-critique
asks whether an output is good enough, debugging asks why it failed.
Content is verbatim from the source deck; only the layout is ours.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, ASIDE_W, ASIDE_X, AVOID, BLUE, COL2_W, COL2_X,
                      CONTENT_W, GOOD, GREEN, GREY_TEXT, GUARDRAIL, MAIN_W,
                      MARGIN, NEUTRAL, T_BODY, T_CARD, T_HINT, T_LEAD, T_META,
                      T_STATEMENT, band, blue_slide, card, divider, eyebrow,
                      footer, lead, listing, new_slide, runs, textbox, title,
                      write)

LABEL = "05  Debugging loop"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_41(prs):
    s = blue_slide(prs)
    divider(s, "05", ["Debugging loop"],
            "Diagnose poor results instead of starting over.",
            chips=("LEARN", "SEE", "TRY", "IMPROVE"),
            ghost=("TRY", "IMPROVE"))
    _foot(s, None, 41)


def slide_42(prs):
    s = new_slide(prs)
    title(s, "Quality checking and failure diagnosis are not the same thing.")

    eyebrow(s, "Self-critique", x=COL2_X[0], w=COL2_W, colour=GOOD.accent)
    sc = card(s, COL2_X[0], 150, COL2_W, 258, GOOD.surface, pad=18)
    write(sc, [
        ("Is this output good enough?", T_CARD, True, GOOD.accent, None),
        ("You already know what good looks like, and you compare the output "
         "against criteria.", T_BODY, False, BLUE, 12),
        ("Example", T_META, True, GREY_TEXT, 16),
        ("Does this customer communication clearly explain the required next "
         "step?", T_HINT, False, BLUE, 4),
    ], anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Debugging", x=COL2_X[1], w=COL2_W, colour=AVOID.accent)
    db = card(s, COL2_X[1], 150, COL2_W, 258, NEUTRAL.surface, pad=18)
    write(db, [
        ("Why did this output fail?", T_CARD, True, AVOID.accent, None),
        ("The result is poor, but the reason is unclear, so you investigate "
         "the prompt and instructions.", T_BODY, False, BLUE, 12),
        ("Example", T_META, True, GREY_TEXT, 16),
        ("Why did the claims summary bury the key decision in paragraph "
         "five?", T_HINT, False, BLUE, 4),
    ], anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Key distinction",
         "Self-critique evaluates the output. Debugging diagnoses the cause.")
    _foot(s, "LEARN", 42)


def slide_43(prs):
    """Overflow risk: a four-question diagnosis plus the failure symptoms and
    the iterative-refinement related concept. Symptoms to the aside, the four
    questions as the main column, related concept to a strip."""
    s = new_slide(prs)
    title(s, "Before rewriting the prompt, identify what actually went wrong.")

    eyebrow(s, "Ask four questions", w=MAIN_W)
    questions = [
        ("1  What specifically failed?",
         "Too detailed; management-relevant information not prioritised."),
        ("2  Why might it have failed?",
         "The audience was named, but its information need was not defined."),
        ("3  What is missing or ambiguous?",
         "No length, prioritisation logic or required structure."),
        ("4  What one change should we test first?",
         "Define the management information need."),
    ]
    top, pitch = 146, 58
    for i, (q, a) in enumerate(questions):
        y = top + i * pitch
        cell = card(s, MARGIN, y, MAIN_W, pitch - 8, NEUTRAL.surface, pad=10)
        runs(cell, [(q + "   ", True, GREEN), (a, False, BLUE)],
             size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "The prompt that failed", x=ASIDE_X, w=ASIDE_W)
    failed = card(s, ASIDE_X, 146, ASIDE_W, 92, GUARDRAIL.surface, pad=12)
    write(failed, [("Summarise this claims performance report for senior "
                    "management.", T_HINT, False, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE)
    eyebrow(s, "The result was", x=ASIDE_X, w=ASIDE_W, y=250)
    result = card(s, ASIDE_X, 272, ASIDE_W, 118, NEUTRAL.surface, pad=12)
    write(result, [(t, T_HINT, False, BLUE, None if i == 0 else 6)
                   for i, t in enumerate((
                       "Three pages long",
                       "Full of operational detail",
                       "Missing the main trend",
                       "No decision highlighted"))],
          anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Key idea",
         "Diagnose → change one thing → rerun → compare.", GOOD)
    _foot(s, "LEARN", 43)


def slide_44(prs):
    s = new_slide(prs)
    title(s, "Ask for diagnosis before asking for another answer.")

    eyebrow(s, "Reusable prompt", w=COL2_W)
    prompt = card(s, MARGIN, 146, COL2_W, 296, NEUTRAL.surface, pad=18)
    write(prompt, [
        ("The result below did not meet my expectations.",
         T_BODY, False, BLUE, None),
        ("Do not rewrite it yet. Diagnose the failure:",
         T_BODY, True, BLUE, 8),
        ("1  What specifically is wrong with the result?",
         T_BODY, False, BLUE, 8),
        ("2  Which part of my prompt most likely caused it?",
         T_BODY, False, BLUE, 3),
        ("3  What instruction, context or criterion is missing?",
         T_BODY, False, BLUE, 3),
        ("4  What single change should we test first?",
         T_BODY, False, BLUE, 3),
        ("Then propose a revised prompt that changes only that issue. Do not "
         "execute it until I approve the change.",
         T_HINT, False, GREY_TEXT, 12),
    ])

    eyebrow(s, "Why one change?", x=COL2_X[1], w=COL2_W, colour=GUARDRAIL.accent)
    why = card(s, COL2_X[1], 146, COL2_W, 296, GUARDRAIL.surface, pad=20)
    write(why, [("If you change five things at once, you do not know what "
                 "actually improved the result.", T_LEAD, False, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "LEARN", 44)


def slide_45(prs):
    """Overflow risk: a multiple-choice diagnosis with the reveal and the
    one-change follow-up. Options as a chip row, the answer as a band."""
    s = new_slide(prs)
    title(s, "Do not fix the output. Fix the reason it failed.")
    lead(s, "Original task: summarise this monthly claims report for senior "
            "management.")

    eyebrow(s, "The weak result", x=COL2_X[0], w=COL2_W)
    weak = card(s, COL2_X[0], 150, COL2_W, 150, NEUTRAL.surface, pad=16)
    write(weak, [(t, T_HINT, False, BLUE, None if i == 0 else 6)
                 for i, t in enumerate((
                     "Reproduces most of the source",
                     "Too much operational detail",
                     "Does not identify the main change",
                     "Ends without a decision or action"))],
          anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "What is most likely missing?", x=COL2_X[1], w=COL2_W)
    opts = [("A", "More source information", False),
            ("B", "Clearer audience needs", True),
            ("C", "More professional wording", False),
            ("D", "A longer prompt", False)]
    for i, (letter, text, correct) in enumerate(opts):
        y = 150 + i * 40
        role = GOOD if correct else NEUTRAL
        cell = card(s, COL2_X[1], y, COL2_W, 34, role.surface, pad=10)
        runs(cell, [(f"{letter}   ", True,
                     GOOD.accent if correct else GREY_TEXT),
                    (text, correct, BLUE)],
             size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)

    change = card(s, MARGIN, 322, CONTENT_W, 56, GOOD.surface, pad=14)
    runs(change, [("Change one thing   ", True, GOOD.accent),
                  ("Focus only on material changes, business impact, risks "
                   "and decisions required. Maximum five bullets.",
                   False, BLUE)], size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Rerun",
         "Did the targeted change solve the actual problem?", GOOD)
    _foot(s, "SEE", 45)


SLIDES = [slide_41, slide_42, slide_43, slide_44, slide_45]
