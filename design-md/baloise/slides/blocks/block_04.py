"""Block 4 - Self-critique, rubrics & guardrails (slides 31-40).

Ten slides, full LEARN -> SEE -> TRY -> IMPROVE cycle. GUARDRAIL (purple) is
central here: slide 34 defines guardrails, and they read as rules, not don'ts.
Content is verbatim from the source deck; only the layout is ours.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

from slidekit import (icon, bullet_list, WHITE, CHOICE, ACTION, ASIDE_W, ASIDE_X, AVOID, BLUE, COL2_W, COL2_X,
                      CONTENT_TOP_LEAD,
                      CONTENT_W, GOOD, GREEN, GREY_TEXT, GUARDRAIL, MAIN_W,
                      MARGIN, NEUTRAL, T_BODY, T_CARD, T_HINT, T_LEAD, T_META,
                      T_STATEMENT, badge, band, blue_slide, card, divider,
                      eyebrow, flow_row, footer, lead, listing, new_slide,
                      runs, textbox, title, write)

LABEL = "04  Self-critique, rubrics & guardrails"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_31(prs):
    s = blue_slide(prs)
    divider(s, "04", ["Self-critique, rubrics", "& guardrails"],
            "Define what “good” means — then check against it.",
            chips=("LEARN", "SEE", "TRY", "IMPROVE"))
    _foot(s, None, 31)


def slide_32(prs):
    """Overflow risk: four criteria + the 'improve is not enough' framing +
    the rubric related concept. Criteria go in a 2x2 grid, rubric to a strip."""
    s = new_slide(prs)
    title(s, "Say what “good” means before you ask AI to improve something.")
    lead(s, "“Improve this communication” does not define what better means.")

    eyebrow(s, "The criteria", y=CONTENT_TOP_LEAD)
    criteria = [
        ("Be clear", "Can a non-expert understand what is changing?"),
        ("Be concise", "Does it avoid unnecessary background?"),
        ("Explain impact", "Does the customer understand what it means for "
         "them?"),
        ("Give a next step", "Do they know what to do?"),
    ]
    for i, (head, q) in enumerate(criteria):
        x = COL2_X[i % 2]
        y = 162 + (i // 2) * 96
        cell = card(s, x, y, COL2_W, 84, NEUTRAL.surface, pad=16)
        write(cell, [(head, T_CARD, True, BLUE, None),
                     (q, T_HINT, False, BLUE, 4)], anchor=MSO_ANCHOR.MIDDLE)

    rubric = card(s, MARGIN, 362, CONTENT_W, 60, NEUTRAL.surface, pad=14)
    runs(rubric, [("Related concept — rubric   ", True, GREY_TEXT),
                  ("A structured set of criteria used to evaluate an output. "
                   "Match the number and detail of criteria to the task.",
                   False, BLUE)], size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Key idea",
         "Explicit criteria turn “better” into something you can inspect.")
    _foot(s, "LEARN", 32)


def slide_33(prs):
    s = new_slide(prs)
    title(s, "Make the model evaluate before asking it to revise.")

    flow_row(s, [
        ("1  Draft", "Create version 1."),
        ("2  Evaluate", "Compare against criteria."),
        ("3  Identify gaps", "Where does it fall short?"),
        ("4  Revise", "Change where gaps were found."),
    ], top=150, cell_h=118, gap=20, role=NEUTRAL, head_colour=GREEN)

    eyebrow(s, "Example", y=288)
    ex = [
        ("Criterion", "The customer should understand the required action "
         "within 10 seconds.", GOOD),
        ("Finding", "The required action appears only in the final "
         "paragraph.", NEUTRAL),
        ("Revision", "Move the action to the beginning.", GOOD),
    ]
    x = MARGIN
    w = (CONTENT_W - 2 * 18) / 3
    for head, body, role in ex:
        cell = card(s, x, 310, w, 88, role.surface, pad=12)
        write(cell, [(head, T_BODY, True,
                      role.accent if role is GOOD else GREY_TEXT, None),
                     (body, T_HINT, False, BLUE, 4)],
              anchor=MSO_ANCHOR.MIDDLE)
        x += w + 18

    band(s, "Key idea",
         "A useful critique explains why a change is needed.", GOOD)
    _foot(s, "LEARN", 33)


def slide_34(prs):
    """Five rules in a row said nothing on their own. Setting the failure
    beside them shows what the rules are for."""
    s = new_slide(prs)
    title(s, "Tell AI what to do when the information is missing.")
    lead(s, "If the source does not say why a premium changed, AI may try to "
            "complete the story.")

    eyebrow(s, "Without a rule", x=MARGIN, w=328)
    gap = card(s, MARGIN, 176, 328, 250, AVOID.surface, pad=20)
    icon(s, "alert-triangle", MARGIN + 20, 196, 26, AVOID.accent)
    write(gap, [
        ("The model fills the gap", T_CARD, True, AVOID.accent, None),
        ("It invents a plausible reason, states it as fact, and the reader "
         "has no way to tell which part was in the source.",
         T_BODY, False, BLUE, 10),
    ], anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Expected behaviour", x=424, w=495)
    rules = card(s, 424, 176, 495, 250, NEUTRAL.surface, pad=20)
    bullet_list(rules, (
        "If the reason is not provided, do not infer one.",
        "Flag missing information explicitly.",
        "Separate confirmed facts from assumptions.",
        "Do not promise outcomes unsupported by the source material.",
        "Ask for clarification when missing information changes the answer.",
    ), size=T_BODY, marker="→")
    rules.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    band(s, "Key idea",
         "Guardrails define acceptable behaviour when the task cannot be "
         "completed confidently.")
    _foot(s, "LEARN", 34)


def slide_35(prs):
    s = new_slide(prs)
    title(s, "A self-check gives you control, not proof.")

    eyebrow(s, "It can help check", x=COL2_X[0], w=COL2_W, colour=GOOD.accent)
    can = card(s, COL2_X[0], 150, COL2_W, 214, GOOD.surface, pad=18)
    write(can, [(t, T_BODY, False, BLUE, None if i == 0 else 8)
                for i, t in enumerate((
                    "Whether stated criteria were followed",
                    "Whether obvious elements are missing",
                    "Whether structure and clarity improved",
                    "Whether instructions conflict"))],
          anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "It cannot prove", x=COL2_X[1], w=COL2_W, colour=AVOID.accent)
    cannot = card(s, COL2_X[1], 150, COL2_W, 214, AVOID.surface, pad=18)
    write(cannot, [(t, T_BODY, False, BLUE, None if i == 0 else 8)
                   for i, t in enumerate((
                       "Factual accuracy",
                       "Completeness",
                       "Correct policy interpretation",
                       "Legal or regulatory compliance",
                       "That every error was detected"))],
          anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Key idea",
         "Use self-critique to improve control — not to outsource "
         "validation.", GOOD)
    _foot(s, "LEARN", 35)


def slide_36(prs):
    """Overflow risk: a long reusable prompt. Give it the full width."""
    s = new_slide(prs)
    title(s, "Evaluate against criteria before revising.")

    eyebrow(s, "Reusable prompt", w=MAIN_W)
    prompt = card(s, MARGIN, 146, MAIN_W, 296, NEUTRAL.surface, pad=18)
    write(prompt, [
        ("Review the draft below against the following criteria:",
         T_BODY, False, BLUE, None),
        ("1 [criterion]   2 [criterion]   3 [criterion]   4 [criterion]",
         T_BODY, True, BLUE, 8),
        ("For each criterion:", T_BODY, True, BLUE, 10),
        ("rate it Met / Partly met / Not met, explain your reasoning "
         "briefly, and identify the relevant part of the draft.",
         T_HINT, False, GREY_TEXT, 3),
        ("Then:", T_BODY, True, BLUE, 10),
        ("1  Identify the two most important gaps.", T_BODY, False, BLUE, 6),
        ("2  Explain what should change.", T_BODY, False, BLUE, 3),
        ("3  Produce one revised version.", T_BODY, False, BLUE, 3),
        ("If essential information is missing, flag it instead of inventing "
         "it.", T_HINT, False, BLUE, 10),
    ])

    eyebrow(s, "Use when", x=ASIDE_X, w=ASIDE_W, colour=GOOD.accent)
    use = card(s, ASIDE_X, 146, ASIDE_W, 296, GOOD.surface, pad=16)
    write(use, [("You have a draft and can define observable quality "
                 "criteria.", T_LEAD, False, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "LEARN", 36)


def slide_37(prs):
    s = new_slide(prs)
    title(s, "Do clear criteria make the second version better?")
    lead(s, "We need to communicate a change to how customers submit claim "
            "documents.")

    eyebrow(s, "The four criteria", w=MAIN_W)
    listing(s, [
        ("1", "Explain what is changing", None),
        ("2", "Explain what the customer needs to do", None),
        ("3", "Use plain language", None),
        ("4", "Avoid unsupported assumptions or promises", None),
    ], top=150, span=196, width=MAIN_W)

    eyebrow(s, "Process", x=ASIDE_X, w=ASIDE_W, colour=GREEN)
    proc = card(s, ASIDE_X, 150, ASIDE_W, 140, GOOD.surface, pad=14)
    write(proc, [(t, T_BODY, True, GOOD.accent, None if i == 0 else 8)
                 for i, t in enumerate(
                     ("Draft", "Evaluate", "Identify gaps", "Revise"))],
          anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Watch for",
         "Does version 2 improve because the criteria exposed a real gap?")
    _foot(s, "SEE", 37)


def slide_38(prs):
    s = new_slide(prs)
    title(s, "A good revision fixes the gap, not just the wording.")

    eyebrow(s, "Version 1", x=COL2_X[0], w=COL2_W)
    v1 = card(s, COL2_X[0], 146, COL2_W, 132, NEUTRAL.surface, pad=16)
    write(v1, [("We are continuously improving our claims services and would "
                "like to inform you of an adjustment to the process for "
                "providing additional documents. In future, supporting "
                "documents can be submitted digitally.",
                T_HINT, False, BLUE, None)], anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Self-critique", x=COL2_X[0], w=COL2_W, y=286)
    crit = card(s, COL2_X[0], 308, COL2_W, 134, NEUTRAL.surface, pad=14)
    write(crit, [
        ("Clear change? Partly.", T_HINT, False, BLUE, None),
        ("Clear customer action? No.", T_HINT, False, BLUE, 5),
        ("Plain language? Partly.", T_HINT, False, BLUE, 5),
        ("Unsupported content? “Continuously improving” is unnecessary.",
         T_HINT, False, BLUE, 5),
    ], anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Version 2", x=COL2_X[1], w=COL2_W, colour=GOOD.accent)
    v2 = card(s, COL2_X[1], 146, COL2_W, 232, GOOD.surface, pad=16)
    write(v2, [
        ("Need to send us additional documents for your claim?",
         T_BODY, True, GOOD.accent, None),
        ("You can now upload them directly through our online service.",
         T_HINT, False, BLUE, 8),
        ("What you need to do: use the upload link provided with your claim "
         "information and add the requested documents there.",
         T_HINT, False, BLUE, 8),
        ("If no additional documents are requested, no action is required.",
         T_HINT, False, BLUE, 8),
    ], anchor=MSO_ANCHOR.MIDDLE)

    imp = card(s, COL2_X[1], 388, COL2_W, 54, GOOD.surface, pad=12)
    runs(imp, [("Improved   ", True, GOOD.accent),
               ("faster orientation, clearer action, less wording.",
                False, BLUE)], size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "SEE", 38)


def slide_39(prs):
    s = new_slide(prs)
    title(s, "Improve one of your earlier outputs.", width=729)
    lead(s, "Your task")
    badge(s, "Time  4 min")

    steps = [
        ("1", "Choose an output you created earlier.", None),
        ("2", "Define 3–5 criteria for a strong result.",
         "Clear, concise, audience-appropriate, actionable, complete enough."),
        ("3", "Ask AI to evaluate the output.", None),
        ("4", "Review its diagnosis — do you agree?", None),
        ("5", "Ask for one revised version.", None),
    ]
    top, pitch = 150, 52
    for i, (num, text, hint) in enumerate(steps):
        y = top + i * pitch
        cell = card(s, MARGIN, y, CONTENT_W, pitch - 8, ACTION.surface,
                    pad=8)
        rows = [(f"{num}   ", True, ACTION.accent), (text, True, BLUE)]
        if hint:
            rows.append(("  —  " + hint, False, GREY_TEXT))
        runs(cell, rows, size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Final check",
         "Is version 2 actually better according to your criteria?", ACTION)
    _foot(s, "TRY", 39)


def slide_40(prs):
    s = new_slide(prs)
    title(s, "Did the critique create a better result?")
    lead(s, "Rate version 2.")

    x = MARGIN
    labels = ["1 — No improvement", "2", "3", "4", "5 — Clearly better"]
    for text in labels:
        chip = card(s, x, 158, 163, 84, None, outline=CHOICE.surface, pad=8)
        write(chip, [(text, T_BODY, False, WHITE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += 163 + 16

    eyebrow(s, "What made the difference", y=262)
    x = MARGIN
    w = (CONTENT_W - 3 * 16) / 4
    for text in ("Better criteria?", "An identified gap?", "Clearer "
                 "guardrails?", "Different wording?"):
        cell = card(s, x, 286, w, 62, NEUTRAL.surface, pad=12)
        write(cell, [(text, T_HINT, True, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += w + 16

    cta = card(s, MARGIN, 366, CONTENT_W, 76, ACTION.surface, pad=18)
    runs(cta, [("In the chat   ", True, ACTION.accent),
               ("Share your rating: 1–5.", False, BLUE)],
         size=T_STATEMENT, anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "IMPROVE", 40)


SLIDES = [slide_31, slide_32, slide_33, slide_34, slide_35, slide_36,
          slide_37, slide_38, slide_39, slide_40]
