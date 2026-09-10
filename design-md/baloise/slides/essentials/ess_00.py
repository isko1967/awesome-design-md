"""Session 1, opening (slides 1-5).

Title, outcome, the Learn-See-Try-Improve cycle and the two Slido
interactions. Content is from the source deck; the layout follows the
Session 2 system.
"""
from lxml import etree
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, AVOID, BLUE, CHOICE, CONTENT_W, GOOD, MARGIN,
                      NEUTRAL, T_BODY, T_CARD, T_HINT, T_LEAD, T_STATEMENT,
                      WHITE, _ph, card, eyebrow, flow_row, footer, lead,
                      new_slide, runs, textbox, title, write)

LABEL = "Prompting Workshop — Session 1"

CHIP_H = 46
CHIP_GAP = 17


def _foot(slide, number, phase=None):
    footer(slide, LABEL, phase, number)


def slido(slide, code_hint, note, y):
    """The recurring 'go to Slido' call to action, as in Session 2."""
    strip = card(slide, MARGIN, y, CONTENT_W, 54, ACTION.surface, pad=16)
    runs(strip, [("Go to Slido   ", True, ACTION.accent),
                 (code_hint, True, BLUE),
                 (f"    {note}" if note else "", False, BLUE)],
         size=T_LEAD, anchor=MSO_ANCHOR.MIDDLE)
    return strip


def option_chips(slide, options, top, per_row, h=CHIP_H):
    """Answer options as filled chips - what the participant picks is CHOICE."""
    width = (CONTENT_W - (per_row - 1) * CHIP_GAP) / per_row
    for i, text in enumerate(options):
        row, col = divmod(i, per_row)
        chip = card(slide, MARGIN + col * (width + CHIP_GAP),
                    top + row * (h + CHIP_GAP), width, h, CHOICE.surface,
                    pad=8)
        write(chip, [(text, T_BODY, False, WHITE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def lettered_chips(slide, options, top, pitch=52, h=44):
    """A-B-C-D answer options, one per row."""
    for i, (letter, text) in enumerate(options):
        cell = card(slide, MARGIN, top + i * pitch, CONTENT_W, h,
                    CHOICE.surface, pad=12)
        runs(cell, [(f"{letter}   ", True, WHITE), (text, False, WHITE)],
             size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)


# The corporate title slide, reproduced rather than redesigned: the same
# Title-green layout, the same paragraph levels, the same date field. Only
# the workshop name is corrected - the source said "Advanced Workshop" on a
# deck whose every footer said Beginner.
TITLE_BODY = """<p:txBody xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <a:bodyPr/><a:lstStyle/>
  <a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>Group AI Week: Prompting Workshop</a:t></a:r></a:p>
  <a:p><a:pPr lvl="1"/><a:r><a:rPr lang="en-US" dirty="0"/><a:t>Essentials Workshop</a:t></a:r></a:p>
  <a:p><a:pPr lvl="2"/><a:endParaRPr lang="en-US" dirty="0"/></a:p>
  <a:p><a:pPr lvl="2"/><a:r><a:rPr lang="en-US" dirty="0"/><a:t>Trainer Name</a:t></a:r></a:p>
  <a:p><a:pPr lvl="2"/><a:endParaRPr lang="en-US" dirty="0"/></a:p>
  <a:p><a:pPr lvl="2"/><a:r><a:rPr lang="en-US" dirty="0"/><a:t>Helvetia Baloise Group</a:t></a:r>
    <a:br><a:rPr lang="en-US" dirty="0"/></a:br>
    <a:fld id="{0CEF993E-C9A4-4754-961D-C4282081E58A}" type="datetime3">
      <a:rPr lang="en-US"/><a:pPr lvl="2"/><a:t>21 September 2026</a:t></a:fld>
    <a:endParaRPr lang="en-US" dirty="0"/></a:p>
</p:txBody>"""


def slide_01(prs):
    s = new_slide(prs, with_title=False, layout="Title-green")
    box = _ph(s, 10)
    body = etree.fromstring(TITLE_BODY)
    box._element.replace(box.text_frame._txBody, body)


def slide_02(prs):
    s = new_slide(prs)
    title(s, "What you will be able to do today.")
    lead(s, "Turn one task from your own work into a prompt that briefs AI "
            "properly — and improve it when the first result is not good "
            "enough.")

    eyebrow(s, "Your outcome", y=196)
    outcome = card(s, MARGIN, 226, CONTENT_W, 186, NEUTRAL.surface, pad=24)
    write(outcome, [("“I can turn a work task into a good prompt and improve "
                     "it.”", T_STATEMENT, True, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    _foot(s, 2)


def slide_03(prs):
    s = new_slide(prs)
    title(s, "Learn it. See it. Try it. Improve it.")
    lead(s, "Short inputs. Live demonstrations. Individual practice. Group "
            "reflection.")

    flow_row(s, [
        ("Learn", "A short input, never more than ten minutes"),
        ("See", "A live demo on a real task, including the failures"),
        ("Try", "You work on your own task, on your own"),
        ("Improve", "We compare what changed and why"),
    ], top=188, cell_h=204)
    _foot(s, 3)


def slide_04(prs):
    s = new_slide(prs)
    title(s, "How confident are you right now?")
    lead(s, "Can you get a useful result from AI for a work task?")

    option_chips(s, ("1 — not yet", "2", "3", "4", "5 — very"),
                 top=172, per_row=5, h=76)

    note = card(s, MARGIN, 278, CONTENT_W, 76, NEUTRAL.surface, pad=16)
    runs(note, [("Facilitator   ", True, BLUE),
                ("Read the distribution aloud, then move on. No individual "
                 "answers are shown.", False, BLUE)],
         size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)

    slido(s, "[SLIDO CODE]", "2 min.", y=378)
    _foot(s, 4, "INTERACT")


def slide_05(prs):
    s = new_slide(prs)
    title(s, "What should we work on in the Prompt Clinic?")
    lead(s, "Submit a task or situation from your daily work where you would "
            "like AI to help you.")

    rules = card(s, MARGIN, 150, CONTENT_W, 106, AVOID.surface, pad=16)
    write(rules, [
        ("Two rules for every submission", T_CARD, True, AVOID.accent, None),
        ("Describe the situation, not the data. No personal, customer or "
         "confidential information — [INTERNAL DATA-HANDLING GUIDANCE].",
         T_BODY, False, BLUE, 6),
    ], anchor=MSO_ANCHOR.MIDDLE)

    use = card(s, MARGIN, 272, CONTENT_W, 92, NEUTRAL.surface, pad=16)
    write(use, [
        ("How we use it", T_CARD, True, BLUE, None),
        ("You can upvote each other’s submissions. We work on the most-voted "
         "ones live, after they have been screened.", T_BODY, False, BLUE, 6),
    ], anchor=MSO_ANCHOR.MIDDLE)

    slido(s, "[SLIDO CODE]", "Stays open until the break.", y=382)
    _foot(s, 5, "INTERACT")


SLIDES = [slide_01, slide_02, slide_03, slide_04, slide_05]
