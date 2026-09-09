"""Block 0 - Opening (slides 1-6).

Title, learning objective, scope, agenda and the two Slido interactions.
Content is verbatim from the source deck; only the layout is ours.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, BLUE, CONTENT_W, GOOD, GREY_TEXT, GUARDRAIL,
                      MARGIN, NEUTRAL, T_BODY, T_CARD, T_HINT, T_LEAD, T_META,
                      T_STATEMENT, WHITE, band, blue_slide, card, divider,
                      eyebrow, footer, lead, listing, new_slide, runs,
                      textbox, title, write)

LABEL = "Prompting Workshop — Session 2"

# a chip row of options for the two Slido interactions ------------------------
CHIP_H = 46
CHIP_GAP = 17


def _foot(slide, number):
    footer(slide, LABEL, None, number)


def _slido(slide, code_hint, note, y):
    """The recurring 'go to Slido' call to action, in the participation colour."""
    strip = card(slide, MARGIN, y, CONTENT_W, 54, ACTION.surface, pad=16)
    runs(strip, [("Go to Slido   ", True, ACTION.accent),
                 (code_hint, True, BLUE),
                 (f"    {note}" if note else "", False, GREY_TEXT)],
         size=T_LEAD, anchor=MSO_ANCHOR.MIDDLE)
    return strip


def _option_chips(slide, options, top, per_row):
    """Wrap option labels into evenly spaced chips over `per_row` per row."""
    width = (CONTENT_W - (per_row - 1) * CHIP_GAP) / per_row
    for i, text in enumerate(options):
        row, col = divmod(i, per_row)
        x = MARGIN + col * (width + CHIP_GAP)
        y = top + row * (CHIP_H + CHIP_GAP)
        chip = card(slide, x, y, width, CHIP_H, None, outline=ACTION.accent,
                    pad=8)
        write(chip, [(text, T_BODY, False, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def slide_01(prs):
    s = blue_slide(prs)
    write(textbox(s, MARGIN, 84, CONTENT_W, 24),
          [("PROMPTING WORKSHOP — SESSION 2", T_META, True, WHITE, None)])
    divider(s, "", ["Advanced prompting", "for recurring work"],
            "Five techniques, three practice rounds and a Prompt Clinic.")


def slide_02(prs):
    s = new_slide(prs)
    title(s, "Five techniques. One goal.")
    lead(s, "Use advanced prompting techniques to get more consistent, "
            "controllable and reusable results from AI.")

    eyebrow(s, "By the end of this session, you should be able to")
    listing(s, [
        ("1", "Recognise which prompting problem you are facing.", None),
        ("2", "Choose an appropriate technique.", None),
        ("3", "Apply it to your own recurring work.", None),
        ("4", "Improve a prompt without simply starting over.", None),
    ], top=150, span=280)
    _foot(s, 2)


def slide_03(prs):
    s = new_slide(prs)
    title(s, "What we will not cover today.")
    lead(s, "Today builds on basic prompting principles.")

    eyebrow(s, "We will not revisit")
    listing(s, [
        (None, "LLM fundamentals", None),
        (None, "Prompting fundamentals and the prompt as a briefing", None),
        (None, "The six basic prompt components", None),
        (None, "Providing source material", None),
        (None, "Basic data protection and tool rules", None),
    ], role=NEUTRAL, top=148, span=252)

    band(s, "Missing one of these?",
         "You can still participate today. Everything is available in the "
         "Academy.", GOOD)
    _foot(s, 3)


def slide_04(prs):
    s = new_slide(prs)
    title(s, "Today’s agenda.", has_lead=False)

    eyebrow(s, "Five prompting techniques")
    listing(s, [
        ("01", "Few-shot & negative examples", None),
        ("02", "Persistent context & system instructions", None),
        ("03", "Decomposition & plan-then-execute", None),
        ("04", "Self-critique, rubrics & guardrails", None),
        ("05", "Debugging loop", None),
    ], top=148, span=196)

    apply = card(s, MARGIN, 364, 428, 96, ACTION.surface, pad=16)
    write(apply, [("Apply — Prompt Clinic", T_CARD, True, ACTION.accent, None),
                  ("Apply the techniques to real prompting challenges.",
                   T_BODY, False, BLUE, 6)], anchor=MSO_ANCHOR.MIDDLE)
    transfer = card(s, 491, 364, 428, 96, ACTION.surface, pad=16)
    write(transfer, [("Transfer", T_CARD, True, ACTION.accent, None),
                     ("Build and save a prompt you can use in your own work.",
                      T_BODY, False, BLUE, 6)], anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, 4)


def slide_05(prs):
    s = new_slide(prs)
    eyebrow(s, "Interact", colour=ACTION.accent)
    title(s, "How do you use AI today?")
    lead(s, "Choose the two activities you currently use AI for most often.")

    _option_chips(s, ("Drafting", "Summarising", "Ideation", "Research",
                      "Analysis", "Planning", "Other"), top=150, per_row=4)
    _slido(s, "[SLIDO CODE]", "Pick two.", y=406)
    _foot(s, 5)


def slide_06(prs):
    s = new_slide(prs)
    eyebrow(s, "Interact", colour=ACTION.accent)
    title(s, "Which recurring task would you most like to improve with AI?")
    lead(s, "Submit one task or prompt we could use later in the Prompt "
            "Clinic.")

    eyebrow(s, "A good submission is", y=150)
    listing(s, [
        (None, "Recurring", None),
        (None, "Concrete", None),
        (None, "Understandable without specialist knowledge", None),
        (None, "Safe to discuss with the group", None),
    ], top=174, span=150)

    guard = card(s, MARGIN, 336, CONTENT_W, 50, GUARDRAIL.surface, pad=14)
    runs(guard, [("Keep it generic   ", True, GUARDRAIL.accent),
                 ("Do not enter personal, customer or confidential "
                  "information.", False, BLUE)],
         size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)
    _slido(s, "[SLIDO CODE]", "Submissions remain open until the break.",
           y=398)
    _foot(s, 6)


SLIDES = [slide_01, slide_02, slide_03, slide_04, slide_05, slide_06]
