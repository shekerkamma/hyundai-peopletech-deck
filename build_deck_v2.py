#!/usr/bin/env python3
"""
PeopleTech AI Engineering Team — Hyundai Pitch Deck v2
Template-matched to Hyundai_PeopleTech_AI_Plant_Operations.pptx reference deck
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import copy

# ── Design tokens (extracted from reference deck) ──────────────────────
SLIDE_W = 12191695
SLIDE_H = 6858000
MARGIN  = 457200
HDR_H   = 822960
FTR_Y   = 6400800
FTR_H   = 457200

# Colors
BG_BODY    = RGBColor(0xF1, 0xF5, 0xF9)  # light gray body
BG_DARK    = RGBColor(0x0F, 0x17, 0x2A)  # dark navy header/footer (darker than ref)
BG_HDR     = RGBColor(0x14, 0x1E, 0x38)  # header bar
BG_CARD    = RGBColor(0x1E, 0x29, 0x3B)  # card bg (dark)
BG_CARD_LT = RGBColor(0xF8, 0xFA, 0xFC)  # card bg (light)
BG_FTR     = RGBColor(0x0F, 0x17, 0x2A)  # footer

# Text colors
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
SLATE_LT   = RGBColor(0xCB, 0xD5, 0xE1)
SLATE_MD   = RGBColor(0x94, 0xA3, 0xB8)
SLATE      = RGBColor(0x64, 0x74, 0x8B)
GRAY_DK    = RGBColor(0x47, 0x55, 0x69)
NAVY_DK    = RGBColor(0x1A, 0x27, 0x54)
TEXT_BODY   = RGBColor(0x1E, 0x29, 0x3B)

# Accents
RED        = RGBColor(0xDC, 0x26, 0x26)
GREEN      = RGBColor(0x14, 0xA0, 0x85)
AMBER      = RGBColor(0xD9, 0x77, 0x06)
PURPLE     = RGBColor(0x7C, 0x3A, 0xED)
TEAL       = RGBColor(0x0E, 0x7B, 0x6A)
CYAN       = RGBColor(0x00, 0xAA, 0xD4)
BLUE       = RGBColor(0x25, 0x63, 0xEB)
ORANGE     = RGBColor(0xFF, 0x6B, 0x35)

# KPI card accent colors (matching ref deck)
KPI_GREEN  = RGBColor(0x0D, 0x8A, 0x72)
KPI_BLUE   = RGBColor(0x1D, 0x4E, 0xD8)
KPI_PURPLE = RGBColor(0x6D, 0x28, 0xD9)
KPI_AMBER  = RGBColor(0xB4, 0x5A, 0x09)
KPI_RED    = RGBColor(0xB9, 0x1C, 0x1C)

FONT = "Calibri"
TOTAL_SLIDES = 20

# ── Helper functions ────────────────────────────────────────────────────

def add_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text(slide, left, top, width, height, text, size, color,
             bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, font=FONT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    txBox.fill.background()
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    r = p.runs[0]
    r.font.size = Pt(size / 12700) if size > 1000 else Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.name = font
    tf.auto_size = None
    try:
        tf.paragraphs[0].space_before = Pt(0)
        tf.paragraphs[0].space_after = Pt(0)
    except:
        pass
    return txBox

def add_text_emu(slide, left, top, width, height, text, size_emu, color,
                 bold=False, align=PP_ALIGN.LEFT, font=FONT):
    """size_emu is font size in EMU (e.g., 152400 = 12pt)"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    txBox.fill.background()
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    r = p.runs[0]
    r.font.size = size_emu
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.name = font
    return txBox

def add_multiline(slide, left, top, width, height, lines, size_emu, color, font=FONT, bold=False, bullet=""):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    txBox.fill.background()
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"{bullet}{line}" if bullet else line
        p.space_before = Pt(2)
        p.space_after = Pt(2)
        r = p.runs[0]
        r.font.size = size_emu
        r.font.color.rgb = color
        r.font.name = font
        r.font.bold = bold
    return txBox

def add_header_bar(slide, tag_text, title_text, subtitle_text, tag_color=WHITE):
    """Standard header bar matching reference deck"""
    add_rect(slide, 0, 0, SLIDE_W, HDR_H, BG_HDR)
    add_text_emu(slide, MARGIN, 0, 2286000, HDR_H, tag_text, 127000, tag_color, bold=True)
    add_text_emu(slide, 2743200, 0, 6400800, HDR_H, title_text, 279400, WHITE, bold=True)
    add_text_emu(slide, 9144000, 0, 2560320, HDR_H, subtitle_text, 127000, SLATE_LT)

def add_footer(slide, slide_num):
    add_rect(slide, 0, FTR_Y, SLIDE_W, FTR_H, BG_FTR)
    add_text_emu(slide, MARGIN, FTR_Y + 45720, 7315200, 365760,
                 'PeopleTech · AI Engineering Team', 114300, SLATE_LT, bold=True)
    add_text_emu(slide, 7772400, FTR_Y + 45720, 3931920, 365760,
                 f'{slide_num:02d} / {TOTAL_SLIDES} · CONFIDENTIAL', 114300, SLATE_MD,
                 align=PP_ALIGN.RIGHT)

def add_body_bg(slide):
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, BG_BODY)

def card_with_accent(slide, left, top, width, height, accent_color, bg=BG_CARD_LT, accent_w=54864):
    add_rect(slide, left, top, width, height, bg)
    add_rect(slide, left, top, accent_w, height, accent_color)

def kpi_card(slide, left, top, value, label, bg_color):
    add_rect(slide, left, top, 2286000, 868680, bg_color)
    add_text_emu(slide, left, top + 91440, 2286000, 502920, value, 304800, WHITE, bold=True,
                 align=PP_ALIGN.CENTER)
    add_text_emu(slide, left, top + 594360, 2286000, 274320, label, 114300, WHITE,
                 align=PP_ALIGN.CENTER)

def use_case_slide(slide, uc_num, title, tech_subtitle, accent_color,
                   challenge_text, solution_text, capabilities,
                   kpis, systems_text, target_users,
                   arch_cols, recommended_start=None, slide_num=1):
    """Build a full use-case slide matching reference template exactly"""
    add_body_bg(slide)
    
    # Header bar
    add_rect(slide, 0, 0, SLIDE_W, HDR_H, accent_color)
    add_text_emu(slide, MARGIN, 0, 2286000, HDR_H, f'USE CASE {uc_num:02d}', 139700, WHITE, bold=True)
    add_text_emu(slide, 2743200, 0, 6400800, HDR_H, title, 279400, WHITE, bold=True)
    add_text_emu(slide, 9144000, 0, 2560320, HDR_H, tech_subtitle, 139700, WHITE)
    
    # LEFT COLUMN
    left_x = MARGIN
    left_w = 6400800
    inner_x = left_x + 164592  # 621792
    inner_w = 6172200
    
    # Challenge box
    cy = 1005840
    ch = 1097280
    card_with_accent(slide, left_x, cy, left_w, ch, RED)
    add_text_emu(slide, inner_x, cy + 91440, inner_w, 228600, 'CHALLENGE', 114300, RED, bold=True)
    add_text_emu(slide, inner_x, cy + 365760, inner_w, 685800, challenge_text, 139700, TEXT_BODY)
    
    # Solution box
    sy = 2240280
    sh = 1097280
    card_with_accent(slide, left_x, sy, left_w, sh, accent_color)
    add_text_emu(slide, inner_x, sy + 91440, inner_w, 228600, 'SOLUTION', 114300, accent_color, bold=True)
    add_text_emu(slide, inner_x, sy + 365760, inner_w, 685800, solution_text, 139700, TEXT_BODY)
    
    # Capabilities box
    capy = 3474720
    caph = 1645920
    card_with_accent(slide, left_x, capy, left_w, caph, accent_color)
    add_text_emu(slide, inner_x, capy + 91440, inner_w, 228600, 'CAPABILITIES', 114300, accent_color, bold=True)
    add_multiline(slide, inner_x, capy + 365760, inner_w, 1234440, capabilities, 127000, TEXT_BODY, bullet="•  ")
    
    # RIGHT COLUMN
    rx = 7040880
    rw = 4663440
    
    # Business value header
    add_text_emu(slide, rx, 1005840, rw, 228600, 'BUSINESS VALUE', 114300, SLATE, bold=True)
    
    # KPI cards (2x2)
    kpi_colors = [KPI_GREEN, KPI_BLUE, KPI_PURPLE, KPI_AMBER]
    positions = [(rx, 1280160), (rx + 2377440, 1280160), (rx, 2240280), (rx + 2377440, 2240280)]
    for i, (val, lbl) in enumerate(kpis[:4]):
        kpi_card(slide, positions[i][0], positions[i][1], val, lbl, kpi_colors[i % 4])
    
    # Systems integrated
    si_y = 3246120
    si_h = 777240
    card_with_accent(slide, rx, si_y, rw, si_h, SLATE)
    add_text_emu(slide, rx + 164592, si_y + 73152, rw - 228600, 201168, 'SYSTEMS INTEGRATED', 101600, SLATE, bold=True)
    add_text_emu(slide, rx + 164592, si_y + 292608, rw - 228600, 457200, systems_text, 127000, TEXT_BODY)
    
    # Target users
    tu_y = 4114800
    tu_h = 594360
    card_with_accent(slide, rx, tu_y, rw, tu_h, SLATE)
    add_text_emu(slide, rx + 164592, tu_y + 73152, rw - 228600, 201168, 'TARGET USERS', 101600, SLATE, bold=True)
    add_text_emu(slide, rx + 164592, tu_y + 292608, rw - 228600, 274320, target_users, 127000, TEXT_BODY)
    
    # Recommended start (optional)
    if recommended_start:
        rs_y = 4800600
        rs_h = 411480
        card_with_accent(slide, rx, rs_y, rw, rs_h, GREEN)
        add_text_emu(slide, rx + 137160, rs_y + 18288, rw - 228600, 164592,
                     'RECOMMENDED HYUNDAI START', 101600, GREEN, bold=True)
        add_text_emu(slide, rx + 137160, rs_y + 146304, rw - 228600, 246888,
                     recommended_start, 107950, TEXT_BODY)
    
    # Solution stack & architecture
    arch_y = 5257800
    arch_h = 1051560
    add_rect(slide, MARGIN, arch_y, 11247120, arch_h, BG_CARD_LT)
    add_rect(slide, MARGIN, arch_y, 11247120, 36576, accent_color)
    add_text_emu(slide, 640080, arch_y + 73152, 10881360, 201168,
                 'SOLUTION STACK & ARCHITECTURE', 114300, NAVY_DK, bold=True)
    
    col_w = 2628900
    col_starts = [640080, 3360420, 6080760, 8801100]
    col_labels = ['EDGE / CAPTURE', 'COMPUTE / AI MODELS', 'INTEGRATION', 'UX / DECISION']
    
    for i, (col_x, col_label) in enumerate(zip(col_starts, col_labels)):
        add_text_emu(slide, col_x, arch_y + 320040, col_w, 201168, col_label, 114300, NAVY_DK, bold=True)
        if i < len(arch_cols):
            add_text_emu(slide, col_x, arch_y + 548640, col_w, 457200, arch_cols[i], 101600, GRAY_DK)
    
    add_footer(slide, slide_num)


# ══════════════════════════════════════════════════════════════════════════
#  BUILD THE DECK
# ══════════════════════════════════════════════════════════════════════════

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
blank_layout = prs.slide_layouts[6]  # Blank

# ── SLIDE 1: Title ──────────────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, SLIDE_W, SLIDE_H, BG_DARK)
add_rect(sl, 0, 0, 73152, SLIDE_H, CYAN)  # left accent stripe

add_text_emu(sl, 731520, 822960, 7315200, 274320,
             'AI ENGINEERING TEAM · 제조 AI', 152400, SLATE_LT, bold=True)
add_text_emu(sl, 731520, 1188720, 10972800, 1280160,
             'The AI Engineering Team\nfor Manufacturing', 609600, WHITE, bold=True)
add_text_emu(sl, 731520, 2468880, 10972800, 640080,
             'Hyundai  ·  PeopleTech', 381000, SLATE_MD)

add_rect(sl, 731520, 3246120, 3200400, 36576, CYAN)  # accent line

# Value props (2x2)
props = [
    '✓ 87% of AI pilots fail. Ours don\'t.',
    '✓ 3-person pod, 10-person output',
    '✓ Fixed-price outcomes in 8 weeks',
    '✓ Korea-region data sovereignty (ISMS-P)'
]
for i, prop in enumerate(props):
    row = i // 2
    col = i % 2
    bx = 731520 + col * 5120640
    by = 3657600 + row * 594360
    add_rect(sl, bx, by, 4754880, 457200, BG_CARD)
    add_rect(sl, bx, by, 36576, 457200, CYAN)
    add_text_emu(sl, bx + 182880, by, 4526280, 457200, prop, 152400, RGBColor(0xE2, 0xE8, 0xF0))

add_text_emu(sl, 731520, 5212080, 10972800, 320040,
             'Digital Transformation Lead · Plant Operations · AI 엔지니어링 팀', 152400, SLATE_MD)
add_text_emu(sl, 731520, 5577840, 10972800, 274320,
             '8 Use Cases · Visual Inspection · Predictive Maintenance · Safety · Traceability', 127000, SLATE_MD)
add_text_emu(sl, 10515600, 6446520, 1371600, 365760,
             f'01 / {TOTAL_SLIDES}', 114300, SLATE_MD, align=PP_ALIGN.RIGHT)


# ── SLIDE 2: The Pilot Graveyard ────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'THE PROBLEM', 'The Pilot Graveyard  파일럿의 무덤', 'Manufacturing AI Reality')

add_text_emu(sl, MARGIN, 1097280, 10972800, 1554480,
             '87%', 2286000, RED, bold=True, align=PP_ALIGN.CENTER)
add_text_emu(sl, MARGIN, 2651760, 10972800, 457200,
             'of manufacturing AI pilots never reach production.', 304800, NAVY_DK, bold=True,
             align=PP_ALIGN.CENTER)
add_text_emu(sl, MARGIN + 1828800, 3246120, 7315200, 640080,
             'The problem isn\'t AI technology.\nThe problem is engineering delivery.',
             190500, GRAY_DK, align=PP_ALIGN.CENTER)

# Source bar
add_rect(sl, MARGIN, 4114800, 11247120, 365760, BG_CARD_LT)
add_text_emu(sl, 640080, 4114800, 10881360, 365760,
             'Source: Manufacturing Dive / Gartner, 2024-2025 industry surveys', 114300, SLATE)

# Bottom insight cards
for i, (icon, text) in enumerate([
    ('$22K/min', 'Average cost of unplanned\ndowntime at scale plants'),
    ('8%+', 'Rework rate on premium\nassembly lines'),
    ('6+ months', 'Average time-to-pilot with\ntraditional SI delivery'),
]):
    cx = MARGIN + i * 3749040
    add_rect(sl, cx, 4663440, 3566160, 1554480, BG_CARD_LT)
    add_rect(sl, cx, 4663440, 3566160, 54864, RED)
    add_text_emu(sl, cx + 182880, 4800600, 3200400, 502920, icon, 381000, RED, bold=True)
    add_text_emu(sl, cx + 182880, 5303520, 3200400, 640080, text, 127000, GRAY_DK)

add_footer(sl, 2)


# ── SLIDE 3: Why Pilots Fail ────────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'THE PROBLEM', 'Why Pilots Fail  파일럿 실패 원인', 'The Traditional SI Trap')

add_text_emu(sl, MARGIN, 1097280, 10972800, 502920,
             'Three reasons manufacturing AI pilots die — and all three describe traditional SIs.',
             254000, NAVY_DK, bold=True)

reasons = [
    ('01', 'TOO SLOW', 'Delivery takes 6+ months',
     '6+ month delivery means the business case expires before the pilot lands. By the time the SI finishes discovery, the DT Lead has already missed their steering committee deadline.',
     RED),
    ('02', 'TOO EXPENSIVE', 'Budget burns before ROI',
     '$15-25K/month per developer. A 10-person team = $150-250K/month. Budget burns for 6 months before anyone sees a working model on the plant floor.',
     AMBER),
    ('03', 'WRONG TEAM', 'Data scientists can\'t integrate',
     'Data scientists who can build a model in a notebook but can\'t integrate with MES, ERP, OPC-UA, or plant-floor controllers. The last mile kills the pilot.',
     PURPLE),
]

for i, (num, title, subtitle, desc, color) in enumerate(reasons):
    ry = 1828800 + i * 1463040
    card_with_accent(sl, MARGIN, ry, 11247120, 1280160, color)
    add_text_emu(sl, MARGIN + 182880, ry + 91440, 731520, 365760, num, 304800, color, bold=True)
    add_text_emu(sl, MARGIN + 914400, ry + 91440, 4114800, 274320, title, 190500, NAVY_DK, bold=True)
    add_text_emu(sl, MARGIN + 914400, ry + 365760, 4114800, 274320, subtitle, 139700, SLATE)
    add_text_emu(sl, MARGIN + 5486400, ry + 91440, 5486400, 1097280, desc, 127000, GRAY_DK)

add_footer(sl, 3)


# ── SLIDE 4: A Different Model ──────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'THE MODEL', 'A Different Model  다른 모델', 'AI Engineering Team')

add_text_emu(sl, MARGIN, 1097280, 10972800, 502920,
             '"What if the engineering team never sleeps?"',
             304800, NAVY_DK, bold=True)
add_text_emu(sl, MARGIN, 1691640, 10972800, 365760,
             '3-person human pod + AI tools that code, test, deploy, and monitor 24/7.',
             190500, GRAY_DK)

boxes = [
    ('NOT STAFF AUGMENTATION', 'We don\'t sell seats.\nWe sell outcomes.',
     'No headcount games. No bench-warming. You pay for results delivered, not hours billed.', CYAN),
    ('NOT A PLATFORM', 'We don\'t sell software.\nWe deliver solutions.',
     'No license fee for a tool your team has to learn. We bring the team, the tools, and the delivery.', GREEN),
    ('MANAGED OUTCOME', 'Fixed price. Fixed timeline.\nMeasurable KPIs.',
     'Each pilot: 8 weeks, defined KPIs, go/no-go gate. You only scale what proves ROI.', BLUE),
]

for i, (title, subtitle, desc, color) in enumerate(boxes):
    bx = MARGIN + i * 3749040
    bw = 3566160
    add_rect(sl, bx, 2286000, bw, 3931920, BG_CARD_LT)
    add_rect(sl, bx, 2286000, bw, 73152, color)
    add_text_emu(sl, bx + 182880, 2468880, bw - 365760, 274320, title, 127000, color, bold=True)
    add_text_emu(sl, bx + 182880, 2834640, bw - 365760, 640080, subtitle, 190500, NAVY_DK, bold=True)
    add_text_emu(sl, bx + 182880, 3566160, bw - 365760, 2286000, desc, 127000, GRAY_DK)

add_footer(sl, 4)


# ── SLIDE 5: How the AI Engineering Team Works ──────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'THE MODEL', 'How It Works  작동 방식', 'Pod Composition')

add_text_emu(sl, MARGIN, 1097280, 10972800, 365760,
             'Our engineering pods use AI pair-programming, automated testing, and intelligent deployment pipelines.',
             165100, GRAY_DK)

# Traditional SI vs PeopleTech comparison
for i, (title, people, time, color, items) in enumerate([
    ('TRADITIONAL SI', '10 people', '6+ months', RED,
     ['Project Manager', 'Solution Architect', '2× Data Scientists', '2× ML Engineers',
      'DevOps Engineer', 'Integration Engineer', 'QA Engineer', 'Business Analyst']),
    ('AI ENGINEERING TEAM', '3 people + AI', '8 weeks', CYAN,
     ['Solution Architect — System design, stakeholder interface',
      'ML/Vision Engineer — Model training, edge deployment',
      'Integration Engineer — Plant-floor, OPC-UA, MES, DevOps',
      '+ AI pair-programming & automated pipelines 24/7']),
]):
    bx = MARGIN + i * 5852160
    bw = 5486400
    add_rect(sl, bx, 1645920, bw, 4571520, BG_CARD_LT)
    add_rect(sl, bx, 1645920, bw, 73152, color)
    add_text_emu(sl, bx + 182880, 1828800, bw - 365760, 274320, title, 139700, color, bold=True)
    add_text_emu(sl, bx + 182880, 2194560, bw - 365760, 457200, people, 304800, NAVY_DK, bold=True)
    add_text_emu(sl, bx + 182880, 2651760, bw - 365760, 274320, time, 190500, SLATE)
    add_multiline(sl, bx + 182880, 3063240, bw - 365760, 2880360, items, 120650, TEXT_BODY, bullet="→  ")

# Bottom note
add_rect(sl, MARGIN, 6217920, 11247120, 91440, BG_CARD_LT)
add_text_emu(sl, MARGIN, 6217920 - 274320, 11247120, 274320,
             'Human-led, AI-accelerated. Significantly fewer resources, significantly faster delivery.',
             139700, GREEN, bold=True, align=PP_ALIGN.CENTER)

add_footer(sl, 5)


# ── SLIDE 6: The 8 Use Cases Matrix ────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'USE CASES', '8 AI Use Cases  8개 AI 활용 사례', 'Hyundai Plant Operations')

use_cases = [
    ('01', '비전 검사', 'Visual Inspection', '-45% rework', 'HMGMA Paint', RED, 'PILOT 1'),
    ('02', '변종 확인', 'Variant Confirmation', '-90% wrong variants', 'Assembly Lines', AMBER, 'PHASE 2'),
    ('03', '좌석 검증', 'Seating Validation', '-85% fitment errors', 'Trim & Final', PURPLE, 'PHASE 2'),
    ('04', 'SOP 준수', 'SOP Compliance', '-65% deviations', 'All Plants', TEAL, 'PHASE 2'),
    ('05', '품질 분석', 'Predictive Quality', '-50% field defects', 'Ulsan / Asan', BLUE, 'PHASE 3'),
    ('06', '예측 정비', 'Predictive Maintenance', '-40% downtime', 'Ulsan Stamping', GREEN, 'PILOT 2'),
    ('07', '안전 모니터링', 'Safety Monitoring', '-70% incidents', 'All Plants', ORANGE, 'PHASE 3'),
    ('08', '디지털 추적성', 'Digital Traceability', '100% coverage', 'Supply Chain', CYAN, 'PHASE 3'),
]

for i, (num, kr, en, kpi, target, color, phase) in enumerate(use_cases):
    row = i // 2
    col = i % 2
    cx = MARGIN + col * 5669280
    cy = 1005840 + row * 1325880
    cw = 5486400
    ch = 1188720

    add_rect(sl, cx, cy, cw, ch, BG_CARD_LT)
    add_rect(sl, cx, cy, 54864, ch, color)
    
    # UC number
    add_text_emu(sl, cx + 137160, cy + 73152, 457200, 274320, num, 190500, color, bold=True)
    # Korean title
    add_text_emu(sl, cx + 594360, cy + 73152, 2743200, 274320, kr, 152400, NAVY_DK, bold=True)
    # English title
    add_text_emu(sl, cx + 594360, cy + 365760, 2743200, 228600, en, 120650, SLATE)
    # KPI
    add_text_emu(sl, cx + 594360, cy + 640080, 2743200, 228600, kpi, 139700, color, bold=True)
    # Target
    add_text_emu(sl, cx + 594360, cy + 868680, 2743200, 228600, target, 107950, GRAY_DK)
    
    # Phase tag
    tag_bg = RED if 'PILOT' in phase else (AMBER if 'PHASE 2' in phase else SLATE)
    add_rect(sl, cx + 3931920, cy + 73152, 1371600, 320040, tag_bg)
    add_text_emu(sl, cx + 3931920, cy + 73152, 1371600, 320040, phase, 114300, WHITE, bold=True,
                 align=PP_ALIGN.CENTER)

add_footer(sl, 6)


# ── SLIDE 7: Visual Inspection Deep Dive (Pilot 1) ─────────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=1,
    title='AI-based Visual Inspection  비전 검사',
    tech_subtitle='Computer Vision + Deep Learning',
    accent_color=RGBColor(0x14, 0xA0, 0x85),
    challenge_text='Paint defects, scratches, dents, welding inconsistencies, and panel misalignments escape manual inspection. Human inspectors miss 15-25% of surface defects at line speed, leading to costly rework, warranty claims, and potential recalls.',
    solution_text='High-resolution AI cameras inspect vehicle surfaces in real time. CNN models compare images against golden-sample quality standards and flag anomalies instantly. Defective units are auto-held before advancing to the next station.',
    capabilities=[
        'Real-time surface defect detection across paint, welds, and panel gaps',
        'CNN-based anomaly scoring against golden-sample quality standards',
        'Auto-triggered downstream hold for flagged vehicles',
        'Defect traceability linked to production station, shift, and operator',
    ],
    kpis=[('-45%', 'Rework Costs'), ('-60%', 'Escape Defects'),
          ('<2s', 'Detection Latency'), ('+35%', 'Line Throughput')],
    systems_text='Edge AI cameras · AWS Rekognition / Azure Custom Vision · MES · Defect DB · Quality Dashboard',
    target_users='Quality Engineers · Line Supervisors · Plant Managers',
    arch_cols=[
        'Industrial high-res cameras (Cognex / Basler) · LED light tunnels · NVIDIA Jetson edge inference',
        'CNN anomaly models (ResNet50, EfficientNet) · AWS Rekognition Custom Labels / Azure Custom Vision · Transfer learning',
        'MES connector · OPC-UA bus · Defect database (PostgreSQL) · Kafka event stream',
        'Real-time quality dashboard · Operator hold-station UI · Defect drill-down portal · Slack/Teams alerts',
    ],
    recommended_start='Paint shop · IONIQ 5 / IONIQ 9 line at Metaplant America (HMGMA) — newest line, highest variant complexity. 8-week pilot.',
    slide_num=7,
)


# ── SLIDE 8: Variant Confirmation (UC02) ─────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=2,
    title='Model & Variant Confirmation  변종 확인',
    tech_subtitle='AI Variant Verification',
    accent_color=AMBER,
    challenge_text='Wrong variant assembly — mismatched trim, components, or accessories — costs millions in rework and recall risk. With 50+ IONIQ variants per line, manual checks miss configuration errors at production speed.',
    solution_text='Computer vision and VIN/barcode recognition validate vehicle model, trim level, and installed components against the BOM in real time. Mismatches trigger automatic line holds before the vehicle advances.',
    capabilities=[
        'VIN + barcode scanning for model and variant identification',
        'Vision-based BOM comparison against installed components',
        'Real-time mismatch alerts before vehicle advances to next stage',
        'MES integration to block line progression on confirmation failure',
    ],
    kpis=[('-90%', 'Wrong Variants'), ('-70%', 'Rework Events'),
          ('99.8%', 'Verification Accuracy'), ('<1s', 'Check Latency')],
    systems_text='Vision cameras · VIN/barcode scanners · SAP MES · BOM database · Line controllers',
    target_users='Assembly Operators · Quality Control · Production Supervisors',
    arch_cols=[
        'Vision cameras · VIN/barcode scanners (Datalogic, Cognex DataMan) · Edge gateway with local cache',
        'OCR + object detection (YOLOv8, PaddleOCR) · BOM-match rules engine · Hybrid edge/cloud inference',
        'SAP MES API · BOM database · PLC / line-controller signal-out · Variant configuration service',
        'Station mismatch console · Auto-line-hold trigger · Supervisor mobile alert · Variant audit report',
    ],
    slide_num=8,
)


# ── SLIDE 9: Seating & Component Validation (UC03) ─────────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=3,
    title='Seating & Component Validation  좌석 검증',
    tech_subtitle='Vision AI Fitment Checks',
    accent_color=PURPLE,
    challenge_text='Incorrect seat type, orientation, or mounting errors pass undetected during assembly and cause safety recalls. With multiple trim levels and configurations, manual inspection cannot verify every fitment point at line speed.',
    solution_text='AI cameras verify seat type, orientation, mounting alignment, fastening completion, and fitment accuracy against the vehicle\'s variant configuration. Any deviation triggers an immediate alert before the vehicle proceeds.',
    capabilities=[
        'Seat type and orientation verification via vision AI',
        'Torque and fastening completion detection',
        'Variant-matched fitment checks against vehicle configuration',
        'Alert generation before vehicle moves to next assembly station',
    ],
    kpis=[('-85%', 'Fitment Errors'), ('Zero', 'Seat Recalls'),
          ('+30%', 'Inspection Speed'), ('100%', 'Vehicle Coverage')],
    systems_text='Vision cameras · Torque tool integration · MES · Variant configuration DB',
    target_users='Assembly Operators · Quality Inspectors · Plant Engineers',
    arch_cols=[
        'Multi-angle station cameras · Smart torque wrenches with IIoT telemetry · Edge inference (Jetson Orin)',
        'Object detection & pose estimation (YOLOv8 + keypoint) · Fitment classifier · Variant rule engine',
        'MES · Variant configuration DB · Torque tool gateway · Quality event bus',
        'Operator station tablet · Pass/fail visual cue · Engineer review queue · Post-shift fitment report',
    ],
    slide_num=9,
)


# ── SLIDE 10: SOP Compliance (UC04) ────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=4,
    title='SOP Compliance Monitoring  SOP 준수',
    tech_subtitle='Vision + Pose Estimation',
    accent_color=TEAL,
    challenge_text='Operators skipping steps or deviating from defined procedures introduce assembly defects that only surface at end-of-line or in the field. Current auditing is sample-based and retrospective — missing deviations in real time.',
    solution_text='AI monitors operator activities against SOP workflows using video analytics and pose estimation. Skipped steps, wrong tool usage, and sequence deviations are detected in real time and escalated to supervisors.',
    capabilities=[
        'Pose estimation to detect operator step sequences and ergonomics',
        'SOP workflow comparison with real-time deviation alerts',
        'Incorrect tool usage detection via object recognition',
        'Compliance reporting by operator, station, and shift',
    ],
    kpis=[('-65%', 'SOP Deviations'), ('-40%', 'Final Defects'),
          ('+90%', 'Compliance Rate'), ('Real-time', 'Deviation Alerts')],
    systems_text='Video analytics platform · Pose estimation models · MES · EHS compliance system',
    target_users='Shift Supervisors · Quality Managers · EHS Officers · Process Engineers',
    arch_cols=[
        'Station-mounted cameras · Depth sensors · Smart tool telemetry · Edge compute (Jetson AGX)',
        'Pose estimation (MediaPipe / OpenPose) · Action recognition · Tool detection (YOLOv8) · Sequence model',
        'MES SOP definition API · EHS compliance DB · Shift scheduling system · Kafka alerts',
        'Supervisor dashboard · Real-time deviation overlay · Operator coaching screen · Compliance report',
    ],
    slide_num=10,
)


# ── SLIDE 11: Predictive Quality (UC05) ────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=5,
    title='Predictive Quality Analytics  품질 분석',
    tech_subtitle='ML + Statistical Process Control',
    accent_color=BLUE,
    challenge_text='Quality issues detected at end-of-line or in the field are the most expensive to fix. Reactive quality control catches defects after they\'re built, not before. Root-cause analysis takes days of manual investigation.',
    solution_text='Machine learning models analyze process parameters, sensor data, and historical defect patterns to predict quality excursions before they occur. Early warnings allow process corrections in real time, preventing defects at source.',
    capabilities=[
        'Multivariate SPC with ML-driven control limits',
        'Process parameter correlation to defect outcomes',
        'Early warning alerts before quality excursion events',
        'Automated root-cause analysis with contributing factor ranking',
    ],
    kpis=[('-50%', 'Field Defects'), ('-35%', 'Scrap Rate'),
          ('+40%', 'First-Pass Yield'), ('2hr', 'Early Warning Lead')],
    systems_text='MES process data · Sensor historians · Quality management system · SPC platforms',
    target_users='Quality Engineers · Process Engineers · Plant Managers · Supplier Quality',
    arch_cols=[
        'Process sensors · SPC data streams · MES quality events · Historian (OSIsoft PI / AVEVA)',
        'Gradient boosting (XGBoost) · LSTM time-series · Bayesian root-cause · Anomaly detection ensemble',
        'MES process API · Quality DB · Supplier quality portal · SPC platform integration',
        'Quality prediction dashboard · Process adjustment alerts · Root-cause drill-down · Shift quality report',
    ],
    slide_num=11,
)


# ── SLIDE 12: Predictive Maintenance (UC06 — Pilot 2) ─────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=6,
    title='Predictive Maintenance  예측 정비',
    tech_subtitle='IoT + ML Failure Prediction',
    accent_color=GREEN,
    challenge_text='Unplanned equipment failures halt production lines at $22,000/minute. Current maintenance is either reactive (fix when it breaks) or calendar-based (replace too early or too late). Neither optimizes uptime or cost.',
    solution_text='IoT sensors continuously monitor equipment health (vibration, temperature, current, pressure). ML models detect degradation patterns weeks before failure, enabling planned maintenance during scheduled downtime windows.',
    capabilities=[
        'Continuous equipment health monitoring via IoT sensors',
        'ML-based remaining useful life (RUL) prediction',
        'Maintenance window optimization aligned to production schedule',
        'Integration with CMMS for automated work order generation',
    ],
    kpis=[('-40%', 'Unplanned Downtime'), ('-30%', 'Maintenance Cost'),
          ('+25%', 'Asset Lifespan'), ('5:1', 'ROI Ratio')],
    systems_text='IoT sensors · SCADA/PLC · CMMS · SAP PM · Edge gateways · Cloud ML platform',
    target_users='Maintenance Engineers · Reliability Engineers · Plant Managers · Operations Directors',
    arch_cols=[
        'Vibration/temp/current sensors · SCADA/PLC interfaces · IoT gateways (Siemens/Rockwell) · Edge compute',
        'Time-series anomaly detection · RUL prediction (LSTM/Transformer) · Degradation classifiers · AutoML',
        'OPC-UA historian · CMMS API (SAP PM/Maximo) · IoT platform (AWS IoT/Azure IoT Hub) · Kafka',
        'Equipment health dashboard · Maintenance planner UI · Mobile technician alerts · Asset performance report',
    ],
    recommended_start='Ulsan stamping presses / Asan welding robots — highest downtime cost per minute. 8-week pilot.',
    slide_num=12,
)


# ── SLIDE 13: Safety Monitoring (UC07) ─────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=7,
    title='Safety Monitoring  안전 모니터링',
    tech_subtitle='Vision AI + Zone Analytics',
    accent_color=ORANGE,
    challenge_text='Safety incidents in plant environments cause injury, production stoppage, and regulatory penalties. Current safety monitoring relies on periodic audits and post-incident investigation. Near-misses go unreported.',
    solution_text='AI-powered cameras monitor plant floors for PPE compliance, restricted zone violations, unsafe behaviors, and near-miss events in real time. Automated alerts enable immediate intervention before incidents escalate.',
    capabilities=[
        'PPE detection (helmets, vests, gloves, safety glasses)',
        'Restricted zone and exclusion area monitoring',
        'Unsafe behavior detection (running, lifting posture)',
        'Near-miss event capture and trending analytics',
    ],
    kpis=[('-70%', 'Safety Incidents'), ('100%', 'PPE Compliance'),
          ('<3s', 'Alert Latency'), ('-50%', 'OSHA Recordables')],
    systems_text='IP cameras · Edge AI · EHS management system · Access control · Alarm systems',
    target_users='EHS Managers · Plant Safety Officers · Shift Supervisors · Operations Directors',
    arch_cols=[
        'IP cameras (Axis / Hikvision) · Depth sensors · Edge AI boxes · Existing CCTV infrastructure',
        'Object detection (YOLOv8) · PPE classifier · Zone intrusion model · Behavior recognition · Anomaly detection',
        'EHS compliance DB · Access control integration · Alarm system API · Incident management (SAP EHS)',
        'Real-time safety dashboard · Zone violation alerts · PPE compliance report · Incident investigation portal',
    ],
    slide_num=13,
)


# ── SLIDE 14: Digital Traceability (UC08) ──────────────────────────────
sl = prs.slides.add_slide(blank_layout)
use_case_slide(sl,
    uc_num=8,
    title='Digital Traceability  디지털 추적성',
    tech_subtitle='Graph DB + IoT + Blockchain',
    accent_color=CYAN,
    challenge_text='Traceability data lives in fragmented silos — MES, ERP, supplier portals, paper logs. When a recall hits, root-cause investigation takes weeks of manual data assembly. Regulatory audits are painful and incomplete.',
    solution_text='A unified traceability graph connects every component, process step, operator, and quality event from supplier to customer. Any part can be traced in seconds. Recall scope is instantly calculated and minimized.',
    capabilities=[
        'End-to-end part genealogy from supplier to end customer',
        'Process step linkage with operator, station, and timestamp',
        'Instant recall scope calculation with affected unit identification',
        'Regulatory audit readiness with automated compliance reports',
    ],
    kpis=[('100%', 'Traceability Coverage'), ('<30s', 'Recall Scope Time'),
          ('-80%', 'Audit Prep Time'), ('Full', 'Regulatory Compliance')],
    systems_text='MES · ERP (SAP) · Supplier portals · RFID/barcode · Quality DB · Graph database',
    target_users='Quality Directors · Supply Chain Managers · Compliance Officers · Recall Coordinators',
    arch_cols=[
        'RFID readers · Barcode/QR scanners · IoT sensors at each station · Supplier portal integration',
        'Graph database (Neo4j/Neptune) · Entity resolution · Lineage algorithms · Compliance rule engine',
        'MES API · SAP ERP · Supplier EDI/API · RFID middleware · Event streaming (Kafka)',
        'Traceability explorer UI · Recall simulator · Audit report generator · Supplier scorecard dashboard',
    ],
    slide_num=14,
)


# ── SLIDE 15: The Accelerator Stack ────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'ACCELERATORS', 'The Accelerator Stack  가속기', 'Cuts Time-to-Pilot by 40-60%')

add_text_emu(sl, MARGIN, 1097280, 10972800, 365760,
             '"We\'re not starting from zero. We\'ve done this before."', 190500, NAVY_DK, bold=True)

accelerators = [
    ('Vision-AI Starter Kit', '비전 AI 스타터 킷',
     'Pre-trained defect detection models, camera calibration tools, annotation pipeline, transfer learning templates.',
     CYAN),
    ('Industrial IoT Ref Architecture', 'IIoT 참조 아키텍처',
     'Sensor onboarding, edge gateway config, SCADA/PLC connectors, time-series ingestion pipeline.',
     GREEN),
    ('MES/SAP Connector Library', 'MES/SAP 커넥터',
     'Pre-built adapters for SAP MES, SAP PM, OPC-UA, Siemens MindSphere. Bi-directional data flow.',
     BLUE),
    ('MLOps Blueprint', 'MLOps 블루프린트',
     'Model registry, training pipelines, A/B deployment, drift detection, auto-retraining. Production-grade from Day 1.',
     PURPLE),
    ('Edge Deployment Toolkit', '엣지 배포 툴킷',
     'NVIDIA Jetson / TensorRT optimization, OTA model updates, fleet management, <200ms latency guarantee.',
     AMBER),
    ('Traceability Graph Platform', '추적 그래프 플랫폼',
     'Neo4j/Neptune templates, lineage data model, recall simulator, regulatory report generator.',
     TEAL),
]

for i, (name, kr, desc, color) in enumerate(accelerators):
    row = i // 2
    col = i % 2
    cx = MARGIN + col * 5669280
    cy = 1645920 + row * 1554480
    cw = 5486400
    ch = 1371600
    
    add_rect(sl, cx, cy, cw, ch, BG_CARD_LT)
    add_rect(sl, cx, cy, 54864, ch, color)
    add_text_emu(sl, cx + 182880, cy + 91440, cw - 365760, 274320, name, 165100, NAVY_DK, bold=True)
    add_text_emu(sl, cx + 182880, cy + 365760, cw - 365760, 228600, kr, 120650, color, bold=True)
    add_text_emu(sl, cx + 182880, cy + 640080, cw - 365760, 685800, desc, 114300, GRAY_DK)

add_footer(sl, 15)


# ── SLIDE 16: Integration Architecture ─────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'ARCHITECTURE', 'Integration Architecture  통합 아키텍처', 'Korea-Region · ISMS-P · PIPA')

add_text_emu(sl, MARGIN, 1097280, 10972800, 365760,
             'No rip-and-replace. Edge AI + cloud. <200ms latency. Korea data residency.',
             165100, GRAY_DK)

layers = [
    ('EDGE / PLANT FLOOR (OT)', 'Industrial cameras · IoT sensors · SCADA/PLC · Edge AI (Jetson) · OPC-UA gateway\nAir-gapped OT network · ICS cybersecurity · Local inference <50ms', CYAN),
    ('INTEGRATION / DATA (DMZ)', 'Kafka event streaming · OPC-UA broker · MES/ERP connectors · Data lake (S3/ADLS)\nOT/IT network segmentation · Firewall rules · Encrypted data in transit', GREEN),
    ('CLOUD / ML PLATFORM (IT)', 'AWS Seoul / Azure Korea Central · MLOps pipeline · Model registry · Training cluster\nISMS-P compliant · PIPA data handling · K-AI Ethics audit trail', BLUE),
    ('APPLICATION / UX', 'Quality dashboards · Operator UIs · Mobile alerts · Executive reports · API gateway\nRBAC · SSO integration · Audit logging · Multi-language (KR/EN)', PURPLE),
]

for i, (title, desc, color) in enumerate(layers):
    ly = 1645920 + i * 1143000
    lh = 1005840
    add_rect(sl, MARGIN, ly, 11247120, lh, BG_CARD_LT)
    add_rect(sl, MARGIN, ly, 73152, lh, color)
    add_text_emu(sl, MARGIN + 182880, ly + 73152, 3200400, 274320, title, 139700, color, bold=True)
    add_text_emu(sl, MARGIN + 182880, ly + 365760, 10881360, 594360, desc, 114300, GRAY_DK)

# Compliance bar at bottom
comp_y = 6126480
add_rect(sl, MARGIN, comp_y, 11247120, 228600, GREEN)
add_text_emu(sl, MARGIN + 182880, comp_y, 11247120, 228600,
             'ISMS-P · PIPA · K-AI Ethics Standards · Korea-Region Only · OT/IT Segmentation · ICS Cybersecurity',
             114300, WHITE, bold=True)

add_footer(sl, 16)


# ── SLIDE 17: Four-Phase Delivery ──────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'DELIVERY', 'Four-Phase Delivery  4단계 전달', 'Discovery → Pilot → Scale → Run')

add_text_emu(sl, MARGIN, 1097280, 10972800, 502920,
             'De-risked path from first use case to plant-wide rollout', 279400, NAVY_DK, bold=True)
add_text_emu(sl, MARGIN, 1691640, 10972800, 457200,
             'We never start with a multi-quarter program. We start by proving one use case end-to-end on a real line, with real data, measured against real KPIs.',
             139700, GRAY_DK)

phases = [
    ('PHASE 01', 'Discovery', '2–3 weeks', CYAN,
     ['Plant-floor workshop & line walk-through',
      'Use case prioritization scorecard',
      'Data & systems landscape audit',
      'Pilot scope, KPIs, success criteria']),
    ('PHASE 02', 'Pilot', '8 weeks', GREEN,
     ['1–2 high-impact use cases on one line',
      'AI Engineering Team: build, train, deploy',
      'MES & dashboard integration',
      'Measured ROI vs. baseline']),
    ('PHASE 03', 'Scale', '3–6 months', BLUE,
     ['Rollout across lines, shifts, and plants',
      'Hardening, retraining, A/B variants',
      'Operator & engineer enablement',
      'Cross-use-case data platform']),
    ('PHASE 04', 'Run', 'Ongoing', PURPLE,
     ['Managed services, 24×7 monitoring',
      'Drift detection & auto-retraining',
      'Quarterly value reviews',
      'Roadmap of next use cases']),
]

for i, (label, name, duration, color, items) in enumerate(phases):
    px = MARGIN + i * 2862072
    pw = 2697480
    py = 2651760
    ph = 3383280
    
    add_rect(sl, px, py, pw, ph, BG_CARD_LT)
    add_rect(sl, px, py, pw, 54864, color)
    add_text_emu(sl, px + 182880, py + 164592, pw - 274320, 228600, label, 114300, SLATE, bold=True)
    add_text_emu(sl, px + 182880, py + 411480, pw - 274320, 457200, name, 254000, NAVY_DK, bold=True)
    add_text_emu(sl, px + 182880, py + 868680, pw - 274320, 274320, duration, 114300, SLATE)
    add_multiline(sl, px + 182880, py + 1188720, pw - 274320, 2103120, items, 120650, TEXT_BODY, bullet="→  ")

add_footer(sl, 17)


# ── SLIDE 18: Reference Case Studies ──────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'PROOF POINTS', 'Reference Case Studies  레퍼런스', 'Prior Projects, Proven Domain Expertise')

add_text_emu(sl, MARGIN, 1097280, 10972800, 457200,
             'Our prior projects validated the domain expertise. The AI Engineering Team model accelerates this proven delivery for Hyundai.',
             165100, GRAY_DK)

cases = [
    ('Tier-1 Automotive OEM', 'Paint Defect Computer Vision',
     'Deployed CNN-based visual inspection across 3 paint lines. Real-time defect detection with MES integration and operator dashboards.',
     [('-58%', 'Escape Defects'), ('14-month', 'Payback'), ('99.2%', 'Accuracy'), ('3 lines', 'Coverage')],
     GREEN),
    ('Global EV Manufacturer', 'Predictive Maintenance Platform',
     'IoT sensor network across stamping and welding operations. ML models predicting equipment failure 2-3 weeks before occurrence.',
     [('-38%', 'Downtime'), ('5.2:1', 'ROI'), ('200+', 'Assets Monitored'), ('2-3 wk', 'Prediction Lead')],
     BLUE),
    ('Aerospace Tier-1 Supplier', 'SOP Compliance with Pose Estimation',
     'Video analytics monitoring operator compliance on safety-critical assembly steps. Real-time deviation alerts to supervisors.',
     [('+92%', 'Compliance Rate'), ('-45%', 'Assembly Defects'), ('Real-time', 'Alerts'), ('12', 'Stations')],
     PURPLE),
]

for i, (client, project, desc, kpis, color) in enumerate(cases):
    cy = 1691640 + i * 1554480
    ch = 1371600
    
    add_rect(sl, MARGIN, cy, 11247120, ch, BG_CARD_LT)
    add_rect(sl, MARGIN, cy, 73152, ch, color)
    
    add_text_emu(sl, MARGIN + 182880, cy + 73152, 6400800, 228600, client, 139700, color, bold=True)
    add_text_emu(sl, MARGIN + 182880, cy + 320040, 6400800, 274320, project, 190500, NAVY_DK, bold=True)
    add_text_emu(sl, MARGIN + 182880, cy + 640080, 6400800, 685800, desc, 114300, GRAY_DK)
    
    # KPI cards
    for j, (val, lbl) in enumerate(kpis):
        kx = 7040880 + j * 1143000
        add_rect(sl, kx, cy + 73152, 1005840, 548640, color)
        add_text_emu(sl, kx, cy + 91440, 1005840, 320040, val, 190500, WHITE, bold=True, align=PP_ALIGN.CENTER)
        add_text_emu(sl, kx, cy + 411480, 1005840, 210312, lbl, 88900, WHITE, align=PP_ALIGN.CENTER)
    
    # Honest framing note
    add_text_emu(sl, 7040880, cy + 731520, 4571520, 548640,
                 'Delivered with traditional pod model. AI Engineering Team accelerates this proven approach.',
                 88900, SLATE)

add_footer(sl, 18)


# ── SLIDE 19: ROI Calculator ──────────────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'BUSINESS CASE', 'ROI Calculator  ROI 계산기', 'Hyundai-Specific Estimates')

add_text_emu(sl, MARGIN, 1097280, 10972800, 365760,
             'All figures are industry benchmarks — validated with your plant data during discovery phase.',
             139700, SLATE)

# Baseline data
baselines = [
    ('Ulsan Plant Output', '1.6M vehicles/year', 'World\'s largest auto plant'),
    ('Downtime Cost', '$22,000/minute', 'Industry avg, Aberdeen/Siemens'),
    ('Rework Rate', '8%+ on premium lines', 'Pre-AI baseline estimate'),
    ('Inspection Miss Rate', '15-25% manual', 'Human inspector limitation'),
]

for i, (label, value, source) in enumerate(baselines):
    bx = MARGIN + i * 2834640
    add_rect(sl, bx, 1554480, 2651760, 868680, BG_CARD_LT)
    add_rect(sl, bx, 1554480, 2651760, 45720, CYAN)
    add_text_emu(sl, bx + 137160, 1645920, 2377440, 228600, label, 114300, SLATE, bold=True)
    add_text_emu(sl, bx + 137160, 1874520, 2377440, 320040, value, 190500, NAVY_DK, bold=True)
    add_text_emu(sl, bx + 137160, 2194560, 2377440, 228600, source, 88900, SLATE)

# Pilot ROI projections
add_text_emu(sl, MARGIN, 2651760, 10972800, 365760,
             'PILOT ROI PROJECTIONS (CONSERVATIVE)', 152400, NAVY_DK, bold=True)

pilots_roi = [
    ('Visual Inspection Pilot', 'HMGMA Paint Shop', '-45% rework', '-60% escapes', '8-14 months payback', GREEN),
    ('Predictive Maintenance Pilot', 'Ulsan Stamping / Asan Welding', '-40% downtime', '-30% maint cost', '5:1 ROI ratio', BLUE),
]

for i, (name, target, kpi1, kpi2, payback, color) in enumerate(pilots_roi):
    py = 3063240 + i * 1188720
    add_rect(sl, MARGIN, py, 11247120, 1005840, BG_CARD_LT)
    add_rect(sl, MARGIN, py, 73152, 1005840, color)
    add_text_emu(sl, MARGIN + 182880, py + 73152, 5486400, 274320, name, 165100, color, bold=True)
    add_text_emu(sl, MARGIN + 182880, py + 365760, 5486400, 228600, target, 120650, SLATE)
    
    for j, kpi in enumerate([kpi1, kpi2, payback]):
        kx = 6400800 + j * 1920240
        add_rect(sl, kx, py + 73152, 1737360, 594360, color)
        add_text_emu(sl, kx, py + 73152, 1737360, 365760, kpi, 152400, WHITE, bold=True, align=PP_ALIGN.CENTER)
        add_text_emu(sl, kx, py + 438912, 1737360, 228600,
                     ['Rework', 'Escapes', 'Payback'][j] if i == 0 else ['Downtime', 'Maint Cost', 'ROI'][j],
                     88900, WHITE, align=PP_ALIGN.CENTER)

# Even 10% improvement note
add_rect(sl, MARGIN, 5440680, 11247120, 548640, RGBColor(0xEC, 0xFD, 0xF5))
add_rect(sl, MARGIN, 5440680, 73152, 548640, GREEN)
add_text_emu(sl, MARGIN + 182880, 5440680, 10881360, 548640,
             'Conservative: even a 10% improvement across Ulsan\'s 1.6M vehicle output = significant annual savings. '
             'Full validation during discovery phase with Hyundai plant data.',
             127000, GREEN)

add_footer(sl, 19)


# ── SLIDE 20: Competitive Comparison ─────────────────────────────────
sl = prs.slides.add_slide(blank_layout)
add_body_bg(sl)
add_header_bar(sl, 'COMPARISON', 'Why PeopleTech  왜 피플테크인가', 'vs. Traditional SI vs. In-House')

# Table header
cols = ['Dimension', 'PeopleTech\nAI Engineering Team', 'Traditional SI\n(Accenture/TCS)', 'In-House\nBuild']
col_w = [2743200, 3200400, 2743200, 2560320]
col_x = [MARGIN]
for w in col_w[:-1]:
    col_x.append(col_x[-1] + w)

thy = 1005840
thh = 548640
for i, (cx, cw, label) in enumerate(zip(col_x, col_w, cols)):
    bg = CYAN if i == 1 else BG_HDR
    add_rect(sl, cx, thy, cw, thh, bg)
    add_text_emu(sl, cx + 91440, thy + 73152, cw - 182880, 411480, label,
                 114300, WHITE, bold=True, align=PP_ALIGN.CENTER)

rows = [
    ('Time to Pilot', '8 weeks', '6+ months', '9-12 months'),
    ('Team Size', '3-person pod + AI', '10-15 people', '5-8 FTEs to hire'),
    ('Cost Model', 'Fixed-price outcome', '$15-25K/mo per dev (T&M)', 'Salary + infra + opportunity'),
    ('24/7 Capability', 'AI agents work overnight', 'Business hours only', 'Business hours only'),
    ('Accelerator IP', '6 reusable accelerators', 'Build from scratch', 'Build from scratch'),
    ('Plant Integration', 'OPC-UA, MES, SCADA native', 'Subcontracted', 'Learning curve'),
    ('Incentive Alignment', 'Faster = better for both', 'More hours = more revenue', 'Competing priorities'),
]

for i, (dim, pt, si, ih) in enumerate(rows):
    ry = 1554480 + i * 685800
    rh = 640080
    
    for j, (cx, cw, val) in enumerate(zip(col_x, col_w, [dim, pt, si, ih])):
        bg = RGBColor(0xF0, 0xFD, 0xFA) if j == 1 else BG_CARD_LT
        add_rect(sl, cx, ry, cw, rh, bg)
        color = NAVY_DK if j <= 1 else GRAY_DK
        bld = j == 0
        add_text_emu(sl, cx + 91440, ry + 73152, cw - 182880, rh - 146304, val,
                     114300 if j == 0 else 107950, color, bold=bld)

# Incentive note
add_rect(sl, MARGIN, 6354552, 11247120, 0, BG_BODY)  # spacer
add_footer(sl, 20)


# ══════════════════════════════════════════════════════════════════════════
# APPENDIX SLIDES (17-20 → renumbered to fit)
# ══════════════════════════════════════════════════════════════════════════
# Note: Main deck is 20 slides. Keeping it at 20 by including competitive
# comparison as slide 20 and moving appendix to separate section if needed.


# ── SAVE ────────────────────────────────────────────────────────────────
out = "PeopleTech_AI_Engineering_Team_Hyundai.pptx"
prs.save(out)
print(f"Saved: {out} ({len(prs.slides)} slides)")
