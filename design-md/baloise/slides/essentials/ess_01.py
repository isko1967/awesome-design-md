"""01 - How AI answers (slides 6-12).

The vague prompt, the first demo, how the model produces text, the two
limits it brings with it, the data rules and the check-you-skipped poll.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (AVOID, BLUE, COL2_W, COL2_X, COL3_W, COL3_X, CONTENT_W,
                      GOOD, MARGIN, NEUTRAL, T_BODY, T_CARD, T_HINT, T_LEAD,
                      T_STATEMENT, band, card, eyebrow, footer, lead,
                      listing, new_slide, runs, task_header, textbox, title,
                      write)
from essentials.ess_00 import lettered_chips, slido

LABEL = "01  How AI answers"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_06(prs):
    s = new_slide(prs)
    title(s, "Look at this prompt for ten seconds.", has_lead=False)

    eyebrow(s, "The prompt", y=150)
    prompt = card(s, MARGIN, 182, CONTENT_W, 236, NEUTRAL.surface, pad=24)
    write(prompt, [("“Write a project update.”", T_STATEMENT, True, BLUE,
                    None)],
          anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    band(s, "In the chat",
         "What could go wrong here? What does the AI not know?")
    _foot(s, "INTERACT", 6)


def slide_07(prs):
    s = new_slide(prs)
    title(s, "The output sounds fine — but it guessed the task.", width=729)
    task_header(s, "Demo 1", "First run")

    listing(s, [
        (None, "The audience is unclear.", None),
        (None, "The purpose is assumed.", None),
        (None, "The delay may be buried.", None),
        (None, "No action or deadline is visible.", None),
    ], role=AVOID, top=150, span=260)

    band(s, "Remember", "Fluent is not the same as fit for purpose.")
    _foot(s, "SEE", 7)


def slide_08(prs):
    s = new_slide(prs)
    title(s, "How AI produces an answer.")
    lead(s, "It predicts likely language from the context available now.")

    good = card(s, COL2_X[0], 150, COL2_W, 210, NEUTRAL.surface, pad=20)
    write(good, [
        ("Good at sounding right", T_CARD, True, BLUE, None),
        ("It is optimised to produce text that reads like the kind of text "
         "you asked for.", T_BODY, False, BLUE, 10),
    ], anchor=MSO_ANCHOR.MIDDLE)

    blind = card(s, COL2_X[1], 150, COL2_W, 210, AVOID.surface, pad=20)
    write(blind, [
        ("Blind to what you withheld", T_CARD, True, AVOID.accent, None),
        ("No memory of your project, no access to your inbox, no sense of "
         "your audience — unless you supply it.", T_BODY, False, BLUE, 10),
    ], anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Two consequences",
         "Both of them are your job, not the tool’s.")
    _foot(s, "LEARN", 8)


def slide_09(prs):
    s = new_slide(prs)
    title(s, "Whatever you leave unsaid becomes a guess.", has_lead=False)

    eyebrow(s, "The working test", y=152)
    belongs = card(s, COL2_X[0], 188, COL2_W, 190, GOOD.surface, pad=20)
    write(belongs, [
        ("Put it in the prompt", T_CARD, True, GOOD.accent, None),
        ("What would change the answer if the AI knew it? That belongs in "
         "the prompt.", T_BODY, False, BLUE, 10),
    ], anchor=MSO_ANCHOR.MIDDLE)

    leave = card(s, COL2_X[1], 188, COL2_W, 190, AVOID.surface, pad=20)
    write(leave, [
        ("Leave it out", T_CARD, True, AVOID.accent, None),
        ("Anything else does not — more context is not automatically better "
         "context.", T_BODY, False, BLUE, 10),
    ], anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "LEARN", 9)


def slide_10(prs):
    s = new_slide(prs)
    title(s, "Confident can still be wrong.")
    lead(s, "It does not signal uncertainty the way a colleague would.")

    eyebrow(s, "Always check by hand", y=150)
    for i, item in enumerate(("Every figure", "Every name", "Every date")):
        cell = card(s, COL3_X[i], 186, COL3_W, 112, NEUTRAL.surface, pad=14)
        write(cell, [(item, T_CARD, True, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    audience = card(s, MARGIN, 320, CONTENT_W, 90, NEUTRAL.surface, pad=16)
    write(audience, [("And whether this is appropriate for the audience at "
                      "all.", T_BODY, True, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    band(s, "The rule", "Co-pilot, not autopilot.")
    _foot(s, "LEARN", 10)


def slide_11(prs):
    s = new_slide(prs)
    title(s, "Pause before you paste.")
    lead(s, "Same rules as any other tool that leaves your desk.")

    items = [
        ("Approved tool", "[APPROVED INTERNAL AI TOOL]"),
        ("Permitted information", "[INTERNAL DATA-HANDLING GUIDANCE]"),
        ("Describe, don’t paste",
         "When in doubt, describe the situation generically instead of "
         "pasting the source material."),
    ]
    for i, (head, body) in enumerate(items):
        cell = card(s, COL3_X[i], 150, COL3_W, 176, NEUTRAL.surface, pad=16)
        write(cell, [(head, T_CARD, True, BLUE, None),
                     (body, T_HINT, False, BLUE, 10)],
              anchor=MSO_ANCHOR.MIDDLE)

    rule = card(s, MARGIN, 348, CONTENT_W, 66, AVOID.surface, pad=16)
    runs(rule, [("Rule of thumb   ", True, AVOID.accent),
                ("No personal, customer or confidential information — in "
                 "this session or in your own work.", False, BLUE)],
         size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "LEARN", 11)


def slide_12(prs):
    s = new_slide(prs)
    title(s, "Which check did you skip last time?")
    lead(s, "Think of the last time you used AI output at work.")

    lettered_chips(s, [
        ("A", "Facts and figures"),
        ("B", "Sensitive information"),
        ("C", "Audience fit"),
        ("D", "None — I checked all three"),
    ], top=150)

    slido(s, "[SLIDO CODE]", "2 min.", y=372)
    _foot(s, "INTERACT", 12)


SLIDES = [slide_06, slide_07, slide_08, slide_09, slide_10, slide_11,
          slide_12]
