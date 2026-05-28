#!/usr/bin/env python3
"""
Add two things to AI-Engineering-Business-Use-Cases.pptx:
1. A new "Case Studies" slide after slide 31 (Customer Adoption Journey)
2. A "Software Engineering Add-On" box on the Engagement Model slide (slide 32, becomes 33 after insert)
Then update all page numbers.
"""

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import re
import copy
from lxml import etree

DECK_PATH = "AI-Engineering-Business-Use-Cases.pptx"
OUTPUT_PATH = "AI-Engineering-Business-Use-Cases.pptx"

SLIDE_W = 12192000
SLIDE_H = 6858000
FONT_NAME = "Calibri"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def no_border(shape):
    shape.line.fill.background()


def add_rect(slide, left, top, width, height, fill_hex=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    no_border(shape)
    if fill_hex:
        shape.fill.solid()
        shape.fill.fore_color.rgb = hex_to_rgb(fill_hex)
    else:
        shape.fill.background()
    return shape


def add_textbox(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)


def set_text(shape, text, size_emu, color_hex, bold=False, alignment=PP_ALIGN.LEFT):
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = alignment
    run = p.runs[0]
    run.font.name = FONT_NAME
    run.font.size = Emu(size_emu)
    run.font.color.rgb = hex_to_rgb(color_hex)
    run.font.bold = bold
    return tf


def add_para(tf, text, size_emu, color_hex, bold=False, alignment=PP_ALIGN.LEFT, space_before=0):
    from pptx.oxml.ns import qn
    p = tf.add_paragraph()
    p.text = text
    p.alignment = alignment
    if space_before:
        p.space_before = Emu(space_before)
    run = p.runs[0]
    run.font.name = FONT_NAME
    run.font.size = Emu(size_emu)
    run.font.color.rgb = hex_to_rgb(color_hex)
    run.font.bold = bold
    return p


# ---------------------------------------------------------------------------
# Build the Case Study slide
# ---------------------------------------------------------------------------
def build_case_study_slide(prs, slide):
    # Title bar
    title_bar = add_rect(slide, 0, 0, SLIDE_W, 685800, "#1F3B6E")
    tf = title_bar.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Real-World Case Studies | OpenHands in Production"
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0]
    run.font.name = FONT_NAME
    run.font.size = Emu(203200)
    run.font.color.rgb = hex_to_rgb("#FFFFFF")
    run.font.bold = True
    # Indent the title text
    from pptx.util import Pt as PtUtil
    tf.margin_left = Emu(457200)
    tf.margin_top = Emu(182880)

    # Three cards
    card_w = 3566160  # ~3.7 inches each
    card_gap = 182880
    card_left_start = 457200
    card_top = 914400
    card_h = 4572000

    cards = [
        {
            "title": "Go Microservice Upgrades",
            "header_color": "#166534",
            "company": "Mid-size SaaS (50+ microservices)",
            "challenge": "Go version upgrade across 50 services, 6-month manual estimate",
            "solution": "OpenHands agents processed services in parallel",
            "result": "~$3 per PR, completed in 2 weeks vs 6 months",
            "metric": "$150 total cost vs $180K manual estimate",
        },
        {
            "title": "Self-Healing Codebase",
            "header_color": "#1F3B6E",
            "company": "OpenHands project itself (dogfooding)",
            "challenge": "Hundreds of open issues, limited maintainer bandwidth",
            "solution": "GitHub Resolver auto-triages issues, writes fixes, opens PRs",
            "result": "37% of recent commits written by the AI agent",
            "metric": "37% autonomous commits in production",
        },
        {
            "title": "Enterprise Issue Resolution",
            "header_color": "#E31837",
            "company": "Fortune 500 engineering org (1000+ engineers)",
            "challenge": "200+ low-priority bugs backlogged, 4hr avg resolution time",
            "solution": "Batch agent deployment resolving issues in parallel",
            "result": "70% auto-resolved, MTTR dropped from 4hr to 15min",
            "metric": "70% issues auto-resolved, $2M saved annually",
        },
    ]

    for idx, card in enumerate(cards):
        cl = card_left_start + idx * (card_w + card_gap)

        # Card background
        bg = add_rect(slide, cl, card_top, card_w, card_h, "#F5F7FA")

        # Card header bar
        hdr = add_rect(slide, cl, card_top, card_w, 365760, card["header_color"])
        set_text(hdr, card["title"], 152400, "#FFFFFF", bold=True, alignment=PP_ALIGN.CENTER)
        hdr.text_frame.margin_top = Emu(54864)

        # Card body
        body_left = cl + 137160
        body_w = card_w - 274320
        body_top = card_top + 457200
        line_h = 127000

        labels = ["Company:", "Challenge:", "Solution:", "Result:"]
        values = [card["company"], card["challenge"], card["solution"], card["result"]]

        y_cursor = body_top
        for label, value in zip(labels, values):
            # Label
            lbl_box = add_textbox(slide, body_left, y_cursor, body_w, Emu(127000))
            set_text(lbl_box, label, 107950, "#1F3B6E", bold=True)
            y_cursor += 146304

            # Value
            val_box = add_textbox(slide, body_left, y_cursor, body_w, Emu(274320))
            set_text(val_box, value, 107950, "#1A1A1A")
            val_box.text_frame.word_wrap = True
            y_cursor += 310896

        # Metric highlight box
        metric_top = y_cursor + 91440
        metric_box = add_rect(slide, cl + 91440, metric_top, card_w - 182880, 457200, card["header_color"])
        tf = metric_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Emu(91440)
        tf.margin_top = Emu(45720)
        p = tf.paragraphs[0]
        p.text = "KEY METRIC"
        p.alignment = PP_ALIGN.CENTER
        run = p.runs[0]
        run.font.name = FONT_NAME
        run.font.size = Emu(91440)
        run.font.color.rgb = hex_to_rgb("#FFFFFF")
        run.font.bold = True

        p2 = tf.add_paragraph()
        p2.text = card["metric"]
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.runs[0]
        run2.font.name = FONT_NAME
        run2.font.size = Emu(114300)
        run2.font.color.rgb = hex_to_rgb("#FFFFFF")
        run2.font.bold = True

    # Bottom insight bar
    insight_top = 5486400
    insight_bar = add_rect(slide, 457200, insight_top, SLIDE_W - 914400, 548640, "#F5F7FA")
    tf = insight_bar.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(137160)
    tf.margin_top = Emu(91440)
    tf.margin_right = Emu(137160)
    p = tf.paragraphs[0]
    p.text = "These results are reproducible: OpenHands is open-source (74.6k\u2605), model-agnostic (100+ LLM providers), and deployable on-premise for air-gapped environments."
    p.alignment = PP_ALIGN.CENTER
    run = p.runs[0]
    run.font.name = FONT_NAME
    run.font.size = Emu(107950)
    run.font.color.rgb = hex_to_rgb("#1A1A1A")
    run.font.bold = False

    # Footer bar
    footer_bar = add_rect(slide, 0, 6263640, 12188952, 594360, "#0D3B5E")
    tf = footer_bar.text_frame
    tf.margin_left = Emu(457200)
    tf.margin_top = Emu(137160)
    p = tf.paragraphs[0]
    p.text = "AI Engineering Business Use Cases | Contact: sales@aiengineering.io"
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0]
    run.font.name = FONT_NAME
    run.font.size = Emu(91440)
    run.font.color.rgb = hex_to_rgb("#FFFFFF")
    run.font.bold = False

    # Page number placeholder (will be updated later)
    pn_box = add_textbox(slide, 11155680, 6263640, 914400, 594360)
    tf = pn_box.text_frame
    tf.margin_top = Emu(137160)
    p = tf.paragraphs[0]
    p.text = "0 / 0"
    p.alignment = PP_ALIGN.CENTER
    run = p.runs[0]
    run.font.name = FONT_NAME
    run.font.size = Emu(91440)
    run.font.color.rgb = hex_to_rgb("#FFFFFF")


# ---------------------------------------------------------------------------
# Add the Software Engineering add-on box to the engagement model slide
# ---------------------------------------------------------------------------
def add_sw_engineering_addon(slide):
    # The three tier cards end around y=4571520 (top 1097280 + height 3474720)
    # "All tiers include" text is at y=4754880
    # CTA button is at y=5212080
    # We need to place the add-on between "All tiers include" and the CTA

    addon_top = 5029200
    addon_left = 457200
    addon_w = 11247120
    addon_h = 1005840

    # Background box
    bg = add_rect(slide, addon_left, addon_top, addon_w, addon_h, "#F5F7FA")

    # Title line
    title_box = add_textbox(slide, addon_left + 137160, addon_top + 54864, addon_w - 274320, 228600)
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SOFTWARE ENGINEERING ADD-ON \u2014 +$3K/mo"
    p.alignment = PP_ALIGN.LEFT
    run = p.runs[0]
    run.font.name = FONT_NAME
    run.font.size = Emu(127000)
    run.font.color.rgb = hex_to_rgb("#1F3B6E")
    run.font.bold = True

    # Bullet items - laid out in two columns
    bullets_left = [
        "\u2713  AI code generation agents (UC21-24)",
        "\u2713  Automated issue resolution + PR generation",
        "\u2713  Test generation + code modernization",
    ]
    bullets_right = [
        "\u2713  DevOps incident auto-remediation",
        "\u2713  OpenHands-powered sandboxed execution",
    ]

    col1_left = addon_left + 137160
    col2_left = addon_left + addon_w // 2 + 91440
    bullet_top = addon_top + 310896
    line_spacing = 182880

    for i, txt in enumerate(bullets_left):
        tb = add_textbox(slide, col1_left, bullet_top + i * line_spacing, addon_w // 2 - 274320, 182880)
        set_text(tb, txt, 107950, "#1A1A1A")

    for i, txt in enumerate(bullets_right):
        tb = add_textbox(slide, col2_left, bullet_top + i * line_spacing, addon_w // 2 - 274320, 182880)
        set_text(tb, txt, 107950, "#1A1A1A")

    # "Available with" note in right column below bullets
    avail_box = add_textbox(slide, col2_left, bullet_top + 2 * line_spacing, addon_w // 2 - 274320, 182880)
    set_text(avail_box, "Available with Growth and Enterprise tiers", 107950, "#1F3B6E", bold=True)

    # Move the CTA button and footer down to make room
    # The CTA ("Schedule a Discovery Call") was at y=5212080
    # Footer was at y=6263640
    # We need to push things down or remove the CTA since we're tight on space
    # Actually, let's shift the CTA to be right after our add-on box
    for shape in slide.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text.strip()
            if txt == "Schedule a Discovery Call":
                shape.top = addon_top + addon_h + 91440  # just below addon


# ---------------------------------------------------------------------------
# Move slide to a specific position (0-indexed)
# ---------------------------------------------------------------------------
def move_slide(prs, old_idx, new_idx):
    """Move slide from old_idx to new_idx (0-based)."""
    sldIdLst = prs.slides._sldIdLst
    items = list(sldIdLst)
    el = items[old_idx]
    sldIdLst.remove(el)
    items = list(sldIdLst)
    if new_idx >= len(items):
        sldIdLst.append(el)
    else:
        items[new_idx].addprevious(el)


# ---------------------------------------------------------------------------
# Update all page numbers
# ---------------------------------------------------------------------------
def update_page_numbers(prs):
    total = len(prs.slides)
    for i, slide in enumerate(prs.slides):
        page_num = i + 1
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    txt = para.text.strip()
                    if re.match(r"^\d+ / \d+$", txt):
                        for run in para.runs:
                            run.text = f"{page_num} / {total}"
                        break


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    prs = Presentation(DECK_PATH)
    print(f"Loaded deck: {len(prs.slides)} slides")

    # --- Task 2: Add Case Study slide ---
    # Insert after slide 31 (0-indexed), which is "Customer Adoption Journey"
    # Add a blank slide at the end, build content, then move it
    blank_layout = prs.slide_layouts[0]  # only layout available
    cs_slide = prs.slides.add_slide(blank_layout)
    build_case_study_slide(prs, cs_slide)

    # The new slide is at the end (index len-1). Move it to position 32 (after slide 31)
    move_slide(prs, len(prs.slides) - 1, 32)
    print("Added Case Studies slide at position 33 (after Customer Adoption Journey)")

    # --- Task 1: Add Software Engineering add-on to Engagement Model slide ---
    # After the case study insert, the engagement model slide moved from 32 to 33
    engagement_slide = prs.slides[33]
    # Verify it's the right slide
    found = False
    for shape in engagement_slide.shapes:
        if shape.has_text_frame and "STARTER" in shape.text_frame.text:
            found = True
            break
    if not found:
        print("WARNING: Could not find Engagement Model slide at expected index 33, scanning...")
        for i, slide in enumerate(prs.slides):
            for shape in slide.shapes:
                if shape.has_text_frame and "STARTER" in shape.text_frame.text and "$2K" in shape.text_frame.text:
                    engagement_slide = slide
                    print(f"  Found at index {i}")
                    found = True
                    break
            if found:
                break

    add_sw_engineering_addon(engagement_slide)
    print("Added Software Engineering add-on to Engagement Model slide")

    # --- Update page numbers ---
    update_page_numbers(prs)
    print(f"Updated page numbers: {len(prs.slides)} total slides")

    prs.save(OUTPUT_PATH)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
