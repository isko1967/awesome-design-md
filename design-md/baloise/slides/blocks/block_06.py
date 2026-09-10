"""Block 6 - Prompt Clinic (slides 46-49).

A tangerine opener, the eight-step Clinic loop (FLOW loop), one mandatory full
live case and one optional compressed case. Live-case fields stay as
placeholders - they are filled from participant submissions on the day.
Content is verbatim from the source deck; only the layout is ours.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (task_header, WHITE, CHOICE, ACTION, AVOID, BLUE, COL2_W, COL2_X, CONTENT_W, GOOD,
                      GREEN, GREY_TEXT, GUARDRAIL, MARGIN, NEUTRAL, T_BODY,
                      T_CARD, T_DIVIDER, T_HINT, T_LEAD, T_META, T_NUMBER,
                      T_STATEMENT, badge, band, blue_slide, card, divider,
                      eyebrow, footer, lead, new_slide, runs,
                      tangerine_slide, textbox, title, write)

LABEL = "06  Prompt Clinic"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_46(prs):
    """The Clinic opener. Naming the five techniques turns an empty field into
    the agenda for what follows."""
    s = blue_slide(prs)
    write(textbox(s, MARGIN, 120, CONTENT_W, 66),
          [("Prompt Clinic", T_DIVIDER, True, WHITE, None)])
    write(textbox(s, MARGIN, 200, CONTENT_W, 32),
          [("Real tasks. Diagnose → change → compare.",
            T_STATEMENT, False, WHITE, None)])
    write(textbox(s, MARGIN, 244, CONTENT_W, 26),
          [("Now we combine the five techniques.", T_LEAD, True, WHITE, None)])

    techniques = ["01 Few-shot", "02 Persistent context", "03 Decomposition",
                  "04 Self-critique", "05 Debugging"]
    width = (CONTENT_W - 16 * 4) / 5
    for i, text in enumerate(techniques):
        chip = card(s, MARGIN + i * (width + 16), 320, width, 84, WHITE,
                    pad=12)
        write(chip, [(text, T_BODY, True, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    footer(s, LABEL, None, 46)


def slide_47(prs):
    """FLOW loop - eight steps in a 4x2 grid. Step titles are kept under 24
    characters (a content constraint from ARCHETYPES.md) so every cell fits
    the same grid. Top row flows right, bottom row flows left, so the last
    step sits under the first and the loop closes visually."""
    s = new_slide(prs)
    title(s, "The Prompt Clinic loop.", has_lead=False)

    steps = [
        ("01", "Situation", "What are we trying to achieve?"),
        ("02", "Define good", "What would a good result do?"),
        ("03", "Choose technique", "Which technique fits best?"),
        ("04", "Build & run", "Test the prompt."),
        ("05", "Diagnose", "Why did the result fail?"),
        ("06", "Change one thing", "Make one targeted change."),
        ("07", "Rerun", "Test again."),
        ("08", "Compare", "Better? Why?"),
    ]
    cols, gap_x, gap_y = 4, 20, 24
    cell_w = (CONTENT_W - (cols - 1) * gap_x) / cols
    cell_h = 104
    top = 150
    # top row left-to-right (0-3), bottom row left-to-right holds 4-7 but we
    # place them so 07,06,05 read right-to-left back towards 04 -> the loop
    order = [0, 1, 2, 3, 7, 6, 5, 4]
    positions = {}
    for slot, idx in enumerate(order):
        row, col = divmod(slot, cols)
        x = MARGIN + col * (cell_w + gap_x)
        y = top + row * (cell_h + gap_y)
        positions[idx] = (x, y)
        num, head, sub = steps[idx]
        role = GOOD if idx in (0, 4) else NEUTRAL
        cell = card(s, x, y, cell_w, cell_h, role.surface, pad=12)
        write(cell, [
            (num, T_META, True, GREEN if role is GOOD else GREY_TEXT, None),
            (head, T_BODY, True, BLUE, 4),
            (sub, T_HINT, False, GREY_TEXT, 6),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    # connectors: → along the top row, ↓ from 04 to 05, ← along the bottom row
    def connector(x, y, glyph, w=gap_x, h=22):
        box = textbox(s, x, y, w, h)
        write(box, [(glyph, T_HINT, False, BLUE, None)],
              align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    midy = top + cell_h / 2 - 11
    for col in range(cols - 1):
        cx = MARGIN + (col + 1) * cell_w + col * gap_x
        connector(cx, midy, "→")
    # 04 (top-right) down to 05 (bottom-right)
    x4, y4 = positions[3]
    connector(x4 + cell_w / 2 - 9, y4 + cell_h + 1, "↓", w=18, h=gap_y - 2)
    midy2 = top + cell_h + gap_y + cell_h / 2 - 11
    for col in range(cols - 1):
        cx = MARGIN + (col + 1) * cell_w + col * gap_x
        connector(cx, midy2, "←")

    band(s, "The loop",
         "Steps 05–08 repeat until the result is good enough.", GOOD)
    _foot(s, None, 47)


def _clinic_field(slide, x, y, w, h, label, body, role=NEUTRAL,
                  label_colour=None, size=T_HINT):
    cell = card(slide, x, y, w, h, role.surface, pad=12)
    write(cell, [(label, T_META, True, label_colour or GREY_TEXT, None),
                 (body, size, False, BLUE, 5)], anchor=MSO_ANCHOR.MIDDLE)
    return cell


def slide_48(prs):
    """Live case 1 - the mandatory full case. Fields are placeholders."""
    s = new_slide(prs)
    title(s, "Live case: [selected participant task].", width=729,
          has_lead=False)
    task_header(s, "Live case", "Case 1")

    _clinic_field(s, MARGIN, 150, COL2_W, 76, "Situation",
                  "[Insert genericised submitted case]")
    _clinic_field(s, MARGIN, 234, COL2_W, 76, "Current prompt",
                  "[Insert current prompt]")
    _clinic_field(s, MARGIN, 318, COL2_W, 76, "Define good",
                  "What would a good result need to do?")

    eyebrow(s, "Choose technique", x=COL2_X[1], w=COL2_W,
            colour=ACTION.accent)
    techs = ["01 Few-shot", "02 Persistent context", "03 Decomposition",
             "04 Self-critique", "05 Debugging"]
    x = COL2_X[1]
    ty = 176
    w = (COL2_W - 16) / 2
    for i, t in enumerate(techs):
        col, row = i % 2, i // 2
        chip = card(s, x + col * (w + 16), ty + row * 42, w, 34, None,
                    outline=CHOICE.surface, pad=8)
        write(chip, [(t, T_HINT, True, WHITE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    _clinic_field(s, COL2_X[1], 296, COL2_W, 76, "Diagnose",
                  "Missing context, unclear criteria, wrong structure, or an "
                  "instruction that is not specific enough.", role=NEUTRAL)
    _clinic_field(s, COL2_X[1], 380, COL2_W, 58, "Our change",
                  "[Fill in live]", role=ACTION, label_colour=ACTION.accent)

    band(s, "Compare", "Better? Why?")
    _foot(s, None, 48)


def slide_49(prs):
    """Optional compressed mini case."""
    s = new_slide(prs)
    title(s, "Mini case: [selected participant task].", width=729,
          has_lead=False)
    task_header(s, "Mini case", "Optional")

    steps = [
        ("1  Situation", "What are we trying to achieve?"),
        ("2  Choose technique", "Which technique fits?"),
        ("3  Diagnose", "What is the main issue?"),
        ("4  Change one thing", "What is the smallest useful change?"),
        ("5  Compare", "Better? Why?"),
    ]
    top, pitch = 146, 54
    for i, (head, sub) in enumerate(steps):
        y = top + i * pitch
        cell = card(s, MARGIN, y, CONTENT_W, pitch - 8, NEUTRAL.surface,
                    pad=10)
        runs(cell, [(head + "   ", True, GREEN), (sub, False, GREY_TEXT)],
             size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)

    note = card(s, MARGIN, 420, CONTENT_W, 40, NEUTRAL.surface, pad=10)
    write(note, [("Only if time allows.", T_BODY, True, GREY_TEXT, None)],
          anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    _foot(s, None, 49)


SLIDES = [slide_46, slide_47, slide_48, slide_49]
