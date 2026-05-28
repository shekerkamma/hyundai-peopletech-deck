#!/usr/bin/env python3
"""
Add architecture companion slides for UC21-24 (Software Engineering vertical)
to AI-Engineering-Business-Use-Cases.pptx.

Each architecture slide is a visual data-flow diagram built with python-pptx shapes.
"""

import re
import copy
from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree

PPTX_PATH = "AI-Engineering-Business-Use-Cases.pptx"

# Slide dimensions
SLIDE_W = 12192000
SLIDE_H = 6858000

# Colors
NAVY = RGBColor(0x1F, 0x3B, 0x6E)
FOOTER_BG = RGBColor(0x0D, 0x3B, 0x5E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CHARCOAL = RGBColor(0x1A, 0x1A, 0x1A)
GRAY_BORDER = RGBColor(0xD0, 0xD5, 0xDD)
MUTED = RGBColor(0x6B, 0x72, 0x80)

# Box category colors
BOX_STYLES = {
    "input":       {"fill": RGBColor(0xFF, 0xFF, 0xFF), "border": RGBColor(0xD0, 0xD5, 0xDD), "text": CHARCOAL},
    "core":        {"fill": RGBColor(0x1F, 0x3B, 0x6E), "border": RGBColor(0x1F, 0x3B, 0x6E), "text": WHITE},
    "integration": {"fill": RGBColor(0xE0, 0xE7, 0xFF), "border": RGBColor(0x81, 0x8C, 0xF8), "text": CHARCOAL},
    "output":      {"fill": RGBColor(0xDC, 0xFC, 0xE7), "border": RGBColor(0x16, 0x65, 0x34), "text": CHARCOAL},
    "security":    {"fill": RGBColor(0xFE, 0xE2, 0xE2), "border": RGBColor(0xE3, 0x18, 0x37), "text": CHARCOAL},
    "storage":     {"fill": RGBColor(0xFE, 0xF3, 0xC7), "border": RGBColor(0x92, 0x40, 0x0E), "text": CHARCOAL},
}

# Box dimensions
BOX_W = Emu(1400000)
BOX_H = Emu(650000)
ARROW_H = Emu(18000)
ARROW_W = Emu(280000)

# Layout constants
DIAGRAM_TOP = Emu(750000)
DIAGRAM_LEFT = Emu(400000)
ROW_SPACING = Emu(200000)   # vertical gap between rows
COL_SPACING = Emu(320000)   # horizontal gap between boxes


def add_box(slide, left, top, label, sublabel, style_name):
    """Add a styled rectangle with label text."""
    style = BOX_STYLES[style_name]
    shape = slide.shapes.add_shape(1, left, top, BOX_W, BOX_H)  # 1 = rectangle
    shape.fill.solid()
    shape.fill.fore_color.rgb = style["fill"]
    shape.line.color.rgb = style["border"]
    shape.line.width = Pt(1.2)

    # Clear default text, add label
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = label
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = style["text"]
    run.font.name = "Calibri"

    if sublabel:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = sublabel
        run2.font.size = Pt(7)
        run2.font.color.rgb = MUTED if style_name != "core" else RGBColor(0xBB, 0xBB, 0xBB)
        run2.font.name = "Calibri"

    return shape


def add_arrow_h(slide, left, top):
    """Add a horizontal arrow (thin rectangle with triangle) between boxes."""
    # Thin rectangle as arrow body
    arrow = slide.shapes.add_shape(1, left, top, ARROW_W, ARROW_H)
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = GRAY_BORDER
    arrow.line.fill.background()  # no border

    # Small triangle arrowhead
    tri_w = Emu(80000)
    tri_h = Emu(80000)
    tri_left = left + ARROW_W - Emu(10000)
    tri_top = top - Emu(31000)
    tri = slide.shapes.add_shape(
        5,  # isosceles triangle — we'll use a right-arrow shape instead
        tri_left, tri_top, tri_w, tri_h
    )
    tri.fill.solid()
    tri.fill.fore_color.rgb = GRAY_BORDER
    tri.line.fill.background()
    tri.rotation = 90.0
    return arrow


def add_side_box(slide, left, top, label, sublabel, style_name, target_top):
    """Add a side box with a vertical connector to a target row."""
    box = add_box(slide, left, top, label, sublabel, style_name)
    # Vertical connector line
    line_left = left + BOX_W // 2 - Emu(9000)
    if top < target_top:
        line_top = top + BOX_H
        line_h = target_top - line_top
    else:
        line_top = target_top + BOX_H
        line_h = top - line_top
    if line_h > 0:
        conn = slide.shapes.add_shape(1, line_left, line_top, Emu(18000), line_h)
        conn.fill.solid()
        conn.fill.fore_color.rgb = GRAY_BORDER
        conn.line.fill.background()
    return box


def add_title_bar(slide, title_text):
    """Add navy title bar matching UC slide style."""
    # Background bar
    bar = slide.shapes.add_shape(1, Emu(274320), Emu(182880), Emu(11640312), Emu(384048))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()

    # Title text
    tb = slide.shapes.add_textbox(Emu(411480), Emu(182880), Emu(11338560), Emu(384048))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = title_text
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.font.name = "Calibri"


def add_footer_bar(slide, page_text, total):
    """Add footer bar matching existing slides."""
    # Dark footer background
    bar = slide.shapes.add_shape(1, 0, Emu(6263640), Emu(12188952), Emu(594360))
    bar.fill.solid()
    bar.fill.fore_color.rgb = FOOTER_BG
    bar.line.fill.background()

    # Footer label
    tb = slide.shapes.add_textbox(Emu(274320), Emu(6263640), Emu(10000000), Emu(594360))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "AI Engineering Business Use Cases | Confidential"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
    run.font.name = "Calibri"

    # Page number
    pn = slide.shapes.add_shape(1, Emu(11155680), Emu(6263640), Emu(914400), Emu(594360))
    pn.fill.solid()
    pn.fill.fore_color.rgb = FOOTER_BG
    pn.line.fill.background()
    pntf = pn.text_frame
    pntf.word_wrap = False
    pp = pntf.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    run2 = pp.add_run()
    run2.text = page_text
    run2.font.size = Pt(10)
    run2.font.color.rgb = WHITE
    run2.font.name = "Calibri"


def add_bottom_label(slide, text):
    """Add a bottom annotation label above the footer."""
    tb = slide.shapes.add_textbox(Emu(400000), Emu(5900000), Emu(11400000), Emu(300000))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(8)
    run.font.italic = True
    run.font.color.rgb = MUTED
    run.font.name = "Calibri"


def row_top(row_idx):
    """Calculate top position for a row (0-indexed)."""
    return DIAGRAM_TOP + row_idx * (BOX_H + ROW_SPACING)


def col_left(col_idx):
    """Calculate left position for a column in a 3-col row."""
    return DIAGRAM_LEFT + col_idx * (BOX_W + COL_SPACING)


def build_row(slide, row_idx, boxes):
    """
    Build a row of boxes with arrows between them.
    boxes: list of (label, sublabel, style_name)
    """
    top = row_top(row_idx)
    for i, (label, sublabel, style) in enumerate(boxes):
        left = col_left(i)
        add_box(slide, left, top, label, sublabel, style)
        if i < len(boxes) - 1:
            # Arrow between this box and next
            arrow_left = left + BOX_W + Emu(20000)
            arrow_top = top + BOX_H // 2 - ARROW_H // 2
            add_arrow_h(slide, arrow_left, arrow_top)


def add_row_label(slide, row_idx, text):
    """Add a small row label to the left of the row."""
    top = row_top(row_idx) + BOX_H // 2 - Emu(80000)
    tb = slide.shapes.add_textbox(Emu(50000), top, Emu(330000), Emu(160000))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(6)
    run.font.bold = True
    run.font.color.rgb = MUTED
    run.font.name = "Calibri"


# ---- Architecture definitions ----

def build_uc21(slide):
    """UC21 - AI-Powered Code Generation"""
    add_title_bar(slide, "UC21 Architecture | AI-Powered Code Generation")

    # Row 0: Triggers
    add_row_label(slide, 0, "TRIGGER")
    build_row(slide, 0, [
        ("GitHub Issue", "webhook trigger", "input"),
        ("Webhook /\nLabel Event", "event filter", "input"),
        ("Agent Server", "FastAPI runtime", "integration"),
    ])

    # Row 1: Agent Core
    add_row_label(slide, 1, "AGENT")
    build_row(slide, 1, [
        ("CodeAct Agent", "plan + execute", "core"),
        ("LLM Router", "LiteLLM proxy", "core"),
        ("Claude 4.5 /\nGPT-5.2", "model backend", "core"),
    ])

    # Row 2: Execution
    add_row_label(slide, 2, "EXEC")
    build_row(slide, 2, [
        ("Docker Sandbox", "isolated runtime", "integration"),
        ("Bash + Python\n+ Browser", "tool execution", "integration"),
        ("File System", "overlay mount", "storage"),
    ])

    # Row 3: Output
    add_row_label(slide, 3, "OUTPUT")
    build_row(slide, 3, [
        ("Git Operations", "branch + commit", "output"),
        ("PR Generation", "diff + description", "output"),
        ("CI/CD Pipeline", "automated checks", "output"),
    ])

    # Side boxes
    side_left = col_left(3) + Emu(100000)
    add_side_box(slide, side_left, row_top(1), "Event Store", "append-only log", "storage", row_top(1))
    add_side_box(slide, side_left, row_top(2), "SecurityAnalyzer", "SAST + secrets", "security", row_top(2))

    # Vertical arrows between rows
    for r in range(3):
        mid_col = col_left(1) + BOX_W // 2 - Emu(9000)
        vtop = row_top(r) + BOX_H
        vbot = row_top(r + 1)
        if vbot > vtop:
            conn = slide.shapes.add_shape(1, mid_col, vtop, Emu(18000), vbot - vtop)
            conn.fill.solid()
            conn.fill.fore_color.rgb = GRAY_BORDER
            conn.line.fill.background()

    add_bottom_label(slide, "Event-sourced architecture: every action logged, deterministic replay, full audit trail")


def build_uc22(slide):
    """UC22 - Automated Test Generation"""
    add_title_bar(slide, "UC22 Architecture | Automated Test Generation")

    add_row_label(slide, 0, "ANALYZE")
    build_row(slide, 0, [
        ("Codebase Analysis", "repo ingestion", "input"),
        ("AST Parser +\nCoverage Map", "static analysis", "integration"),
        ("Gap Identifier", "missing coverage", "integration"),
    ])

    add_row_label(slide, 1, "AGENTS")
    build_row(slide, 1, [
        ("Test Agent", "multi-agent fan-out", "core"),
        ("Unit Agent |\nIntegration Agent", "specialized writers", "core"),
        ("E2E Agent", "browser + API tests", "core"),
    ])

    add_row_label(slide, 2, "EXEC")
    build_row(slide, 2, [
        ("Sandbox Execution", "isolated container", "integration"),
        ("Test Runner", "pytest / jest", "integration"),
        ("Coverage Report", "line + branch %", "storage"),
    ])

    add_row_label(slide, 3, "OUTPUT")
    build_row(slide, 3, [
        ("Validation Gate", "pass/fail threshold", "output"),
        ("PR with Tests", "auto-generated", "output"),
        ("CI Merge", "automated pipeline", "output"),
    ])

    side_left = col_left(3) + Emu(100000)
    add_side_box(slide, side_left, row_top(1), "SWT-Bench Model", "benchmark eval", "storage", row_top(1))
    add_side_box(slide, side_left, row_top(3), "SAST Scanner", "security check", "security", row_top(3))

    for r in range(3):
        mid_col = col_left(1) + BOX_W // 2 - Emu(9000)
        vtop = row_top(r) + BOX_H
        vbot = row_top(r + 1)
        if vbot > vtop:
            conn = slide.shapes.add_shape(1, mid_col, vtop, Emu(18000), vbot - vtop)
            conn.fill.solid()
            conn.fill.fore_color.rgb = GRAY_BORDER
            conn.line.fill.background()

    add_bottom_label(slide, "Multi-agent fan-out: parallel test generation across unit, integration, and E2E layers")


def build_uc23(slide):
    """UC23 - Code Modernization"""
    add_title_bar(slide, "UC23 Architecture | Code Modernization & Tech Debt")

    add_row_label(slide, 0, "SCAN")
    build_row(slide, 0, [
        ("Dependency Scanner", "outdated packages", "input"),
        ("Package Registry", "npm / pip / maven", "input"),
        ("Vulnerability DB", "NVD + GHSA", "security"),
    ])

    add_row_label(slide, 1, "AGENT")
    build_row(slide, 1, [
        ("Migration Agent", "upgrade strategy", "core"),
        ("Pattern Analyzer", "code patterns", "core"),
        ("Code Transformer", "AST rewrite", "core"),
    ])

    add_row_label(slide, 2, "SCALE")
    build_row(slide, 2, [
        ("Multi-Repo\nOrchestrator", "repo fan-out", "integration"),
        ("Parallel Agent Pool", "N workers", "integration"),
        ("Sandbox per Repo", "isolated builds", "integration"),
    ])

    add_row_label(slide, 3, "OUTPUT")
    build_row(slide, 3, [
        ("Regression Tests", "compatibility check", "output"),
        ("PR per Service", "~$3 each", "output"),
        ("Auto Merge Queue", "sequenced landing", "output"),
    ])

    side_left = col_left(3) + Emu(100000)
    add_side_box(slide, side_left, row_top(1), "ADR Generator", "decision records", "storage", row_top(1))
    add_side_box(slide, side_left, row_top(0), "Drift Monitor", "continuous scan", "security", row_top(0))

    for r in range(3):
        mid_col = col_left(1) + BOX_W // 2 - Emu(9000)
        vtop = row_top(r) + BOX_H
        vbot = row_top(r + 1)
        if vbot > vtop:
            conn = slide.shapes.add_shape(1, mid_col, vtop, Emu(18000), vbot - vtop)
            conn.fill.solid()
            conn.fill.fore_color.rgb = GRAY_BORDER
            conn.line.fill.background()

    add_bottom_label(slide, "Multi-repo orchestration: parallel agent pool processes N services simultaneously at ~$3/PR")


def build_uc24(slide):
    """UC24 - DevOps & Incident Response"""
    add_title_bar(slide, "UC24 Architecture | DevOps & Incident Response")

    add_row_label(slide, 0, "DETECT")
    build_row(slide, 0, [
        ("PagerDuty Alert", "incident trigger", "input"),
        ("Log Aggregator", "DataDog ingest", "input"),
        ("Correlation Engine", "signal grouping", "integration"),
    ])

    add_row_label(slide, 1, "ANALYZE")
    build_row(slide, 1, [
        ("Root Cause Agent", "hypothesis engine", "core"),
        ("Log Analysis LLM", "pattern extraction", "core"),
        ("Runbook Matcher", "playbook lookup", "core"),
    ])

    add_row_label(slide, 2, "REMEDIATE")
    build_row(slide, 2, [
        ("Remediation Agent", "action executor", "integration"),
        ("Terraform API |\nK8s API", "infra mutation", "integration"),
        ("GitHub API", "code rollback", "integration"),
    ])

    add_row_label(slide, 3, "VERIFY")
    build_row(slide, 3, [
        ("Validation", "health checks", "output"),
        ("Canary Deploy", "progressive rollout", "output"),
        ("Incident Closed", "auto-resolve", "output"),
    ])

    side_left = col_left(3) + Emu(100000)
    add_side_box(slide, side_left, row_top(2), "Blast Radius\nController", "scope limiter", "security", row_top(2))
    add_side_box(slide, side_left, row_top(0) + (row_top(3) - row_top(0)) // 2, "Audit Logger", "all-stage trace", "storage", row_top(1))

    for r in range(3):
        mid_col = col_left(1) + BOX_W // 2 - Emu(9000)
        vtop = row_top(r) + BOX_H
        vbot = row_top(r + 1)
        if vbot > vtop:
            conn = slide.shapes.add_shape(1, mid_col, vtop, Emu(18000), vbot - vtop)
            conn.fill.solid()
            conn.fill.fore_color.rgb = GRAY_BORDER
            conn.line.fill.background()

    add_bottom_label(slide, "Closed-loop incident response: detect, diagnose, remediate, and verify with blast-radius controls")


# ---- Main logic ----

def find_slide_index(prs, search_text):
    """Find slide index by searching for text content."""
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    if search_text in para.text:
                        return i
    return None


def insert_slide_after(prs, after_index):
    """Add a blank slide and move it to position after_index + 1."""
    layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(layout)

    # Move the new slide (currently last) to right after after_index
    sldIdLst = prs.slides._sldIdLst
    # Get fresh list of elements each time
    items = list(sldIdLst)
    new_elem = items[-1]  # just-added slide is last
    sldIdLst.remove(new_elem)
    # Re-read after removal to get correct positions
    items = list(sldIdLst)
    target_elem = items[after_index]
    target_elem.addnext(new_elem)

    return slide


def update_page_numbers(prs):
    """Update all page numbers in format 'N / M' or 'X / X' across all slides."""
    total = len(prs.slides)
    pattern = re.compile(r'^(\d+\s*/\s*\d+|X\s*/\s*X)$')
    for i, slide in enumerate(prs.slides):
        page_num = i + 1
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if pattern.match(run.text.strip()):
                            run.text = f"{page_num} / {total}"


def main():
    prs = Presentation(PPTX_PATH)

    # Define UC architectures
    uc_configs = [
        ("UC21 |", "UC21 Architecture | AI-Powered Code Generation", build_uc21),
        ("UC22 |", "UC22 Architecture | Automated Test Generation", build_uc22),
        ("UC23 |", "UC23 Architecture | Code Modernization", build_uc23),
        ("UC24 |", "UC24 Architecture | DevOps & Incident Response", build_uc24),
    ]

    # First pass: find all target indices
    targets = []
    for search_text, title, builder in uc_configs:
        idx = find_slide_index(prs, search_text)
        if idx is None:
            print(f"WARNING: Could not find slide with '{search_text}' - skipping")
            continue
        targets.append((idx, search_text, title, builder))

    # Insert in REVERSE order so earlier indices stay valid
    inserted = []
    for idx, search_text, title, builder in reversed(targets):
        print(f"Found '{search_text}' at slide {idx + 1}, inserting arch slide after it...")

        slide = insert_slide_after(prs, idx)

        # Set white background
        bg = slide.background
        bg.fill.solid()
        bg.fill.fore_color.rgb = WHITE

        # Build the diagram
        builder(slide)

        # Add footer (page number will be fixed later)
        add_footer_bar(slide, "X / X", len(prs.slides))

        inserted.append((search_text.strip(" |"), idx + 2))  # 1-indexed

    inserted.reverse()  # restore original order for display

    # Update all page numbers
    update_page_numbers(prs)

    prs.save(PPTX_PATH)

    print(f"\nSuccess! Added {len(inserted)} architecture slides to {PPTX_PATH}")
    print(f"Total slides: {len(prs.slides)}")
    for uc, pos in inserted:
        print(f"  {uc} Architecture -> slide {pos}")


if __name__ == "__main__":
    main()
