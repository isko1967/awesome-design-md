"""02 - The prompt as a briefing (slides 13-19).

The briefing analogy, the three essentials and their boosters, the six
building blocks, the vague-to-precise pair, the first practice round, the
reflection and the pattern names participants will hear elsewhere.
"""
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from slidekit import (ACTION, AVOID, BA_W, BA_X, BLUE, COL2_W, COL2_X, COL3_W,
                      COL3_X, COL4_W, COL4_X, CONTENT_W, GOOD, GREEN, MARGIN,
                      NEUTRAL, T_BODY, T_CARD, T_HINT, T_LEAD, T_META,
                      T_STATEMENT, band, card, chevron, eyebrow, footer, lead,
                      new_slide, runs, task_header, textbox, title, write)
from essentials.ess_00 import lettered_chips

LABEL = "02  The prompt as a briefing"


def _foot(slide, phase, number):
    footer(slide, LABEL, phase, number)


def slide_13(prs):
    s = new_slide(prs)
    title(s, "A prompt is a briefing, not a magic command.", has_lead=False)

    eyebrow(s, "The comparison", y=150)
    comparison = card(s, MARGIN, 186, CONTENT_W, 86, NEUTRAL.surface, pad=20)
    write(comparison, [("You are briefing a capable new colleague who has no "
                        "context.", T_STATEMENT, True, BLUE, None)],
          anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    for i, item in enumerate(("What you need", "Why", "For whom",
                              "What good looks like")):
        cell = card(s, COL4_X[i], 300, COL4_W, 108, GOOD.surface, pad=12)
        write(cell, [(item, T_BODY, True, GOOD.accent, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    _foot(s, "LEARN", 13)


def slide_14(prs):
    s = new_slide(prs)
    title(s, "Start with three essentials.")
    lead(s, "Add control only where it improves the result.")

    essentials = [
        ("Task", "What should AI do?",
         "Name the action and the outcome, not the topic."),
        ("Context", "What does it need to know?",
         "Only the facts that would change the answer."),
        ("Format", "What should the result look like?",
         "Headings, length, structure."),
    ]
    for i, (head, question, hint) in enumerate(essentials):
        cell = card(s, COL3_X[i], 150, COL3_W, 150, GOOD.surface, pad=16)
        write(cell, [(head, T_CARD, True, GOOD.accent, None),
                     (question, T_BODY, True, BLUE, 8),
                     (hint, T_HINT, False, BLUE, 6)],
              anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "Boosters", y=320)
    for i, item in enumerate(("Role", "Example", "Tone")):
        chip = card(s, COL3_X[i], 352, COL3_W, 48, NEUTRAL.surface, pad=10)
        write(chip, [(item, T_BODY, True, BLUE, None)],
              anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    band(s, "Not a checklist",
         "Use a booster only when it reduces uncertainty. A prompt is not "
         "better because it is longer.")
    _foot(s, "LEARN", 14)


def slide_15(prs):
    s = new_slide(prs)
    title(s, "Six building blocks.")
    lead(s, "Use the ones that reduce uncertainty.")

    blocks = [
        ("Task", "Action and outcome", True),
        ("Context", "Only facts that change the answer", True),
        ("Format", "Headings, length, structure", True),
        ("Role", "A useful perspective to answer from", False),
        ("Example", "Show what acceptable looks like", False),
        ("Tone", "Fit the audience", False),
    ]
    gap_x, gap_y = 20, 22
    w = (CONTENT_W - 2 * gap_x) / 3
    h = 136
    for i, (head, body, essential) in enumerate(blocks):
        row, col = divmod(i, 3)
        role = GOOD if essential else NEUTRAL
        cell = card(s, MARGIN + col * (w + gap_x), 150 + row * (h + gap_y),
                    w, h, role.surface, pad=16)
        write(cell, [(head, T_CARD, True,
                      GOOD.accent if essential else BLUE, None),
                     (body, T_BODY, False, BLUE, 8)],
              anchor=MSO_ANCHOR.MIDDLE)

    _foot(s, "LEARN", 15)


def slide_16(prs):
    s = new_slide(prs)
    title(s, "The same request, briefed properly.")

    eyebrow(s, "Before", x=BA_X[0], w=BA_W)
    eyebrow(s, "After", x=BA_X[1], w=BA_W, colour=GOOD.accent)

    before = card(s, BA_X[0], 146, BA_W, 296, NEUTRAL.surface, pad=20)
    write(before, [("Write a project update.", T_STATEMENT, False, BLUE,
                    None)], anchor=MSO_ANCHOR.MIDDLE)

    after = card(s, BA_X[1], 146, BA_W, 296, GOOD.surface, pad=20)
    chevron(s, 294)
    paragraphs = [
        "Write a short project update for the two team leads who have to "
        "re-plan their work.",
        "Status: release moves from 14 Oct to 4 Nov. Cause: vendor interface "
        "defects found in test. Budget unchanged. Owner of the fix: not yet "
        "assigned.",
        "Format: four short paragraphs, no headings. State the new date in "
        "the first sentence. Do not speculate about the cause. If something "
        "is missing, write “not provided” — do not fill the gap.",
    ]
    write(after, [(text, T_HINT, False, BLUE, None if i == 0 else 10)
                  for i, text in enumerate(paragraphs)],
          anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "SEE", 16)


def slide_17(prs):
    s = new_slide(prs)
    title(s, "Write a prompt for a task you actually have.", width=729)
    task_header(s, "Your task", "9 min")

    steps = [
        ("1", "Pick a task you actually have this week."),
        ("2", "Write it with task, context and format."),
        ("3", "Add one booster — only if you can say why."),
        ("4", "Run it. Keep the result open."),
    ]
    top, pitch = 150, 62
    for i, (num, text) in enumerate(steps):
        cell = card(s, MARGIN, top + i * pitch, CONTENT_W, pitch - 10,
                    ACTION.surface, pad=12)
        runs(cell, [(f"{num}   ", True, GREEN), (text, True, BLUE)],
             size=T_BODY, anchor=MSO_ANCHOR.MIDDLE)

    band(s, "On your own",
         "Keep it generic — no personal, customer or confidential "
         "information.")
    _foot(s, "TRY", 17)


def slide_18(prs):
    s = new_slide(prs)
    title(s, "Which addition removed the most guessing?", has_lead=False)
    task_header(s, "Reflect", "3 min", y=140)

    lettered_chips(s, [
        ("A", "Naming the audience"),
        ("B", "Giving the real status"),
        ("C", "Setting the format"),
        ("D", "Saying what not to do"),
    ], top=190, pitch=56, h=46)
    _foot(s, "IMPROVE", 18)


def slide_19(prs):
    s = new_slide(prs)
    title(s, "Start with the work verb.")
    lead(s, "Patterns help you start — they do not replace judgment.")

    verbs = [
        ("Brief", "Create something from a need."),
        ("Rewrite", "Transform text that already exists."),
        ("Summarize", "Reduce to what matters for one reader."),
        ("Extract", "Pull structured facts from messy input."),
    ]
    for i, (head, body) in enumerate(verbs):
        cell = card(s, COL4_X[i], 150, COL4_W, 104, NEUTRAL.surface, pad=14)
        write(cell, [(head, T_CARD, True, BLUE, None),
                     (body, T_HINT, False, BLUE, 8)],
              anchor=MSO_ANCHOR.MIDDLE)

    eyebrow(s, "You may hear RTF or TAG", y=274)
    rtf = card(s, COL2_X[0], 306, COL2_W, 126, NEUTRAL.surface, pad=16)
    write(rtf, [
        ("R — Role: You review supplier updates.", T_HINT, False, BLUE, None),
        ("T — Task: Summarize this delay for two team leads who must "
         "re-plan.", T_HINT, False, BLUE, 6),
        ("F — Format: Four short paragraphs, new date in the first "
         "sentence.", T_HINT, False, BLUE, 6),
    ], anchor=MSO_ANCHOR.MIDDLE)

    tag = card(s, COL2_X[1], 306, COL2_W, 126, NEUTRAL.surface, pad=16)
    write(tag, [
        ("T — Task     A — Action     G — Goal", T_HINT, True, BLUE, None),
        ("Same three questions, different labels. Use whichever one you "
         "actually remember — they are checklists, not techniques.",
         T_HINT, False, BLUE, 8),
    ], anchor=MSO_ANCHOR.MIDDLE)
    _foot(s, "LEARN", 19)


SLIDES = [slide_13, slide_14, slide_15, slide_16, slide_17, slide_18,
          slide_19]
