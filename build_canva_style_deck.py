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
                   systems=None, target_users=None):
    """Build a use case slide matching the reference design."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ── Left teal panel ─────────────────────────────────────────────────
    add_rect(slide, 0, 0, PANEL_W, SLIDE_H, TEAL)

    # Title — replace \n with space to avoid overlap, use single-line
    clean_title = title.replace("\n", " — ")
    add_text_box(slide, Inches(0.4), Inches(0.25), PANEL_W - Inches(0.7), Inches(0.6),
                 clean_title, font_size=24, color=WHITE, bold=True, font_name="Calibri")

    # Accent line under title
    add_rect(slide, Inches(0.4), Inches(0.85), Inches(2), Inches(0.03), DARK_NAVY)

    # ── CHALLENGE section ───────────────────────────────────────────────
    y = Inches(1.0)
    add_text_box(slide, Inches(0.4), y, Inches(1.5), Inches(0.25),
                 "CHALLENGE", font_size=9, color=DARK_NAVY, bold=True,
                 font_name="Calibri")
    y += Inches(0.22)
    col_w = Inches(3.8)
    challenge_text = "\n".join(f"• {l}" for l in challenge_lines[:3])
    add_text_box(slide, Inches(0.4), y, col_w, Inches(1.1),
                 challenge_text, font_size=8, color=DARK_NAVY, font_name="Calibri")

    # ── SOLUTION section ────────────────────────────────────────────────
    sol_x = Inches(4.4)
    add_text_box(slide, sol_x, Inches(1.0), Inches(1.5), Inches(0.25),
                 "SOLUTION", font_size=9, color=DARK_NAVY, bold=True,
                 font_name="Calibri")
    solution_text = "\n".join(f"• {l}" for l in solution_lines[:3])
    add_text_box(slide, sol_x, Inches(1.22), col_w, Inches(1.1),
                 solution_text, font_size=8, color=DARK_NAVY, font_name="Calibri")

    # ── Results stat boxes ──────────────────────────────────────────────
    stat_y = Inches(2.55)
    if results:
        for i, (num, label) in enumerate(results[:4]):
            stat_x = Inches(0.4) + Inches(i * 2.05)
            add_stat_box(slide, stat_x, stat_y, num, label)

    # ── GOVERNANCE / YC section ─────────────────────────────────────────
    gov_y = Inches(3.65)
    if governance_lines:
        add_text_box(slide, Inches(0.4), gov_y, Inches(3.5), Inches(0.22),
                     "GOVERNANCE & SECURITY", font_size=8, color=DARK_NAVY,
                     bold=True, font_name="Calibri")
        gov_text = "\n".join(f"• {l}" for l in governance_lines[:2])
        add_text_box(slide, Inches(0.4), gov_y + Inches(0.22), Inches(3.8), Inches(0.7),
                     gov_text, font_size=7, color=DARK_NAVY, font_name="Calibri")

    if yc_lines:
        add_text_box(slide, sol_x, gov_y, Inches(3.5), Inches(0.22),
                     "YC COMPETITIVE LANDSCAPE", font_size=8, color=DARK_NAVY,
                     bold=True, font_name="Calibri")
        yc_text = "\n".join(f"• {l}" for l in yc_lines[:3])
        add_text_box(slide, sol_x, gov_y + Inches(0.22), Inches(3.8), Inches(0.7),
                     yc_text, font_size=7, color=DARK_NAVY, font_name="Calibri")

    # ── Solution stack bar ──────────────────────────────────────────────
    stack_y = Inches(4.7)
    if stack_lines:
        add_rect(slide, Inches(0.3), stack_y, PANEL_W - Inches(0.5), Inches(0.85), DARK_NAVY)
        add_text_box(slide, Inches(0.4), stack_y + Inches(0.05), Inches(2), Inches(0.2),
                     "SOLUTION STACK", font_size=8, color=TEAL, bold=True,
                     font_name="Calibri")
        for i, (layer, detail) in enumerate(stack_lines[:4]):
            col_x = Inches(0.4) + Inches(i * 2.05)
            add_text_box(slide, col_x, stack_y + Inches(0.25), Inches(1.9), Inches(0.2),
                         layer, font_size=7, color=TEAL, bold=True, font_name="Calibri")
            add_text_box(slide, col_x, stack_y + Inches(0.45), Inches(1.9), Inches(0.35),
                         detail, font_size=7, color=WHITE, font_name="Calibri")

    # ── Systems + Target Users bar ──────────────────────────────────────
    bar_y = Inches(5.7)
    if systems:
        add_rect(slide, Inches(0.3), bar_y, Inches(4), Inches(0.35), ACCENT_TEAL)
        sys_text = "SYSTEMS: " + "  |  ".join(systems[:4])
        add_text_box(slide, Inches(0.4), bar_y + Inches(0.04), Inches(3.8), Inches(0.28),
                     sys_text, font_size=7, color=WHITE, bold=True, font_name="Calibri")

    if target_users:
        add_rect(slide, Inches(4.5), bar_y, Inches(4), Inches(0.35), DARK_TEAL)
        usr_text = "USERS: " + target_users
        add_text_box(slide, Inches(4.6), bar_y + Inches(0.04), Inches(3.8), Inches(0.28),
                     usr_text, font_size=7, color=WHITE, bold=True, font_name="Calibri")

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
    add_text_box(slide, Inches(0.4), Inches(0.25), PANEL_W - Inches(0.7), Inches(0.55),
                 clean_title, font_size=22, color=WHITE, bold=True, font_name="Calibri")
    add_rect(slide, Inches(0.4), Inches(0.8), Inches(2), Inches(0.03), DARK_NAVY)

    # Column 1
    add_text_box(slide, Inches(0.4), Inches(1.0), Inches(3.5), Inches(0.25),
                 col1_title, font_size=10, color=DARK_NAVY, bold=True, font_name="Calibri")
    c1_text = "\n".join(f"• {l}" for l in col1_lines)
    add_text_box(slide, Inches(0.4), Inches(1.25), Inches(3.8), Inches(3.8),
                 c1_text, font_size=8, color=DARK_NAVY, font_name="Calibri")

    # Column 2
    add_text_box(slide, Inches(4.4), Inches(1.0), Inches(3.5), Inches(0.25),
                 col2_title, font_size=10, color=DARK_NAVY, bold=True, font_name="Calibri")
    c2_text = "\n".join(f"• {l}" for l in col2_lines)
    add_text_box(slide, Inches(4.4), Inches(1.25), Inches(3.8), Inches(3.8),
                 c2_text, font_size=8, color=DARK_NAVY, font_name="Calibri")

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
        ],
        "solution": [
            "CNN-based real-time defect detection with edge-deployed YOLOv8 models",
            "Multi-camera fusion covering 360° component inspection at line speed",
            "Automated MES feedback loop: defect triggers line-stop within 200ms",
            "Continuous model retraining from operator-labeled corrections",
        ],
        "results": [("99.2%", "Detection Accuracy"), ("85%", "False Positive Reduction"),
                    ("$1.8M", "Annual Savings"), ("4-6 wk", "Deployment")],
        "governance": [
            "Model validation per IEC 62443 industrial cybersecurity standard",
            "Image data retention: 7 years for traceability, encrypted at rest",
            "Edge device certificate rotation every 90 days, firmware signed",
        ],
        "yc": ["Overview (W19, 40 emp) — general MFG AI",
               "Ocular AI (W24, 6 emp) — defect detection",
               "Bucket Robotics (S24, 5 emp) — automated inspection",
               "F4 Industries (S25) — factory floor CV"],
        "stack": [("EDGE / CAPTURE", "Industrial cameras\nEdge GPU (Jetson)"),
                  ("COMPUTE / AI", "YOLOv8\nCNN ensemble"),
                  ("INTEGRATION", "SAP MES connector\nMQTT broker"),
                  ("UX / DECISION", "Quality dashboard\nReal-time alerting")],
        "systems": ["SAP MES", "Camera Systems", "Edge GPU", "TF Serving"],
        "users": "Quality Engineers | Line Supervisors | Plant Managers",
    },
    {
        "title": "UC02 | Model & Variant\nConfirmation",
        "photo": "uc02",
        "challenge": [
            "3-5% assembly mismatch rate causing costly rework and warranty claims",
            "$500K average warranty cost per variant error across production batches",
            "Manual VIN validation bottleneck: 45-sec per unit slowing line throughput",
            "BOM version sync lag between engineering and production floor",
        ],
        "solution": [
            "Automated VIN/barcode scanning with real-time BOM cross-validation",
            "Variant mismatch alerting with instant operator HMI notification",
            "Multi-source BOM reconciliation: engineering ECO, production BOM, supplier ASN",
            "Historical mismatch pattern analysis for proactive fixture verification",
        ],
        "results": [("99.8%", "Variant Accuracy"), ("90%", "Mismatch Reduction"),
                    ("<2 sec", "Validation Time"), ("2-3 wk", "Deployment")],
        "governance": [
            "BOM version control: every scan logged with BOM revision hash",
            "Recall-grade traceability: component-to-VIN linkage retained 15 years",
            "Scanner calibration audit per ISO 15416 barcode quality standard",
        ],
        "yc": None,
        "stack": [("EDGE / CAPTURE", "Barcode readers\nRFID scanners"),
                  ("COMPUTE / AI", "BOM validation\nPattern matching"),
                  ("INTEGRATION", "SAP MES API\nECO sync service"),
                  ("UX / DECISION", "Operator HMI alerts\nShift reports")],
        "systems": ["SAP MES", "Barcode Scanners", "BOM Database", "ECO System"],
        "users": "Assembly Operators | Quality Auditors | Production Engineers",
    },
    {
        "title": "UC03 | Seating & Component\nValidation",
        "photo": "uc03",
        "challenge": [
            "Torque compliance failures undetected until end-of-line QA, causing rework",
            "Fitment issues cause line stops costing $15K/minute in lost throughput",
            "Manual torque verification logs incomplete, creating audit gaps",
            "Multi-variant seating configs increase error probability 3x",
        ],
        "solution": [
            "Vision-based fitment validation confirming correct component seating",
            "Torque tool integration: digital values streamed and validated against spec",
            "Real-time compliance dashboards aggregating torque, fitment, and sequence",
            "Automated non-conformance reports generated within seconds",
        ],
        "results": [("60%", "Integration Effort ↓"), ("0", "Undetected Failures"),
                    ("Real-time", "Compliance Monitor"), ("<1 sec", "Validation Latency")],
        "governance": [
            "Torque data retention per IATF 16949 automotive quality management",
            "Vision model validated against known-good reference images quarterly",
            "Calibration records linked to torque tool serial numbers",
        ],
        "yc": None,
        "stack": [("EDGE / CAPTURE", "Vision cameras\nTorque sensors"),
                  ("COMPUTE / AI", "Fitment ML models\nSpec validation"),
                  ("INTEGRATION", "MES + torque APIs\nSCADA interface"),
                  ("UX / DECISION", "Compliance dashboard\nNCR generator")],
        "systems": ["Torque Tools", "MES", "Vision Cameras", "SCADA"],
        "users": "Assembly Technicians | Quality Engineers | Process Engineers",
    },
    {
        "title": "UC04 | SOP Compliance\nMonitoring",
        "photo": "uc04",
        "challenge": [
            "12% SOP deviation rate undetected in manual observation audits",
            "Safety incidents from skipped steps (avg 3.2 incidents/quarter)",
            "Audit prep requires 80+ hours of manual video review per quarter",
            "Inconsistent adherence across shifts with no real-time correction",
        ],
        "solution": [
            "Pose estimation + activity recognition for real-time SOP adherence",
            "Step-sequence verification: alerts if operator skips critical steps",
            "Automated audit evidence with timestamped video clips per procedure",
            "Shift-level compliance scoring with trend analysis and coaching",
        ],
        "results": [("95%", "Compliance Detection"), ("70%", "Safety Deviation ↓"),
                    ("Hrs→Min", "Audit Prep Time"), ("Real-time", "Alert Delivery")],
        "governance": [
            "Worker privacy: pose data anonymized, no facial recognition, GDPR compliant",
            "Video retention limited to 30 days unless flagged for incident review",
            "Works council / union notification required in EU jurisdictions",
        ],
        "yc": None,
        "stack": [("EDGE / CAPTURE", "CCTV cameras\nEdge compute"),
                  ("COMPUTE / AI", "Pose estimation\nActivity recognition"),
                  ("INTEGRATION", "EHS platform API\nLMS webhook"),
                  ("UX / DECISION", "Supervisor alerts\nCoaching reports")],
        "systems": ["CCTV", "EHS Platform", "Training LMS", "MES"],
        "users": "Line Supervisors | EHS Managers | Training Coordinators",
    },
    {
        "title": "UC05 | Predictive Quality\nAnalytics",
        "photo": "uc05",
        "challenge": [
            "2-4% scrap rate from undetected process drift across 50+ variables",
            "Root cause analysis takes 48+ hours of manual cross-correlation",
            "Feature engineering bottleneck: data scientists spend 70% on data prep",
            "Siloed sensor data prevents cross-process correlation insights",
        ],
        "solution": [
            "Sensor fusion: unified time-series from temperature, pressure, vibration",
            "ML feature stores with automated feature engineering and selection",
            "Explainability dashboards showing SHAP values for each prediction",
            "Preemptive process adjustment recommendations before defects materialize",
        ],
        "results": [("40%", "Scrap Rate ↓"), ("48hr→15m", "Root Cause Analysis"),
                    ("Auto", "ML Pipeline Gen"), ("50+", "Cross-Variable Corr")],
        "governance": [
            "Feature store lineage: every feature traceable to raw sensor source",
            "Model explainability required per ISO 22989",
            "Sensor calibration validation, flagging drift > 2% from baseline",
        ],
        "yc": None,
        "stack": [("EDGE / CAPTURE", "IoT sensor array\nEdge aggregation"),
                  ("COMPUTE / AI", "Sensor fusion\nXGBoost + SHAP"),
                  ("INTEGRATION", "InfluxDB + feature store\nKafka streams"),
                  ("UX / DECISION", "Explainability dashboard\nAlert engine")],
        "systems": ["IoT Sensors", "InfluxDB", "Feature Store", "Data Lake"],
        "users": "Process Engineers | Data Scientists | Quality Managers",
    },
    {
        "title": "UC06 | Predictive\nMaintenance",
        "photo": "uc06",
        "challenge": [
            "Unplanned downtime costs $260K/hour avg across automotive manufacturing",
            "Reactive maintenance 3-5x costlier than predictive approaches",
            "Maintenance scheduling based on fixed intervals, not equipment health",
            "Vibration/acoustic anomaly patterns missed by periodic manual inspections",
        ],
        "solution": [
            "Vibration, acoustic, and temperature anomaly detection via LSTM autoencoders",
            "Equipment health scoring: 0-100 composite from multi-sensor fusion",
            "Auto-generated SAP PM work orders when health score drops below threshold",
            "Remaining useful life (RUL) prediction with confidence intervals",
        ],
        "results": [("45%", "Downtime ↓"), ("25%", "Maintenance Cost ↓"),
                    ("0-100", "Health Score"), ("40%", "Faster Implementation")],
        "governance": [
            "Sensor data Level 2 (Internal), encrypted in transit via TLS 1.3",
            "Maintenance decision audit trail: work order linked to model prediction",
            "False alarm rate monitored: target <5%, retrained if exceeded",
        ],
        "yc": ["Inviscid AI (W26, 2 emp) — physics-informed ML",
               "Palifer (S19, acquired) — predictive analytics",
               "InfluxData (W13, 210 emp) — time-series DB"],
        "stack": [("EDGE / CAPTURE", "Vibration sensors\nAcoustic sensors"),
                  ("COMPUTE / AI", "LSTM autoencoder\nRUL prediction"),
                  ("INTEGRATION", "SAP PM + IoT gateway\nMQTT broker"),
                  ("UX / DECISION", "Maintenance console\nHealth dashboard")],
        "systems": ["SAP PM", "IoT Gateways", "MQTT", "Edge Compute"],
        "users": "Maintenance Technicians | Reliability Engineers | Plant Managers",
    },
    {
        "title": "UC07 | Safety Monitoring\n& PPE Detection",
        "photo": "uc07",
        "challenge": [
            "PPE non-compliance observed in 8-12% of shift observations",
            "Restricted zone violations undetected until post-incident review",
            "Manual incident reports take 2+ hours, delaying corrective action",
            "OSHA recordable rate stagnant despite increased training investment",
        ],
        "solution": [
            "Real-time PPE detection: hard hat, vest, goggles, gloves via edge CV",
            "Geofenced zone intrusion alerts with <3 second supervisor notification",
            "AI-generated incident reports from video evidence with auto-classification",
            "Safety trend analytics: heatmaps by zone, shift, and role",
        ],
        "results": [("98%", "PPE Compliance"), ("100%", "Zone Violation Capture"),
                    ("80%", "Faster Documentation"), ("2-3 wk", "Deployment")],
        "governance": [
            "No facial recognition: PPE detection uses body-region segmentation only",
            "Alert data retained 1 year per OSHA 1904 recordkeeping",
            "Thermal camera data classified Level 2, not shared with HR systems",
        ],
        "yc": ["Protex AI (S21, 5 emp) — workplace safety CV"],
        "stack": [("EDGE / CAPTURE", "CCTV + thermal cams\nEdge GPU nodes"),
                  ("COMPUTE / AI", "Safety CV models\nZone geofencing"),
                  ("INTEGRATION", "EHS platform API\nSMS/push alerts"),
                  ("UX / DECISION", "Supervisor mobile app\nSafety heatmaps")],
        "systems": ["CCTV", "EHS Platform", "Alerting Systems", "Mobile MDM"],
        "users": "EHS Managers | Shift Supervisors | Safety Officers",
    },
    {
        "title": "UC08 | Digital Traceability\n& Recall",
        "photo": "uc08",
        "challenge": [
            "Recall investigation takes 2-4 weeks of manual component genealogy tracing",
            "Component genealogy gaps across tier 1-3 suppliers create liability exposure",
            "$35M average recall cost; scope overestimation adds 20-40%",
            "Paper-based lot tracking prevents real-time genealogy queries",
        ],
        "solution": [
            "Graph database (Neo4j) product genealogy: full component-to-vehicle lineage",
            "RFID + barcode tracking at every station creating immutable production record",
            "Automated recall scope analysis: pinpoint affected VINs in minutes",
            "Supplier integration: ASN data linked to production genealogy",
        ],
        "results": [("75%", "Faster Recall"), ("Full", "Production Genealogy"),
                    ("Auto", "Recall Scope Analysis"), ("Audit-Ready", "Compliance")],
        "governance": [
            "Traceability data retained 15+ years per NHTSA TREAD Act",
            "Immutable audit log: no genealogy deletion, append-only ledger",
            "Supplier data governed by mutual NDA, classification Level 3",
        ],
        "yc": ["Cognitio Labs (S23) — supply chain intelligence",
               "Autumn Labs (S24, 3 emp) — manufacturing traceability"],
        "stack": [("EDGE / CAPTURE", "RFID readers\nBarcode scanners"),
                  ("COMPUTE / AI", "Neo4j graph analytics\nLineage engine"),
                  ("INTEGRATION", "SAP + supplier APIs\nASN ingestion"),
                  ("UX / DECISION", "Traceability dashboard\nRecall analyzer")],
        "systems": ["SAP", "RFID", "Neo4j", "Supplier Portal"],
        "users": "Quality Directors | Compliance Officers | Supply Chain Managers",
    },
]

# ── Additional UC data (Healthcare, Legal, Real Estate, Marketing, SW Eng) ──

ADDITIONAL_UCS = [
    {"title": "UC09 | Patient Intake\nAutomation", "photo": "uc09",
     "challenge": ["15-minute avg intake time per patient creating bottlenecks", "23% form error rate from manual data entry causing billing issues", "Clinical staff spend 60% of time on admin vs patient care", "Multi-system data entry: same info keyed into EHR, billing, scheduling"],
     "solution": ["AI-powered form validation with real-time error detection", "Auto EHR population via FHIR R4 API: demographics, insurance, history", "Intelligent scheduling via Calendly + provider availability matching", "SMS/voice intake via Twilio for patients without portal access"],
     "results": [("3 min", "Intake (from 15)"), ("95%", "Form Accuracy"), ("40%", "Admin Time ↓"), ("$3-5K/mo", "Savings per Practice")],
     "governance": ["HIPAA BAA required; PHI encryption AES-256 at rest", "Audit logging per HITECH Act: every PHI access timestamped", "Patient consent management: opt-in/opt-out tracked per FHIR"],
     "yc": ["Understood Care (S24) — patient engagement", "HealthKey (W25) — health records", "Morf Health (S22) — care coordination"],
     "stack": [("EDGE / CAPTURE", "Web portal\nMobile + SMS"), ("COMPUTE / AI", "Claude NLP\nForm validation ML"), ("INTEGRATION", "FHIR + Twilio + Calendly\nEHR write-back"), ("UX / DECISION", "Patient dashboard\nStaff queue view")],
     "systems": ["Epic/Cerner EHR", "FHIR R4 API", "Calendly", "Twilio"], "users": "Front Desk Staff | Clinical Coordinators | Practice Managers"},
    {"title": "UC10 | Insurance\nVerification", "photo": "uc10",
     "challenge": ["30% claim denial rate from eligibility errors", "48-hour avg verification turnaround delays scheduling", "$25 cost per manual verification call, 12 min per call", "Prior auth requirements change frequently; staff miss updates"],
     "solution": ["Pre-appointment AI eligibility verification against payer feeds", "Automated prior auth submission with clinical documentation", "Denial prediction model: flags high-risk claims before submission", "Payer rule change monitoring: auto-updates workflows within 24hrs"],
     "results": [("85%", "First-Pass Approval"), ("5 min", "Verification (from 48hr)"), ("$5", "Cost per Verif (from $25)"), ("60%", "Denial Rate ↓")],
     "governance": ["EDI 270/271 compliance per HIPAA X12 standards", "Claims data Level 3 (Confidential), encrypted end-to-end", "Denial prediction audited for demographic bias quarterly"],
     "yc": ["Stream (S22) — claims processing", "Avallon AI (Sp25) — insurance verification", "Curacel (W22) — claims AI"],
     "stack": [("EDGE / CAPTURE", "Payer EDI feeds\nFax OCR ingestion"), ("COMPUTE / AI", "Claims ML models\nDenial prediction"), ("INTEGRATION", "Payer API + EHR\nClearinghouse EDI"), ("UX / DECISION", "Verification dashboard\nDenial analytics")],
     "systems": ["Payer EDI/APIs", "EHR", "Billing System", "Clearinghouse"], "users": "Billing Staff | Prior Auth Specialists | Revenue Cycle Managers"},
    {"title": "UC11 | HIPAA Compliance\nPortal", "photo": "uc11",
     "challenge": ["Manual audit prep consumes 120+ staff-hours per year", "PHI access logging gaps: 15% of access events untracked", "$1.5M avg HIPAA breach penalty; $6.3M for willful neglect", "Risk assessments annual but threats evolve continuously"],
     "solution": ["Automated audit trail aggregation from EHR, IAM, email, storage", "Real-time PHI access monitoring with anomaly detection", "Continuous compliance scoring with gap identification", "Breach risk scoring: quantified risk per system, updated daily"],
     "results": [("80%", "Audit Prep Time ↓"), ("100%", "PHI Access Logging"), ("Real-time", "Compliance Status"), ("Daily", "Breach Risk Scoring")],
     "governance": ["HIPAA Security Rule: admin, physical, tech safeguards automated", "HITECH Breach Notification: 60-day automated workflow", "BA management: BAA tracking, annual review, termination workflow"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Access log collectors\nSIEM feeds"), ("COMPUTE / AI", "Anomaly detection ML\nCompliance rules"), ("INTEGRATION", "IAM + EHR + email\nS3 audit storage"), ("UX / DECISION", "Compliance dashboard\nRisk heat map")],
     "systems": ["EHR", "IAM (Okta/Azure AD)", "S3 Storage", "SIEM"], "users": "Compliance Officers | HIPAA Privacy Officers | IT Security"},
    {"title": "UC12 | Contract Generation\n& Review", "photo": "uc12",
     "challenge": ["4-6 hours per contract draft for routine agreements", "Inconsistent clause usage creating enforceability risks", "$350/hr attorney time on routine document assembly", "15% of contracts sent with outdated clause libraries"],
     "solution": ["AI drafting from firm-specific templates + clause library", "Automated review: risk scoring per clause, deviation flagged", "Clause recommendation based on deal type and jurisdiction", "DocuSign integration for seamless review-sign workflow"],
     "results": [("45 min", "Draft Time (from 4-6h)"), ("90%", "Clause Consistency"), ("75%", "Attorney Time ↓"), ("$3-5K/mo", "Savings per Firm")],
     "governance": ["Attorney-client privilege: generated drafts access-controlled", "Clause library Git-backed, partner-approved changes only", "Output always marked draft; human sign-off required"],
     "yc": ["Ironclad (S15, 700 emp) — contract lifecycle", "Draftwise (S20, 50 emp) — contract drafting", "General Legal (W26) — AI legal assistant"],
     "stack": [("EDGE / CAPTURE", "Document upload\nOCR ingestion"), ("COMPUTE / AI", "Claude + templates\nRisk scoring"), ("INTEGRATION", "DocuSign + DMS APIs\nEmail integration"), ("UX / DECISION", "Attorney review portal\nClause library UI")],
     "systems": ["DocuSign", "iManage", "Gmail", "Billing"], "users": "Associates | Partners | Paralegals | Legal Ops"},
    {"title": "UC13 | Legal Research\nSummarization", "photo": "uc13",
     "challenge": ["8-12 hours per research task for junior associates", "Manual search covers only 60-70% of relevant case law", "65% of billable hours on research vs analysis", "Citation verification manual; hallucinated citations a known risk"],
     "solution": ["AI precedent search across Westlaw, LexisNexis, brief archives", "Structured summaries with jurisdiction-specific relevance scoring", "Citation-linked outputs: every claim traced to source", "Collaborative research workspace for shared briefs"],
     "results": [("2 hrs", "Research (from 8-12)"), ("95%", "Precedent Coverage"), ("70%", "Junior Workload ↓"), ("Verified", "Citation Accuracy")],
     "governance": ["Every citation validated against source database", "Research memos marked AI-assisted per bar disclosure rules", "No client data to external models; on-premise RAG for privileged"],
     "yc": ["Vector Legal (W26) — AI legal research", "Docsum (S23) — document summarization"],
     "stack": [("EDGE / CAPTURE", "Legal DB connectors\nBrief bank indexer"), ("COMPUTE / AI", "RAG pipeline\nClaude reasoning"), ("INTEGRATION", "Westlaw + LexisNexis\nDMS search"), ("UX / DECISION", "Brief generator\nCitation viewer")],
     "systems": ["Westlaw", "LexisNexis", "iManage DMS", "Brief Bank"], "users": "Junior Associates | Senior Associates | Research Librarians"},
    {"title": "UC14 | Legal Billing\nAutomation", "photo": "uc14",
     "challenge": ["15-20% revenue leakage from unbilled time entries", "Manual timesheet reconciliation: 5+ hrs/week per coordinator", "30-day avg invoice cycle from capture to payment", "8% of invoices rejected for LEDES/UTBMS formatting errors"],
     "solution": ["AI activity capture from calendar, email, document edits", "Auto timesheet generation with matter-code assignment", "LEDES-compliant invoice automation with client rate cards", "Expense auto-categorization from receipts and travel"],
     "results": [("95%", "Billable Capture"), ("15%", "Revenue Recovery"), ("5 days", "Invoice Cycle (from 30)"), ("Auto", "Expense Categorization")],
     "governance": ["Billing data Level 3, SOX-adjacent controls for >$10M firms", "Time entry audit: AI suggestion vs attorney-approved entry", "LEDES/UTBMS validation before submission"],
     "yc": ["JustPaid (W23, 20 emp) — invoice automation", "Peakflo (W22, 45 emp) — accounts receivable"],
     "stack": [("EDGE / CAPTURE", "Email/calendar monitors\nDoc edit tracking"), ("COMPUTE / AI", "Activity classification\nNarrative generation"), ("INTEGRATION", "QB + Stripe APIs\nLEDES formatter"), ("UX / DECISION", "Billing dashboard\nClient portal")],
     "systems": ["QuickBooks", "Gmail", "Calendar", "Stripe"], "users": "Associates | Billing Coordinators | Managing Partners"},
    {"title": "UC15 | Lease Document\nGeneration", "photo": "uc15",
     "challenge": ["2-3 hours per lease with manual clause selection", "$45K avg litigation cost per lease dispute", "Inconsistent terms across agents creating liability", "Jurisdiction requirements missed in 6% of leases"],
     "solution": ["AI lease generation pulling property/tenant data from CRM", "Jurisdiction-aware clause library by state/county", "E-signature via DocuSign with tenant identity verification", "Lease comparison tool: highlights deviations from standard"],
     "results": [("15 min", "Generation (from 2-3h)"), ("98%", "Clause Accuracy"), ("0", "Jurisdiction Errors"), ("$2-4K/mo", "Savings per Brokerage")],
     "governance": ["PII handling: tenant SSN/income encrypted AES-256, purged after signing", "State-specific rules updated quarterly from legal database", "Fair housing compliance: AI terms audited for discriminatory language"],
     "yc": ["Clau (S20, 90 emp) — real estate AI", "Homeflow (W23) — property management", "Goldbridge (F25) — RE technology"],
     "stack": [("EDGE / CAPTURE", "CRM data feed\nProperty DB"), ("COMPUTE / AI", "Claude + lease templates\nClause selector"), ("INTEGRATION", "DocuSign + CRM APIs\nCounty lookup"), ("UX / DECISION", "Agent portal\nTenant self-service")],
     "systems": ["CRM", "DocuSign", "Zillow API", "County Records"], "users": "Leasing Agents | Property Managers | Broker Compliance"},
    {"title": "UC16 | Lead Scoring &\nSmart Routing", "photo": "uc16",
     "challenge": ["40% of leads receive first response >4 hours after inquiry", "Unqualified leads consume 60% of agent follow-up time", "Manual CRM entry: 45 min/day on data entry vs engagement", "Lead source attribution broken: marketing ROI unmeasurable"],
     "solution": ["AI lead scoring using interest signals and financial readiness", "Smart routing to best-fit agent by expertise and geography", "Auto CRM enrichment from Zillow views, ad clicks, emails", "Campaign trigger automation for high-score leads"],
     "results": [("15 min", "Response (from 4 hrs)"), ("35%", "Conversion Lift"), ("50%", "Unqualified ↓"), ("Auto", "CRM Enrichment")],
     "governance": ["Fair housing: scoring audited for demographic bias quarterly", "Lead data: 2yr active, 5yr archived per broker compliance", "CAN-SPAM and TCPA compliance for automated outreach"],
     "yc": ["PropReturns (S21, 40 emp) — RE analytics", "Smart Alto (W17) — lead qualification"],
     "stack": [("EDGE / CAPTURE", "Lead capture forms\nZillow API"), ("COMPUTE / AI", "XGBoost scoring\nBehavioral ML"), ("INTEGRATION", "CRM + Meta + email\nZapier triggers"), ("UX / DECISION", "Agent assignment UI\nLead pipeline view")],
     "systems": ["CRM", "Zillow", "Meta Ads", "Email/SMS"], "users": "Listing Agents | Buyer Agents | Team Leads | Marketing"},
    {"title": "UC17 | Commission Analytics\n& Reporting", "photo": "uc17",
     "challenge": ["Month-end calculations take 3+ days of manual spreadsheet work", "12% of agents dispute commissions monthly", "No real-time visibility into earned vs pending vs paid", "Split commission scenarios miscalculated 8% of the time"],
     "solution": ["Auto commission engine with configurable splits, tiers, bonuses", "Deal attribution: listing agreements linked to closing and payment", "Real-time financial dashboards for agents and management", "Agent performance ranking with trend analysis"],
     "results": [("Same-day", "Commission Reports"), ("99.5%", "Calculation Accuracy"), ("80%", "Dispute Reduction"), ("Live", "Performance Ranking")],
     "governance": ["Financial data Level 3, SOX-adjacent controls for >$10M revenue", "Commission audit trail: every step logged with rule version", "1099 generation from commission data, IRS-compliant"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Transaction feeds\nMLS closing data"), ("COMPUTE / AI", "Commission rules\nSplit calculator"), ("INTEGRATION", "QB + Stripe + CRM\n1099 generator"), ("UX / DECISION", "Financial dashboard\nAgent leaderboard")],
     "systems": ["CRM", "QuickBooks", "Stripe", "MLS"], "users": "Agents | Brokerage Managers | Accounting | Team Leads"},
    {"title": "UC18 | SEO Audit &\nOptimization", "photo": "uc18",
     "challenge": ["Manual SEO audits take 20+ hours per client site", "Recommendations outdated by publish time: 2-week lag", "No competitive position tracking: flying blind on SERPs", "Technical SEO issues missed without engineering support"],
     "solution": ["Automated crawl with technical SEO scoring (Core Web Vitals)", "AI content recommendations: keyword gaps, topical authority", "Weekly competitive position monitoring with SERP tracking", "Prioritized fix list with estimated traffic impact"],
     "results": [("2 hrs", "Audit (from 20+)"), ("Per-page", "Recommendations"), ("Weekly", "Competitive Tracking"), ("$2-4K/mo", "Revenue per Client")],
     "governance": ["Crawl rate limiting: respects robots.txt, max 5 req/sec", "Competitor data from public SERPs only, no gated scraping", "Client data isolated: multi-tenant with per-client encryption"],
     "yc": ["Positional (S21, acquired) — SEO tooling"],
     "stack": [("EDGE / CAPTURE", "Web crawler\nSitemap parser"), ("COMPUTE / AI", "NLP content analysis\nKeyword gap ML"), ("INTEGRATION", "GA + Search Console\nSERP tracker"), ("UX / DECISION", "SEO dashboard\nClient report gen")],
     "systems": ["Google Analytics", "Search Console", "WordPress", "Screaming Frog"], "users": "SEO Specialists | Content Strategists | Agency Managers"},
    {"title": "UC19 | Campaign Performance\nDashboard", "photo": "uc19",
     "challenge": ["8+ hrs/week per account manager on manual reporting", "Inconsistent metrics: each platform defines conversion differently", "Client reporting delays: 3-5 days from period end", "Anomaly detection manual: budget overspend caught late"],
     "solution": ["Automated ingestion from Google Ads, Meta, LinkedIn, TikTok", "Unified metric normalization: standardized attribution model", "AI insight generation: auto-surfaces trends and anomalies", "White-label client dashboards with auto report generation"],
     "results": [("Real-time", "Unified Dashboard"), ("90%", "Reporting Time ↓"), ("Auto", "Client Reports"), ("Instant", "Anomaly Detection")],
     "governance": ["Platform API usage within rate limits and ToS", "Client ad spend data Level 2, segregated per client", "GDPR: no PII in analytics; all data aggregated"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Platform API connectors\nETL pipelines"), ("COMPUTE / AI", "Analytics aggregation\nAnomaly detection"), ("INTEGRATION", "Multi-platform APIs\nData warehouse"), ("UX / DECISION", "Client dashboard\nReport PDF generator")],
     "systems": ["Google Analytics", "Meta Ads API", "LinkedIn Ads", "Buffer"], "users": "Account Managers | Media Buyers | Agency Directors"},
    {"title": "UC20 | Content Pipeline\nAutomation", "photo": "uc20",
     "challenge": ["5-day avg content cycle from brief to publish", "Approval bottlenecks: content sits 2+ days in review queues", "Inconsistent brand voice across blog, social, email, ad copy", "Manual A/B testing: 3+ hrs per test limiting experimentation"],
     "solution": ["AI content generation from structured briefs + brand voice model", "Automated approval workflows with parallel reviewer routing", "Multi-channel publishing: one brief → blog, social, email, ad", "Auto A/B variant generation with performance-based selection"],
     "results": [("1 day", "Cycle (from 5 days)"), ("80%", "Faster Approvals"), ("Consistent", "Brand Voice"), ("Auto", "A/B Variants")],
     "governance": ["Brand guidelines enforced via style model", "Content audit trail: every generation and approval timestamped", "FTC compliance: AI-generated content flagged for disclosure"],
     "yc": None,
     "stack": [("EDGE / CAPTURE", "Content brief input\nAsset library"), ("COMPUTE / AI", "Claude generation\nBrand voice model"), ("INTEGRATION", "CMS + social APIs\nEmail platform"), ("UX / DECISION", "Editorial dashboard\nPublishing scheduler")],
     "systems": ["WordPress", "Buffer", "CMS", "Slack"], "users": "Content Managers | Copywriters | Brand Managers"},
    {"title": "UC21 | AI-Powered Code\nGeneration", "photo": "uc21",
     "challenge": ["30-40% of engineering hours on routine bug fixes", "PR review bottleneck: avg 2-day cycle time from issue to merge", "Legacy codebases accumulate 200+ open issues with no bandwidth", "Junior onboarding takes 3-6 months before meaningful contributions"],
     "solution": ["OpenHands autonomous agents: analyze issues, write fixes, open PRs", "Sandboxed execution: every agent in isolated Docker container", "Event-sourced architecture: deterministic replay, full audit trail", "Self-improving: 37% of agent's own commits written by agent"],
     "results": [("77.6%", "SWE-Bench Resolve"), ("~$3", "Cost per PR"), ("37%", "Self-Written Commits"), ("2-4 wk", "Deployment")],
     "governance": ["All AI code marked AI-assisted; human approval before merge", "Sandboxed execution prevents host access; secrets masked", "SecurityAnalyzer rates tool calls LOW/MEDIUM/HIGH risk"],
     "yc": ["OpenHands (74.6k★) — open-source autonomous dev", "Devin/Cognition ($175M) — commercial AI developer", "Factory AI (S24) — autonomous code agents"],
     "stack": [("AGENT / SDK", "OpenHands SDK\nCodeAct agent"), ("COMPUTE / AI", "Claude 4.5 Opus\nGPT-5.2 Codex"), ("INTEGRATION", "GitHub Actions\nMCP connectors"), ("UX / DECISION", "PR review portal\nAgent dashboard")],
     "systems": ["GitHub", "GitLab", "Docker", "CI/CD"], "users": "Engineering Leads | DevOps Managers | VP Engineering"},
    {"title": "UC22 | Automated Test\nGeneration", "photo": "uc22",
     "challenge": ["Legacy codebases average 35% test coverage", "15% of deployments cause incidents in first 24 hours", "Test maintenance: 20% of suites break with each refactor", "Security testing requires specialized expertise most lack"],
     "solution": ["AI agents generate comprehensive test suites (SWT-Bench validated)", "Multi-agent fan-out: parallel generation across unit/integration/E2E", "Automated test maintenance: detect broken tests, auto-fix after refactor", "Security-focused: OWASP Top 10 coverage with pen-test scenarios"],
     "results": [("35→85%", "Test Coverage ↑"), ("60%", "Fewer Prod Regressions"), ("10x", "Test Gen Speed"), ("1-2 wk", "Setup")],
     "governance": ["Generated tests reviewed by senior engineer before CI", "No production PII in fixtures; synthetic data generation", "Coverage metrics: minimum 80% threshold enforced via CI gates"],
     "yc": ["QA Wolf (W19, 80 emp) — E2E testing as service", "Carbonate (S23) — AI test generation", "Momentic (S23) — autonomous E2E testing"],
     "stack": [("AGENT / SDK", "OpenHands agents\nSWT-Bench model"), ("COMPUTE / AI", "Claude reasoning\nCode analysis"), ("INTEGRATION", "CI/CD hooks\nCoverage APIs"), ("UX / DECISION", "Coverage dashboard\nRisk heatmap")],
     "systems": ["GitHub", "Jest/Pytest", "CI/CD", "SAST Tools"], "users": "QA Engineers | Engineering Managers | Security Teams"},
    {"title": "UC23 | Code Modernization\n& Tech Debt", "photo": "uc23",
     "challenge": ["40% of dev time navigating and working around legacy code", "Framework migrations (Angular→React) take 6-18 months manually", "Average enterprise has 200+ outdated packages deferred due to risk", "Monolith decomposition requires deep knowledge often lost to attrition"],
     "solution": ["AI multi-repo dependency upgrades at ~$3 per PR across hundreds of services", "Autonomous framework migration: generates idiomatic code in target framework", "Monolith decomposition: identifies service boundaries, extracts and tests", "Greenfield scaffolding: commit0-validated development from specs"],
     "results": [("~$3", "Cost per Migration PR"), ("80%", "Tech Debt ↓"), ("6→1 mo", "Migration Timeline"), ("100+", "Repos per Sprint")],
     "governance": ["All migration PRs include automated regression test results", "Security patches auto-merged; major versions require human approval", "ADRs auto-generated for each decomposition step"],
     "yc": ["Grit.io (W22) — automated code migrations", "Moderne (S21, 50 emp) — large-scale refactoring", "Sourcegraph Cody (S14, 300+) — code intelligence"],
     "stack": [("ANALYSIS", "Dependency graph\nDead code scan"), ("COMPUTE / AI", "Claude Opus\nMulti-agent chain"), ("INTEGRATION", "Package registries\nCI validation"), ("UX / DECISION", "Migration tracker\nRisk scoring")],
     "systems": ["GitHub", "npm/pip/maven", "Docker", "Terraform"], "users": "Platform Engineers | Tech Leads | CTOs"},
    {"title": "UC24 | DevOps & Incident\nResponse", "photo": "uc24",
     "challenge": ["MTTR averages 4+ hours for production incidents", "On-call spends 60% of incident time on log correlation", "CI/CD pipeline failures block 15-20% of deployments", "Terraform state diverges from reality across 50+ microservices"],
     "solution": ["AI agents analyze logs, pinpoint root causes, generate fix PRs", "Automated CI/CD debugging: reads build logs, identifies failures, pushes fixes", "IaC auto-remediation: drift detection → Terraform PR → validated apply", "Runbook automation: executes playbooks with human escalation"],
     "results": [("4hr→15m", "MTTR"), ("70%", "Auto-Resolved"), ("85%", "CI/CD Fix Rate"), ("24/7", "Always-On Coverage")],
     "governance": ["Production access read-only for agents; writes require approval", "Every agent action logged with timestamp and rationale", "Blast radius controls: auto-remediation limited to non-critical"],
     "yc": ["Rootly (S21, 45 emp) — incident management", "incident.io (S21, 120 emp) — incident response", "Firehydrant (W20, 90 emp) — incident management"],
     "stack": [("OBSERVE", "DataDog logs\nPagerDuty alerts"), ("COMPUTE / AI", "Log analysis LLM\nRoot cause agent"), ("INTEGRATION", "Terraform API\nK8s API"), ("UX / DECISION", "Incident dashboard\nRunbook executor")],
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
                       uc["systems"], uc["users"])

    # Slides 13-28: Additional UCs
    for i, uc in enumerate(ADDITIONAL_UCS):
        build_uc_slide(prs, 13 + i, TOTAL_SLIDES, uc["title"], uc["photo"],
                       uc["challenge"], uc["solution"], uc["results"],
                       uc["stack"], uc["governance"], uc["yc"],
                       uc["systems"], uc["users"])

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
