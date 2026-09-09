#!/usr/bin/env python3
"""Measure a built deck for text overflow and out-of-bounds shapes.

Reads every text frame back out of the .pptx, re-wraps it with Arial metrics
and compares the required height against the shape. Catches overflow without
having to render and eyeball each slide.

Usage:  python3 check.py <deck.pptx>
"""
import sys

from pptx import Presentation
from pptx.util import Emu

from slidekit import SLIDE_H, SLIDE_W, wrapped_lines

# Role surfaces, by the hex the template's colour list defines for them.
# Grey and white carry no role, so they never count towards the limit.
ROLE_SURFACE = {"CBF2EC": "GOOD", "94E3D4": "GOOD",
                "FFD7D7": "AVOID", "FFACA6": "AVOID",
                "FFECBC": "ACTION", "FAE052": "ACTION",
                "E1D9FF": "PURPLE", "B8B2FF": "PURPLE"}
MAX_ROLES_PER_SLIDE = 2

# what the corporate master applies when a run declares no size of its own
INHERITED = {"TITLE": 24.0, "CENTER_TITLE": 24.0,
             "FOOTER": 10.0, "SLIDE_NUMBER": 10.0, "DATE": 10.0}
INHERITED_DEFAULT = 16.0


def pt(value):
    return Emu(value).emu / 12700


def frame_height(shape, width):
    """Height the shape's text needs, mirroring how write() sets spacing."""
    total = 0.0
    kind = ""
    if shape.is_placeholder:
        try:
            kind = str(shape.placeholder_format.type).split(" ")[0]
        except ValueError:
            kind = ""
    default = INHERITED.get(kind, INHERITED_DEFAULT)

    for i, para in enumerate(shape.text_frame.paragraphs):
        text = "".join(r.text for r in para.runs)
        if not text:
            continue
        sizes = [r.font.size.pt for r in para.runs if r.font.size is not None]
        size = max(sizes) if sizes else default
        bold = any(r.font.bold for r in para.runs)
        if para.space_before is not None and i:
            total += para.space_before.pt
        leading = (para.line_spacing.pt
                   if hasattr(para.line_spacing, "pt") and para.line_spacing
                   else round(size * 1.35))
        total += len(wrapped_lines(text, width, size, bold)) * leading
    return total


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    prs = Presentation(sys.argv[1])
    problems = []

    for index, slide in enumerate(prs.slides, 1):
        boxes = []
        for shape in slide.shapes:
            left, top = pt(shape.left), pt(shape.top)
            right, bottom = left + pt(shape.width), top + pt(shape.height)

            if left < -1 or top < -1 or right > SLIDE_W + 1 or \
                    bottom > SLIDE_H + 1:
                problems.append(
                    f"slide {index}: {shape.name} leaves the canvas "
                    f"({left:.0f},{top:.0f})-({right:.0f},{bottom:.0f})")

            if not shape.has_text_frame or not shape.text_frame.text.strip():
                continue

            tf = shape.text_frame
            pad_x = (tf.margin_left.pt if tf.margin_left is not None else 7.2) \
                + (tf.margin_right.pt if tf.margin_right is not None else 7.2)
            pad_y = (tf.margin_top.pt if tf.margin_top is not None else 3.6) \
                + (tf.margin_bottom.pt if tf.margin_bottom is not None else 3.6)

            needed = frame_height(shape, pt(shape.width) - pad_x)
            available = pt(shape.height) - pad_y
            if needed > available + 1:
                problems.append(
                    f"slide {index}: {shape.name!r} overflows by "
                    f"{needed - available:.0f}pt "
                    f"(needs {needed:.0f}, has {available:.0f}) - "
                    f"{shape.text_frame.text[:45]!r}")

            for r in para_runs(shape):
                if r.font.size is not None and r.font.size.pt < 12:
                    problems.append(
                        f"slide {index}: {r.text[:30]!r} at {r.font.size.pt}pt")

            boxes.append((shape.name, left, top, right, bottom))

        problems.extend(overlaps(index, boxes))
        problems.extend(role_load(index, slide))

    print("\n".join(problems) if problems
          else f"{len(prs.slides._sldIdLst)} slides: no overflow, "
               "no collisions, nothing below 12pt")
    sys.exit(1 if problems else 0)


def role_load(index, slide):
    """More than two roles on one slide and colour stops meaning anything."""
    found = []
    roles = set()
    for shape in slide.shapes:
        try:
            if shape.fill.type != 1:
                continue
            role = ROLE_SURFACE.get(str(shape.fill.fore_color.rgb))
        except Exception:
            continue
        if role:
            roles.add(role)
    if "PURPLE" in roles:
        found.append(f"slide {index}: purple is no longer a role")
    if len(roles) > MAX_ROLES_PER_SLIDE:
        found.append(f"slide {index}: {len(roles)} roles at once "
                     f"({', '.join(sorted(roles))})")
    return found


def para_runs(shape):
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            yield run


def overlaps(index, boxes):
    """Report text boxes that sit on top of each other."""
    found = []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            ox = min(a[3], b[3]) - max(a[1], b[1])
            oy = min(a[4], b[4]) - max(a[2], b[2])
            if ox > 4 and oy > 4:
                found.append(f"slide {index}: {a[0]!r} and {b[0]!r} overlap "
                             f"by {ox:.0f}x{oy:.0f}pt")
    return found


if __name__ == "__main__":
    main()
