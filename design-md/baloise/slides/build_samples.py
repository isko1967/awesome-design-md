#!/usr/bin/env python3
"""Build the five sample slides for Block 1 on the Helvetia corporate master.

The composition is our own: every slide is laid out shape by shape rather than
poured into the template's content layouts, whose boxes dictated the content
instead of serving it.

What the corporate template contributes: Arial as the theme font, the exact
colour values, the margins and content zone, the column measures, the footer
band and the logo. Slides sit on the "1 Content" layout because that is the
plainest one that still inherits the master graphics.

Usage:  python3 build_samples.py <corporate.potx|.pptx> <out.pptx>
"""
import copy
import sys
import zipfile

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

# --- colours, taken verbatim from the template theme -------------------------
PRIMARY = RGBColor(0x00, 0x0D, 0x6E)    # dk1/dk2 - standard text blue
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN_DARK = RGBColor(0x1B, 0x59, 0x51)  # accent1
GREEN_MID = RGBColor(0x94, 0xE3, 0xD4)   # chapter surface
GREEN_SOFT = RGBColor(0xCB, 0xF2, 0xEC)  # panel surface
RED_DARK = RGBColor(0xD9, 0x30, 0x4C)    # accent3
RED_SOFT = RGBColor(0xFF, 0xD7, 0xD7)    # panel surface
AMBER_SOFT = RGBColor(0xFF, 0xEC, 0xBC)  # panel surface
# the template defines no neutral tint, so the design system's grey is used
GREY_SURFACE = RGBColor(0xF6, 0xF6, 0xF6)
GREY_TEXT = RGBColor(0x74, 0x74, 0x74)

# --- geometry, taken from the template ---------------------------------------
MARGIN = 41
CONTENT_W = 879
CONTENT_TOP = 120
CONTENT_BOTTOM = 480
COL2_W, COL2_X = 428, (41, 491)
COL3_W, COL3_X = 278, (41, 341, 642)

# --- type scale, ours, with the title met in the middle at 32pt --------------
T_NUMBER = 96
T_DIVIDER = 48
T_TITLE = 32
T_STATEMENT = 24
T_CARD = 20
T_LEAD = 18
T_BODY = 16
T_HINT = 13
T_META = 12

CORNER_PT = 12
BLOCK_FOOTER = "01  Few-shot & negative examples"


# --- template plumbing -------------------------------------------------------
def load_template(path):
    """python-pptx rejects the .potx content type, so rewrite it in memory."""
    if not path.lower().endswith(".potx"):
        return Presentation(path)
    tpl = ("application/vnd.openxmlformats-officedocument"
           ".presentationml.template.main+xml")
    prs_type = ("application/vnd.openxmlformats-officedocument"
                ".presentationml.presentation.main+xml")
    tmp = path + ".converted.pptx"
    with zipfile.ZipFile(path) as zin, \
            zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(tpl.encode(), prs_type.encode())
            zout.writestr(item, data)
    return Presentation(tmp)


def drop_existing_slides(prs):
    """Start from an empty deck but keep masters, layouts and theme."""
    id_list = prs.slides._sldIdLst
    rel_ns = ("{http://schemas.openxmlformats.org/officeDocument/2006/"
              "relationships}id")
    for sld_id in list(id_list):
        prs.part.drop_rel(sld_id.get(rel_ns))
        id_list.remove(sld_id)


def layout(prs, name):
    for lay in prs.slide_masters[0].slide_layouts:
        if lay.name == name:
            return lay
    raise KeyError(f"layout {name!r} not in template")


def ph(slide, idx):
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == idx:
            return shape
    raise KeyError(f"placeholder idx={idx} not on slide")


def drop(slide, *indices):
    for idx in indices:
        try:
            shape = ph(slide, idx)
        except KeyError:
            continue
        shape._element.getparent().remove(shape._element)


def background(slide, rgb):
    """Paint the slide background; master graphics still draw on top of it."""
    cSld = slide._element.find(qn("p:cSld"))
    bg = etree.Element(qn("p:bg"))
    bg_pr = etree.SubElement(bg, qn("p:bgPr"))
    fill = etree.SubElement(bg_pr, qn("a:solidFill"))
    etree.SubElement(fill, qn("a:srgbClr")).set("val", str(rgb))
    etree.SubElement(bg_pr, qn("a:effectLst"))
    cSld.insert(0, bg)   # p:bg must precede p:spTree


def inherit(slide, idx):
    """Copy a placeholder from the layout onto the slide.

    PowerPoint does not put footer, date and slide-number placeholders on new
    slides, so the corporate footer band stays empty unless it is copied in.
    """
    for shape in slide.slide_layout.placeholders:
        if shape.placeholder_format.idx == idx:
            slide.shapes._spTree.append(copy.deepcopy(shape._element))
            return ph(slide, idx)
    raise KeyError(f"layout has no placeholder idx={idx}")


# --- drawing helpers ---------------------------------------------------------
def write(shape, rows, wrap=True, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
    """Fill a text frame. Each row: (text, size, bold, colour, space_before)."""
    tf = shape.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.clear()
    for i, (text, size, bold, colour, before) in enumerate(rows):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if before is not None:
            p.space_before = Pt(before)
        if size is not None:
            p.line_spacing = Pt(round(size * 1.3))
        run = p.add_run()
        run.text = text
        if size is not None:
            run.font.size = Pt(size)
        if bold is not None:
            run.font.bold = bold
        if colour is not None:
            run.font.color.rgb = colour
    return shape


def card(slide, x, y, w, h, fill, pad=16):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Pt(x), Pt(y), Pt(w), Pt(h))
    shape.adjustments[0] = CORNER_PT / min(w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.margin_left = tf.margin_right = Pt(pad)
    tf.margin_top = tf.margin_bottom = Pt(pad - 2)
    tf.word_wrap = True
    return shape


def textbox(slide, x, y, w, h):
    box = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    tf = box.text_frame
    tf.margin_left = tf.margin_right = Pt(0)
    tf.margin_top = tf.margin_bottom = Pt(0)
    tf.word_wrap = True
    return box


def title(slide, text):
    """The corporate title placeholder, set to our 32pt step."""
    return write(ph(slide, 0), [(text, T_TITLE, True, PRIMARY, None)])


def lead(slide, text):
    return write(textbox(slide, MARGIN, 88, CONTENT_W, 26),
                 [(text, T_LEAD, False, PRIMARY, None)])


def label(slide, x, y, w, text, colour=GREY_TEXT):
    return write(textbox(slide, x, y, w, 18),
                 [(text.upper(), T_META, True, colour, None)])


def footer(slide, phase, number):
    kinds = {s.placeholder_format.idx: str(s.placeholder_format.type)
             for s in slide.slide_layout.placeholders}
    text = f"{BLOCK_FOOTER}   ·   {phase}" if phase else BLOCK_FOOTER
    for idx, kind in kinds.items():
        if "FOOTER" in kind:
            write(inherit(slide, idx), [(text, None, None, None, None)])
        elif "SLIDE_NUMBER" in kind:
            shape = write(inherit(slide, idx),
                          [(str(number), None, None, None, None)])
            shape.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT


def new_slide(prs, bg=None):
    slide = prs.slides.add_slide(layout(prs, "1 Content"))
    drop(slide, 13, 14)   # the layout's own content boxes are not used
    if bg is not None:
        background(slide, bg)
    return slide


# --- slides ------------------------------------------------------------------
def slide_07_divider(prs):
    s = new_slide(prs, bg=GREEN_MID)
    drop(s, 0)

    write(textbox(s, MARGIN, 112, 176, 130),
          [("01", T_NUMBER, True, PRIMARY, None)])
    write(textbox(s, 225, 122, 695, 150),
          [("Few-shot &", T_DIVIDER, True, PRIMARY, None),
           ("negative examples", T_DIVIDER, True, PRIMARY, None)])
    write(textbox(s, 225, 278, 695, 30),
          [("Show the model what good looks like.", T_CARD, False, PRIMARY,
            None)])

    x = MARGIN
    for step in ("LEARN", "SEE", "TRY", "IMPROVE"):
        chip = card(s, x, 376, 207, 84, WHITE)
        write(chip, [(step, T_LEAD, True, PRIMARY, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += 207 + 17

    footer(s, None, 7)


def slide_10_how(prs):
    s = new_slide(prs)
    title(s, "Tell the model what to learn from each example.")

    label(s, MARGIN, CONTENT_TOP, COL2_W, "What to specify")
    positive = card(s, MARGIN, 146, COL2_W, 140, GREEN_SOFT)
    write(positive, [
        ("Positive example", T_CARD, True, GREEN_DARK, None),
        ("Follow its", T_BODY, True, PRIMARY, 10),
        ("tone · structure · level of detail", T_BODY, False, PRIMARY, 2),
    ])
    negative = card(s, MARGIN, 302, COL2_W, 140, RED_SOFT)
    write(negative, [
        ("Negative example", T_CARD, True, RED_DARK, None),
        ("Avoid its", T_BODY, True, PRIMARY, 10),
        ("unnecessary background · vague wording · lack of clear actions",
         T_BODY, False, PRIMARY, 2),
    ])

    label(s, COL2_X[1], CONTENT_TOP, COL2_W, "The prompt")
    prompt = card(s, COL2_X[1], 146, COL2_W, 296, GREY_SURFACE)
    write(prompt, [
        ("Use the examples below as guidance for the new output.",
         T_BODY, False, PRIMARY, None),
        ("Positive example:", T_BODY, True, PRIMARY, 12),
        ("[insert example]", T_BODY, False, GREY_TEXT, 0),
        ("Negative example:", T_BODY, True, PRIMARY, 12),
        ("[insert example]", T_BODY, False, GREY_TEXT, 0),
        ("Now complete this task:", T_BODY, True, PRIMARY, 12),
        ("[insert task]", T_BODY, False, GREY_TEXT, 0),
        ("Do not copy the content of the examples. Use them only as guidance "
         "for how the new output should be written.",
         T_HINT, False, GREY_TEXT, 14),
    ])

    band = card(s, MARGIN, 452, CONTENT_W, 28, GREEN_SOFT, pad=12)
    tf = band.text_frame
    tf.margin_top = tf.margin_bottom = Pt(3)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    for text, bold, colour in (
            ("Use when   ", True, GREEN_DARK),
            ("The desired quality is easier to demonstrate than to describe.",
             False, PRIMARY)):
        run = p.add_run()
        run.text = text
        run.font.size = Pt(T_BODY)
        run.font.bold = bold
        run.font.color.rgb = colour
    band.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    footer(s, "LEARN", 10)


def slide_12_before_after(prs):
    s = new_slide(prs)
    title(s, "Same task. Clearer guidance.")

    label(s, COL2_X[0], CONTENT_TOP, COL2_W, "Without examples")
    label(s, COL2_X[1], CONTENT_TOP, COL2_W, "With examples", GREEN_DARK)

    left = card(s, COL2_X[0], 146, COL2_W, 290, GREY_SURFACE, pad=20)
    write(left, [
        ("Recent severe weather events have led to an increase in claims "
         "volumes. The claims organisation is currently taking several "
         "actions to manage the situation. Additional capacity has been made "
         "available, and developments will continue to be monitored.",
         T_BODY, False, PRIMARY, None),
    ], anchor=MSO_ANCHOR.MIDDLE)

    right = card(s, COL2_X[1], 146, COL2_W, 290, GREEN_SOFT, pad=20)
    rows = []
    for i, (heading, text) in enumerate([
            ("Status — Attention required",
             "Severe-weather claims increased volumes and processing times."),
            ("Response", "Additional external capacity has been activated."),
            ("Customer impact",
             "No change to current customer communication is required."),
            ("Next watchpoint",
             "Reassess processing times at the end of the week.")]):
        rows.append((heading, T_BODY, True, GREEN_DARK, None if i == 0 else 12))
        rows.append((text, T_BODY, False, PRIMARY, 0))
    write(right, rows, anchor=MSO_ANCHOR.MIDDLE)

    band = card(s, MARGIN, 448, CONTENT_W, 32, GREEN_SOFT, pad=14)
    tf = band.text_frame
    tf.margin_top = tf.margin_bottom = Pt(4)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    for text, bold, colour in (
            ("What changed?   ", True, PRIMARY),
            ("More specific · more structured · more actionable",
             False, GREEN_DARK)):
        run = p.add_run()
        run.text = text
        run.font.size = Pt(T_BODY)
        run.font.bold = bold
        run.font.color.rgb = colour

    footer(s, "SEE", 12)


def slide_13_practice(prs):
    s = new_slide(prs)
    title(s, "Use examples to guide your own output.")
    lead(s, "Your task")

    badge = card(s, 790, 36, 130, 40, GREEN_MID, pad=6)
    write(badge, [("TIME  5 MIN", T_BODY, True, PRIMARY, None)],
          anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

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
        x = COL3_X[i % 3]
        y = 150 if i < 3 else 325
        cell = card(s, x, y, COL3_W, 155, GREEN_SOFT)
        rows = [(number, T_STATEMENT, True, GREEN_DARK, None),
                (text, T_LEAD, True, PRIMARY, 6)]
        if hint:
            rows.append((hint, T_HINT, False, GREY_TEXT, 6))
        write(cell, rows)

    # sixth cell: the compliance note gets a slot of its own rather than a
    # footnote, and the amber panel colour marks it as a condition of the task
    note = card(s, COL3_X[2], 325, COL3_W, 155, AMBER_SOFT)
    write(note, [
        ("Before you start", T_LEAD, True, PRIMARY, None),
        ("Keep all information generic. Do not enter personal, customer or "
         "confidential information.", T_BODY, False, PRIMARY, 8),
    ])

    footer(s, "TRY", 13)


def slide_14_reflection(prs):
    s = new_slide(prs, bg=GREEN_SOFT)
    title(s, "Did the examples give you more control?")
    lead(s, "Compare the result with what you would normally receive.")

    write(textbox(s, MARGIN, 140, 500, 28),
          [("What changed most?", T_CARD, True, PRIMARY, None)])

    x = MARGIN
    for text in ("Tone", "Structure", "Level of detail", "Wording",
                 "Nothing meaningful"):
        chip = card(s, x, 180, 163, 110, WHITE)
        write(chip, [(text, T_LEAD, False, PRIMARY, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += 163 + 16

    cta = card(s, MARGIN, 326, CONTENT_W, 124, WHITE, pad=24)
    write(cta, [
        ("In the chat", T_BODY, True, GREEN_DARK, None),
        ("Share the one thing that changed most.", T_STATEMENT, False,
         PRIMARY, 8),
    ], anchor=MSO_ANCHOR.MIDDLE)

    footer(s, "IMPROVE", 14)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    prs = load_template(sys.argv[1])
    drop_existing_slides(prs)
    for builder in (slide_07_divider, slide_10_how, slide_12_before_after,
                    slide_13_practice, slide_14_reflection):
        builder(prs)
    prs.save(sys.argv[2])
    print(f"wrote {sys.argv[2]} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    main()
