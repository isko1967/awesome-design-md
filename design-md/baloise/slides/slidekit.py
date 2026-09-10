"""Shared layout system for the prompting-workshop deck.

Everything visual lives here so that the block modules only carry content.
Corporate values (Arial, the named colour list, margins, content zone, column
measures, footer band) come from the .potx; the composition is our own.

Colour carries meaning and never rotates by block:

    GOOD       the target state - positive examples, the improved output
    AVOID      the don't - negative examples, the pattern to steer away from
    GUARDRAIL  limits and rules - compliance notes, "do not", stop conditions
    NEUTRAL    raw material - the weak "before" output, prompt canvases
    ACTION     the participant's turn - practice, polls, clinic, transfer

Colour marks the artefact, not the sentence above it: a card that only names
an example stays neutral; the role colour goes on the example itself.
"""
import copy
import io
import os
import re
import tempfile
import zipfile

import cairosvg
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
RED, RED_LIGHT, RED_3 = rgb("D9304C"), rgb("FFACA6"), rgb("FFD7D7")
TANGERINE_1, TANGERINE_LIGHT, TANGERINE_3 = (rgb("B24A00"), rgb("FAE052"),
                                             rgb("FFECBC"))
# the corporate list has no neutral tint; these come from the design system
GREY_SURFACE = rgb("F6F6F6")
# There is no corporate grey for type. On a light ground text is Helvetia
# blue, on a dark one it is white; GREY_TEXT stays as a name so the block
# modules keep importing, but it resolves to blue.
GREY_TEXT = BLUE


class Role:
    """A semantic colour role: what the colour is saying, not which hue it is."""

    def __init__(self, surface, accent, ground=None):
        self.surface = surface
        self.accent = accent
        self.ground = ground or surface


GOOD = Role(GREEN_3, GREEN, GREEN_LIGHT)
# Helvetia Red on Red Tint 3 measures 3.6:1, which fails AA for body text.
# Red Tint 1 is the dark end of the same family and reaches 6.3:1, matching
# how the green role uses its dark base.
AVOID = Role(RED_3, rgb("99172D"), RED_LIGHT)
# Purple was a fourth role that nobody asked for; guardrails are things you
# must not do, so they belong to AVOID. The name stays as an alias so the
# block modules keep importing, but it resolves to red.
GUARDRAIL = AVOID
NEUTRAL = Role(GREY_SURFACE, GREY_TEXT, GREY_SURFACE)
ACTION = Role(GREY_SURFACE, GREY_TEXT, GREY_SURFACE)
# Something to pick reads as Helvetia blue with white type. Tangerine was
# carrying that job on 37 surfaces, far too loud for a supporting signal.
CHOICE = Role(BLUE, WHITE, BLUE)

# --- geometry, from the corporate template -----------------------------------
SLIDE_W, SLIDE_H = 960, 540
MARGIN = 41
CONTENT_W = 879
CONTENT_TOP = 120
CONTENT_BOTTOM = 480
BAND_TOP = 448          # full-width closing band
GUTTER = 22
COL2_W, COL2_X = 428, (41, 491)
# before -> after pairs run on a wider gutter, so the chevron sits
# between the two cards instead of on top of one of them
BA_GAP = 55
BA_W, BA_X = 412, (41, 508)
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

# Measured across the corporate template: 86 of 114 rounded shapes sit
# between 3 and 5pt, with 4pt the clear mode. The design system documents the
# same value as its "normal" radius; 12pt was its "large" radius, meant for
# overlays rather than for every card.
CORNER_PT = 4



# --- text metrics ------------------------------------------------------------
# Liberation Sans is metric-compatible with Arial, so measuring with it gives
# the same line breaks PowerPoint will produce on a corporate machine. Set
# SLIDEKIT_FONT_DIR to point at a directory holding LiberationSans-Regular.ttf
# and -Bold.ttf when they are not at the usual system path (e.g. Arimo, which
# shares Arial metrics, instanced under those names).
_FONT_DIR = os.environ.get(
    "SLIDEKIT_FONT_DIR", "/usr/share/fonts/truetype/liberation")
_FONT_FILE = {
    False: os.path.join(_FONT_DIR, "LiberationSans-Regular.ttf"),
    True: os.path.join(_FONT_DIR, "LiberationSans-Bold.ttf"),
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
    buffer = io.BytesIO()
    with zipfile.ZipFile(path) as zin, \
            zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(tpl.encode(), prs_type.encode())
            zout.writestr(item, data)
    buffer.seek(0)
    return Presentation(buffer)


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
    """A filled rounded rectangle.

    The brand uses no outlines, so `outline` is honoured only as a fill of
    last resort: an outline-only call becomes a solid CHOICE surface.
    """
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Pt(x), Pt(y), Pt(w), Pt(h))
    shape.adjustments[0] = CORNER_PT / min(w, h)
    if fill is None and outline is not None:
        fill = CHOICE.surface        # outlines are not part of the brand
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
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


def chevron(slide, y, h=34, x=None, colour=None):
    """The step from the "before" column to the "after" column.

    Centred in the widened BA gutter, so it never touches either card, and
    solid rather than outlined - the brand uses no outlines.
    """
    w = round(h * 0.7)
    if x is None:
        x = BA_X[0] + BA_W + (BA_GAP - w) / 2
    shape = slide.shapes.add_shape(MSO_SHAPE.CHEVRON,
                                   Pt(x), Pt(y - h / 2), Pt(w), Pt(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = colour or BLUE
    shape.line.fill.background()
    shape.shadow.inherit = False
    shape.text_frame.word_wrap = False
    return shape


def arrow(slide, x, y, size=16, colour=None, glyph="→"):
    box = textbox(slide, x, y, size + 10, size + 8)
    write(box, [(glyph, size, False, colour or GREY_TEXT, None)],
          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return box


# --- page furniture ----------------------------------------------------------
TITLE_STEPS = (T_TITLE, 30, 28)
TITLE_Y = 48          # the master says 38; 10pt lower stops the header
                      # reading as text pinned into the corner
LEAD_Y = 100
CONTENT_START = 132   # where the first content shape sits, on every slide

# Where content may start. A slide with a lead needs real air under the header
# block, otherwise title, lead, label and first card read as one mass pinned
# to the top-left corner. Without a lead the corporate 120 still applies.
CONTENT_TOP_LEAD = 136


def title(slide, text, width=CONTENT_W, has_lead=True, top=TITLE_Y):
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
    if lines > 1:
        if has_lead:
            # Shrinking below 28pt makes the title look stranded next to an
            # 18pt lead, so the wording has to give instead.
            print(f"  TITLE TOO LONG for one line at {TITLE_STEPS[-1]}pt, "
                  f"reword: {text!r}")
        else:
            size, lines = T_TITLE, len(
                wrapped_lines(text, width - 4, T_TITLE, bold=True))

    shape.left = Pt(MARGIN)
    shape.top = Pt(top)
    shape.height = Pt(round(size * 1.35) * lines + 8)
    write(shape, [(text, size, True, BLUE, None)])
    return top + round(size * 1.35) * lines + 8


def lead(slide, text, y=LEAD_Y, width=CONTENT_W):
    """The line under the title. Never larger than the title above it.

    Sizes its box to the wrapped height so a lead that runs to two lines is
    not clipped; the content zone starts at 146, leaving room for two.
    """
    lines = len(wrapped_lines(text, width, T_LEAD))
    h = lines * round(T_LEAD * 1.35)
    return write(textbox(slide, MARGIN, y, width, h),
                 [(text, T_LEAD, False, BLUE, None)])


def icon_inline(slide, name, x, text_y, text_size=T_BODY, colour=None):
    """An icon on the same optical line as the text it precedes.

    Every hand-placed icon drifted off the baseline because the offset was
    guessed per call. The glyph box is 1.15x the cap height and its centre is
    set on the text's centre, so it lines up wherever it is used. Returns the
    x at which the text should start.
    """
    size = round(text_size * 1.15)
    line = round(text_size * 1.35)
    icon(slide, name, x, text_y + (line - size) / 2 + 1, size, colour or BLUE)
    return x + size + 10



EYEBROW_MAX = 24
LABEL_NAME = "Label"
LABEL_ICON_NAME = "LabelIcon"

# Which icon belongs to which recurring label. Only labels that name a
# familiar thing get one; a label with no obvious motif stays plain rather
# than borrowing a vague symbol.
LABEL_ICON = {
    "Example": "document", "The prompt": "document",
    "Reusable prompt": "document", "Starting prompt": "document",
    "Both runs": "document", "The four criteria": "check-circle",
    "The criteria": "check-circle", "Watch for": "search",
    "Self-critique": "search", "Review before execution": "search",
    "The weak result": "alert-triangle", "The result was": "alert-triangle",
    "It failed": "alert-triangle",
    "Why one change?": "info-circle", "Use when": "info-circle",
    "Scenario": "message", "What the model infers": "settings",
    "What to specify": "settings", "Process": "refresh",
    "What made the difference": "refresh",
    "With examples": "check-circle", "With context": "check-circle",
    "Version 2": "check-circle", "Version 2 adds": "check-circle",
}
LABEL_GAP = 10   # between a label and the field it names


def eyebrow(slide, text, x=MARGIN, y=CONTENT_TOP, w=CONTENT_W, colour=None):
    """A short label in capitals.

    Capitals are hard to read in quantity, so an eyebrow is a label of a few
    words, never a sentence. Anything longer belongs in the lead or in the
    card itself.
    """
    if len(text) > EYEBROW_MAX:
        raise ValueError(
            f"eyebrow is {len(text)} characters, max {EYEBROW_MAX}: {text!r}")
    # Capitals read slowly and, set in grey, the label drifted away from the
    # thing it names. Sentence case in brand blue, moved down towards its
    # element, ties the two together.
    # Dropping capitals removed the signal that said "this is a label", so
    # the weight has to come from size and colour instead. Sitting a little
    # higher also puts real air between the label and the field below it.
    motif = LABEL_ICON.get(text)
    start = x
    if motif:
        start = icon_inline(slide, motif, x + 1, y - 6, T_LEAD, colour or BLUE)
        slide.shapes[-1].name = LABEL_ICON_NAME
    box = textbox(slide, start, y - 6, w - (start - x), 24)
    box.name = LABEL_NAME          # snap_labels() pins it to its own field
    return write(box, [(text, T_LEAD, True, colour or BLUE, None)])


def badge(slide, text, x=790, y=36, w=130, h=40, role=ACTION):
    chip = card(slide, x, y, w, h, role.surface, pad=6)
    return write(chip, [(text, T_BODY, True, BLUE, None)],
                 anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def band(slide, label_text, body_text, role=None, y=BAND_TOP, h=32):
    """The recurring full-width closing statement.

    Always neutral. It is furniture that appears on nearly every slide, so
    giving it a role colour turned that colour into background noise instead
    of a signal. `role` is accepted and ignored so the block modules keep
    working; the argument should be dropped as they are touched.
    """
    # the lamp eats 46pt of width, so a long statement can need a second line
    lines = len(wrapped_lines(f"{label_text}   {body_text}",
                              CONTENT_W - 46 - 14, T_BODY, bold=False))
    h = max(h, lines * round(T_BODY * 1.35) + 10)
    strip = card(slide, MARGIN, y, CONTENT_W, h, NEUTRAL.surface, pad=14)
    strip.text_frame.margin_top = strip.text_frame.margin_bottom = Pt(4)
    strip.text_frame.margin_left = Pt(46)
    brand_icon(slide, "light-bulb-green", MARGIN + 12, y + 4, h - 8)
    return runs(strip, [(f"{label_text}   ", True, BLUE),
                        (body_text, False, BLUE)])


PHASES = ("LEARN", "SEE", "TRY", "IMPROVE", "INTERACT")
PHASE_W, PHASE_H, PHASE_GAP, PHASE_Y = 84, 18, 6, 22
PHASE_NAME = "Phase"


def phase_chips(slide, active):
    """The cycle as a row of chips in the top right corner.

    Taken from the prepared workshop template: the phase is visible on every
    slide instead of hiding in the footer, and the participants can see where
    in LEARN - SEE - TRY - IMPROVE they are.
    """
    total = len(PHASES) * PHASE_W + (len(PHASES) - 1) * PHASE_GAP
    x = MARGIN + CONTENT_W - total
    for name in PHASES:
        on = name == active
        chip = card(slide, x, PHASE_Y, PHASE_W, PHASE_H,
                    GOOD.ground if on else GREY_SURFACE, pad=4)
        chip.name = PHASE_NAME
        chip.text_frame.margin_top = chip.text_frame.margin_bottom = Pt(0)
        # no caps-lock labels anywhere in the deck
        write(chip, [(name.capitalize(), 10, True, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        x += PHASE_W + PHASE_GAP


def icon_tile(slide, name, x, y, size=32, role=None):
    """An icon on a tinted tile, the way the workshop template sets them."""
    role = role or GOOD
    card(slide, x, y, size, size, role.ground, pad=0)
    icon(slide, name, x + size * 0.22, y + size * 0.22, size * 0.56, BLUE)


def footer(slide, block_label, phase, number):
    kinds = {s.placeholder_format.idx: str(s.placeholder_format.type)
             for s in slide.slide_layout.placeholders}
    if phase in PHASES:
        phase_chips(slide, phase)
    text = block_label
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


def tangerine_slide(prs):   # kept as a name so the block modules still call it
    """A full-bleed tangerine landmark: the break, clinic opener and close.

    Grounds are structural: participation landmarks sit on tangerine. The ink
    is corporate blue - the light-tangerine ground keeps the dark master logo
    visible, so '1 Content' is fine here.
    """
    # The brand's serial-colouring rule asks for one primary palette per
    # presentation, so the landmarks share the technique dividers' blue
    # ground rather than opening a second family.
    return blue_slide(prs)


def blue_slide(prs):
    """A full-bleed corporate-blue slide with the white logo."""
    return new_slide(prs, with_title=False, layout="Quote-blue")


# --- archetypes --------------------------------------------------------------
CHIP_W, CHIP_GAP, CHIP_H, CHIP_Y = 207, 17, 84, 376


def divider(slide, number, title_lines, subline, chips=(), ghost=(),
            ink=WHITE):
    # A hollow chip needed an outline, which the brand does not use, and it
    # read as a mistake rather than as "this block stops here". A block now
    # shows only the steps it runs, spread over the same width.
    chips = tuple(c for c in chips if c not in ghost)
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

    if chips:
        width = (CONTENT_W - CHIP_GAP * (len(chips) - 1)) / len(chips)
        for i, text in enumerate(chips):
            chip = card(slide, MARGIN + i * (width + CHIP_GAP), CHIP_Y,
                        width, CHIP_H, ink)
            write(chip, [(text.capitalize() if text.isupper() else text,
                          T_LEAD, True, BLUE, None)],
                  anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return slide


def rows_layout(count, top=146, span=294):
    """Even row pitch for LIST, so every list in the deck shares a rhythm."""
    pitch = span / count
    height = pitch - min(10, pitch * 0.18)
    return [(top + i * pitch, height) for i in range(count)], height


def listing(slide, items, role=None, top=146, span=294, width=CONTENT_W,
            index_w=44):
    # A set of items with no numbers was still being pushed right by the
    # width of the missing number, which left them floating mid-slide.
    if not any(index for index, _, _ in items):
        index_w = 0
    """3-7 peer items: an index, a statement, and an optional hint.

    Not CONCEPT (no two-way comparison to imply) and not PRACTICE (which
    signals "your turn" in tangerine). Rows are plain unless the whole set
    carries a meaning, in which case they take that role's surface.
    """
    placements, height = rows_layout(len(items), top, span)
    pad = 10 if height < 56 else 14
    for (y, h), (index, statement, hint) in zip(placements, items):
        if role is not None:
            holder = card(slide, MARGIN, y, width, h, role.surface, pad=pad)
            rows = [(statement, T_BODY, True, BLUE, None)]
            if hint:
                rows.append((hint, T_HINT, False, role.accent, 4))
            if index:
                rows.insert(0, (index, T_BODY, True, role.accent, None))
            write(holder, rows, anchor=MSO_ANCHOR.MIDDLE)
            continue
        if index:
            write(textbox(slide, MARGIN, y, index_w, h),
                  [(index, T_STATEMENT, True, GREEN, None)],
                  anchor=MSO_ANCHOR.MIDDLE)
        body = textbox(slide, MARGIN + index_w, y, width - index_w, h)
        rows = [(statement, T_BODY, True, BLUE, None)]
        if hint:
            rows.append((hint, T_HINT, False, GREY_TEXT, 4))
        write(body, rows, anchor=MSO_ANCHOR.MIDDLE)
    return height


def flow_column(slide, x, w, steps, top, cell_h, gap=22, role=NEUTRAL,
                connector="↓", head_colour=None, size=T_BODY, pad=None):
    """A vertical run of steps with a connector glyph between each.

    FLOW's building block: the order is the message, so every step is the
    same width and the connector is explicit. `steps` are (heading, body)
    pairs; body may be None for a bare step. The connector is drawn in a box
    that exactly fills the gap between two cells, so it never overlaps either.
    On a dense slide, pass a smaller `size` to fit more steps in the column.
    """
    head_colour = head_colour or role.accent
    if pad is None:
        pad = 6 if cell_h < 48 else 12
    y = top
    for i, (heading, body) in enumerate(steps):
        if i and gap >= 16:
            # 12pt connector in a box that fills the gap; never sub-12pt,
            # never taller than the gap, so check.py stays quiet.
            box = textbox(slide, x + w / 2 - 9, y - gap, 18, gap)
            write(box, [(connector, 12, False, GREY_TEXT, None)],
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cell = card(slide, x, y, w, cell_h, role.surface, pad=pad)
        rows = [(heading, size, True, head_colour, None)]
        if body:
            rows.append((body, T_HINT, False, BLUE, 4))
        write(cell, rows, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER
              if body is None else PP_ALIGN.LEFT)
        y += cell_h + gap
    return y


def flow_row(slide, steps, top, cell_h, x=MARGIN, width=CONTENT_W, gap=26,
             role=NEUTRAL, head_colour=None):
    """A horizontal run of steps, arrow between each. Order is the message.

    The arrow sits in a box the width of the gap, centred vertically, so it
    never overlaps the cells on either side.
    """
    head_colour = head_colour or role.accent
    n = len(steps)
    cell_w = (width - (n - 1) * gap) / n
    for i, (heading, body) in enumerate(steps):
        cx = x + i * (cell_w + gap)
        if i:
            box = textbox(slide, cx - gap, top + cell_h / 2 - 11, gap, 22)
            write(box, [("→", 16, False, GREY_TEXT, None)],
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cell = card(slide, cx, top, cell_w, cell_h, role.surface, pad=12)
        rows = [(heading, T_BODY, True, head_colour, None)]
        if body:
            rows.append((body, T_HINT, False, BLUE, 4))
        write(cell, rows, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return cell_w


def settle(slide, start=CONTENT_START, floor=BAND_TOP):
    """Give every slide the same gap between header and content.

    The block modules hard-code the y of their first content shape, and those
    values drifted from 108 to 168 across the deck. Rather than chase them one
    by one, this shifts the whole content band so that its top always sits at
    `start`, as long as the bottom still clears the closing band.
    """
    movable = []
    for shape in slide.shapes:
        top = shape.top / 12700
        if shape.is_placeholder and shape.placeholder_format.idx == 0:
            continue
        if top < 100 or top >= 448:
            continue
        movable.append((shape, top, top + shape.height / 12700))
    if not movable:
        return 0

    wanted = start - min(t for _, t, _ in movable)
    if wanted <= 0:
        return 0

    # Shift by whatever slack the slide has. A slide with none keeps its
    # tighter header; check.py reports it, so the content gets trimmed by hand
    # rather than by a rule that cannot see which card is already full.
    slack = floor - max(b for _, _, b in movable)
    delta = min(wanted, slack)
    if delta <= 0:
        return 0
    for shape, _, _ in movable:
        shape.top = shape.top + int(round(delta * 12700))
    return delta


def snap_labels(slide, gap=LABEL_GAP):
    """Pin every label to the field beneath it.

    Labels were placed at a y of their own, so the distance to the thing they
    name drifted from slide to slide and they ended up floating between the
    header and the content. Each one is moved to sit a fixed gap above the
    nearest shape below it that shares its column.
    """
    labels = [sh for sh in slide.shapes if sh.name == LABEL_NAME]
    glyphs = [sh for sh in slide.shapes if sh.name == LABEL_ICON_NAME]
    others = [sh for sh in slide.shapes
              if sh.name not in (LABEL_NAME, LABEL_ICON_NAME)]
    for label in labels:
        left, right = label.left, label.left + label.width
        below = [sh for sh in others
                 if sh.top > label.top
                 and sh.left < right and (sh.left + sh.width) > left]
        if not below:
            continue
        target = min(sh.top for sh in below)
        # never climb into the lead: on a full slide the gap gives instead
        above = [sh.top + sh.height for sh in others
                 if sh.top < label.top
                 and sh.left < right and (sh.left + sh.width) > left]
        ceiling = max(above) + int(round(6 * 12700)) if above else 0
        ideal = target - int(round((gap + 24) * 12700))
        # raise to clear the lead, but never far enough to sit on the field
        was = label.top
        label.top = min(max(ideal, ceiling), target - int(round(24 * 12700)))
        # the label's icon is its own shape and has to travel with it
        for glyph in glyphs:
            if abs(glyph.top - was) < int(round(14 * 12700)) \
                    and abs(glyph.left - label.left) < int(round(40 * 12700)):
                glyph.top += label.top - was


# --- icons -------------------------------------------------------------------
# The design system's UI icons (Streamline Core Solid) as single-path SVGs.
# They carry a fill attribute, so they can be recoloured before rasterising.
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "assets", "icons")
_ICON_CACHE = {}


def icon(slide, name, x, y, size=20, colour=None):
    """Place one design-system icon.

    PowerPoint will not render an SVG reliably across versions, so each icon
    is rasterised at 8x and placed as a PNG.
    """
    colour = colour or BLUE
    key = (name, str(colour), size)
    if key not in _ICON_CACHE:
        with open(os.path.join(ICON_DIR, f"{name}.svg"), "rb") as handle:
            svg = handle.read().decode("utf-8")
        svg = re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="#{colour}"', svg, count=1)
        png = os.path.join(tempfile.gettempdir(),
                           f"ds-{name}-{colour}-{size}.png")
        if not os.path.exists(png):
            cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=png,
                             output_width=size * 8, output_height=size * 8)
        _ICON_CACHE[key] = png
    return slide.shapes.add_picture(_ICON_CACHE[key], Pt(x), Pt(y),
                                    Pt(size), Pt(size))


def label_block(slide, text, x, y, w, role=None):
    """A filled label sitting on top of the field it names.

    Taken from Helvetia's own decks, where a dark family colour carries the
    section name in white above the lighter content boxes. It anchors the
    label instead of letting it float between the header and the content.
    """
    role = role or CHOICE
    dark = role.accent if role is not CHOICE else CHOICE.surface
    block = card(slide, x, y, w, 26, dark, pad=12)
    block.text_frame.margin_top = block.text_frame.margin_bottom = Pt(2)
    return write(block, [(text, T_HINT, True, WHITE, None)],
                 anchor=MSO_ANCHOR.MIDDLE)


BRAND_ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "assets", "brand-icons")


def brand_icon(slide, name, x, y, size=28):
    """One of the design system's brand icons.

    These are two-tone and ship pre-coloured per family, so unlike the UI
    icons they are placed as they are. Most of the 431 motifs are insurance
    products; only a handful are generic enough for a workshop deck.
    """
    png = os.path.join(tempfile.gettempdir(), f"ds-brand-{name}-{size}.png")
    if not os.path.exists(png):
        cairosvg.svg2png(url=os.path.join(BRAND_ICON_DIR, f"{name}.svg"),
                         write_to=png, output_width=size * 8,
                         output_height=size * 8)
    return slide.shapes.add_picture(png, Pt(x), Pt(y), Pt(size), Pt(size))


def bullet_list(shape, items, size=T_BODY, colour=None, marker="•"):
    """A real list. A stack of bare words reads as leftover text."""
    colour = colour or BLUE
    tf = shape.text_frame
    tf.word_wrap = True
    tf.clear()
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = Pt(round(size * 1.45))
        if i:
            p.space_before = Pt(4)
        mark = p.add_run()
        mark.text = f"{marker}   "
        mark.font.size = Pt(size)
        mark.font.color.rgb = GOOD.accent
        body = p.add_run()
        body.text = item
        body.font.size = Pt(size)
        body.font.color.rgb = colour
    return shape


def task_header(slide, label, badge_text=None, y=104, role=None):
    """The section line under a title: a heading on the left, an optional
    badge on the right.

    A bare sentence set in regular type read as leftover text rather than as
    the heading of what follows, and the badge sat in the title row where it
    now collides with the phase chips.
    """
    write(textbox(slide, MARGIN, y, 500, 26),
          [(label, T_LEAD, True, BLUE, None)])
    if badge_text:
        role = role or CHOICE
        chip = card(slide, 770, y - 5, 150, 34, role.surface, pad=8)
        write(chip, [(badge_text, T_BODY, True,
                      WHITE if role is CHOICE else BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return y + 34
