#!/usr/bin/env python3
"""
Add a Customer Journey Map slide to the AI Engineering Business Use Cases deck.
Maps all 24 UCs to a 4-stage enterprise adoption path.
Insert after Implementation Roadmap (slide 31), before Engagement Model (slide 32).
"""

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

FONT = "Calibri"
NAVY = RGBColor(0x1F, 0x3B, 0x6E)
RED = RGBColor(0xE3, 0x18, 0x37)
GREEN = RGBColor(0x16, 0x65, 0x34)
DARK_TEXT = RGBColor(0x1A, 0x1A, 0x1A)
GRAY = RGBColor(0x6B, 0x72, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
AMBER = RGBColor(0x92, 0x40, 0x0E)
DARK_BAR = RGBColor(0x0D, 0x3B, 0x5E)
LIGHT_BG = RGBColor(0xF5, 0xF7, 0xFA)
LIGHT_PAGE = RGBColor(0xAA, 0xAA, 0xAA)

# Stage colors
STAGE_COLORS = [
    RGBColor(0x6B, 0x72, 0x80),  # Stage 1 - gray
    RGBColor(0x92, 0x40, 0x0E),  # Stage 2 - amber
    RGBColor(0x16, 0x65, 0x34),  # Stage 3 - green
    RGBColor(0x1F, 0x3B, 0x6E),  # Stage 4 - navy
]

STAGE_BG = [
    RGBColor(0xF9, 0xFA, 0xFB),  # lightest gray
    RGBColor(0xFF, 0xF7, 0xED),  # light amber
    RGBColor(0xF0, 0xFD, 0xF4),  # light green
    RGBColor(0xEF, 0xF6, 0xFF),  # light blue
]


def add_shape(slide, left, top, width, height, fill_color=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    return shape


def add_text_box(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)


def set_text(tf, text, size, color, bold=None, alignment=None):
    tf.word_wrap = True
    p = tf.paragraphs[0]
    if alignment:
        p.alignment = alignment
    r = p.add_run()
    r.text = text
    r.font.name = FONT
    r.font.size = size
    r.font.color.rgb = color
    if bold is not None:
        r.font.bold = bold
    return r


def add_para(tf, text, size, color, bold=None, alignment=None, space_before=None):
    from pptx.oxml.ns import qn as _qn
    p = tf.add_paragraph()
    if alignment:
        p.alignment = alignment
    if space_before is not None:
        p.space_before = space_before
    r = p.add_run()
    r.text = text
    r.font.name = FONT
    r.font.size = size
    r.font.color.rgb = color
    if bold is not None:
        r.font.bold = bold
    return r


def main():
    prs = Presentation("AI-Engineering-Business-Use-Cases.pptx")

    total_slides = len(prs.slides) + 1  # adding 1 slide
    insert_at = 31  # after Implementation Roadmap (idx 30), before Engagement Model

    layout = prs.slides[1].slide_layout  # use same layout as strategy overview
    slide = prs.slides.add_slide(layout)

    # Move to correct position
    slides_el = prs.slides._sldIdLst
    slide_id = slides_el[-1]
    slides_el.remove(slide_id)
    children = list(slides_el)
    if insert_at < len(children):
        slides_el.insert(insert_at, slide_id)
    else:
        slides_el.append(slide_id)

    # Remove default placeholders
    for sp in list(slide.shapes):
        slide.shapes._spTree.remove(sp._element)

    # ── Title ──
    tb = add_text_box(slide, 457200, 182880, 9144000, 384048)
    set_text(tb.text_frame, "Customer Adoption Journey", 304800, NAVY, bold=True)

    tb = add_text_box(slide, 457200, 566928, 11000000, 274320)
    set_text(tb.text_frame, "24 Use Cases Mapped to Enterprise AI Maturity — Pilot to Autonomous Operations", 152400, GRAY)

    # ── 4 Stages as columns ──
    stages = [
        {
            "name": "STAGE 1: QUICK WINS",
            "timeline": "Month 1-2  |  Pilot",
            "desc": "Low-complexity, high-visibility wins that prove AI value and build stakeholder confidence",
            "ucs": [
                ("UC02", "Barcode/BOM Validation"),
                ("UC07", "PPE Detection"),
                ("UC09", "Patient Intake"),
                ("UC15", "Lease Generation"),
                ("UC18", "SEO Audit"),
                ("UC20", "Content Pipeline"),
            ],
            "outcome": "3-5 pilots live\nNPS > 40\n< 5% error rate",
        },
        {
            "name": "STAGE 2: DEPARTMENTAL",
            "timeline": "Month 3-4  |  Scale",
            "desc": "Expand within departments; add integrations and cross-system data flows",
            "ucs": [
                ("UC01", "Visual Inspection"),
                ("UC06", "Predictive Maintenance"),
                ("UC10", "Insurance Verification"),
                ("UC12", "Contract Generation"),
                ("UC14", "Legal Billing"),
                ("UC16", "Lead Scoring"),
                ("UC17", "Commission Analytics"),
                ("UC19", "Campaign Dashboard"),
            ],
            "outcome": "$50K MRR\n90% retention\n10-15 clients",
        },
        {
            "name": "STAGE 3: ENTERPRISE",
            "timeline": "Month 5-8  |  Integrate",
            "desc": "Cross-functional orchestration; shared MCP infrastructure; compliance certifications",
            "ucs": [
                ("UC03", "Seating Validation"),
                ("UC04", "SOP Compliance"),
                ("UC05", "Predictive Quality"),
                ("UC08", "Digital Traceability"),
                ("UC11", "HIPAA Compliance"),
                ("UC13", "Legal Research"),
                ("UC22", "Auto Test Gen"),
            ],
            "outcome": "$120K MRR\n2+ verticals\nSOC 2 certified",
        },
        {
            "name": "STAGE 4: AUTONOMOUS",
            "timeline": "Month 9-12  |  Optimize",
            "desc": "Self-improving agent networks; agents building agents; autonomous decision loops",
            "ucs": [
                ("UC21", "AI Code Generation"),
                ("UC23", "Code Modernization"),
                ("UC24", "DevOps & Incident"),
            ],
            "outcome": "$400K+ MRR\n4+ verticals\n50+ clients",
        },
    ]

    col_w = 2697480
    col_gap = 136680
    start_x = 457200
    header_h = 274320
    card_top = 1097280
    card_h = 4206240

    for i, stage in enumerate(stages):
        x = start_x + i * (col_w + col_gap)
        color = STAGE_COLORS[i]
        bg = STAGE_BG[i]

        # Card background
        add_shape(slide, x, card_top, col_w, card_h, bg)

        # Stage header bar
        add_shape(slide, x, card_top, col_w, header_h, color)
        tb = add_text_box(slide, x, card_top, col_w, header_h)
        set_text(tb.text_frame, stage["name"], 114300, WHITE, bold=True, alignment=PP_ALIGN.CENTER)

        # Timeline
        y = card_top + header_h + 45720
        tb = add_text_box(slide, x + 54864, y, col_w - 109728, 164592)
        set_text(tb.text_frame, stage["timeline"], 101600, color, bold=True, alignment=PP_ALIGN.CENTER)

        # Description
        y += 182880
        tb = add_text_box(slide, x + 54864, y, col_w - 109728, 365760)
        set_text(tb.text_frame, stage["desc"], 88900, GRAY)

        # Divider line
        y += 347472
        add_shape(slide, x + 91440, y, col_w - 182880, 18288, RGBColor(0xE5, 0xE7, 0xEB))

        # UC list
        y += 54864
        tb = add_text_box(slide, x + 54864, y, col_w - 109728, 36576)
        set_text(tb.text_frame, "USE CASES", 88900, color, bold=True)

        y += 146304
        tb = add_text_box(slide, x + 54864, y, col_w - 109728, 2200000)
        first = True
        for uc_id, uc_name in stage["ucs"]:
            if first:
                r = set_text(tb.text_frame, f"{uc_id}", 88900, color, bold=True)
                # Add the name part as separate run in same para
                r2 = tb.text_frame.paragraphs[0].add_run()
                r2.text = f"  {uc_name}"
                r2.font.name = FONT
                r2.font.size = 88900
                r2.font.color.rgb = DARK_TEXT
                first = False
            else:
                p = tb.text_frame.add_paragraph()
                p.space_before = Pt(2)
                r = p.add_run()
                r.text = f"{uc_id}"
                r.font.name = FONT
                r.font.size = 88900
                r.font.color.rgb = color
                r.font.bold = True
                r2 = p.add_run()
                r2.text = f"  {uc_name}"
                r2.font.name = FONT
                r2.font.size = 88900
                r2.font.color.rgb = DARK_TEXT

        # Outcome box at bottom
        outcome_h = 457200
        outcome_y = card_top + card_h - outcome_h - 54864
        add_shape(slide, x + 54864, outcome_y, col_w - 109728, outcome_h, WHITE)
        tb = add_text_box(slide, x + 54864, outcome_y, col_w - 109728, 36576)
        set_text(tb.text_frame, "TARGET OUTCOME", 88900, color, bold=True, alignment=PP_ALIGN.CENTER)

        tb = add_text_box(slide, x + 91440, outcome_y + 128016, col_w - 182880, outcome_h - 146304)
        lines = stage["outcome"].split("\n")
        set_text(tb.text_frame, lines[0], 101600, DARK_TEXT, bold=True, alignment=PP_ALIGN.CENTER)
        for line in lines[1:]:
            add_para(tb.text_frame, line, 101600, DARK_TEXT, bold=True, alignment=PP_ALIGN.CENTER)

    # ── Arrow connectors between stages ──
    for i in range(3):
        ax = start_x + (i + 1) * (col_w + col_gap) - col_gap + 18288
        ay = card_top + card_h // 2 - 91440
        tb = add_text_box(slide, ax, ay, col_gap - 36576, 182880)
        set_text(tb.text_frame, "▶", 203200, RGBColor(0xD1, 0xD5, 0xDB), bold=True, alignment=PP_ALIGN.CENTER)

    # ── Bottom insight bar ──
    insight_y = card_top + card_h + 91440
    add_shape(slide, 457200, insight_y, 11278800, 365760, LIGHT_BG)
    tb = add_text_box(slide, 548640, insight_y + 27432, 11095920, 310896)
    r = set_text(tb.text_frame, "Key insight: ", 107950, RED, bold=True)
    r2 = tb.text_frame.paragraphs[0].add_run()
    r2.text = "Stage 1-2 UCs generate revenue and case studies that fund Stage 3-4 deployments. Stage 4 agents (UC21-24) then accelerate delivery of all other UCs — creating a compounding capability flywheel."
    r2.font.name = FONT
    r2.font.size = 107950
    r2.font.color.rgb = DARK_TEXT

    # ── Footer ──
    add_shape(slide, 0, 6263640, 12188952, 594360, DARK_BAR)
    tb = add_text_box(slide, 0, 6263640, 12188952, 594360)
    set_text(tb.text_frame, "AI Engineering Business Use Cases | Confidential", 127000, WHITE, alignment=PP_ALIGN.CENTER)
    tb = add_text_box(slide, 11155680, 6263640, 914400, 594360)
    set_text(tb.text_frame, f"{insert_at + 1} / {total_slides}", 114300, LIGHT_PAGE, alignment=PP_ALIGN.RIGHT)

    # Update all page numbers
    import re
    for idx, s in enumerate(prs.slides):
        for shape in s.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = para.text.strip()
                    if re.match(r'^\d+ / \d+$', text):
                        for run in para.runs:
                            run.text = f"{idx + 1} / {total_slides}"

    prs.save("AI-Engineering-Business-Use-Cases.pptx")
    print(f"✓ Added Customer Adoption Journey slide at position {insert_at + 1}/{total_slides}")
    print(f"  → 24 UCs mapped across 4 stages: Quick Wins → Departmental → Enterprise → Autonomous")
    print(f"  → Includes timeline, target outcomes, and capability flywheel insight")


if __name__ == "__main__":
    main()
