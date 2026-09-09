"""Shared layout system for the prompting-workshop deck.

Everything visual lives here so that the block modules only carry content.
Corporate values (Arial, the named colour list, margins, content zone, column
measures, footer band) come from the .potx; the composition is our own.

Colour carries meaning and never rotates by block:

    GOOD       the target state - positive examples, the improved output
    CAUTION    what to avoid - negative examples, guardrails, limits, compliance
    NEUTRAL    raw material - the weak "before" output, prompt canvases
    ACTION     the participant's turn - practice, polls, clinic, transfer

Red is held in reserve and deliberately unused.
"""
import copy
import zipfile

from lxml import etree
from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt


def rgb(value):
    return RGBColor.from_string(value)


# --- the named corporate colour list, ppt/theme/theme1.xml <a:custClrLst> -----
BLUE = rgb("000D6E")
WHITE = rgb("FFFFFF")
GREEN, GREEN_LIGHT, GREEN_3 = rgb("1B5951"), rgb("94E3D4"), rgb("CBF2EC")
PURPLE, PURPLE_LIGHT, PURPLE_3 = rgb("6C2273"), rgb("B8B2FF"), rgb("E1D9FF")
TANGERINE_1, TANGERINE_LIGHT, TANGERINE_3 = (rgb("B24A00"), rgb("FAE052"),
                                             rgb("FFECBC"))
# the corporate list has no neutral tint; these come from the design system
GREY_SURFACE, GREY_TEXT = rgb("F6F6F6"), rgb("747474")


class Role:
    """A semantic colour role: what the colour is saying, not which hue it is."""

    def __init__(self, surface, accent, ground=None):
        self.surface = surface
        self.accent = accent
        self.ground = ground or surface


GOOD = Role(GREEN_3, GREEN, GREEN_LIGHT)
CAUTION = Role(PURPLE_3, PURPLE, PURPLE_LIGHT)
NEUTRAL = Role(GREY_SURFACE, GREY_TEXT, GREY_SURFACE)
ACTION = Role(TANGERINE_3, TANGERINE_1, TANGERINE_LIGHT)

# --- geometry, from the corporate template -----------------------------------
SLIDE_W, SLIDE_H = 960, 540
MARGIN = 41
CONTENT_W = 879
CONTENT_TOP = 120
CONTENT_BOTTOM = 480
BAND_TOP = 448          # full-width closing band
GUTTER = 22
COL2_W, COL2_X = 428, (41, 491)
COL3_W, COL3_X = 278, (41, 341, 642)
COL4_W, COL4_X = 203, (41, 266, 491, 716)
MAIN_W, ASIDE_W, ASIDE_X = 653, 203, 717

# --- type scale --------------------------------------------------------------
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



# --- text metrics ------------------------------------------------------------
# Liberation Sans is metric-compatible with Arial, so measuring with it gives
# the same line breaks PowerPoint will produce on a corporate machine.
_FONT_FILE = {
    False: "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    True: "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
}
_FONT_CACHE = {}
_SUBPT = 4   # measure at 4x and divide, for sub-point precision


def _font(size, bold):
    key = (round(size * _SUBPT), bool(bold))
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(_FONT_FILE[bool(bold)],
                                              max(int(round(size * _SUBPT)), 1))
    return _FONT_CACHE[key]


def text_width(text, size, bold=False):
    """Width of one line in points."""
    return _font(size, bold).getlength(text) / _SUBPT


def wrapped_lines(text, width, size, bold=False):
    """The lines PowerPoint will break `text` into inside `width` points."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if current and text_width(trial, size, bold) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines or [""]


def fit_size(text, width, sizes, bold=True):
    """Largest of `sizes` at which `text` still fits on one line."""
    for size in sizes:
        if text_width(text, size, bold) <= width:
            return size
    return sizes[-1]


def rows_height(rows, width):
    """Height the rows from write() will occupy inside `width` points."""
    total = 0.0
    for i, (text, size, bold, _colour, before) in enumerate(rows):
        size = size or T_BODY
        if before and i:
            total += before
        total += len(wrapped_lines(text, width, size, bold)) * round(size * 1.35)
    return total


def fits(rows, width, height, pad=16):
    """True if the rows fit a card of this size, allowing for its padding."""
    return rows_height(rows, width - 2 * pad) <= height - 2 * max(pad - 2, 4)


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
    id_list = prs.slides._sldIdLst
    rel = ("{http://schemas.openxmlformats.org/officeDocument/2006/"
           "relationships}id")
    for sld_id in list(id_list):
        prs.part.drop_rel(sld_id.get(rel))
        id_list.remove(sld_id)


def _layout(prs, name):
    for lay in prs.slide_masters[0].slide_layouts:
        if lay.name == name:
            return lay
    raise KeyError(f"layout {name!r} not in template")


def _ph(slide, idx):
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == idx:
            return shape
    raise KeyError(f"placeholder idx={idx} not on slide")


def _drop(slide, *indices):
    for idx in indices:
        try:
            shape = _ph(slide, idx)
        except KeyError:
            continue
        shape._element.getparent().remove(shape._element)


def _background(slide, colour):
    """Paint the ground; master graphics still draw on top of it."""
    cSld = slide._element.find(qn("p:cSld"))
    bg = etree.Element(qn("p:bg"))
    bg_pr = etree.SubElement(bg, qn("p:bgPr"))
    fill = etree.SubElement(bg_pr, qn("a:solidFill"))
    etree.SubElement(fill, qn("a:srgbClr")).set("val", str(colour))
    etree.SubElement(bg_pr, qn("a:effectLst"))
    cSld.insert(0, bg)


def _inherit(slide, idx):
    """PowerPoint omits footer placeholders on new slides; copy them in."""
    for shape in slide.slide_layout.placeholders:
        if shape.placeholder_format.idx == idx:
            slide.shapes._spTree.append(copy.deepcopy(shape._element))
            return _ph(slide, idx)
    raise KeyError(f"layout has no placeholder idx={idx}")


# --- drawing primitives ------------------------------------------------------
def write(shape, rows, wrap=True, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
    """Fill a text frame. Row = (text, size, bold, colour, space_before).

    Autoshapes centre their text by default, so alignment is always set.
    """
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
            p.line_spacing = Pt(round(size * 1.35))
        run = p.add_run()
        run.text = text
        if size is not None:
            run.font.size = Pt(size)
        if bold is not None:
            run.font.bold = bold
        if colour is not None:
            run.font.color.rgb = colour
    return shape


def runs(shape, parts, size=T_BODY, anchor=MSO_ANCHOR.MIDDLE):
    """One paragraph made of differently formatted runs."""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.line_spacing = Pt(round(size * 1.35))
    for text, bold, colour in parts:
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = colour
    return shape


def card(slide, x, y, w, h, fill, pad=16, outline=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Pt(x), Pt(y), Pt(w), Pt(h))
    shape.adjustments[0] = CORNER_PT / min(w, h)
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    if outline is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = outline
        shape.line.width = Pt(2)
    shape.shadow.inherit = False
    tf = shape.text_frame
    tf.margin_left = tf.margin_right = Pt(pad)
    tf.margin_top = tf.margin_bottom = Pt(max(pad - 2, 4))
    tf.word_wrap = True
    return shape


def textbox(slide, x, y, w, h):
    box = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    tf = box.text_frame
    tf.margin_left = tf.margin_right = Pt(0)
    tf.margin_top = tf.margin_bottom = Pt(0)
    tf.word_wrap = True
    return box


def arrow(slide, x, y, size=16, colour=None):
    box = textbox(slide, x, y, size + 8, size + 6)
    write(box, [("→", size, False, colour or GREY_TEXT, None)],
          align=PP_ALIGN.CENTER)
    return box


# --- page furniture ----------------------------------------------------------
TITLE_STEPS = (T_TITLE, 30, 28, 26)
LEAD_Y = 90


def title(slide, text, width=CONTENT_W, has_lead=True):
    """Set the action title and return the y at which content may start.

    A title that does not fit steps down one size at a time. Only when no
    lead sits beneath it may it run to two lines, and then the content zone
    moves down to make room. The floor is T_LEAD + 2 so the title can never
    end up at or below the size of the line under it.
    """
    shape = _ph(slide, 0)
    shape.text_frame.margin_left = shape.text_frame.margin_right = Pt(0)
    shape.width = Pt(width)

    size = fit_size(text, width - 4, TITLE_STEPS, bold=True)
    lines = len(wrapped_lines(text, width - 4, size, bold=True))
    if lines > 1 and has_lead:
        # a second line would collide with the lead, so keep shrinking
        for step in range(T_TITLE, T_LEAD + 1, -2):
            if text_width(text, step, True) <= width - 4:
                size, lines = step, 1
                break
        else:
            size, lines = T_LEAD + 2, len(
                wrapped_lines(text, width - 4, T_LEAD + 2, bold=True))
    if lines > 2:
        print(f"  title needs {lines} lines at {size}pt - shorten the wording: "
              f"{text[:60]!r}")

    shape.height = Pt(round(size * 1.35) * lines + 8)
    write(shape, [(text, size, True, BLUE, None)])
    return 38 + round(size * 1.35) * lines + 8


def lead(slide, text, y=LEAD_Y):
    """The line under the title. Never larger than the title above it."""
    return write(textbox(slide, MARGIN, y, CONTENT_W, 26),
                 [(text, T_LEAD, False, BLUE, None)])


def eyebrow(slide, text, x=MARGIN, y=CONTENT_TOP, w=CONTENT_W, colour=None):
    return write(textbox(slide, x, y, w, 18),
                 [(text.upper(), T_META, True, colour or GREY_TEXT, None)])


def badge(slide, text, x=790, y=36, w=130, h=40, role=ACTION):
    chip = card(slide, x, y, w, h, role.surface, pad=6)
    return write(chip, [(text, T_BODY, True, BLUE, None)],
                 anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def band(slide, label_text, body_text, role=NEUTRAL, y=BAND_TOP, h=32):
    """Fixed height so the closing statement sits identically on every slide."""
    """The recurring full-width closing statement."""
    strip = card(slide, MARGIN, y, CONTENT_W, h, role.surface, pad=14)
    strip.text_frame.margin_top = strip.text_frame.margin_bottom = Pt(4)
    label_colour = BLUE if role is NEUTRAL else role.accent
    return runs(strip, [(f"{label_text}   ", True, label_colour),
                        (body_text, False, BLUE)])


def footer(slide, block_label, phase, number):
    kinds = {s.placeholder_format.idx: str(s.placeholder_format.type)
             for s in slide.slide_layout.placeholders}
    text = f"{block_label}   ·   {phase}" if phase else block_label
    for idx, kind in kinds.items():
        if "FOOTER" in kind:
            write(_inherit(slide, idx), [(text, None, None, None, None)])
        elif "SLIDE_NUMBER" in kind:
            shape = write(_inherit(slide, idx),
                          [(str(number), None, None, None, None)])
            shape.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT


def new_slide(prs, ground=None, with_title=True, layout="1 Content"):
    """'1 Content' is the plainest layout that still inherits the logo.

    Blue slides use 'Quote-blue' instead: it carries the corporate blue ground
    and the white version of the logo, which the dark-blue master logo cannot
    provide.
    """
    slide = prs.slides.add_slide(_layout(prs, layout))
    _drop(slide, 13, 14, 16)      # the layout's own content boxes go unused
    if not with_title:
        _drop(slide, 0)
    if ground is not None:
        _background(slide, ground)
    return slide


def blue_slide(prs):
    """A full-bleed corporate-blue slide with the white logo."""
    return new_slide(prs, with_title=False, layout="Quote-blue")


# --- archetypes --------------------------------------------------------------
CHIP_W, CHIP_GAP, CHIP_H, CHIP_Y = 207, 17, 84, 376


def divider(slide, number, title_lines, subline, chips=(), ghost=(),
            ink=WHITE):
    """Block opener and its variants: cover, break, clinic opener, close.

    Grounds are structural, never semantic: technique dividers and the cover
    sit on corporate blue, the participation landmarks on tangerine. Green
    would read as "this chapter is the good state", and green is reserved for
    the target state everywhere else in the deck.
    """
    if number:
        write(textbox(slide, MARGIN, 112, 176, 130),
              [(number, T_NUMBER, True, ink, None)])
    x_text = 225 if number else MARGIN
    rows = [(line, T_DIVIDER, True, ink, None) for line in title_lines]
    write(textbox(slide, x_text, 122, 920 - x_text, 150), rows)
    if subline:
        write(textbox(slide, x_text, 278, 920 - x_text, 30),
              [(subline, T_CARD, False, ink, None)])

    x = MARGIN
    for text in chips:
        faded = text in ghost
        chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Pt(x),
                                      Pt(CHIP_Y), Pt(CHIP_W), Pt(CHIP_H))
        chip.adjustments[0] = CORNER_PT / CHIP_H
        chip.shadow.inherit = False
        if faded:
            # a step this block does not contain: shown, but not filled in
            chip.fill.background()
            chip.line.color.rgb = ink
            chip.line.width = Pt(2)
        else:
            chip.fill.solid()
            chip.fill.fore_color.rgb = ink
            chip.line.fill.background()
        chip.text_frame.word_wrap = True
        write(chip, [(text, T_LEAD, True, ink if faded else BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += CHIP_W + CHIP_GAP
    return slide


def rows_layout(count, top=146, span=294):
    """Even row pitch for LIST, so every list in the deck shares a rhythm."""
    pitch = span / count
    height = pitch - min(10, pitch * 0.18)
    return [(top + i * pitch, height) for i in range(count)], height


def listing(slide, items, role=None, top=146, span=294, width=CONTENT_W,
            index_w=44):
    """3-7 peer items: an index, a statement, and an optional hint.

    Not CONCEPT (no two-way comparison to imply) and not PRACTICE (which
    signals "your turn" in tangerine). Rows are plain unless the whole set
    carries a meaning, in which case they take that role's surface.
    """
    placements, height = rows_layout(len(items), top, span)
    for (y, h), (index, statement, hint) in zip(placements, items):
        if role is not None:
            holder = card(slide, MARGIN, y, width, h, role.surface, pad=14)
            rows = [(statement, T_BODY, True, BLUE, None)]
            if hint:
                rows.append((hint, T_HINT, False, role.accent, 4))
            if index:
                rows.insert(0, (index, T_BODY, True, role.accent, None))
            write(holder, rows, anchor=MSO_ANCHOR.MIDDLE)
            continue
        if index:
            write(textbox(slide, MARGIN, y + 2, index_w, 26),
                  [(index, T_STATEMENT, True, GREEN, None)])
        body = textbox(slide, MARGIN + index_w, y, width - index_w, h)
        rows = [(statement, T_BODY, True, BLUE, None)]
        if hint:
            rows.append((hint, T_HINT, False, GREY_TEXT, 4))
        write(body, rows)
    return height
