#!/usr/bin/env python3
"""
Add architecture companion slides for UC15-UC20 (Real Estate + Marketing).
Each slide is a visual data-flow diagram with boxes and arrows.
Inserts each architecture slide immediately AFTER its parent UC slide.
"""

import re
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

FONT = "Calibri"
PPTX_PATH = "AI-Engineering-Business-Use-Cases.pptx"

# ── Color palette ──
NAVY = RGBColor(0x1F, 0x3B, 0x6E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_BAR = RGBColor(0x0D, 0x3B, 0x5E)
GRAY_BORDER = RGBColor(0xD0, 0xD5, 0xDD)
LIGHT_BLUE = RGBColor(0xE0, 0xE7, 0xFF)
INDIGO = RGBColor(0x81, 0x8C, 0xF8)
LIGHT_GREEN = RGBColor(0xDC, 0xFC, 0xE7)
GREEN = RGBColor(0x16, 0x65, 0x34)
LIGHT_RED = RGBColor(0xFE, 0xE2, 0xE2)
RED = RGBColor(0xE3, 0x18, 0x37)
LIGHT_YELLOW = RGBColor(0xFE, 0xF3, 0xC7)
AMBER = RGBColor(0x92, 0x40, 0x0E)
DARK_TEXT = RGBColor(0x1A, 0x1A, 0x1A)
ARROW_FILL = RGBColor(0xD0, 0xD5, 0xDD)

# Box type → (fill, border, text_color)
STYLE = {
    "input":      (WHITE, GRAY_BORDER, DARK_TEXT),
    "core":       (NAVY, None, WHITE),
    "integration":(LIGHT_BLUE, INDIGO, DARK_TEXT),
    "output":     (LIGHT_GREEN, GREEN, DARK_TEXT),
    "security":   (LIGHT_RED, RED, DARK_TEXT),
    "storage":    (LIGHT_YELLOW, AMBER, DARK_TEXT),
}

# ── Diagram layout constants ──
BOX_W = Emu(2000000)
BOX_H = Emu(700000)
COL_STARTS = [Emu(400000), Emu(3600000), Emu(6800000)]  # 3 columns
ROW_STARTS = [Emu(750000), Emu(2050000), Emu(3350000), Emu(4650000)]  # 4 rows
HARROW_H = Emu(18000)
VARROW_W = Emu(18000)

SIDE_X = Emu(9600000)
SIDE_W = Emu(2200000)
SIDE_H = Emu(700000)


# ── UC definitions ──
UC_DEFS = {
    "UC15": {
        "search": "UC15 |",
        "title": "UC15 Architecture | Lease Document Generation",
        "rows": [
            [("CRM Data Feed", "input"), ("Property Database", "storage"), ("Tenant Application", "input")],
            [("Claude Lease Engine", "core"), ("Jurisdiction Clause\nSelector", "core"), ("Addenda Generator", "core")],
            [("DocuSign eSign API", "integration"), ("Identity Verification", "integration"), ("County Records\nLookup", "integration")],
            [("Agent Portal", "output"), ("Tenant Self-Service", "output"), ("Compliance Archive", "output")],
        ],
        "side": [("Fair Housing\nAuditor", "security"), ("PII Encryption\n(AES-256)", "security")],
    },
    "UC16": {
        "search": "UC16 |",
        "title": "UC16 Architecture | Lead Scoring & Smart Routing",
        "rows": [
            [("Lead Capture Forms", "input"), ("Zillow API Feed", "input"), ("Meta Ads Webhook", "input")],
            [("XGBoost Scoring\nModel", "core"), ("Behavioral ML\nPipeline", "core"), ("Financial Readiness\nScorer", "core")],
            [("CRM Enrichment\nEngine", "integration"), ("Agent Matching\nAlgorithm", "integration"), ("Campaign Trigger", "integration")],
            [("Response Dashboard", "output"), ("Agent Mobile App", "output"), ("Marketing ROI\nTracker", "output")],
        ],
        "side": [("Fair Housing\nBias Audit", "security"), ("CAN-SPAM/TCPA\nGate", "security")],
    },
    "UC17": {
        "search": "UC17 |",
        "title": "UC17 Architecture | Commission Analytics & Reporting",
        "rows": [
            [("Transaction Feed\n(MLS)", "input"), ("Closing Documents", "input"), ("Listing Agreements", "input")],
            [("Commission Rules\nEngine", "core"), ("Split Calculator", "core"), ("Tier/Bonus Logic", "core")],
            [("QuickBooks API", "integration"), ("Stripe Payment API", "integration"), ("1099 Generator", "integration")],
            [("Financial Dashboard", "output"), ("Agent Leaderboard", "output"), ("Dispute Resolution\nPortal", "output")],
        ],
        "side": [("Calculation\nAudit Trail", "security"), ("SOX Controls", "security")],
    },
    "UC18": {
        "search": "UC18 |",
        "title": "UC18 Architecture | SEO Audit & Optimization",
        "rows": [
            [("Sitemap Parser", "input"), ("Web Crawler\n(rate-limited)", "input"), ("Competitor SERP\nTracker", "input")],
            [("NLP Content\nAnalyzer", "core"), ("Keyword Gap ML", "core"), ("Technical SEO\nScorer", "core")],
            [("Google Analytics\nAPI", "integration"), ("Search Console API", "integration"), ("Core Web Vitals\nMonitor", "integration")],
            [("SEO Dashboard", "output"), ("Client Report\nGenerator", "output"), ("Fix Priority Queue", "output")],
        ],
        "side": [("robots.txt\nRespector", "security"), ("Multi-Tenant\nIsolation", "security")],
    },
    "UC19": {
        "search": "UC19 |",
        "title": "UC19 Architecture | Campaign Performance Dashboard",
        "rows": [
            [("Google Ads API", "input"), ("Meta Ads API", "input"), ("LinkedIn/TikTok\nAPIs", "input")],
            [("ETL Pipeline", "core"), ("Attribution\nNormalizer", "core"), ("Anomaly Detection\nML", "core")],
            [("Data Warehouse\n(unified)", "storage"), ("Metric Aggregator", "integration"), ("Insight Generator", "integration")],
            [("Client Dashboard\n(white-label)", "output"), ("Report PDF\nGenerator", "output"), ("Budget Alert\nEngine", "output")],
        ],
        "side": [("OAuth Token\nRotation", "security"), ("GDPR Aggregation\nGate", "security")],
    },
    "UC20": {
        "search": "UC20 |",
        "title": "UC20 Architecture | Content Pipeline Automation",
        "rows": [
            [("Content Brief\nInput", "input"), ("Asset Library", "storage"), ("Brand Voice Model", "input")],
            [("Claude Content\nGenerator", "core"), ("Multi-Channel\nAdapter", "core"), ("A/B Variant Engine", "core")],
            [("Approval Workflow\nRouter", "integration"), ("Stakeholder Review\nQueue", "integration"), ("Escalation Timer", "integration")],
            [("CMS Publisher", "output"), ("Social Scheduler\n(Buffer)", "output"), ("Email Platform", "output")],
        ],
        "side": [("FTC Disclosure\nFlagger", "security"), ("Brand Guideline\nEnforcer", "security")],
    },
}


def add_box(slide, left, top, width, height, label, style_key):
    """Add a styled rectangle with label text."""
    fill_c, border_c, text_c = STYLE[style_key]
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_c
    if border_c:
        shape.line.color.rgb = border_c
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    # Text
    tf = shape.text_frame
    tf.word_wrap = True
    # Split label into title line and possible sublabel
    lines = label.split("\n")
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = lines[0]
    r.font.name = FONT
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = text_c
    if len(lines) > 1:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = lines[1]
        r2.font.name = FONT
        r2.font.size = Pt(7)
        r2.font.bold = False
        r2.font.color.rgb = text_c
    return shape


def add_harrow(slide, x1, y_center, length):
    """Horizontal arrow (thin filled rectangle)."""
    shape = slide.shapes.add_shape(1, x1, y_center - HARROW_H // 2, length, HARROW_H)
    shape.fill.solid()
    shape.fill.fore_color.rgb = ARROW_FILL
    shape.line.fill.background()
    return shape


def add_varrow(slide, x_center, y1, length):
    """Vertical arrow (thin filled rectangle)."""
    shape = slide.shapes.add_shape(1, x_center - VARROW_W // 2, y1, VARROW_W, length)
    shape.fill.solid()
    shape.fill.fore_color.rgb = ARROW_FILL
    shape.line.fill.background()
    return shape


def build_arch_slide(prs, slide, uc_key, uc_def):
    """Populate an architecture slide with diagram shapes."""

    # Remove default placeholders
    for sp in list(slide.shapes):
        slide.shapes._spTree.remove(sp._element)

    # ── Title bar ──
    title_bar = slide.shapes.add_shape(1, Emu(0), Emu(0), Emu(12192000), Emu(640080))
    title_bar.fill.solid()
    title_bar.fill.fore_color.rgb = NAVY
    title_bar.line.fill.background()

    tb = slide.shapes.add_textbox(Emu(274320), Emu(182880), Emu(11640312), Emu(384048))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = uc_def["title"]
    r.font.name = FONT
    r.font.size = Emu(203200)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # ── Footer bar ──
    footer = slide.shapes.add_shape(1, Emu(0), Emu(6263640), Emu(12192000), Emu(594360))
    footer.fill.solid()
    footer.fill.fore_color.rgb = DARK_BAR
    footer.line.fill.background()

    ftb = slide.shapes.add_textbox(Emu(274320), Emu(6355080), Emu(11640312), Emu(365760))
    ftf = ftb.text_frame
    ftf.word_wrap = True
    fp = ftf.paragraphs[0]
    fp.alignment = PP_ALIGN.CENTER
    fr = fp.add_run()
    fr.text = "AI Engineering Business Use Cases | Confidential"
    fr.font.name = FONT
    fr.font.size = Pt(10)
    fr.font.color.rgb = WHITE

    # ── Grid boxes ──
    for r_idx, row in enumerate(uc_def["rows"]):
        for c_idx, (label, stype) in enumerate(row):
            x = COL_STARTS[c_idx]
            y = ROW_STARTS[r_idx]
            add_box(slide, x, y, BOX_W, BOX_H, label, stype)

            # Horizontal arrow to next box in same row
            if c_idx < len(row) - 1:
                arrow_x = x + BOX_W
                arrow_len = COL_STARTS[c_idx + 1] - (x + BOX_W)
                add_harrow(slide, arrow_x, y + BOX_H // 2, arrow_len)

        # Vertical arrows from this row's center column to next row
        if r_idx < len(uc_def["rows"]) - 1:
            vc_x = COL_STARTS[1] + BOX_W // 2
            vc_y = ROW_STARTS[r_idx] + BOX_H
            vc_len = ROW_STARTS[r_idx + 1] - (ROW_STARTS[r_idx] + BOX_H)
            add_varrow(slide, vc_x, vc_y, vc_len)

    # ── Side boxes (security/governance) ──
    side_tops = [Emu(1600000), Emu(3000000)]
    for s_idx, (label, stype) in enumerate(uc_def["side"]):
        sy = side_tops[s_idx]
        add_box(slide, SIDE_X, sy, SIDE_W, SIDE_H, label, stype)

        # Dashed connector from center column to side box
        conn_x = COL_STARTS[2] + BOX_W
        conn_len = SIDE_X - conn_x
        if conn_len > 0:
            add_harrow(slide, conn_x, sy + SIDE_H // 2, conn_len)


def find_slide_index(prs, search_text):
    """Find the index of a slide whose title contains search_text."""
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                if search_text in shape.text_frame.text:
                    return i
    return None


def move_slide(prs, from_idx, to_idx):
    """Move a slide from from_idx to to_idx in the slide list."""
    slides_el = prs.slides._sldIdLst
    children = list(slides_el)
    slide_id = children[from_idx]
    slides_el.remove(slide_id)
    children = list(slides_el)
    if to_idx <= len(children):
        slides_el.insert(to_idx, slide_id)
    else:
        slides_el.append(slide_id)


def update_page_numbers(prs):
    """Update all N / M page numbers across the deck."""
    total = len(prs.slides)
    pat = re.compile(r'^(\d+)\s*/\s*(\d+)$')
    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                m = pat.match(text)
                if m:
                    new_text = f"{i + 1} / {total}"
                    for para in shape.text_frame.paragraphs:
                        for run in para.runs:
                            if pat.match(run.text.strip()):
                                run.text = new_text


def main():
    prs = Presentation(PPTX_PATH)
    layout = prs.slides[1].slide_layout  # reuse existing layout

    inserted = 0
    results = []

    # Process in reverse order so earlier insertions don't shift later indices
    for uc_key in reversed(["UC15", "UC16", "UC17", "UC18", "UC19", "UC20"]):
        uc_def = UC_DEFS[uc_key]
        idx = find_slide_index(prs, uc_def["search"])
        if idx is None:
            print(f"WARNING: Could not find slide for {uc_key}")
            continue

        # Add new slide at end
        slide = prs.slides.add_slide(layout)
        build_arch_slide(prs, slide, uc_key, uc_def)

        # Move from end to right after the UC slide
        end_idx = len(prs.slides) - 1
        target_idx = idx + 1 + inserted  # account for previously inserted slides after this point
        # Actually since we go in reverse, no adjustment needed for "after" slides
        # We insert right after the found index
        move_slide(prs, end_idx, idx + 1)
        inserted += 1
        results.append((uc_key, idx + 1))

    # Add page numbers to new slides
    total = len(prs.slides)
    for slide in prs.slides:
        has_page_num = False
        for shape in slide.shapes:
            if shape.has_text_frame:
                if re.match(r'^\d+\s*/\s*\d+$', shape.text_frame.text.strip()):
                    has_page_num = True
                    break
        if not has_page_num:
            # Add page number textbox (bottom-right)
            tb = slide.shapes.add_textbox(Emu(10800000), Emu(6400000), Emu(1200000), Emu(300000))
            tf = tb.text_frame
            tf.word_wrap = False
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT
            r = p.add_run()
            r.text = "0 / 0"  # placeholder, will be updated
            r.font.name = FONT
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)

    # Update all page numbers
    update_page_numbers(prs)

    prs.save(PPTX_PATH)
    print(f"SUCCESS: Added {inserted} architecture slides to {PPTX_PATH}")
    print(f"Total slides: {len(prs.slides)}")
    for uc_key, pos in sorted(results):
        print(f"  {uc_key} architecture → inserted at position {pos + 1} (0-indexed: {pos})")


if __name__ == "__main__":
    main()
