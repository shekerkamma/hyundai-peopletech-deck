#!/usr/bin/env python3
"""
Add architecture companion slides for UC09-UC14 (Healthcare + Legal verticals)
into AI-Engineering-Business-Use-Cases.pptx.

Each architecture slide is inserted immediately AFTER its parent UC slide.
Visual data-flow diagrams built with python-pptx shapes (boxes + arrows).
"""

import copy
import re
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

PPTX_PATH = "AI-Engineering-Business-Use-Cases.pptx"

# Color scheme
NAVY = RGBColor(0x1F, 0x3B, 0x6E)
FOOTER_BG = RGBColor(0x0D, 0x3B, 0x5E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_BORDER = RGBColor(0xD0, 0xD5, 0xDD)
ARROW_FILL = RGBColor(0xD0, 0xD5, 0xDD)

BOX_COLORS = {
    "input":       {"fill": RGBColor(0xFF, 0xFF, 0xFF), "border": RGBColor(0xD0, 0xD5, 0xDD)},
    "ai":          {"fill": RGBColor(0x1F, 0x3B, 0x6E), "border": None,                        "text": WHITE},
    "integration": {"fill": RGBColor(0xE0, 0xE7, 0xFF), "border": RGBColor(0x81, 0x8C, 0xF8)},
    "output":      {"fill": RGBColor(0xDC, 0xFC, 0xE7), "border": RGBColor(0x16, 0x65, 0x34)},
    "security":    {"fill": RGBColor(0xFE, 0xE2, 0xE2), "border": RGBColor(0xE3, 0x18, 0x37)},
    "storage":     {"fill": RGBColor(0xFE, 0xF3, 0xC7), "border": RGBColor(0x92, 0x40, 0x0E)},
}

# Box dimensions
BOX_W = Emu(2000000)
BOX_H = Emu(700000)
H_GAP = Emu(400000)
V_GAP = Emu(350000)
ARROW_H_HEIGHT = Emu(18000)
ARROW_V_WIDTH = Emu(18000)

# Diagram area
DIAG_X_START = Emu(400000)
DIAG_Y_START = Emu(700000)

# Architecture data for UC09-UC14
UC_ARCHITECTURES = {
    "UC09": {
        "title": "UC09 Architecture | Patient Intake Automation",
        "rows": [
            {"type": "input", "boxes": ["Patient Portal\n(Web/Mobile)", "SMS/Voice\n(Twilio)", "Fax OCR Engine"]},
            {"type": "ai", "boxes": ["Claude NLP\nProcessor", "Form Validation\nML", "Entity\nExtraction"]},
            {"type": "integration", "boxes": ["FHIR R4 API\nGateway", "Epic/Cerner EHR\nWrite-back", "Calendly\nScheduler"]},
            {"type": "output", "boxes": ["Patient\nDashboard", "Staff Queue\nView", "Billing\nPre-pop"]},
        ],
        "side_boxes": [
            {"text": "HIPAA Encryption\n(AES-256)", "type": "security", "connect_row": 2, "connect_col": 0},
            {"text": "Consent\nManager", "type": "security", "connect_row": 0, "connect_col": 0},
        ],
    },
    "UC10": {
        "title": "UC10 Architecture | Insurance Verification",
        "rows": [
            {"type": "input", "boxes": ["Appointment\nTrigger", "Payer EDI 270\nRequest", "Prior Auth\nRules DB"]},
            {"type": "ai", "boxes": ["Eligibility\nML Model", "Denial Prediction\nEngine", "Clinical Doc\nMatcher"]},
            {"type": "integration", "boxes": ["Clearinghouse\nEDI Gateway", "Payer API\nRouter", "EHR Billing\nModule"]},
            {"type": "output", "boxes": ["Verification\nDashboard", "Denial\nAnalytics", "Auto-Resubmission\nQueue"]},
        ],
        "side_boxes": [
            {"text": "Payer Rule Monitor\n(24hr sync)", "type": "storage", "connect_row": 1, "connect_col": 2},
            {"text": "Bias Audit\n(quarterly)", "type": "security", "connect_row": 3, "connect_col": 1},
        ],
    },
    "UC11": {
        "title": "UC11 Architecture | HIPAA Compliance Portal",
        "rows": [
            {"type": "input", "boxes": ["EHR Access\nLogs", "IAM Events\n(Okta/Azure AD)", "Email DLP\nScanner"]},
            {"type": "ai", "boxes": ["Log Aggregation\nEngine", "Anomaly Detection\nML", "Compliance\nRules Engine"]},
            {"type": "integration", "boxes": ["Risk Scoring\nModule", "Breach Assessment\nWorkflow", "Remediation\nTracker"]},
            {"type": "output", "boxes": ["Compliance\nDashboard", "Risk\nHeat Map", "Audit Report\nGenerator"]},
        ],
        "side_boxes": [
            {"text": "HITECH Notification\n(60-day)", "type": "security", "connect_row": 2, "connect_col": 1},
            {"text": "BAA Tracking\nSystem", "type": "storage", "connect_row": 0, "connect_col": 2},
        ],
    },
    "UC12": {
        "title": "UC12 Architecture | Contract Generation & Review",
        "rows": [
            {"type": "input", "boxes": ["Deal Intake\nForm", "Clause Library\n(Git-backed)", "Template\nEngine"]},
            {"type": "ai", "boxes": ["Claude Drafting\nAgent", "Risk Scoring\nModel", "Deviation\nDetector"]},
            {"type": "integration", "boxes": ["iManage\nDMS API", "DocuSign\neSign API", "Version\nControl"]},
            {"type": "output", "boxes": ["Attorney Review\nPortal", "Clause\nLibrary UI", "Audit\nTrail"]},
        ],
        "side_boxes": [
            {"text": "Privilege\nMarker", "type": "security", "connect_row": 1, "connect_col": 0},
            {"text": "Partner\nApproval Gate", "type": "security", "connect_row": 2, "connect_col": 2},
        ],
    },
    "UC13": {
        "title": "UC13 Architecture | Legal Research Summarization",
        "rows": [
            {"type": "input", "boxes": ["Research Query\nInput", "Westlaw\nAPI", "LexisNexis\nAPI"]},
            {"type": "ai", "boxes": ["RAG Pipeline\n(pgvector)", "Claude Reasoning\nEngine", "Citation\nVerifier"]},
            {"type": "integration", "boxes": ["Brief Bank\nIndexer", "Jurisdiction\nScorer", "Relevance\nRanker"]},
            {"type": "output", "boxes": ["Research Brief\nGenerator", "Citation\nViewer", "Collaborative\nWorkspace"]},
        ],
        "side_boxes": [
            {"text": "On-Premise RAG\n(privileged)", "type": "security", "connect_row": 1, "connect_col": 0},
            {"text": "Bar Disclosure\nMarker", "type": "security", "connect_row": 3, "connect_col": 0},
        ],
    },
    "UC14": {
        "title": "UC14 Architecture | Legal Billing Automation",
        "rows": [
            {"type": "input", "boxes": ["Calendar\nMonitor", "Email Activity\nTracker", "Doc Edit\nLogger"]},
            {"type": "ai", "boxes": ["Activity\nClassification ML", "Matter-Code\nAssigner", "Narrative\nGenerator"]},
            {"type": "integration", "boxes": ["LEDES\nFormatter", "QuickBooks\nAPI", "Stripe Payment\nAPI"]},
            {"type": "output", "boxes": ["Billing\nDashboard", "Client\nPortal", "1099\nGenerator"]},
        ],
        "side_boxes": [
            {"text": "Time Entry\nAudit Trail", "type": "security", "connect_row": 1, "connect_col": 2},
            {"text": "UTBMS\nValidator", "type": "storage", "connect_row": 2, "connect_col": 0},
        ],
    },
}


def add_box(slide, left, top, width, height, text, box_type, bold_first_line=True):
    """Add a styled rectangle with text."""
    shape = slide.shapes.add_shape(1, left, top, width, height)
    colors = BOX_COLORS[box_type]

    shape.fill.solid()
    shape.fill.fore_color.rgb = colors["fill"]

    if colors.get("border") is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = colors["border"]
        shape.line.width = Pt(1)

    text_color = colors.get("text", RGBColor(0x1A, 0x1A, 0x2E))

    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = line
        run.font.name = "Calibri"
        run.font.color.rgb = text_color
        if i == 0 and bold_first_line:
            run.font.size = Pt(9)
            run.font.bold = True
        else:
            run.font.size = Pt(7)
            run.font.bold = False

    try:
        tf.paragraphs[0].space_before = Pt(0)
        shape.text_frame.margin_top = Emu(50000)
        shape.text_frame.margin_bottom = Emu(30000)
    except Exception:
        pass

    return shape


def add_h_arrow(slide, x, y, width):
    """Horizontal arrow (thin rect) between boxes in same row."""
    shape = slide.shapes.add_shape(1, x, y, width, ARROW_H_HEIGHT)
    shape.fill.solid()
    shape.fill.fore_color.rgb = ARROW_FILL
    shape.line.fill.background()
    return shape


def add_v_arrow(slide, x, y, height):
    """Vertical arrow (thin rect) between rows."""
    shape = slide.shapes.add_shape(1, x, y, ARROW_V_WIDTH, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = ARROW_FILL
    shape.line.fill.background()
    return shape


def add_title_bar(slide, title_text):
    """Navy title bar at top."""
    shape = slide.shapes.add_shape(1, Emu(274320), Emu(182880), Emu(11640312), Emu(384048))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = title_text
    run.font.name = "Calibri"
    run.font.size = Emu(203200)
    run.font.bold = True
    run.font.color.rgb = WHITE
    try:
        tf.margin_left = Emu(100000)
        tf.margin_top = Emu(40000)
    except Exception:
        pass
    return shape


def add_footer_bar(slide, page_num, total):
    """Footer bar at bottom."""
    # Main footer
    shape = slide.shapes.add_shape(1, 0, Emu(6263640), Emu(12188952), Emu(594360))
    shape.fill.solid()
    shape.fill.fore_color.rgb = FOOTER_BG
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = "AI Engineering Business Use Cases | Confidential"
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.color.rgb = WHITE
    try:
        tf.margin_left = Emu(300000)
        shape.text_frame.auto_size = None
        p.space_before = Pt(0)
    except Exception:
        pass

    # Page number
    pn_shape = slide.shapes.add_shape(1, Emu(11155680), Emu(6263640), Emu(914400), Emu(594360))
    pn_shape.fill.solid()
    pn_shape.fill.fore_color.rgb = FOOTER_BG
    pn_shape.line.fill.background()
    tf2 = pn_shape.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = f"{page_num} / {total}"
    run2.font.name = "Calibri"
    run2.font.size = Pt(10)
    run2.font.color.rgb = WHITE

    return shape


def build_architecture_slide(slide, arch_data, page_num, total):
    """Build a full architecture diagram on the given slide."""
    add_title_bar(slide, arch_data["title"])

    rows = arch_data["rows"]
    num_rows = len(rows)

    # Calculate positions for main grid
    box_positions = []  # [(left, top)] for each box in each row

    for row_idx, row in enumerate(rows):
        num_boxes = len(row["boxes"])
        row_y = DIAG_Y_START + (BOX_H + V_GAP) * row_idx
        # Center boxes horizontally within diagram area (leave room for side boxes)
        total_row_width = BOX_W * num_boxes + H_GAP * (num_boxes - 1)
        row_x_start = DIAG_X_START + Emu(200000)  # slight indent

        row_positions = []
        for col_idx in range(num_boxes):
            box_x = row_x_start + (BOX_W + H_GAP) * col_idx
            row_positions.append((box_x, row_y))

        box_positions.append(row_positions)

    # Draw boxes
    for row_idx, row in enumerate(rows):
        for col_idx, box_text in enumerate(row["boxes"]):
            left, top = box_positions[row_idx][col_idx]
            add_box(slide, left, top, BOX_W, BOX_H, box_text, row["type"])

        # Draw horizontal arrows between boxes in this row
        for col_idx in range(len(row["boxes"]) - 1):
            x1, y1 = box_positions[row_idx][col_idx]
            x2, y2 = box_positions[row_idx][col_idx + 1]
            arrow_x = x1 + BOX_W
            arrow_y = y1 + BOX_H // 2 - ARROW_H_HEIGHT // 2
            arrow_w = x2 - (x1 + BOX_W)
            if arrow_w > 0:
                add_h_arrow(slide, arrow_x, arrow_y, arrow_w)

    # Draw vertical arrows between rows (from middle box of each row)
    for row_idx in range(num_rows - 1):
        # Use middle column
        mid_col = len(rows[row_idx]["boxes"]) // 2
        if mid_col < len(box_positions[row_idx]) and mid_col < len(box_positions[row_idx + 1]):
            x1, y1 = box_positions[row_idx][mid_col]
            x2, y2 = box_positions[row_idx + 1][mid_col]
            arrow_x = x1 + BOX_W // 2 - ARROW_V_WIDTH // 2
            arrow_y = y1 + BOX_H
            arrow_h = y2 - (y1 + BOX_H)
            if arrow_h > 0:
                add_v_arrow(slide, arrow_x, arrow_y, arrow_h)

    # Draw side boxes
    side_x = DIAG_X_START + Emu(200000) + (BOX_W + H_GAP) * 3 + H_GAP + Emu(200000)
    side_box_w = Emu(1700000)
    side_box_h = Emu(550000)

    for sb_idx, sb in enumerate(arch_data.get("side_boxes", [])):
        connect_row = sb["connect_row"]
        connect_col = sb["connect_col"]
        # Position side box to the right of the grid
        sb_y = box_positions[connect_row][0][1] + Emu(75000)
        sb_x = side_x

        add_box(slide, sb_x, sb_y, side_box_w, side_box_h, sb["text"], sb["type"])

        # Draw connector arrow from side box to the target box
        target_x, target_y = box_positions[connect_row][connect_col]
        # Horizontal connector from side box left edge to target box right edge
        if connect_col == len(box_positions[connect_row]) - 1:
            # Connect from left of side box to right of last grid box
            conn_x = target_x + BOX_W
            conn_y = target_y + BOX_H // 2 - ARROW_H_HEIGHT // 2
            conn_w = sb_x - conn_x
            if conn_w > 0:
                add_h_arrow(slide, conn_x, conn_y, conn_w)
        else:
            # Connect from left of side box to right of target box
            conn_x = target_x + BOX_W
            conn_y = target_y + BOX_H // 2 - ARROW_H_HEIGHT // 2
            conn_w = sb_x - conn_x
            if conn_w > 0:
                add_h_arrow(slide, conn_x, conn_y, conn_w)

    # Add row type labels on left margin
    row_labels = {
        "input": "INPUT",
        "ai": "AI / COMPUTE",
        "integration": "INTEGRATION",
        "output": "OUTPUT",
    }
    for row_idx, row in enumerate(rows):
        label_y = box_positions[row_idx][0][1] + Emu(200000)
        label = row_labels.get(row["type"], row["type"].upper())
        lbl_shape = slide.shapes.add_shape(1, Emu(50000), label_y, Emu(340000), Emu(300000))
        lbl_shape.fill.background()
        lbl_shape.line.fill.background()
        tf = lbl_shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = label
        run.font.name = "Calibri"
        run.font.size = Pt(6)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)

    add_footer_bar(slide, page_num, total)


def find_slide_index(prs, search_prefix):
    """Find slide index where title starts with search_prefix."""
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    if para.text.strip().startswith(search_prefix):
                        return i
    return None


def move_slide(prs, old_index, new_index):
    """Move slide from old_index to new_index in the slide list."""
    sldIdLst = prs.slides._sldIdLst
    slides = list(sldIdLst)
    el = slides[old_index]
    sldIdLst.remove(el)
    if new_index >= len(list(sldIdLst)):
        sldIdLst.append(el)
    else:
        ref = list(sldIdLst)[new_index]
        sldIdLst.insert(sldIdLst.index(ref), el)


def update_page_numbers(prs):
    """Update all page number shapes (pattern: N / M)."""
    total = len(prs.slides)
    page_pattern = re.compile(r'^\d+\s*/\s*\d+$')
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    txt = para.text.strip()
                    if page_pattern.match(txt):
                        for run in para.runs:
                            run.text = f"{i + 1} / {total}"
                        break


def main():
    prs = Presentation(PPTX_PATH)
    print(f"Loaded {PPTX_PATH} with {len(prs.slides)} slides")

    # Process UC09-UC14 in reverse order so insertion indices stay stable
    uc_ids = ["UC14", "UC13", "UC12", "UC11", "UC10", "UC09"]
    inserted = []

    for uc_id in uc_ids:
        search_prefix = f"{uc_id} |"
        idx = find_slide_index(prs, search_prefix)
        if idx is None:
            print(f"WARNING: Could not find slide for {uc_id}, skipping")
            continue

        # Add a new blank slide (use the layout from the existing slide)
        slide_layout = prs.slide_layouts[0]  # only layout available (DEFAULT)
        new_slide = prs.slides.add_slide(slide_layout)

        # The new slide is appended at the end; move it to idx+1
        current_end = len(prs.slides) - 1
        target_pos = idx + 1
        move_slide(prs, current_end, target_pos)

        print(f"  Inserted arch slide for {uc_id} after slide {idx} (now at position {target_pos})")
        inserted.append((uc_id, target_pos))

    # Now build the diagrams on the inserted slides
    # Re-find each architecture slide by searching for UC slides and taking the next one
    total = len(prs.slides)
    for uc_id in ["UC09", "UC10", "UC11", "UC12", "UC13", "UC14"]:
        search_prefix = f"{uc_id} |"
        idx = find_slide_index(prs, search_prefix)
        if idx is None:
            continue
        arch_slide = prs.slides[idx + 1]
        page_num = idx + 2  # 1-based
        arch_data = UC_ARCHITECTURES[uc_id]
        build_architecture_slide(arch_slide, arch_data, page_num, total)
        print(f"  Built diagram for {uc_id} on slide {idx + 1} (page {page_num}/{total})")

    # Update all page numbers
    update_page_numbers(prs)
    print(f"  Updated page numbers across all {total} slides")

    prs.save(PPTX_PATH)
    print(f"\nSaved {PPTX_PATH} with {total} slides (was 38, added 6 architecture slides)")
    print("Done!")


if __name__ == "__main__":
    main()
