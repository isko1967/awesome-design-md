"""05 - Transfer & close (slides 30-31) and the appendix (32-35).

The transfer practice, the four things to remember, and the reference
material that is not presented in the 120 minutes.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, BLUE, CONTENT_W, GOOD, GREEN, MARGIN, NEUTRAL,
                      T_BODY, T_CARD, T_DIVIDER, T_HINT, T_LEAD, T_META,
                      T_STATEMENT, WHITE, band, blue_slide, card, divider,
                      eyebrow, footer, lead, listing, new_slide, runs,
                      task_header, textbox, title, write)

LABEL = "05  Transfer & close"
APPENDIX = "Appendix"


def slide_30(prs):
    s = new_slide(prs)
    title(s, "Write the prompt you will use next time.", width=729)
    task_header(s, "Your task", "6 min")

    steps = [
        ("1", "Pick one task you do repeatedly."),
        ("2", "Write the complete prompt you will use next time."),
        ("3", "Save it where you will actually find it again."),
    ]
    top, pitch = 156, 76
    for i, (num, text) in enumerate(steps):
        cell = card(s, MARGIN, top + i * pitch, CONTENT_W, pitch - 12,
                    ACTION.surface, pad=14)
        runs(cell, [(f"{num}   ", True, GREEN), (text, True, BLUE)],
             size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Not in a chat window that closes",
         "A prompt you cannot find again is a prompt you will rewrite.")
    footer(s, LABEL, "TRY", 30)


def slide_31(prs):
    s = new_slide(prs)
    title(s, "The four things to take with you.", has_lead=False)

    listing(s, [
        ("01", "A prompt is a briefing, not a command.", None),
        ("02", "Whatever you leave unsaid becomes a guess.", None),
        ("03", "Change one thing so you can see what worked.", None),
        ("04", "Confident is not correct — check figures, names, dates, "
               "audience.", None),
    ], top=160, span=272)
    footer(s, LABEL, None, 31)


def slide_32(prs):
    s = blue_slide(prs)
    divider(s, "A", ["Appendix"],
            "Reference material — not presented in the 120 minutes.")
    footer(s, APPENDIX, None, 32)


def slide_33(prs):
    s = new_slide(prs)
    title(s, "Terms you may hear.", has_lead=False)

    terms = [
        ("Artificial intelligence",
         "The broad field of systems performing tasks that need "
         "intelligence."),
        ("Machine learning",
         "Systems that learn patterns from data rather than following "
         "written rules."),
        ("Deep learning",
         "Machine learning using neural networks with many layers."),
        ("Generative AI",
         "Models that produce new content rather than only classifying "
         "existing content."),
        ("Large language model",
         "A generative model for text. This is what you are prompting."),
        ("Context",
         "Everything the model can see right now: your instruction, your "
         "input, the conversation so far."),
    ]
    top, pitch = 146, 48
    for i, (term, meaning) in enumerate(terms):
        cell = card(s, MARGIN, top + i * pitch, CONTENT_W, pitch - 8,
                    NEUTRAL.surface, pad=10)
        runs(cell, [(term + "   ", True, BLUE), (meaning, False, BLUE)],
             size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "Why this is in the appendix",
         "None of these distinctions change how you write a prompt.")
    footer(s, APPENDIX, None, 33)


def slide_34(prs):
    s = new_slide(prs)
    title(s, "The six blocks as questions.", has_lead=False)

    blocks = [
        ("Task", "What should AI do? Name the action and the outcome.",
         True),
        ("Context", "What does it need to know that it cannot infer?", True),
        ("Format",
         "What should the result look like? Headings, length, structure.",
         True),
        ("Role", "Whose perspective would produce a better answer?", False),
        ("Example",
         "Can I show what acceptable looks like instead of describing it?",
         False),
        ("Tone", "Who is reading this, and how should it sound to them?",
         False),
    ]
    top, pitch = 146, 48
    for i, (block, question, essential) in enumerate(blocks):
        role = GOOD if essential else NEUTRAL
        cell = card(s, MARGIN, top + i * pitch, CONTENT_W, pitch - 8,
                    role.surface, pad=10)
        runs(cell, [(block + "   ", True,
                     GOOD.accent if essential else BLUE),
                    (question, False, BLUE)],
             size=T_HINT, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "And always",
         "Say what to do when information is missing — and change one thing "
         "at a time when improving.")
    footer(s, APPENDIX, None, 34)


def slide_35(prs):
    """The close. The source's production note ("replace every placeholder")
    is a build reminder, not participant content, so it moves to the
    speaker notes."""
    s = blue_slide(prs)
    write(textbox(s, MARGIN, 108, CONTENT_W, 70),
          [("Where to go next.", T_DIVIDER, True, WHITE, None)])

    cards = [
        ("Learning resources", "[INTERNAL LEARNING RESOURCES]"),
        ("Prompt Gallery", "[PROMPT GALLERY LOCATION]"),
        ("Questions", "[PROGRAMME MAILBOX]"),
        ("Advanced workshop", "[ADVANCED SESSION DATE]"),
    ]
    gap = 20
    w = (CONTENT_W - 3 * gap) / 4
    for i, (head, link) in enumerate(cards):
        cell = card(s, MARGIN + i * (w + gap), 196, w, 134, NEUTRAL.surface,
                    pad=16)
        write(cell, [(head, T_CARD, True, BLUE, None),
                     (link, T_HINT, True, GOOD.accent, 10)],
              anchor=MSO_ANCHOR.TOP)

    close = card(s, MARGIN, 350, CONTENT_W, 62, NEUTRAL.surface, pad=16)
    write(close, [("Write one prompt. Save it. Improve it.",
                   T_STATEMENT, True, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    s.notes_slide.notes_text_frame.text = (
        "Before delivery: replace every placeholder in this deck — ten "
        "remain, across seven distinct items.")
    footer(s, APPENDIX, None, 35)


SLIDES = [slide_30, slide_31, slide_32, slide_33, slide_34, slide_35]
