#!/usr/bin/env python3
"""Build the five sample slides for Block 1 on the Helvetia corporate master.

Corporate template is the primary source: slide size, theme fonts and colours,
title/footer placeholders and the layout geometry all come from the .potx.
Custom shapes are added only where no corporate layout covers the composition,
and they use the template's own tints.

Usage:  python3 build_samples.py <corporate.potx|.pptx> <out.pptx>
"""
import copy
import sys
import zipfile

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

# --- palette: taken from the template theme and the Helvetia design tokens ----
PRIMARY = RGBColor(0x00, 0x0D, 0x6E)   # tx2 / core blue
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY_TEXT = RGBColor(0x74, 0x74, 0x74)  # Grey.5
GREY_SURFACE = RGBColor(0xF6, 0xF6, 0xF6)  # Grey.1
GREEN_1 = RGBColor(0xE9, 0xFB, 0xF7)   # tint 1 - surface
GREEN_2 = RGBColor(0xCB, 0xF2, 0xEC)   # tint 2 - template panel colour
GREEN_3 = RGBColor(0x94, 0xE3, 0xD4)   # tint 3 - template chapter colour
GREEN_6 = RGBColor(0x1B, 0x59, 0x51)   # accent1 - text on green
WARN_1 = RGBColor(0xFF, 0xF9, 0xE8)    # warning surface
WARN_6 = RGBColor(0x7D, 0x4A, 0x0D)    # warning text

BLOCK_FOOTER = "01  Few-shot & negative examples"
CORNER_PT = 12  # the template's rounded-box corner radius


# --- helpers -----------------------------------------------------------------
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
    for sld_id in list(id_list):
        rid = sld_id.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/"
            "relationships}id"
        )
        prs.part.drop_rel(rid)
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


def drop(slide, idx):
    """Remove an unused placeholder so it cannot render prompt text.

    Only safe for untinted placeholders: a removed placeholder is inherited
    back from the layout by some renderers, which would redraw its fill.
    """
    try:
        shape = ph(slide, idx)
    except KeyError:
        return
    shape._element.getparent().remove(shape._element)


def write(shape, paragraphs, wrap=True, anchor=MSO_ANCHOR.TOP,
          align=PP_ALIGN.LEFT):
    """Fill a text frame. Each entry: (text, level, size, bold, colour, space_before).

    Autoshapes centre their text by default, so alignment is always set.
    """
    tf = shape.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.clear()
    for i, spec in enumerate(paragraphs):
        text, level, size, bold, colour, space_before = spec
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = level
        p.alignment = align
        if space_before is not None:
            p.space_before = Pt(space_before)
        run = p.add_run()
        run.text = text
        f = run.font
        if size is not None:
            f.size = Pt(size)
        if bold is not None:
            f.bold = bold
        if colour is not None:
            f.color.rgb = colour
    return tf


def card(slide, x, y, w, h, fill, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Pt(x), Pt(y), Pt(w), Pt(h))
    # the adjustment is a fraction of the shorter side, so derive it per shape
    # to keep the same absolute corner radius as the template's boxes
    shape.adjustments[0] = CORNER_PT / min(w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.margin_left = Pt(16)
    tf.margin_right = Pt(16)
    tf.margin_top = Pt(14)
    tf.margin_bottom = Pt(14)
    tf.word_wrap = True
    return shape


def textbox(slide, x, y, w, h):
    box = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    tf = box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Pt(0)
    tf.word_wrap = True
    return box


def inherit(slide, idx):
    """Copy a placeholder from the layout onto the slide.

    PowerPoint does not put footer, date and slide-number placeholders on new
    slides, so the corporate footer band stays empty unless it is copied in.
    Copying keeps the template's own position and character formatting.
    """
    for shape in slide.slide_layout.placeholders:
        if shape.placeholder_format.idx != idx:
            continue
        element = copy.deepcopy(shape._element)
        slide.shapes._spTree.append(element)
        return ph(slide, idx)
    raise KeyError(f"layout has no placeholder idx={idx}")


def footer(slide, phase, number):
    """Corporate footer band: block label, phase of the cycle, slide number."""
    layout_idx = {shape.placeholder_format.idx: str(shape.placeholder_format.type)
                  for shape in slide.slide_layout.placeholders}
    label = f"{BLOCK_FOOTER}   ·   {phase}" if phase else BLOCK_FOOTER
    for idx, kind in layout_idx.items():
        if "FOOTER" in kind:
            write(inherit(slide, idx), [(label, 0, None, None, None, None)])
        elif "SLIDE_NUMBER" in kind:
            shape = inherit(slide, idx)
            write(shape, [(str(number), 0, None, None, None, None)])
            shape.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT


# --- slides ------------------------------------------------------------------
def slide_07_divider(prs):
    """Chapter-green, used exactly as the template intends."""
    s = prs.slides.add_slide(layout(prs, "Chapter-green"))
    write(ph(s, 11), [("01", 0, None, None, None, None)])
    write(ph(s, 10), [
        ("Few-shot &\nnegative examples", 0, None, None, None, None),
        ("Show the model what good looks like.", 2, 18, True, None, 24),
        ("LEARN  →  SEE  →  TRY  →  IMPROVE", 2, 18, False, None, 12),
    ])
    footer(s, None, 7)
    return s


def slide_10_how(prs):
    """Content-Box-green: prompt template in the content area, aside in the box."""
    s = prs.slides.add_slide(layout(prs, "Content-Box-green"))
    write(ph(s, 0), [("Tell the model what to learn from each example.",
                      0, None, None, None, None)])
    drop(s, 15)   # optional subtitle - not used here
    drop(s, 13)   # content placeholder replaced by the prompt card

    prompt = card(s, 41, 120, 653, 300, GREEN_1)
    lines = [
        ("Use the examples below as guidance for the new output.", False, 0),
        ("Positive example:", True, 10),
        ("[insert example]", False, 0),
        ("Follow its:  tone · structure · level of detail", False, 10),
        ("Negative example:", True, 10),
        ("[insert example]", False, 0),
        ("Avoid its:  unnecessary background · vague wording · "
         "lack of clear actions", False, 10),
        ("Now complete this task:", True, 10),
        ("[insert task]", False, 0),
    ]
    tf = prompt.text_frame
    tf.clear()
    for i, (text, bold, before) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if before:
            p.space_before = Pt(before)
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = Pt(21)
        run = p.add_run()
        run.text = text
        run.font.size = Pt(15)
        run.font.bold = bold
        run.font.color.rgb = PRIMARY if bold else GREEN_6

    note = textbox(s, 41, 432, 653, 34)
    write(note, [("Do not copy the content of the examples. Use them only as "
                  "guidance for how the new output should be written.",
                  0, 12, False, GREY_TEXT, None)])

    write(ph(s, 14), [
        ("Use when", 0, 16, True, PRIMARY, None),
        ("The desired quality is easier to demonstrate than to describe.",
         0, 14, False, PRIMARY, 10),
    ])
    footer(s, "LEARN", 10)
    return s


def slide_12_before_after(prs):
    """2 Contents: one comparison, two columns of identical structure."""
    s = prs.slides.add_slide(layout(prs, "2 Contents"))
    write(ph(s, 0), [("Same task. Clearer guidance.", 0, None, None, None, None)])
    drop(s, 15)
    drop(s, 13)
    drop(s, 14)

    for x, label, tone in ((41, "WITHOUT EXAMPLES", "neutral"),
                           (491, "WITH EXAMPLES", "accent")):
        head = textbox(s, x, 120, 428, 20)
        write(head, [(label, 0, 14, True,
                      GREY_TEXT if tone == "neutral" else GREEN_6, None)])

    left = card(s, 41, 148, 428, 272, GREY_SURFACE)
    write(left, [
        ("Recent severe weather events have led to an increase in claims "
         "volumes. The claims organisation is currently taking several actions "
         "to manage the situation. Additional capacity has been made "
         "available, and developments will continue to be monitored.",
         0, 15, False, PRIMARY, None),
    ])
    for p in left.text_frame.paragraphs:
        p.line_spacing = Pt(21)
        p.alignment = PP_ALIGN.LEFT

    right = card(s, 491, 148, 428, 272, GREEN_1)
    blocks = [
        ("Status — Attention required",
         "Severe-weather claims increased volumes and processing times."),
        ("Response", "Additional external capacity has been activated."),
        ("Customer impact",
         "No change to current customer communication is required."),
        ("Next watchpoint",
         "Reassess processing times at the end of the week."),
    ]
    tf = right.text_frame
    tf.clear()
    first = True
    for heading, text in blocks:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        if not first:
            p.space_before = Pt(10)
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = Pt(19)
        r = p.add_run()
        r.text = heading
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = GREEN_6
        q = tf.add_paragraph()
        q.alignment = PP_ALIGN.LEFT
        q.line_spacing = Pt(19)
        r2 = q.add_run()
        r2.text = text
        r2.font.size = Pt(14)
        r2.font.color.rgb = PRIMARY
        first = False

    band = textbox(s, 41, 434, 878, 24)
    tf = band.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    for text, bold, colour in (("What changed?   ", True, PRIMARY),
                               ("More specific · more structured · "
                                "more actionable", False, GREEN_6)):
        r = p.add_run()
        r.text = text
        r.font.size = Pt(16)
        r.font.bold = bold
        r.font.color.rgb = colour

    footer(s, "SEE", 12)
    return s


def slide_13_practice(prs):
    """Content-Box-green: five steps, with time and the compliance note aside."""
    s = prs.slides.add_slide(layout(prs, "Content-Box-green"))
    write(ph(s, 0), [("Use examples to guide your own output.",
                      0, None, None, None, None)])
    drop(s, 15)
    drop(s, 13)   # steps are laid out individually below

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
    y = 126
    for number, text, hint in steps:
        num = textbox(s, 41, y, 28, 24)
        write(num, [(number, 0, 18, True, GREEN_6, None)])
        body = textbox(s, 73, y, 621, 46)
        rows = [(text, 0, 16, True, PRIMARY, None)]
        if hint:
            rows.append((hint, 0, 12, False, GREY_TEXT, 4))
        write(body, rows)
        y += 62

    # The corporate side box carries the time budget and the compliance note.
    # The note stays in the box rather than getting an alert colour of its own:
    # the design system reserves alert colours for system states, and a second
    # colour next to the green box would break the same-spectrum rule.
    write(ph(s, 14), [
        ("TIME", 0, 12, True, PRIMARY, None),
        ("5 MIN", 0, 28, True, PRIMARY, 0),
        ("Before you start", 0, 14, True, PRIMARY, 20),
        ("Keep all information generic. Do not enter personal, customer or "
         "confidential information.", 0, 14, True, PRIMARY, 4),
    ])

    footer(s, "TRY", 13)
    return s


def slide_14_reflection(prs):
    """Headline-green: the quiet end of the block."""
    s = prs.slides.add_slide(layout(prs, "Headline-green"))
    write(ph(s, 0), [("Did the examples give you more control?",
                      0, None, None, None, None)])
    write(ph(s, 14), [("Compare the result with what you would normally "
                       "receive.", 0, None, None, None, None)])

    question = textbox(s, 41, 190, 500, 26)
    write(question, [("What changed most?", 0, 20, True, PRIMARY, None)])

    options = ["Tone", "Structure", "Level of detail", "Wording",
               "Nothing meaningful"]
    x = 41
    for text in options:
        # 16pt Arial runs about 9pt per character; 44pt covers the padding
        w = 44 + len(text) * 9.0
        chip = card(s, x, 232, w, 44, WHITE)
        chip.text_frame.word_wrap = False
        chip.text_frame.margin_left = chip.text_frame.margin_right = Pt(20)
        write(chip, [(text, 0, 16, False, PRIMARY, None)], wrap=False,
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += w + 14

    cta = textbox(s, 41, 342, 700, 60)
    write(cta, [("In the chat", 0, 16, True, GREEN_6, None),
                ("Share the one thing that changed most.",
                 0, 20, False, PRIMARY, 6)])

    footer(s, "IMPROVE", 14)
    return s


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
