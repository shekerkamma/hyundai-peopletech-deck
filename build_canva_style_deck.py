#!/usr/bin/env python3
"""
Build AI Engineering Business Use Cases deck — Canva-professional style.
Consistent layout: teal left panel (title + two-column text) + right photo strip.
"""

import os
import requests
import io
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Dimensions ──────────────────────────────────────────────────────────────
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
PHOTO_W = Inches(4.5)
PANEL_W = Inches(13.333) - PHOTO_W  # ~8.833"

# ── Brand colors ────────────────────────────────────────────────────────────
TEAL        = RGBColor(0x00, 0xC9, 0xA7)
DARK_NAVY   = RGBColor(0x0A, 0x16, 0x28)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_TEAL  = RGBColor(0xE0, 0xF7, 0xF1)
ACCENT_TEAL = RGBColor(0x00, 0x9B, 0x82)
DARK_TEAL   = RGBColor(0x00, 0x8F, 0x75)
SOFT_GRAY   = RGBColor(0xF5, 0xF5, 0xF5)
MID_GRAY    = RGBColor(0x33, 0x33, 0x33)
CHARCOAL    = RGBColor(0x1A, 0x1A, 0x2E)
GOLD        = RGBColor(0xFF, 0xB8, 0x00)

# ── Unsplash photos (free, high-quality) ────────────────────────────────────
PHOTOS = {
    "title":       "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600",
    "strategy":    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600",
    "governance":  "https://images.unsplash.com/photo-1563986768609-322da13575f2?w=600",
    "techstack":   "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600",
    "uc01":        "https://images.unsplash.com/photo-1565043666747-69f6646db940?w=600",
    "uc02":        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600",
    "uc03":        "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=600",
    "uc04":        "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=600",
    "uc05":        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600",
    "uc06":        "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=600",
    "uc07":        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=600",
    "uc08":        "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=600",
    "uc09":        "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600",
    "uc10":        "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600",
    "uc11":        "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600",
    "uc12":        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600",
    "uc13":        "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=600",
    "uc14":        "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600",
    "uc15":        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600",
    "uc16":        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600",
    "uc17":        "https://images.unsplash.com/photo-1554224154-26032ffc0d07?w=600",
    "uc18":        "https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?w=600",
    "uc19":        "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=600",
    "uc20":        "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=600",
    "uc21":        "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600",
    "uc22":        "https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=600",
    "uc23":        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600",
    "uc24":        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600",
    "yc":          "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=600",
    "revenue":     "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600",
    "roadmap":     "https://images.unsplash.com/photo-1507925921958-8a62f3d1a50d?w=600",
    "engagement":  "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600",
    "mcp":         "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600",
    "orchestration":"https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600",
    "risk":        "https://images.unsplash.com/photo-1563986768609-322da13575f2?w=600",
    "summary":     "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600",
}

_photo_cache = {}

def download_photo(key):
    if key in _photo_cache:
        return _photo_cache[key]
    url = PHOTOS.get(key, PHOTOS["title"])
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        buf = io.BytesIO(r.content)
        _photo_cache[key] = buf
        return buf
    except Exception:
        return None


def add_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=12,
                 color=WHITE, bold=False, alignment=PP_ALIGN.LEFT,
                 font_name="Calibri", line_spacing=1.15):
    txbox = slide.shapes.add_textbox(left, top, width, height)
    tf = txbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    p.space_after = Pt(2)
    if line_spacing != 1.15:
        p.line_spacing = Pt(font_size * line_spacing)
    return txbox


def add_multiline_text(slide, left, top, width, height, lines, font_size=10,
                       color=WHITE, font_name="Calibri", line_spacing=1.3,
                       bold_keywords=None):
    """Add text with multiple paragraphs. lines is a list of strings."""
    txbox = slide.shapes.add_textbox(left, top, width, height)
    tf = txbox.text_frame
    tf.word_wrap = True

    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = font_name
        p.space_after = Pt(3)
        p.space_before = Pt(1)

        if bold_keywords and any(kw in line for kw in bold_keywords):
            # Bold the keyword portion
            for kw in bold_keywords:
                if line.startswith(kw):
                    run_b = p.add_run()
                    run_b.text = kw
                    run_b.font.bold = True
                    run_b.font.size = Pt(font_size)
                    run_b.font.color.rgb = color
                    run_b.font.name = font_name
                    run_rest = p.add_run()
                    run_rest.text = line[len(kw):]
                    run_rest.font.size = Pt(font_size)
                    run_rest.font.color.rgb = color
                    run_rest.font.name = font_name
                    break
            else:
                p.text = line
        else:
            p.text = line
    return txbox


def add_stat_box(slide, left, top, number, label, bg_color=DARK_NAVY):
    """Add a stat callout box."""
    box_w, box_h = Inches(1.8), Inches(0.9)
    add_rect(slide, left, top, box_w, box_h, bg_color)
    add_text_box(slide, left, top + Inches(0.05), box_w, Inches(0.45),
                 number, font_size=20, color=GOLD, bold=True,
                 alignment=PP_ALIGN.CENTER, font_name="Calibri")
    add_text_box(slide, left, top + Inches(0.48), box_w, Inches(0.35),
                 label, font_size=8, color=WHITE,
                 alignment=PP_ALIGN.CENTER, font_name="Calibri")


def add_footer(slide, page_num, total):
    add_text_box(slide, Inches(0.3), SLIDE_H - Inches(0.4), Inches(5), Inches(0.3),
                 f"AI Engineering Business Use Cases | Confidential",
                 font_size=7, color=RGBColor(0x88, 0x88, 0x88), font_name="Calibri")
    add_text_box(slide, SLIDE_W - Inches(1.2), SLIDE_H - Inches(0.4), Inches(0.9), Inches(0.3),
                 f"{page_num} / {total}",
                 font_size=7, color=RGBColor(0x88, 0x88, 0x88),
                 alignment=PP_ALIGN.RIGHT, font_name="Calibri")


# ── Slide builders ──────────────────────────────────────────────────────────

def build_title_slide(prs, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    # Full teal background
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, DARK_NAVY)
    # Accent stripe
    add_rect(slide, 0, Inches(2.8), SLIDE_W, Inches(0.06), TEAL)

    # Photo right side with overlay
    photo = download_photo("title")
    if photo:
        photo.seek(0)
        slide.shapes.add_picture(photo, SLIDE_W - PHOTO_W, 0, PHOTO_W, SLIDE_H)
        # Semi-transparent overlay
        add_rect(slide, SLIDE_W - PHOTO_W, 0, PHOTO_W, SLIDE_H,
                 RGBColor(0x0A, 0x16, 0x28))
        slide.shapes[-1].fill.fore_color.rgb = DARK_NAVY
        # Make it semi-transparent via shape properties
        slide.shapes[-1].fill.solid()
        slide.shapes[-1].fill.fore_color.rgb = DARK_NAVY

    # Title text
    add_text_box(slide, Inches(0.8), Inches(1.0), Inches(7), Inches(1.2),
                 "AI Engineering", font_size=48, color=WHITE, bold=True,
                 font_name="Calibri")
    add_text_box(slide, Inches(0.8), Inches(1.9), Inches(7), Inches(1.0),
                 "Business Use Cases", font_size=44, color=TEAL, bold=True,
                 font_name="Calibri")

    add_rect(slide, Inches(0.8), Inches(3.1), Inches(1.5), Inches(0.04), TEAL)

    add_text_box(slide, Inches(0.8), Inches(3.4), Inches(7), Inches(0.5),
                 "Comprehensive Framework", font_size=18, color=LIGHT_TEAL,
                 font_name="Calibri")
    add_text_box(slide, Inches(0.8), Inches(3.9), Inches(7), Inches(0.5),
                 "24 Production-Ready Use Cases Across 7 Verticals",
                 font_size=14, color=WHITE, font_name="Calibri")
    add_text_box(slide, Inches(0.8), Inches(4.3), Inches(7), Inches(0.5),
                 "with YC Competitive Intelligence",
                 font_size=12, color=RGBColor(0x88, 0xCC, 0xBB), font_name="Calibri")

    # Vertical labels
    verticals = ["Manufacturing", "Healthcare", "Legal", "Real Estate",
                 "Marketing", "AI Platforms", "Software Engineering"]
    for i, v in enumerate(verticals):
        x = Inches(0.8) + Inches(i * 1.1)
        add_rect(slide, x, Inches(5.2), Inches(0.95), Inches(0.35), ACCENT_TEAL)
        add_text_box(slide, x, Inches(5.22), Inches(0.95), Inches(0.35),
                     v, font_size=7, color=WHITE, bold=True,
                     alignment=PP_ALIGN.CENTER, font_name="Calibri")

    add_text_box(slide, Inches(0.8), Inches(6.2), Inches(4), Inches(0.4),
                 "May 2026", font_size=11, color=RGBColor(0x88, 0x88, 0x99),
                 font_name="Calibri")
    add_footer(slide, 1, total)


def build_uc_slide(prs, page_num, total, title, photo_key,
                   challenge_lines, solution_lines, results,
                   stack_lines=None, governance_lines=None, yc_lines=None,
                   systems=None, target_users=None, how_it_works=None):
    """Build a use case slide matching the reference design — content-rich layout."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ── Left teal panel ─────────────────────────────────────────────────
    add_rect(slide, 0, 0, PANEL_W, SLIDE_H, TEAL)

    # Title — single line, clean
    clean_title = title.replace("\n", " — ")
    add_text_box(slide, Inches(0.4), Inches(0.2), PANEL_W - Inches(0.7), Inches(0.55),
                 clean_title, font_size=22, color=WHITE, bold=True, font_name="Calibri")
    add_rect(slide, Inches(0.4), Inches(0.72), Inches(2), Inches(0.03), DARK_NAVY)

    # ── CHALLENGE section (left column) ────────────────────────────────
    col_w = Inches(3.85)
    y_section = Inches(0.85)
    add_text_box(slide, Inches(0.4), y_section, Inches(1.5), Inches(0.2),
                 "CHALLENGE", font_size=8, color=DARK_NAVY, bold=True, font_name="Calibri")
    challenge_text = "\n".join(f"• {l}" for l in challenge_lines)
    add_text_box(slide, Inches(0.4), y_section + Inches(0.2), col_w, Inches(1.4),
                 challenge_text, font_size=7.5, color=DARK_NAVY, font_name="Calibri")

    # ── SOLUTION section (right column) ────────────────────────────────
    sol_x = Inches(4.4)
    add_text_box(slide, sol_x, y_section, Inches(1.5), Inches(0.2),
                 "SOLUTION", font_size=8, color=DARK_NAVY, bold=True, font_name="Calibri")
    solution_text = "\n".join(f"• {l}" for l in solution_lines)
    add_text_box(slide, sol_x, y_section + Inches(0.2), col_w, Inches(1.4),
                 solution_text, font_size=7.5, color=DARK_NAVY, font_name="Calibri")

    # ── Results stat boxes ──────────────────────────────────────────────
    stat_y = Inches(2.55)
    if results:
        for i, (num, label) in enumerate(results[:4]):
            stat_x = Inches(0.4) + Inches(i * 2.05)
            add_stat_box(slide, stat_x, stat_y, num, label)

    # ── HOW IT WORKS section (new — fills the gap) ─────────────────────
    hiw_y = Inches(3.55)
    if how_it_works:
        add_text_box(slide, Inches(0.4), hiw_y, Inches(2), Inches(0.2),
                     "HOW IT WORKS", font_size=8, color=DARK_NAVY, bold=True,
                     font_name="Calibri")
        hiw_text = "\n".join(f"→ {l}" for l in how_it_works)
        add_text_box(slide, Inches(0.4), hiw_y + Inches(0.2), PANEL_W - Inches(0.7), Inches(0.65),
                     hiw_text, font_size=7, color=DARK_NAVY, font_name="Calibri")

    # ── GOVERNANCE / YC section ─────────────────────────────────────────
    gov_y = Inches(4.45)
    if governance_lines:
        add_text_box(slide, Inches(0.4), gov_y, Inches(3.5), Inches(0.2),
                     "GOVERNANCE & SECURITY", font_size=7.5, color=DARK_NAVY,
                     bold=True, font_name="Calibri")
        gov_text = "\n".join(f"• {l}" for l in governance_lines)
        add_text_box(slide, Inches(0.4), gov_y + Inches(0.2), col_w, Inches(0.85),
                     gov_text, font_size=7, color=DARK_NAVY, font_name="Calibri")

    if yc_lines:
        add_text_box(slide, sol_x, gov_y, Inches(3.5), Inches(0.2),
                     "COMPETITIVE LANDSCAPE", font_size=7.5, color=DARK_NAVY,
                     bold=True, font_name="Calibri")
        yc_text = "\n".join(f"• {l}" for l in yc_lines)
        add_text_box(slide, sol_x, gov_y + Inches(0.2), col_w, Inches(0.85),
                     yc_text, font_size=7, color=DARK_NAVY, font_name="Calibri")

    # ── Solution stack bar ──────────────────────────────────────────────
    stack_y = Inches(5.55)
    if stack_lines:
        add_rect(slide, Inches(0.3), stack_y, PANEL_W - Inches(0.5), Inches(0.85), DARK_NAVY)
        add_text_box(slide, Inches(0.4), stack_y + Inches(0.04), Inches(2), Inches(0.18),
                     "SOLUTION STACK", font_size=7.5, color=TEAL, bold=True,
                     font_name="Calibri")
        for i, (layer, detail) in enumerate(stack_lines[:4]):
            col_x = Inches(0.4) + Inches(i * 2.05)
            add_text_box(slide, col_x, stack_y + Inches(0.22), Inches(1.9), Inches(0.18),
                         layer, font_size=7, color=TEAL, bold=True, font_name="Calibri")
            add_text_box(slide, col_x, stack_y + Inches(0.42), Inches(1.9), Inches(0.38),
                         detail, font_size=6.5, color=WHITE, font_name="Calibri")

    # ── Systems + Target Users bar ──────────────────────────────────────
    bar_y = Inches(6.5)
    if systems:
        add_rect(slide, Inches(0.3), bar_y, Inches(4), Inches(0.35), ACCENT_TEAL)
        sys_text = "SYSTEMS: " + "  |  ".join(systems[:5])
        add_text_box(slide, Inches(0.4), bar_y + Inches(0.04), Inches(3.8), Inches(0.28),
                     sys_text, font_size=6.5, color=WHITE, bold=True, font_name="Calibri")

    if target_users:
        add_rect(slide, Inches(4.5), bar_y, Inches(4), Inches(0.35), DARK_TEAL)
        usr_text = "USERS: " + target_users
        add_text_box(slide, Inches(4.6), bar_y + Inches(0.04), Inches(3.8), Inches(0.28),
                     usr_text, font_size=6.5, color=WHITE, bold=True, font_name="Calibri")

    # ── Right photo strip ───────────────────────────────────────────────
    photo = download_photo(photo_key)
    if photo:
        photo.seek(0)
        slide.shapes.add_picture(photo, PANEL_W, 0, PHOTO_W, SLIDE_H)

    add_footer(slide, page_num, total)


def build_content_slide(prs, page_num, total, title, photo_key,
                        col1_title, col1_lines, col2_title, col2_lines,
                        bottom_items=None):
    """Build a non-UC content slide (strategy, governance, etc.)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_rect(slide, 0, 0, PANEL_W, SLIDE_H, TEAL)

    # Title — flatten multi-line
    clean_title = title.replace("\n", " — ")
    add_text_box(slide, Inches(0.4), Inches(0.2), PANEL_W - Inches(0.7), Inches(0.5),
                 clean_title, font_size=22, color=WHITE, bold=True, font_name="Calibri")
    add_rect(slide, Inches(0.4), Inches(0.7), Inches(2), Inches(0.03), DARK_NAVY)

    # Column 1
    add_text_box(slide, Inches(0.4), Inches(0.85), Inches(3.5), Inches(0.22),
                 col1_title, font_size=9, color=DARK_NAVY, bold=True, font_name="Calibri")
    c1_text = "\n".join(f"• {l}" for l in col1_lines)
    add_text_box(slide, Inches(0.4), Inches(1.07), Inches(3.85), Inches(4.2),
                 c1_text, font_size=7.5, color=DARK_NAVY, font_name="Calibri")

    # Column 2
    add_text_box(slide, Inches(4.4), Inches(0.85), Inches(3.5), Inches(0.22),
                 col2_title, font_size=9, color=DARK_NAVY, bold=True, font_name="Calibri")
    c2_text = "\n".join(f"• {l}" for l in col2_lines)
    add_text_box(slide, Inches(4.4), Inches(1.07), Inches(3.85), Inches(4.2),
                 c2_text, font_size=7.5, color=DARK_NAVY, font_name="Calibri")

    # Bottom bar
    if bottom_items:
        bar_y = Inches(5.6)
        add_rect(slide, Inches(0.3), bar_y, PANEL_W - Inches(0.5), Inches(0.9), DARK_NAVY)
        for i, (num, label) in enumerate(bottom_items[:4]):
            bx = Inches(0.4) + Inches(i * 2.05)
            add_text_box(slide, bx, bar_y + Inches(0.08), Inches(1.9), Inches(0.38),
                         num, font_size=16, color=GOLD, bold=True,
                         alignment=PP_ALIGN.CENTER, font_name="Calibri")
            add_text_box(slide, bx, bar_y + Inches(0.48), Inches(1.9), Inches(0.3),
                         label, font_size=7, color=WHITE,
                         alignment=PP_ALIGN.CENTER, font_name="Calibri")

    photo = download_photo(photo_key)
    if photo:
        photo.seek(0)
        slide.shapes.add_picture(photo, PANEL_W, 0, PHOTO_W, SLIDE_H)

    add_footer(slide, page_num, total)


# ── USE CASE DATA ───────────────────────────────────────────────────────────

USE_CASES = [
    {
        "title": "UC01 | Visual Inspection\nComputer Vision",
        "photo": "uc01",
        "challenge": [
            "15-20% false positive rate in manual visual inspection across production lines",
            "Inspector fatigue: accuracy degrades after 2-3 hours of repetitive inspection",
            "$2.3M average annual quality cost per plant from missed defects and rework",
            "Inconsistent inspection criteria across shifts and personnel",
            "Hyundai operates 12+ global plants producing 4M+ vehicles/year — scale demands automation",
        ],
        "solution": [
            "CNN-based real-time defect detection with edge-deployed YOLOv8 models (640×640 input, 1.2ms inference)",
            "Multi-camera fusion covering 360° component inspection at line speed (120 units/hr)",
            "Automated MES feedback loop: defect triggers line-stop within 200ms via OPC-UA",
            "Continuous model retraining from operator-labeled corrections using active learning",
            "Transfer learning: pre-trained on ImageNet, fine-tuned on 50K+ plant-specific defect images",
        ],
        "results": [("99.2%", "Detection Accuracy"), ("85%", "False Positive Reduction"),
                    ("$1.8M", "Annual Savings"), ("4-6 wk", "Deployment")],
        "how_it_works": [
            "Camera captures → Edge GPU (Jetson Orin) runs YOLOv8 inference in <2ms → Defect classification (scratch/dent/weld/paint)",
            "Confidence >0.85 triggers auto-reject; 0.5-0.85 routes to operator review queue; <0.5 passes",
            "Rejected parts logged to MES with defect image, location coordinates, and shift context for root-cause analysis",
        ],
        "governance": [
            "Model validation per IEC 62443 industrial cybersecurity standard",
            "Image data retention: 7 years for traceability, encrypted at rest (AES-256)",
            "Edge device certificate rotation every 90 days, firmware signed with HSM",
        ],
        "yc": ["Instrumental (W14, 80 emp) — manufacturing CV analytics platform",
               "Ocular AI (W24, 6 emp) — real-time defect detection",
               "Landing AI (founded by Andrew Ng) — visual inspection platform",
               "Eigen Innovations — thermal + visual inspection for automotive"],
        "stack": [("EDGE / CAPTURE", "GigE Vision cameras\nJetson Orin NX"),
                  ("COMPUTE / AI", "YOLOv8 + EfficientNet\nONNX Runtime"),
                  ("INTEGRATION", "OPC-UA → SAP MES\nMQTT broker"),
                  ("UX / DECISION", "Quality dashboard\nDefect heatmap")],
        "systems": ["SAP MES", "GigE Vision", "Jetson Orin", "TF Serving"],
        "users": "Quality Engineers | Line Supervisors | Plant Managers",
    },
    {
        "title": "UC02 | Model & Variant\nConfirmation",
        "photo": "uc02",
        "challenge": [
            "3-5% assembly mismatch rate causing costly rework and warranty claims",
            "$500K average warranty cost per variant error across production batches",
            "Manual VIN validation bottleneck: 45-sec per unit slowing line throughput",
            "BOM version sync lag between engineering and production floor (avg 4-hr delay)",
            "Hyundai's 200+ trim variants per model line multiply configuration complexity",
        ],
        "solution": [
            "Automated VIN/barcode scanning with real-time BOM cross-validation at every station",
            "Variant mismatch alerting with instant operator HMI notification + audio alarm",
            "Multi-source BOM reconciliation: engineering ECO, production BOM, supplier ASN in real-time",
            "Historical mismatch pattern analysis for proactive fixture verification before shift start",
            "Digital twin integration: virtual BOM validated against physical assembly sequence",
        ],
        "results": [("99.8%", "Variant Accuracy"), ("90%", "Mismatch Reduction"),
                    ("<2 sec", "Validation Time"), ("2-3 wk", "Deployment")],
        "how_it_works": [
            "VIN scanned at station entry → BOM lookup via SAP RFC call (<500ms) → Component list validated against pick sequence",
            "Mismatch detected → HMI flashes red + audio alert → Operator confirms or overrides with supervisor PIN",
            "Every scan event persisted to event store: VIN, station, BOM revision, timestamp — enables 15-year traceability",
        ],
        "governance": [
            "BOM version control: every scan logged with BOM revision hash and ECO reference",
            "Recall-grade traceability: component-to-VIN linkage retained 15 years per NHTSA",
            "Scanner calibration audit per ISO 15416 barcode quality standard (quarterly)",
        ],
        "yc": ["Fictiv (S14, 300+ emp) — digital manufacturing platform",
               "Tulip Interfaces (W15, 200+ emp) — manufacturing apps platform"],
        "stack": [("EDGE / CAPTURE", "Cognex readers\nRFID UHF scanners"),
                  ("COMPUTE / AI", "BOM validation engine\nAnomaly detection"),
                  ("INTEGRATION", "SAP RFC + OData\nECO sync service"),
                  ("UX / DECISION", "Operator HMI alerts\nShift dashboard")],
        "systems": ["SAP MES", "Cognex Scanners", "BOM Database", "ECO System"],
        "users": "Assembly Operators | Quality Auditors | Production Engineers",
    },
    {
        "title": "UC03 | Seating & Component\nValidation",
        "photo": "uc03",
        "challenge": [
            "Torque compliance failures undetected until end-of-line QA, causing 12% rework rate",
            "Fitment issues cause line stops costing $15K/minute in lost throughput",
            "Manual torque verification logs incomplete — only 60% of fasteners digitally recorded",
            "Multi-variant seating configs (leather/cloth/heated/cooled) increase error probability 3x",
            "IATF 16949 audit findings: 23% of plants cited for incomplete torque documentation",
        ],
        "solution": [
            "Vision-based fitment validation confirming correct component seating before fastening",
            "Smart torque tools (Atlas Copco/Desoutter): digital values streamed via open protocol",
            "Real-time compliance dashboards aggregating torque, fitment, sequence, and angle data",
            "Automated non-conformance reports (NCRs) generated within seconds with root-cause hints",
            "Statistical process control (SPC) with Cp/Cpk monitoring per fastener group",
        ],
        "results": [("60%", "Integration Effort ↓"), ("0", "Undetected Failures"),
                    ("Real-time", "Compliance Monitor"), ("<1 sec", "Validation Latency")],
        "how_it_works": [
            "Camera verifies component placement → Torque tool activated only after vision OK → Value streamed to MES",
            "SPC engine calculates Cpk in real-time; Cpk <1.33 triggers process alert to quality engineer",
            "End-of-line QA receives pre-validated pass/fail per VIN — audit trail complete before vehicle exits station",
        ],
        "governance": [
            "Torque data retention per IATF 16949 clause 8.5.2 — complete production records",
            "Vision model validated against golden reference images quarterly (>99% match threshold)",
            "Calibration records linked to torque tool serial numbers with ISO 6789 compliance",
        ],
        "yc": ["Arch Systems (S14) — manufacturing data platform",
               "Pico MES (W21, 15 emp) — lightweight manufacturing execution"],
        "stack": [("EDGE / CAPTURE", "Smart torque tools\nInline cameras"),
                  ("COMPUTE / AI", "Fitment CV models\nSPC engine"),
                  ("INTEGRATION", "MES + open protocol\nSCADA OPC-UA"),
                  ("UX / DECISION", "SPC dashboard\nNCR generator")],
        "systems": ["Atlas Copco", "MES", "Vision Cameras", "SCADA"],
        "users": "Assembly Technicians | Quality Engineers | Process Engineers",
    },
    {
        "title": "UC04 | SOP Compliance\nMonitoring",
        "photo": "uc04",
        "challenge": [
            "12% SOP deviation rate undetected in manual observation audits",
            "Safety incidents from skipped steps: avg 3.2 recordable incidents/quarter per plant",
            "Audit prep requires 80+ hours of manual video review per quarter per line",
            "Inconsistent adherence across 3 shifts with no real-time correction mechanism",
            "Training investment ($2.5M/yr) not translating to measurable compliance improvement",
        ],
        "solution": [
            "Pose estimation (MediaPipe/OpenPose) + activity recognition for real-time SOP adherence",
            "Step-sequence verification: alerts within 5 sec if operator skips critical safety steps",
            "Automated audit evidence with timestamped video clips per procedure (MPEG-DASH)",
            "Shift-level compliance scoring with trend analysis, coaching recommendations, and gamification",
            "Integration with LMS: non-compliant patterns auto-trigger targeted retraining modules",
        ],
        "results": [("95%", "Compliance Detection"), ("70%", "Safety Deviation ↓"),
                    ("Hrs→Min", "Audit Prep Time"), ("Real-time", "Alert Delivery")],
        "how_it_works": [
            "Edge GPU processes CCTV feed → Skeleton extraction (17 keypoints) → Activity classified against SOP model",
            "Sequence engine validates step order: e.g., 'gloves on' must precede 'chemical handling' — violation = instant alert",
            "Compliance score = (completed steps / required steps) × time-in-zone factor — aggregated per shift/line/plant",
        ],
        "governance": [
            "Worker privacy: pose data anonymized (no facial recognition), skeleton-only storage, GDPR Article 35 DPIA",
            "Video retention limited to 30 days unless flagged for incident review (then 1 year)",
            "Works council / union notification required in EU jurisdictions before deployment",
        ],
        "yc": ["Protex AI (S21, 5 emp) — workplace safety CV platform",
               "Voxel (W18, 50 emp) — workplace analytics from cameras"],
        "stack": [("EDGE / CAPTURE", "CCTV + Jetson\nMediaPipe pipeline"),
                  ("COMPUTE / AI", "Pose estimation\nLSTM sequence model"),
                  ("INTEGRATION", "EHS API + LMS\nAlert gateway"),
                  ("UX / DECISION", "Supervisor mobile\nCompliance heatmaps")],
        "systems": ["CCTV", "EHS Platform", "Training LMS", "MES"],
        "users": "Line Supervisors | EHS Managers | Training Coordinators",
    },
    {
        "title": "UC05 | Predictive Quality\nAnalytics",
        "photo": "uc05",
        "challenge": [
            "2-4% scrap rate from undetected process drift across 50+ sensor variables per station",
            "Root cause analysis takes 48+ hours of manual cross-correlation by senior engineers",
            "Feature engineering bottleneck: data scientists spend 70% of time on data prep, not modeling",
            "Siloed sensor data (temperature, pressure, vibration) prevents cross-process correlation",
            "Hyundai's 6-sigma quality target requires <3.4 DPMO — current: 15-25 DPMO on critical dims",
        ],
        "solution": [
            "Sensor fusion: unified time-series from 200+ sensors across welding, stamping, painting",
            "AutoML feature store with automated feature engineering, selection, and drift monitoring",
            "Explainability dashboards showing SHAP values — operators understand why model flags risk",
            "Preemptive process adjustment recommendations pushed to HMI before defects materialize",
            "Federated learning: models train across plants without sharing raw sensor data",
        ],
        "results": [("40%", "Scrap Rate ↓"), ("48hr→15m", "Root Cause Analysis"),
                    ("Auto", "ML Pipeline Gen"), ("50+", "Cross-Variable Corr")],
        "how_it_works": [
            "IoT gateway aggregates 200+ sensor streams at 1Hz → Kafka → Feature store computes 500+ derived features",
            "XGBoost ensemble predicts defect probability per part → SHAP waterfall explains top 5 contributing factors",
            "Risk score >0.7 → HMI shows adjustment recommendation (e.g., 'reduce weld current 3A') → operator confirms",
        ],
        "governance": [
            "Feature store lineage: every feature traceable to raw sensor source with transformation DAG",
            "Model explainability required per ISO 22989 (AI concepts and terminology)",
            "Sensor calibration validation automated: drift >2% from baseline triggers maintenance ticket",
        ],
        "yc": ["Sight Machine (S12, 100+ emp) — manufacturing analytics platform",
               "Uptake (analytics) — industrial AI for asset performance",
               "Arch Systems (S14) — manufacturing data infrastructure"],
        "stack": [("EDGE / CAPTURE", "IoT gateway + OPC-UA\n200+ sensor array"),
                  ("COMPUTE / AI", "XGBoost + SHAP\nAutoML feature store"),
                  ("INTEGRATION", "Kafka → InfluxDB\nSAP MES writeback"),
                  ("UX / DECISION", "SHAP dashboard\nHMI recommendations")],
        "systems": ["IoT Sensors", "InfluxDB", "Kafka", "Feature Store"],
        "users": "Process Engineers | Data Scientists | Quality Managers",
    },
    {
        "title": "UC06 | Predictive\nMaintenance",
        "photo": "uc06",
        "challenge": [
            "Unplanned downtime costs $260K/hour avg across automotive manufacturing lines",
            "Reactive maintenance 3-5x costlier than predictive approaches (Deloitte 2024 study)",
            "Maintenance scheduling based on fixed OEM intervals, not actual equipment health",
            "Vibration/acoustic anomaly patterns missed by periodic manual inspections (monthly)",
            "Hyundai's 20,000+ rotating assets across 12 plants — manual monitoring impossible at scale",
        ],
        "solution": [
            "Vibration (MEMS accelerometer) + acoustic (ultrasonic) + thermal anomaly detection via LSTM autoencoders",
            "Equipment health scoring: 0-100 composite from multi-sensor fusion with trend extrapolation",
            "Auto-generated SAP PM work orders when health score drops below configurable threshold",
            "Remaining useful life (RUL) prediction with confidence intervals for maintenance planning",
            "NASA CMAPSS-inspired degradation modeling adapted for automotive press/stamp/robot assets",
        ],
        "results": [("45%", "Downtime ↓"), ("25%", "Maintenance Cost ↓"),
                    ("0-100", "Health Score"), ("40%", "Faster Implementation")],
        "how_it_works": [
            "Vibration sensor (10kHz sampling) → FFT spectrum analysis → LSTM autoencoder detects anomalous frequency patterns",
            "Health score = weighted ensemble of vibration, thermal, acoustic, and operational (cycle count) signals",
            "Score <70 → yellow alert (plan maintenance) → Score <40 → red alert (SAP PM work order auto-created)",
        ],
        "governance": [
            "Sensor data Level 2 (Internal), encrypted in transit via TLS 1.3, at rest AES-256",
            "Maintenance decision audit trail: work order linked to model prediction, sensor snapshot, and confidence",
            "False alarm rate monitored continuously: target <5%, model retrained if exceeded for 2 consecutive weeks",
        ],
        "yc": ["Augury (W18, 200+ emp) — machine health diagnostics",
               "Petasense (S16) — wireless vibration monitoring",
               "InfluxData (W13, 210 emp) — time-series database",
               "Inviscid AI (W26) — physics-informed ML for equipment"],
        "stack": [("EDGE / CAPTURE", "MEMS accel + ultrasonic\nEdge gateway (Raspberry Pi 5)"),
                  ("COMPUTE / AI", "LSTM autoencoder\nRUL regression model"),
                  ("INTEGRATION", "SAP PM RFC\nMQTT → InfluxDB"),
                  ("UX / DECISION", "Health dashboard\nMaintenance planner")],
        "systems": ["SAP PM", "IoT Gateways", "InfluxDB", "Edge Compute"],
        "users": "Maintenance Technicians | Reliability Engineers | Plant Managers",
    },
    {
        "title": "UC07 | Safety Monitoring\n& PPE Detection",
        "photo": "uc07",
        "challenge": [
            "PPE non-compliance observed in 8-12% of shift observations across auto plants",
            "Restricted zone violations undetected until post-incident review (avg 6-hr delay)",
            "Manual incident reports take 2+ hours per event, delaying corrective action",
            "OSHA recordable rate stagnant at 4.2/100 workers despite $3M annual training spend",
            "Thermal hazard zones near welding/painting require real-time proximity awareness",
        ],
        "solution": [
            "Real-time PPE detection: hard hat, vest, goggles, gloves, ear protection via YOLOv8-seg",
            "Geofenced zone intrusion alerts with <3 second supervisor SMS/push notification",
            "AI-generated incident reports from video evidence with auto-classification (OSHA 300 log)",
            "Safety trend analytics: heatmaps by zone, shift, role with weekly digest for EHS leadership",
            "Thermal camera integration for heat stress monitoring near furnace/paint booth areas",
        ],
        "results": [("98%", "PPE Compliance"), ("100%", "Zone Violation Capture"),
                    ("80%", "Faster Documentation"), ("2-3 wk", "Deployment")],
        "how_it_works": [
            "CCTV feed → YOLOv8-seg model detects PPE items on body regions → Missing item triggers zone-specific alert",
            "Geofence engine: GPS + BLE beacons define restricted zones → Worker badge enters zone → Supervisor notified <3s",
            "Incident report auto-generated: video clip + PPE status + zone + worker role + timestamp → EHS platform API",
        ],
        "governance": [
            "No facial recognition: PPE detection uses body-region segmentation only — fully anonymous",
            "Alert data retained 1 year per OSHA 1904 recordkeeping requirements",
            "Thermal camera data classified Level 2, not shared with HR systems, not used for performance",
        ],
        "yc": ["Protex AI (S21, 5 emp) — workplace safety CV",
               "Voxel (W18, 50 emp) — workplace safety analytics",
               "Intenseye (S21) — AI-powered EHS platform"],
        "stack": [("EDGE / CAPTURE", "CCTV + FLIR thermal\nBLE beacons"),
                  ("COMPUTE / AI", "YOLOv8-seg PPE model\nGeofence engine"),
                  ("INTEGRATION", "EHS API + Twilio\nOSHA 300 formatter"),
                  ("UX / DECISION", "Supervisor mobile app\nSafety heatmaps")],
        "systems": ["CCTV", "EHS Platform", "Twilio", "BLE Beacons"],
        "users": "EHS Managers | Shift Supervisors | Safety Officers",
    },
    {
        "title": "UC08 | Digital Traceability\n& Recall",
        "photo": "uc08",
        "challenge": [
            "Recall investigation takes 2-4 weeks of manual component genealogy tracing",
            "Component genealogy gaps across tier 1-3 suppliers create liability exposure ($100M+)",
            "$35M average recall cost; scope overestimation adds 20-40% unnecessary remediation",
            "Paper-based lot tracking prevents real-time genealogy queries for quality holds",
            "NHTSA requires full traceability within 48 hours — current avg: 14 days",
        ],
        "solution": [
            "Neo4j graph database: full component-to-vehicle genealogy with 5-level supplier depth",
            "RFID + barcode tracking at every station creating immutable production record (30M+ events/day)",
            "Automated recall scope analysis: pinpoint affected VINs in minutes, not weeks",
            "Supplier integration: ASN data linked to production genealogy via EDI 856 + API",
            "Blockchain-anchored audit trail: cryptographic hash of daily genealogy state for tamper evidence",
        ],
        "results": [("75%", "Faster Recall"), ("Full", "Production Genealogy"),
                    ("Auto", "Recall Scope Analysis"), ("Audit-Ready", "Compliance")],
        "how_it_works": [
            "RFID scan at station → Event stored: (part_id, VIN, station, operator, timestamp, supplier_lot) → Neo4j ingestion",
            "Recall query: MATCH path from defective supplier lot → affected parts → installed VINs → owner records in <60 sec",
            "Scope analyzer: statistical sampling validates recall boundaries — prevents over-recall (saves 20-40% of remediation cost)",
        ],
        "governance": [
            "Traceability data retained 15+ years per NHTSA TREAD Act and Hyundai corporate policy",
            "Immutable audit log: append-only ledger with daily blockchain anchor hash",
            "Supplier data governed by mutual NDA, classification Level 3, access audit logged",
        ],
        "yc": ["Fictiv (S14, 300+ emp) — digital manufacturing network",
               "Cognitio Labs (S23) — supply chain intelligence",
               "Autumn Labs (S24) — manufacturing traceability platform"],
        "stack": [("EDGE / CAPTURE", "UHF RFID readers\nCognex scanners"),
                  ("COMPUTE / AI", "Neo4j graph analytics\nRecall scope engine"),
                  ("INTEGRATION", "SAP + EDI 856\nSupplier portal API"),
                  ("UX / DECISION", "Genealogy explorer\nRecall simulator")],
        "systems": ["SAP", "RFID", "Neo4j", "Supplier Portal"],
        "users": "Quality Directors | Compliance Officers | Supply Chain Managers",
    },
]

# ── Additional UC data (Healthcare, Legal, Real Estate, Marketing, SW Eng) ──

ADDITIONAL_UCS = [
    {"title": "UC09 | Patient Intake\nAutomation", "photo": "uc09",
     "challenge": ["15-minute avg intake time per patient creating bottlenecks and wait-time complaints", "23% form error rate from manual data entry causing billing rejections and claim denials", "Clinical staff spend 60% of time on admin vs patient care — burnout drives 35% annual turnover", "Multi-system data entry: same info keyed into EHR, billing, scheduling — 4x redundant effort", "No-show rate 18% without automated appointment reminders and pre-visit engagement"],
     "solution": ["AI-powered form validation with real-time error detection and auto-correction suggestions", "Auto EHR population via FHIR R4 API: demographics, insurance, history, medications, allergies", "Intelligent scheduling via Calendly + provider availability matching + wait-time prediction", "SMS/voice intake via Twilio for patients without portal access — 95% mobile completion rate", "Pre-visit engagement: automated reminders, intake forms, insurance card photo upload"],
     "results": [("3 min", "Intake (from 15)"), ("95%", "Form Accuracy"), ("40%", "Admin Time ↓"), ("$3-5K/mo", "Savings per Practice")],
     "how_it_works": ["Patient receives SMS link 48hr before appointment → Completes intake on mobile → AI validates insurance + demographics", "FHIR R4 write-back: validated data auto-populates EHR patient record + scheduling system + billing module", "Incomplete forms flagged for staff follow-up call; 85% of patients complete without staff intervention"],
     "governance": ["HIPAA BAA required; PHI encryption AES-256 at rest, TLS 1.3 in transit", "Audit logging per HITECH Act: every PHI access timestamped with user, action, and IP", "Patient consent management: opt-in/opt-out tracked per FHIR Consent resource"],
     "yc": ["Understood Care (S24) — patient engagement", "HealthKey (W25) — health records", "Morf Health (S22) — care coordination"],
     "stack": [("EDGE / CAPTURE", "Web portal\nMobile + SMS"), ("COMPUTE / AI", "Claude NLP\nForm validation ML"), ("INTEGRATION", "FHIR R4 + Twilio\nCalendly + EHR"), ("UX / DECISION", "Patient dashboard\nStaff queue view")],
     "systems": ["Epic/Cerner EHR", "FHIR R4 API", "Calendly", "Twilio"], "users": "Front Desk Staff | Clinical Coordinators | Practice Managers"},
    {"title": "UC10 | Insurance\nVerification", "photo": "uc10",
     "challenge": ["30% claim denial rate from eligibility errors — $262B in denied claims annually (US)", "48-hour avg verification turnaround delays patient scheduling and revenue recognition", "$25 cost per manual verification call, 12 min per call — 15 calls/day per FTE", "Prior auth requirements change frequently; staff miss updates causing retroactive denials", "Multiple payer portals: staff toggle between 8-12 different systems daily"],
     "solution": ["Pre-appointment AI eligibility verification against real-time payer feeds (EDI 270/271)", "Automated prior auth submission with clinical documentation auto-attached from EHR", "Denial prediction model: flags high-risk claims before submission — prevents denials proactively", "Payer rule change monitoring: scrapes payer bulletins, auto-updates workflow rules within 24hrs", "Batch verification: entire next-day schedule verified overnight — staff reviews exceptions only"],
     "results": [("85%", "First-Pass Approval"), ("5 min", "Verification (from 48hr)"), ("$5", "Cost per Verif (from $25)"), ("60%", "Denial Rate ↓")],
     "how_it_works": ["Scheduler triggers nightly batch → EDI 270 sent per patient → Payer responds 271 → AI parses coverage details", "High-risk claims scored by denial prediction model (XGBoost on 500K+ historical claims) → Staff reviews flagged items", "Prior auth: clinical notes auto-extracted → Medical necessity letter generated → Submitted via payer portal API"],
     "governance": ["EDI 270/271 compliance per HIPAA X12 standards — all transactions logged", "Claims data Level 3 (Confidential), encrypted end-to-end with per-payer isolation", "Denial prediction model audited for demographic bias quarterly — disparate impact <5% threshold"],
     "yc": ["Stream (S22) — claims processing", "Avallon AI (Sp25) — insurance verification", "Curacel (W22) — claims AI"],
     "stack": [("EDGE / CAPTURE", "Payer EDI feeds\nFax OCR ingestion"), ("COMPUTE / AI", "Claims ML models\nDenial prediction"), ("INTEGRATION", "Payer API + EHR\nClearinghouse EDI"), ("UX / DECISION", "Verification dashboard\nDenial analytics")],
     "systems": ["Payer EDI/APIs", "EHR", "Billing System", "Clearinghouse"], "users": "Billing Staff | Prior Auth Specialists | Revenue Cycle Managers"},
    {"title": "UC11 | HIPAA Compliance\nPortal", "photo": "uc11",
     "challenge": ["Manual audit prep consumes 120+ staff-hours per year across compliance team", "PHI access logging gaps: 15% of access events untracked across EHR, email, file shares", "$1.5M avg HIPAA breach penalty; $6.3M for willful neglect — 725+ breaches reported in 2024", "Risk assessments annual but threats evolve continuously — gap between audits is blind spot", "Business associate (BA) management: 50+ BAs per health system, each requiring BAA tracking"],
     "solution": ["Automated audit trail aggregation from EHR, IAM, email, cloud storage into unified view", "Real-time PHI access monitoring with anomaly detection — flags unusual access patterns in <5 min", "Continuous compliance scoring with gap identification mapped to HIPAA Security Rule safeguards", "Breach risk scoring: quantified risk per system, updated daily, with remediation priority ranking", "BA management automation: BAA tracking, annual review reminders, termination workflow triggers"],
     "results": [("80%", "Audit Prep Time ↓"), ("100%", "PHI Access Logging"), ("Real-time", "Compliance Status"), ("Daily", "Breach Risk Scoring")],
     "how_it_works": ["Log collectors ingest from EHR audit logs + Okta/Azure AD + email DLP + S3 access logs → Unified compliance lake", "Anomaly detection: baseline access patterns per role → Flag deviations (e.g., billing staff accessing clinical notes at 2am)", "Compliance score = (controls_met / controls_required) per HIPAA safeguard category — drill-down to individual control gaps"],
     "governance": ["HIPAA Security Rule: admin, physical, tech safeguards automated with evidence collection", "HITECH Breach Notification: 60-day automated workflow with OCR-assisted notification letter generation", "BA management: BAA tracking, annual review, termination workflow with automated reminders"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Access log collectors\nSIEM feeds"), ("COMPUTE / AI", "Anomaly detection ML\nCompliance rules"), ("INTEGRATION", "IAM + EHR + email\nS3 audit storage"), ("UX / DECISION", "Compliance dashboard\nRisk heat map")],
     "systems": ["EHR", "IAM (Okta/Azure AD)", "S3 Storage", "SIEM"], "users": "Compliance Officers | HIPAA Privacy Officers | IT Security"},
    {"title": "UC12 | Contract Generation\n& Review", "photo": "uc12",
     "challenge": ["4-6 hours per contract draft for routine agreements — 60% of associate billable time", "Inconsistent clause usage creating enforceability risks across 500+ active templates", "$350/hr attorney time on routine document assembly that AI can handle in minutes", "15% of contracts sent with outdated clause libraries — liability exposure per engagement", "Cross-jurisdictional complexity: 50-state variations for employment, lease, NDA agreements"],
     "solution": ["AI drafting from firm-specific templates + Git-versioned clause library with approval workflow", "Automated review: risk scoring per clause with deviation flagging against firm standards", "Clause recommendation engine based on deal type, jurisdiction, counterparty risk profile", "DocuSign integration for seamless review-sign workflow with parallel routing", "Redline comparison: AI highlights substantive changes vs formatting noise in counterparty edits"],
     "results": [("45 min", "Draft Time (from 4-6h)"), ("90%", "Clause Consistency"), ("75%", "Attorney Time ↓"), ("$3-5K/mo", "Savings per Firm")],
     "how_it_works": ["Attorney selects deal type + jurisdiction → AI pulls matching template + clause variants → Draft generated with firm-standard language", "Risk scoring: each clause analyzed for deviation from firm baseline → RED/YELLOW/GREEN per section → Attorney focuses on RED", "Counterparty redline: AI compares incoming vs sent version → Highlights substantive changes → Ignores formatting deltas"],
     "governance": ["Attorney-client privilege: generated drafts access-controlled per matter, audit logged", "Clause library Git-backed: partner-approved changes only, semantic versioning, rollback capability", "Output always marked DRAFT; human sign-off required before client delivery — no autonomous sending"],
     "yc": ["Ironclad (S15, 700 emp) — contract lifecycle", "Draftwise (S20, 50 emp) — contract drafting", "General Legal (W26) — AI legal assistant"],
     "stack": [("EDGE / CAPTURE", "Document upload\nOCR ingestion"), ("COMPUTE / AI", "Claude + templates\nRisk scoring"), ("INTEGRATION", "DocuSign + DMS APIs\nEmail integration"), ("UX / DECISION", "Attorney review portal\nClause library UI")],
     "systems": ["DocuSign", "iManage", "Gmail", "Billing"], "users": "Associates | Partners | Paralegals | Legal Ops"},
    {"title": "UC13 | Legal Research\nSummarization", "photo": "uc13",
     "challenge": ["8-12 hours per research task for junior associates — $350/hr average cost", "Manual search covers only 60-70% of relevant case law — critical precedents missed", "65% of billable hours spent on research vs actual legal analysis and strategy", "Citation verification manual; LLM hallucinated citations are a documented professional risk", "Multi-jurisdictional research multiplies effort 3-5x for interstate or federal matters"],
     "solution": ["AI precedent search across Westlaw, LexisNexis, firm brief archives simultaneously", "Structured summaries with jurisdiction-specific relevance scoring and authority ranking", "Citation-linked outputs: every claim traced to source document with pinpoint paragraph reference", "Collaborative research workspace: multiple attorneys can build on shared research threads", "Shepard's/KeyCite integration: auto-checks if cited cases are still good law"],
     "results": [("2 hrs", "Research (from 8-12)"), ("95%", "Precedent Coverage"), ("70%", "Junior Workload ↓"), ("Verified", "Citation Accuracy")],
     "how_it_works": ["Attorney enters research question → RAG pipeline searches firm briefs + Westlaw + LexisNexis → Ranked results by relevance", "Claude reasoning: synthesizes findings into structured memo with headings, holdings, and distinguishing factors", "Every citation auto-validated: Shepard's check confirms case is still good law → Bad citations flagged RED"],
     "governance": ["Every citation validated against source database — zero tolerance for hallucinated references", "Research memos marked AI-assisted per state bar disclosure rules (ABA Formal Opinion 512)", "No client data sent to external models; on-premise RAG pipeline for privileged materials"],
     "yc": ["Vector Legal (W26) — AI legal research", "Docsum (S23) — document summarization"],
     "stack": [("EDGE / CAPTURE", "Legal DB connectors\nBrief bank indexer"), ("COMPUTE / AI", "RAG pipeline\nClaude reasoning"), ("INTEGRATION", "Westlaw + LexisNexis\nDMS search"), ("UX / DECISION", "Brief generator\nCitation viewer")],
     "systems": ["Westlaw", "LexisNexis", "iManage DMS", "Brief Bank"], "users": "Junior Associates | Senior Associates | Research Librarians"},
    {"title": "UC14 | Legal Billing\nAutomation", "photo": "uc14",
     "challenge": ["15-20% revenue leakage from unbilled time entries — $50K+/yr per attorney lost", "Manual timesheet reconciliation: 5+ hrs/week per billing coordinator", "30-day avg invoice cycle from capture to payment — cash flow impact on smaller firms", "8% of invoices rejected for LEDES/UTBMS formatting errors — delays payment by 30+ days", "Expense categorization: receipts pile up, 25% of reimbursable expenses go unclaimed"],
     "solution": ["AI activity capture from calendar, email, document edits — reconstructs billable day", "Auto timesheet generation with matter-code assignment based on email subject + doc metadata", "LEDES-compliant invoice automation with client rate cards and volume discount rules", "Expense auto-categorization from receipt OCR and travel booking confirmations", "Narrative generation: AI writes time entry descriptions matching firm's billing guidelines"],
     "results": [("95%", "Billable Capture"), ("15%", "Revenue Recovery"), ("5 days", "Invoice Cycle (from 30)"), ("Auto", "Expense Categorization")],
     "how_it_works": ["Calendar + email + doc edits monitored → AI reconstructs daily activity log → Suggests time entries with matter codes", "Attorney reviews AI suggestions in 5 min (vs 30 min manual entry) → Approves/edits → Timesheet submitted", "Month-end: LEDES formatter validates all entries → Client rate card applied → Invoice generated and emailed"],
     "governance": ["Billing data Level 3, SOX-adjacent controls for >$10M revenue firms", "Time entry audit trail: AI suggestion vs attorney-approved final entry preserved", "LEDES/UTBMS validation before submission — rejected entries flagged for correction"],
     "yc": ["JustPaid (W23, 20 emp) — invoice automation", "Peakflo (W22, 45 emp) — accounts receivable"],
     "stack": [("EDGE / CAPTURE", "Email/calendar monitors\nDoc edit tracking"), ("COMPUTE / AI", "Activity classification\nNarrative generation"), ("INTEGRATION", "QB + Stripe APIs\nLEDES formatter"), ("UX / DECISION", "Billing dashboard\nClient portal")],
     "systems": ["QuickBooks", "Gmail", "Calendar", "Stripe"], "users": "Associates | Billing Coordinators | Managing Partners"},
    {"title": "UC15 | Lease Document\nGeneration", "photo": "uc15",
     "challenge": ["2-3 hours per lease with manual clause selection from 200+ clause variants", "$45K avg litigation cost per lease dispute — preventable with consistent language", "Inconsistent terms across 50+ agents creating uneven liability exposure", "Jurisdiction requirements missed in 6% of leases — state/county disclosure laws vary widely", "Lease renewals: 30% of renewals processed late due to manual calendar tracking"],
     "solution": ["AI lease generation pulling property/tenant data from CRM + county-specific requirements", "Jurisdiction-aware clause library by state/county with auto-disclosure attachment", "E-signature via DocuSign with tenant identity verification and income validation", "Lease comparison tool: highlights deviations from brokerage standard in counterparty edits", "Renewal automation: 90-day notice triggers, terms adjustment recommendations based on market data"],
     "results": [("15 min", "Generation (from 2-3h)"), ("98%", "Clause Accuracy"), ("0", "Jurisdiction Errors"), ("$2-4K/mo", "Savings per Brokerage")],
     "how_it_works": ["Agent enters property + tenant info → AI selects jurisdiction template → Clauses auto-populated with market-rate terms", "County disclosure check: cross-references property against county requirements → Auto-attaches lead paint, mold, flood zone disclosures", "DocuSign envelope created → Tenant reviews + signs on mobile → Executed lease filed to DMS + CRM automatically"],
     "governance": ["PII handling: tenant SSN/income encrypted AES-256, purged 30 days after lease execution", "State-specific rules updated quarterly from legal database — Lexis state survey integration", "Fair housing compliance: AI terms audited quarterly for discriminatory language patterns"],
     "yc": ["Clau (S20, 90 emp) — real estate AI", "Homeflow (W23) — property management", "Goldbridge (F25) — RE technology"],
     "stack": [("EDGE / CAPTURE", "CRM data feed\nProperty DB"), ("COMPUTE / AI", "Claude + lease templates\nClause selector"), ("INTEGRATION", "DocuSign + CRM APIs\nCounty lookup"), ("UX / DECISION", "Agent portal\nTenant self-service")],
     "systems": ["CRM", "DocuSign", "Zillow API", "County Records"], "users": "Leasing Agents | Property Managers | Broker Compliance"},
    {"title": "UC16 | Lead Scoring &\nSmart Routing", "photo": "uc16",
     "challenge": ["40% of leads receive first response >4 hours — industry benchmark: <5 min for 9x conversion", "Unqualified leads consume 60% of agent follow-up time — $200+ wasted per dead-end lead", "Manual CRM entry: 45 min/day per agent on data entry vs client engagement", "Lead source attribution broken across 8+ channels: marketing ROI unmeasurable", "Round-robin routing ignores agent expertise — luxury lead goes to starter-home specialist"],
     "solution": ["AI lead scoring using 30+ interest signals: Zillow saves, ad clicks, email opens, price range, pre-approval", "Smart routing to best-fit agent by expertise, geography, availability, and historical conversion rate", "Auto CRM enrichment from Zillow views, Meta ad interactions, email engagement, website behavior", "Campaign trigger automation: high-score leads get immediate SMS + agent notification + property matches", "Lead nurture sequences: automated drip campaigns personalized by property preference and timeline"],
     "results": [("15 min", "Response (from 4 hrs)"), ("35%", "Conversion Lift"), ("50%", "Unqualified ↓"), ("Auto", "CRM Enrichment")],
     "how_it_works": ["Lead submits form/calls → 30+ signals scored by XGBoost model → Score 0-100 with confidence interval", "Score >70 → Instant SMS to best-match agent + auto-CRM entry → Agent sees lead profile + property matches on mobile", "Score 30-70 → Nurture sequence activated → Weekly property updates + market insights → Re-scored on engagement"],
     "governance": ["Fair housing: scoring model audited for demographic bias quarterly — disparate impact <5%", "Lead data: 2yr active retention, 5yr archived per broker compliance requirements", "CAN-SPAM and TCPA compliance for all automated outreach — opt-out honored within 24 hours"],
     "yc": ["PropReturns (S21, 40 emp) — RE analytics", "Smart Alto (W17) — lead qualification"],
     "stack": [("EDGE / CAPTURE", "Lead capture forms\nZillow API"), ("COMPUTE / AI", "XGBoost scoring\nBehavioral ML"), ("INTEGRATION", "CRM + Meta + email\nZapier triggers"), ("UX / DECISION", "Agent assignment UI\nLead pipeline view")],
     "systems": ["CRM", "Zillow", "Meta Ads", "Email/SMS"], "users": "Listing Agents | Buyer Agents | Team Leads | Marketing"},
    {"title": "UC17 | Commission Analytics\n& Reporting", "photo": "uc17",
     "challenge": ["Month-end calculations take 3+ days of manual spreadsheet work across 50+ agents", "12% of agents dispute commissions monthly — trust erosion and admin overhead", "No real-time visibility into earned vs pending vs paid — agents can't forecast income", "Split commission scenarios (co-listing, referral, team) miscalculated 8% of the time", "1099 preparation: year-end reconciliation takes 2 weeks of dedicated accounting time"],
     "solution": ["Auto commission engine with configurable splits, tiers, bonuses, and override rules", "Deal attribution: listing agreements linked to closing, payment, and commission disbursement", "Real-time financial dashboards for agents (earnings) and management (P&L, agent economics)", "Agent performance ranking with trend analysis, conversion funnels, and coaching insights", "Automated 1099 generation from commission data with IRS e-filing integration"],
     "results": [("Same-day", "Commission Reports"), ("99.5%", "Calculation Accuracy"), ("80%", "Dispute Reduction"), ("Live", "Performance Ranking")],
     "how_it_works": ["Closing data from MLS/title company → Commission rules engine applies split/tier/bonus formulas → Agent sees earnings instantly", "Dispute resolution: agent clicks disputed entry → System shows calculation trace with rule version + input data → Transparent resolution", "Year-end: 1099 data pre-compiled from disbursements → Accounting reviews → IRS e-file submitted with one click"],
     "governance": ["Financial data Level 3, SOX-adjacent controls for >$10M revenue brokerages", "Commission audit trail: every calculation step logged with rule version and input values", "1099 generation from commission data, IRS-compliant with e-filing and agent portal access"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Transaction feeds\nMLS closing data"), ("COMPUTE / AI", "Commission rules\nSplit calculator"), ("INTEGRATION", "QB + Stripe + CRM\n1099 generator"), ("UX / DECISION", "Financial dashboard\nAgent leaderboard")],
     "systems": ["CRM", "QuickBooks", "Stripe", "MLS"], "users": "Agents | Brokerage Managers | Accounting | Team Leads"},
    {"title": "UC18 | SEO Audit &\nOptimization", "photo": "uc18",
     "challenge": ["Manual SEO audits take 20+ hours per client site — limits agency to 5-8 clients per strategist", "Recommendations outdated by publish time: 2-week lag between audit and implementation", "No competitive position tracking: flying blind on SERP movements and competitor content strategy", "Technical SEO issues (Core Web Vitals, crawlability, schema) missed without engineering support", "Content gap analysis: manual keyword research covers <30% of opportunity space"],
     "solution": ["Automated crawl with technical SEO scoring: Core Web Vitals, mobile usability, schema validation", "AI content recommendations: keyword gaps, topical authority mapping, content cannibalization detection", "Weekly competitive position monitoring with SERP tracking and movement alerts", "Prioritized fix list with estimated traffic impact per recommendation — ROI-ranked actions", "Content brief generation: AI creates detailed briefs with target keywords, structure, and competitor analysis"],
     "results": [("2 hrs", "Audit (from 20+)"), ("Per-page", "Recommendations"), ("Weekly", "Competitive Tracking"), ("$2-4K/mo", "Revenue per Client")],
     "how_it_works": ["Crawler scans site (respecting robots.txt) → Technical issues scored → Content analyzed for keyword gaps and authority", "AI generates prioritized fix list: each item has estimated traffic impact + implementation difficulty → ROI ranking", "Weekly SERP tracker: monitors 500+ keywords per client → Alerts on position changes >5 → Competitor content flagged"],
     "governance": ["Crawl rate limiting: respects robots.txt, max 5 req/sec, polite user-agent identification", "Competitor data from public SERPs only, no scraping behind authentication or paywalls", "Client data isolated: multi-tenant architecture with per-client encryption keys"],
     "yc": ["Positional (S21, acquired) — SEO tooling", "Clearscope — content optimization platform"],
     "stack": [("EDGE / CAPTURE", "Web crawler\nSitemap parser"), ("COMPUTE / AI", "NLP content analysis\nKeyword gap ML"), ("INTEGRATION", "GA + Search Console\nSERP tracker"), ("UX / DECISION", "SEO dashboard\nClient report gen")],
     "systems": ["Google Analytics", "Search Console", "WordPress", "Screaming Frog"], "users": "SEO Specialists | Content Strategists | Agency Managers"},
    {"title": "UC19 | Campaign Performance\nDashboard", "photo": "uc19",
     "challenge": ["8+ hrs/week per account manager on manual reporting across 4-6 ad platforms", "Inconsistent metrics: each platform defines conversion, attribution, and ROAS differently", "Client reporting delays: 3-5 days from period end — clients demand real-time visibility", "Anomaly detection manual: budget overspend and CPA spikes caught 24-48 hrs late", "Cross-channel attribution: customer journey spans 5+ touchpoints — no unified view"],
     "solution": ["Automated ingestion from Google Ads, Meta, LinkedIn, TikTok, programmatic DSPs", "Unified metric normalization: standardized attribution model across all channels", "AI insight generation: auto-surfaces trends, anomalies, and actionable optimization recommendations", "White-label client dashboards with auto report generation (PDF, email digest, Slack alerts)", "Budget pacing: real-time spend tracking with automated bid adjustments when pacing off-target"],
     "results": [("Real-time", "Unified Dashboard"), ("90%", "Reporting Time ↓"), ("Auto", "Client Reports"), ("Instant", "Anomaly Detection")],
     "how_it_works": ["Platform APIs polled every 15 min → ETL normalizes metrics to unified schema → Data warehouse (BigQuery/Snowflake)", "Anomaly engine: statistical process control on CPA, CTR, spend → Alert if >2σ deviation from 7-day rolling avg", "Weekly AI digest: Claude summarizes performance, highlights top/bottom campaigns, recommends budget reallocation"],
     "governance": ["Platform API usage within rate limits and ToS — OAuth tokens rotated per platform policy", "Client ad spend data Level 2, segregated per client with row-level security in warehouse", "GDPR: no PII in analytics; all data aggregated — individual user journeys anonymized"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Platform API connectors\nETL pipelines"), ("COMPUTE / AI", "Analytics aggregation\nAnomaly detection"), ("INTEGRATION", "Multi-platform APIs\nData warehouse"), ("UX / DECISION", "Client dashboard\nReport PDF generator")],
     "systems": ["Google Analytics", "Meta Ads API", "LinkedIn Ads", "Buffer"], "users": "Account Managers | Media Buyers | Agency Directors"},
    {"title": "UC20 | Content Pipeline\nAutomation", "photo": "uc20",
     "challenge": ["5-day avg content cycle from brief to publish — competitors publish daily", "Approval bottlenecks: content sits 2+ days in review queues across 3-4 stakeholders", "Inconsistent brand voice across blog, social, email, ad copy — 5 writers, 5 styles", "Manual A/B testing: 3+ hrs per test setup limiting experimentation volume", "Content repurposing: blog → social → email done manually — 2hrs per piece per channel"],
     "solution": ["AI content generation from structured briefs + fine-tuned brand voice model", "Automated approval workflows with parallel reviewer routing and deadline escalation", "Multi-channel publishing: one brief → blog post + 5 social variants + email + ad copy", "Auto A/B variant generation with performance-based winner selection after 48hr test", "Content calendar: AI suggests topics based on trending keywords, competitor gaps, seasonal patterns"],
     "results": [("1 day", "Cycle (from 5 days)"), ("80%", "Faster Approvals"), ("Consistent", "Brand Voice"), ("Auto", "A/B Variants")],
     "how_it_works": ["Content brief submitted → Claude generates draft + 3 headline variants + social adaptations → Brand voice score checked", "Parallel approval: content, legal, and brand reviewers notified simultaneously → Majority approval = proceed → Escalation at 24hr", "A/B engine: 2 variants published → Performance measured for 48hr → Winner auto-promoted → Loser paused"],
     "governance": ["Brand guidelines enforced via fine-tuned style model — voice consistency score >85% required", "Content audit trail: every generation, edit, and approval timestamped with reviewer identity", "FTC compliance: AI-generated content flagged for disclosure where required by advertising standards"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Content brief input\nAsset library"), ("COMPUTE / AI", "Claude generation\nBrand voice model"), ("INTEGRATION", "CMS + social APIs\nEmail platform"), ("UX / DECISION", "Editorial dashboard\nPublishing scheduler")],
     "systems": ["WordPress", "Buffer", "CMS", "Slack"], "users": "Content Managers | Copywriters | Brand Managers"},
    {"title": "UC21 | AI-Powered Code\nGeneration", "photo": "uc21",
     "challenge": ["30-40% of engineering hours on routine bug fixes and boilerplate code", "PR review bottleneck: avg 2-day cycle time from issue to merge across teams", "Legacy codebases accumulate 200+ open issues with no bandwidth to address", "Junior onboarding takes 3-6 months before meaningful contributions to production", "Engineering hiring costs $150-250K/yr per dev — autonomous agents offer 10x leverage"],
     "solution": ["OpenHands (68.6k★, $18.8M Series A) autonomous agents: analyze issues, write fixes, open PRs end-to-end", "CodeAct agent framework: agents execute bash, Python, and browser actions in natural language loop", "Event-sourced architecture: every action/observation logged as typed event — deterministic replay and full audit trail", "Sandboxed execution: every agent runs in isolated Docker container — no host access, secrets masked", "Model-agnostic: Claude Opus 4.6 (80.8% SWE-Bench), GPT-5.2 (80.0%), or self-hosted Qwen/DeepSeek"],
     "results": [("80.8%", "SWE-Bench Verified"), ("~$3", "Cost per PR"), ("68.6k★", "GitHub Stars"), ("6 Providers", "Git Platform Support")],
     "how_it_works": ["GitHub issue created → OpenHands resolver agent reads issue + codebase → CodeAct generates fix → Runs tests in sandbox → Opens PR", "EventStream hub: User Message → LLM → Action (bash/code/browser) → Runtime sandbox → Observation → next cycle", "AgentHub registry: CodeActAgent (generalist), BrowsingAgent (web tasks), micro-agents (from natural language specs)"],
     "governance": ["All AI-generated code marked AI-assisted per GitHub metadata; human approval required before merge", "Sandboxed runtime: Docker container with no host filesystem access, network restricted, secrets never exposed", "SecurityAnalyzer rates every tool call LOW/MEDIUM/HIGH risk — HIGH requires human confirmation"],
     "yc": ["OpenHands (68.6k★, $18.8M) — open-source AI dev platform", "Devin/Cognition ($175M raised) — commercial autonomous developer", "Cursor (background agents, 65.7% SWE-Bench) — AI-native IDE", "Codex (GPT-5.5, 56.8% SWE-Bench Pro) — OpenAI's coding agent"],
     "stack": [("AGENT / SDK", "OpenHands SDK\nCodeAct + AgentHub"), ("COMPUTE / AI", "Claude Opus 4.6\nGPT-5.2 / Qwen"), ("INTEGRATION", "GitHub/GitLab/Bitbucket\nMCP + FastMCP"), ("UX / DECISION", "PR review portal\nEventStream viewer")],
     "systems": ["GitHub", "GitLab", "Docker", "CI/CD"], "users": "Engineering Leads | DevOps Managers | VP Engineering"},
    {"title": "UC22 | Automated Test\nGeneration", "photo": "uc22",
     "challenge": ["Legacy codebases average 35% test coverage — most critical paths untested", "15% of deployments cause incidents in first 24 hours due to missing regression tests", "Test maintenance: 20% of test suites break with each major refactor — flaky tests ignored", "Security testing requires specialized expertise most teams lack — OWASP coverage <20%", "Manual test writing: senior engineer produces ~15 test cases/day at $150/hr"],
     "solution": ["OpenHands agents generate comprehensive test suites validated on SWT-Bench (testing benchmark)", "Multi-agent fan-out: parallel generation across unit/integration/E2E layers simultaneously", "Automated test maintenance: detect broken tests post-refactor, auto-fix assertions and mocks", "Security-focused generation: OWASP Top 10 coverage with pen-test scenarios auto-generated", "OpenHands Index testing category: measures real-world test generation quality across models"],
     "results": [("35→85%", "Test Coverage ↑"), ("60%", "Fewer Prod Regressions"), ("10x", "Test Gen Speed"), ("1-2 wk", "Setup")],
     "how_it_works": ["Agent reads source code + existing tests → Identifies untested paths via coverage gap analysis → Generates test files", "SWT-Bench validation: generated tests verified against known-buggy code — must catch the bug to pass benchmark", "CI integration: agent opens PR with test files → Coverage diff shown → Human reviews → Merge adds to CI pipeline"],
     "governance": ["Generated tests reviewed by senior engineer before inclusion in CI pipeline", "No production PII in test fixtures; synthetic data generation via Faker/factory patterns", "Coverage metrics: minimum 80% threshold enforced via CI gates — PR blocked below threshold"],
     "yc": ["QA Wolf (W19, 80 emp) — E2E testing as service ($4M ARR)", "Carbonate (S23) — AI test generation from user flows", "Momentic (S23) — autonomous E2E testing with self-healing", "CodiumAI (now Qodo) — AI test generation IDE extension"],
     "stack": [("AGENT / SDK", "OpenHands agents\nSWT-Bench model"), ("COMPUTE / AI", "Claude reasoning\nCoverage analysis"), ("INTEGRATION", "CI/CD hooks\nCoverage APIs (lcov)"), ("UX / DECISION", "Coverage dashboard\nRisk heatmap")],
     "systems": ["GitHub", "Jest/Pytest", "CI/CD", "SAST Tools"], "users": "QA Engineers | Engineering Managers | Security Teams"},
    {"title": "UC23 | Code Modernization\n& Tech Debt", "photo": "uc23",
     "challenge": ["40% of dev time spent navigating and working around legacy code (Stripe 2023 study)", "Framework migrations (Angular→React, Python 2→3) take 6-18 months manually", "Average enterprise has 200+ outdated packages deferred due to risk of breaking changes", "Monolith decomposition requires deep institutional knowledge often lost to attrition", "Technical debt costs the average company $3.6M/yr in lost productivity (McKinsey)"],
     "solution": ["OpenHands multi-repo dependency upgrades at ~$3 per PR across hundreds of services automatically", "Autonomous framework migration: CodeAct agent generates idiomatic code in target framework with tests", "Monolith decomposition: agent analyzes dependency graph, identifies service boundaries, extracts and tests", "Commit0 benchmark: validates greenfield development quality — agent builds working app from spec", "Dead code elimination: agent identifies unused exports, unreachable branches, and orphaned files"],
     "results": [("~$3", "Cost per Migration PR"), ("80%", "Tech Debt ↓"), ("6→1 mo", "Migration Timeline"), ("100+", "Repos per Sprint")],
     "how_it_works": ["Dependency scanner identifies outdated packages → Agent creates branch → Updates package + fixes breaking changes → Runs tests → Opens PR", "Migration: agent reads source in framework A → Generates equivalent in framework B → Validates output matches behavioral tests", "Commit0 pipeline: spec document → Agent scaffolds project → Builds features iteratively → Integration tests validate completeness"],
     "governance": ["All migration PRs include automated regression test results and diff size metrics", "Security patches (CVE fixes) auto-merged after CI pass; major versions require human approval", "Architecture Decision Records (ADRs) auto-generated for each decomposition or migration step"],
     "yc": ["Grit.io (W22) — automated code migrations at scale", "Moderne (S21, 50 emp) — large-scale refactoring platform", "Sourcegraph Cody (S14, 300+) — code intelligence + search", "CodeRabbit — AI-powered code review and refactoring"],
     "stack": [("ANALYSIS", "Dependency graph\nDead code scanner"), ("COMPUTE / AI", "Claude Opus 4.6\nMulti-agent chain"), ("INTEGRATION", "npm/pip/maven registries\nCI validation"), ("UX / DECISION", "Migration tracker\nRisk scoring board")],
     "systems": ["GitHub", "npm/pip/maven", "Docker", "Terraform"], "users": "Platform Engineers | Tech Leads | CTOs"},
    {"title": "UC24 | DevOps & Incident\nResponse", "photo": "uc24",
     "challenge": ["MTTR averages 4+ hours for production incidents — 65% of time spent on log correlation", "On-call engineers spend 60% of incident time correlating logs across 10+ services", "CI/CD pipeline failures block 15-20% of deployments — most are config/dependency issues", "Terraform state diverges from reality across 50+ microservices — drift detected monthly, not daily", "Alert fatigue: avg SRE receives 200+ alerts/week — 85% are non-actionable noise"],
     "solution": ["OpenHands agents analyze logs + metrics, pinpoint root causes, generate fix PRs autonomously", "Automated CI/CD debugging: agent reads build logs, identifies failure cause, pushes fix within minutes", "IaC auto-remediation: drift detection → Terraform PR → validated plan → human-approved apply", "Runbook automation: agent executes playbook steps with human escalation for destructive actions", "Alert triage: agent classifies alerts, correlates with recent deploys, auto-resolves known patterns"],
     "results": [("4hr→15m", "MTTR"), ("70%", "Auto-Resolved"), ("85%", "CI/CD Fix Rate"), ("24/7", "Always-On Coverage")],
     "how_it_works": ["PagerDuty alert fires → Agent reads alert context + recent deploys + logs → Identifies root cause → Generates fix PR or rollback", "CI failure: agent reads build log → Classifies error (dep/config/test/compile) → Pushes targeted fix → Re-triggers pipeline", "Terraform drift: daily plan comparison → Drift detected → Agent generates corrective PR with plan output → Human approves apply"],
     "governance": ["Production access read-only for agents; all write operations require human approval via Slack/PagerDuty", "Every agent action logged with timestamp, rationale, confidence score, and blast radius assessment", "Blast radius controls: auto-remediation limited to non-critical services; critical services require human-in-the-loop"],
     "yc": ["Rootly (S21, 45 emp) — incident management platform", "incident.io (S21, 120 emp) — incident response automation", "Firehydrant (W20, 90 emp) — reliability platform", "Shoreline.io (acquired by DataDog) — incident automation"],
     "stack": [("OBSERVE", "DataDog + Loki logs\nPagerDuty alerts"), ("COMPUTE / AI", "OpenHands agent\nLog analysis LLM"), ("INTEGRATION", "Terraform API + K8s\nGitHub Actions"), ("UX / DECISION", "Incident dashboard\nRunbook executor")],
     "systems": ["PagerDuty", "DataDog", "Terraform", "GitHub Actions"], "users": "SRE Teams | DevOps Engineers | Incident Commanders"},
]


def main():
    TOTAL_SLIDES = 36
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    print("Building AI Engineering Business Use Cases deck...")
    print("Downloading photos (this may take a minute)...")

    # Slide 1: Title
    build_title_slide(prs, TOTAL_SLIDES)

    # Slide 2: AI Strategy Overview
    build_content_slide(prs, 2, TOTAL_SLIDES, "AI Strategy Overview", "strategy",
        "Enterprise AI Adoption Maturity Model", [
            "Stage 1 Experimental: Chatbot pilots, single-task automation, manual prompt engineering",
            "Stage 2 Departmental: Department-specific agents, RAG pipelines, basic MCP integration — MOST ORGS ARE HERE",
            "Stage 3 Enterprise: Cross-functional agent orchestration, shared MCP infrastructure, model governance platform",
            "Stage 4 Autonomous: Self-improving agent networks, autonomous decision loops, real-time optimization",
        ],
        "Key Performance Indicators", [
            "User adoption rate → Process cycle time reduction → Enterprise productivity gain → Autonomous decision accuracy",
            "Org Structure evolves: Innovation lab → Dedicated AI team → Central AI CoE → AI-native operating model",
            "Governance scales: Informal policies → Model registry → SOC 2/HIPAA frameworks → Continuous audit + kill switches",
        ],
        bottom_items=[("Stage 2", "Most Orgs Today"), ("Stage 3", "Target State"), ("4 Stages", "Maturity Levels"), ("12 mo", "Typical Journey")])

    # Slide 3: Governance
    build_content_slide(prs, 3, TOTAL_SLIDES, "Governance & Security\nFramework", "governance",
        "Data Classification & Access Control", [
            "Level 1 (Public): Marketing content, public APIs, anonymized analytics",
            "Level 2 (Internal): Sensor data, operational metrics, internal comms",
            "Level 3 (Confidential): Financial records, contracts, employee PII",
            "Level 4 (Restricted): Patient records (PHI), SSN, PCI, biometric data",
            "RBAC: Agent → Production Data read-only, scoped, audit-logged",
            "API Keys: 90-day rotation, per-environment scoping, HashiCorp Vault",
        ],
        "Compliance & Model Governance", [
            "SOC 2 Type II: Annual audit, continuous monitoring via Vanta",
            "HIPAA BAA: Required for healthcare, PHI encryption AES-256",
            "GDPR Article 25: Data protection by design, right to explanation",
            "Prompt versioning: Git-tracked, semantic versioning, rollback",
            "Bias monitoring: Demographic parity testing quarterly",
            "Drift detection: KL divergence, auto-retrain at 5% drift",
        ])

    # Slide 4: Tech Stack
    build_content_slide(prs, 4, TOTAL_SLIDES, "Technology Stack\n6-Layer Architecture", "techstack",
        "Presentation → Orchestration → Sub-Agents", [
            "PRESENTATION: React 18 + Next.js 14, Tailwind CSS, Recharts/D3.js, Vercel Edge, PWA, WebSocket",
            "ORCHESTRATION: LangGraph / CrewAI, Claude 3.5 Sonnet (primary), GPT-4o (fallback), Temporal.io, Redis queues",
            "SUB-AGENTS: Specialist agents per vertical, tool-use MCP clients, RAG retrieval, validation/guardrail agents",
        ],
        "Models → MCP Layer → Infrastructure", [
            "MODELS: Claude 4.5 Opus (reasoning), GPT-4o (vision), Whisper v3 (audio), YOLO v8 (detection), XGBoost (tabular)",
            "MCP LAYER: SAP MES connector, FHIR R4, DocuSign eSign, Stripe/QuickBooks, Google Analytics + Search Console",
            "INFRA: AWS EKS + Lambda + S3, PostgreSQL 16 + pgvector, Pinecone, Terraform IaC, DataDog APM, HashiCorp Vault",
        ],
        bottom_items=[("6 Layers", "Production Stack"), ("20+", "MCP Connectors"), ("Multi-Model", "No Vendor Lock-in"), ("99.9%", "Uptime Target")])

    # Slides 5-12: Manufacturing UCs
    for i, uc in enumerate(USE_CASES):
        build_uc_slide(prs, 5 + i, TOTAL_SLIDES, uc["title"], uc["photo"],
                       uc["challenge"], uc["solution"], uc["results"],
                       uc["stack"], uc["governance"], uc["yc"],
                       uc["systems"], uc["users"], uc.get("how_it_works"))

    # Slides 13-28: Additional UCs
    for i, uc in enumerate(ADDITIONAL_UCS):
        build_uc_slide(prs, 13 + i, TOTAL_SLIDES, uc["title"], uc["photo"],
                       uc["challenge"], uc["solution"], uc["results"],
                       uc["stack"], uc["governance"], uc["yc"],
                       uc["systems"], uc["users"], uc.get("how_it_works"))

    # Slide 29: YC Competitive Landscape
    build_content_slide(prs, 29, TOTAL_SLIDES, "YC Competitive\nLandscape", "yc",
        "Threat Matrix by Vertical", [
            "Manufacturing (30 YC cos): MEDIUM threat — our MCP-native integration differentiates vs niche point solutions",
            "Healthcare (20+ YC cos): HIGH threat — our FHIR-native + compliance-first architecture differentiates",
            "Legal (14 YC cos): HIGH threat — full-practice automation vs single-workflow tools like Ironclad",
            "Real Estate (24 YC cos): LOW threat — integrated lease+lead+commission vs fragmented solutions",
            "Marketing (3 YC cos): LOW threat — underserved vertical; multi-channel unification opportunity",
            "AI Platforms (30+ YC cos): HIGH threat — vertical-specific agents on general infrastructure",
        ],
        "Strategic Implications", [
            "Key insight: Manufacturing and Marketing offer least contested entry points",
            "Healthcare and Legal offer highest ACV ($3-5K/mo) but well-funded competition",
            "Our edge: end-to-end vertical coverage vs single-feature YC startups",
            "MCP-native architecture provides 40% faster integration than competitors",
            "Multi-model approach (Claude + GPT-4o) eliminates vendor lock-in risk",
        ],
        bottom_items=[("120+", "YC Competitors Mapped"), ("6", "Verticals Analyzed"), ("MEDIUM", "Avg Threat Level"), ("MCP", "Our Differentiator")])

    # Slide 30: Revenue Model
    build_content_slide(prs, 30, TOTAL_SLIDES, "Revenue Model &\nUnit Economics", "revenue",
        "Revenue per Vertical (Monthly)", [
            "Manufacturing: $5,000-$10,000/mo — complex integration, high-value outcomes",
            "Healthcare: $3,000-$5,000/mo — HIPAA compliance overhead, multi-system",
            "Legal: $3,000-$5,000/mo — high attorney labor displacement value",
            "Real Estate: $2,000-$4,000/mo — high volume, lower complexity per transaction",
            "Marketing: $2,000-$4,000/mo — multi-channel, agency white-label premium",
            "Cost: API $200-500/client, Infra $40-50/client. Gross margin: 65-75% at scale",
        ],
        "Scaling Economics", [
            "Solo (1-5 clients): 40% margin, $15-30K MRR, founder-led",
            "Team (6-20 clients): 55% margin, $50-150K MRR, 3-5 person team",
            "Agency (21-50 clients): 65% margin, $150-400K MRR, self-service onboarding",
            "Enterprise (50+ clients): 72% margin, $400K+ MRR, platform economics",
        ],
        bottom_items=[("18 mo", "Avg Client Retention"), ("3 mo", "CAC Payback"), ("$72K", "Avg LTV"), ("6:1", "LTV/CAC Ratio")])

    # Slide 31: Roadmap
    build_content_slide(prs, 31, TOTAL_SLIDES, "Implementation Roadmap\n12-Month Plan", "roadmap",
        "Phase 1-2: Foundation & Expansion", [
            "Month 1-2 — Foundation & Pilots:",
            "• Select primary vertical (recommend: Manufacturing or Marketing)",
            "• Deploy core stack: Claude + MCP + 3 connectors",
            "• Onboard 3-5 pilots at $1.5K/mo for case study development",
            "• Target: 3 paying pilots, NPS >40, <5% error rate",
            "Month 3-4 — Expansion & Hardening:",
            "• Expand to 8-10 use cases, add 4-6 MCP connectors",
            "• Scale to 10-15 clients at $3-5K/mo standard pricing",
            "• Target: $50K MRR, 90% retention, SOC 2 readiness",
        ],
        "Phase 3-4: Cross-Vertical & Enterprise", [
            "Month 5-6 — Cross-Vertical & Self-Service:",
            "• Launch second vertical (Healthcare or Legal — higher ACV)",
            "• Self-service onboarding portal for connector setup",
            "• Scale to 20-30 clients across 2 verticals",
            "• Target: $120K MRR, self-service activation <48 hrs",
            "Month 7-12 — Enterprise & Scale:",
            "• Enterprise tier: dedicated agents, custom connectors, SLA",
            "• Add remaining verticals from template library",
            "• Scale to 50+ clients; target $400K+ MRR",
            "• Target: SOC 2 certified, 4 verticals, 50+ clients",
        ],
        bottom_items=[("8 wk", "Time to First Revenue"), ("$50K", "MRR at Month 4"), ("$120K", "MRR at Month 6"), ("$400K+", "MRR at Month 12")])

    # Slide 32: Engagement Model
    build_content_slide(prs, 32, TOTAL_SLIDES, "Engagement Model\nThree Tiers", "engagement",
        "Starter & Growth Tiers", [
            "STARTER — $2K/mo:",
            "• 1 vertical focus, up to 3 use cases deployed",
            "• Standard MCP connectors (pre-built)",
            "• Email support (24-hour SLA), shared infrastructure",
            "• Monthly performance reports, 99.5% uptime SLA",
            "",
            "GROWTH — $5K/mo (MOST POPULAR):",
            "• 2 verticals, up to 10 use cases deployed",
            "• Custom MCP connectors (2 included)",
            "• Priority support (4-hour SLA), dedicated compute",
            "• Custom dashboards, dedicated CSM, 99.9% uptime SLA",
        ],
        "Enterprise Tier", [
            "ENTERPRISE — $10K+/mo:",
            "• All verticals unlocked, unlimited use cases",
            "• Custom agent development",
            "• Dedicated support engineer (1-hour SLA)",
            "• Isolated infrastructure (single-tenant option)",
            "• Custom integrations + API access",
            "• Executive business reviews (quarterly)",
            "• 99.95% uptime SLA + penalty credits",
            "",
            "All tiers include: SOC 2 compliance, encryption at rest/transit,",
            "role-based access control, and full audit logging",
        ])

    # Slide 33: MCP Architecture
    build_content_slide(prs, 33, TOTAL_SLIDES, "MCP Integration\nArchitecture", "mcp",
        "Server Architecture", [
            "Protocol: JSON-RPC 2.0 over stdio or HTTP/SSE transport",
            "Tool registry: typed schemas with input validation and output formatting",
            "Resource exposure: structured data access with URI-based addressing",
            "Authentication: OAuth 2.0 / API key per connector, secrets in Vault",
            "Rate limiting: per-client quotas with graceful degradation",
            "Circuit breakers: automatic failover when downstream API degrades",
        ],
        "Connector Catalog (20+ Pre-Built)", [
            "ERP: SAP MES, SAP PM, SAP S/4HANA (RFC + OData)",
            "Healthcare: Epic FHIR R4, Cerner FHIR R4, Payer EDI 270/271",
            "Legal: Westlaw Edge API, LexisNexis, iManage Work 10",
            "CRM: Salesforce, HubSpot, Zoho (REST + Bulk API)",
            "Financial: QuickBooks Online, Stripe, Plaid",
            "Communication: Twilio SMS/Voice, SendGrid, Slack",
        ],
        bottom_items=[("20+", "Pre-Built Connectors"), ("<200ms", "Cached Response"), ("99.9%", "Connector Uptime"), ("OAuth 2.0", "Auth Standard")])

    # Slide 34: Orchestration Patterns
    build_content_slide(prs, 34, TOTAL_SLIDES, "Agent Orchestration\nPatterns", "orchestration",
        "Sequential & Parallel Patterns", [
            "Sequential Pipeline: Linear chain of specialist agents",
            "Example: Contract review: OCR → Clause Extraction → Risk Scoring → Summary",
            "✓ Simple, debuggable, deterministic ordering",
            "✗ Latency scales linearly, single point of failure",
            "",
            "Parallel Fan-Out: Orchestrator dispatches simultaneously, aggregates results",
            "Example: Lead scoring: Profile + Behavioral + Financial → Composite Score",
            "✓ Low latency, independent scaling",
            "✗ Complex aggregation logic, partial failure handling",
        ],
        "Hierarchical & Human-in-the-Loop", [
            "Hierarchical Delegation: Manager decomposes, delegates to sub-agents",
            "Example: SEO audit: Manager → Crawler + Content Analyzer + Competitor Tracker",
            "✓ Dynamic task decomposition, handles novel queries",
            "✗ Higher token cost, manager bottleneck",
            "",
            "Human-in-the-Loop: Agent processes to confidence threshold, then escalates",
            "Example: Insurance: Auto-verify 85% → Flag uncertain → Human review queue",
            "✓ High accuracy for edge cases, builds training data",
            "✗ Requires staffed review queue, variable latency",
        ])

    # Slide 35: Risk Mitigation
    build_content_slide(prs, 35, TOTAL_SLIDES, "Risk Mitigation &\nFailure Modes", "risk",
        "High-Impact Risks", [
            "Model Hallucination (MED likelihood / HIGH impact):",
            "• Output validation schemas, confidence <0.7 triggers human review",
            "• Citation verification for legal/medical outputs",
            "",
            "Data Breach / Leak (LOW / CRITICAL):",
            "• AES-256 encryption, PII redaction, network segmentation",
            "• GDPR 72-hr notification, forensic analysis protocol",
            "",
            "API Rate Limiting (HIGH / MEDIUM):",
            "• Request queuing, exponential backoff, Redis caching",
        ],
        "Operational & Strategic Risks", [
            "Model Drift (MED / MED):",
            "• KL divergence monitoring, auto-retrain at 5% drift",
            "• A/B holdout validation before promotion",
            "",
            "Vendor Lock-in (LOW / HIGH):",
            "• Multi-model: Claude primary, GPT-4o fallback",
            "• Abstraction layer enables 48hr model swap",
            "",
            "Compliance Violation (LOW / CRITICAL):",
            "• Policy-as-code via Open Policy Agent",
            "• Continuous monitoring, quarterly audit cycle",
        ])

    # Slide 36: Executive Summary
    build_content_slide(prs, 36, TOTAL_SLIDES, "Executive Summary\n& Next Steps", "summary",
        "Key Takeaways", [
            "24 production-ready use cases across 7 verticals with proven ROI models",
            "MCP-native architecture enables 40% faster integration than point-solution competitors",
            "YC competitive analysis: Manufacturing and Marketing are least contested entry points",
            "Healthcare and Legal offer highest ACV ($3-5K/mo) but face well-funded competition",
            "Break-even at 8 clients; path to $1M ARR at 21 clients within 12 months",
            "SOC 2, HIPAA, GDPR compliance framework designed in from day one",
            "Multi-model architecture eliminates vendor lock-in risk",
        ],
        "Immediate Next Steps", [
            "Week 1: Vertical selection workshop — align on primary market",
            "Week 2: Core stack deployment — Claude + MCP + 3 connectors in staging",
            "Week 3-4: Pilot recruitment — identify 3-5 design partners",
            "Week 5-6: MVP delivery — 3 core use cases deployed to pilots",
            "Week 7-8: Feedback loop — iterate on accuracy, UX, and integration",
            "Month 3: First paying clients with case study documentation",
        ],
        bottom_items=[("24", "Use Cases Ready"), ("7", "Verticals Covered"), ("40+", "YC Competitors Mapped"), ("8-12 wk", "Time to First Revenue")])

    # Save
    out_path = os.path.join(os.path.dirname(__file__), "AI-Engineering-Business-Use-Cases-Canva-Pro.pptx")
    prs.save(out_path)
    print(f"\n✅ Saved: {out_path}")
    print(f"   {TOTAL_SLIDES} slides | Canva-professional style | PeopleTech brand colors")
    print(f"\nTo upload to Canva: use import-design-from-url with a public link to this file")


if __name__ == "__main__":
    main()
