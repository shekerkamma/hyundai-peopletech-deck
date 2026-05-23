#!/usr/bin/env python3
"""
Enrich AI-Engineering-Business-Use-Cases.pptx with OpenHands content.

Adds:
1. New UC slides for AI-powered software development use cases (OpenHands-informed)
2. Updates Tech Stack slide with OpenHands / autonomous agent layer
3. Updates YC Competitive Landscape with OpenHands data
4. Updates title slide count and executive summary
"""

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from copy import deepcopy
import re

# ── Style Constants (extracted from UC01) ──────────────────────────────
FONT = "Calibri"
# Font sizes (in EMU)
TITLE_SIZE = 203200       # ~16pt - slide title
SECTION_SIZE = 127000     # ~10pt - section headers
BODY_SIZE = 107950        # ~8.5pt - body text
SMALL_SIZE = 101600       # ~8pt - smaller body / YC entries
STACK_SIZE = 88900        # ~7pt - solution stack
KPI_NUM_SIZE = 254000     # ~20pt - big KPI numbers
KPI_LABEL_SIZE = 101600   # ~8pt - KPI labels
FOOTER_SIZE = 127000
PAGE_NUM_SIZE = 114300

# Colors
NAVY = RGBColor(0x1F, 0x3B, 0x6E)
RED = RGBColor(0xE3, 0x18, 0x37)
GREEN = RGBColor(0x16, 0x65, 0x34)
DARK_TEXT = RGBColor(0x1A, 0x1A, 0x1A)
GRAY_TEXT = RGBColor(0x6B, 0x72, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MAGENTA = RGBColor(0x9D, 0x17, 0x4D)
AMBER = RGBColor(0x92, 0x40, 0x0E)
DARK_BAR = RGBColor(0x0D, 0x3B, 0x5E)
LIGHT_BG = RGBColor(0xF5, 0xF7, 0xFA)
STACK_BG = RGBColor(0xF0, 0xF2, 0xF5)
LIGHT_PAGE = RGBColor(0xAA, 0xAA, 0xAA)

# Slide dimensions
SLIDE_W = 12192000
SLIDE_H = 6858000


def add_shape(slide, left, top, width, height, fill_color=None):
    """Add a rectangle shape with optional solid fill."""
    shape = slide.shapes.add_shape(1, left, top, width, height)  # MSO_SHAPE.RECTANGLE
    shape.line.fill.background()  # no border
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    return shape


def add_text_box(slide, left, top, width, height):
    """Add a text box."""
    return slide.shapes.add_textbox(left, top, width, height)


def set_text(tf, text, size, color, bold=None, alignment=None):
    """Set text in a text frame (single paragraph)."""
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


def add_para(tf, text, size, color, bold=None, alignment=None):
    """Add a new paragraph to an existing text frame."""
    p = tf.add_paragraph()
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


def build_uc_slide(prs, slide_index, uc_num, title, subtitle,
                   challenges, solutions, governance,
                   yc_entries, kpis, systems, target_users,
                   stack, total_slides):
    """Build a complete use case slide matching the UC01 layout."""

    # Use the same layout as existing UC slides
    layout = prs.slides[4].slide_layout  # UC01's layout
    slide = prs.slides.add_slide(layout)

    # Move slide to correct position
    slides_el = prs.slides._sldIdLst
    slide_id = slides_el[-1]  # just added
    slides_el.remove(slide_id)
    # Insert at slide_index position
    children = list(slides_el)
    if slide_index < len(children):
        slides_el.insert(slide_index, slide_id)
    else:
        slides_el.append(slide_id)

    # Remove all default placeholder shapes
    for sp in list(slide.shapes):
        slide.shapes._spTree.remove(sp._element)

    page_label = f"{slide_index + 1} / {total_slides}"

    # ── Title bar ──
    add_shape(slide, 274320, 182880, 11640312, 384048, NAVY)
    tb = add_text_box(slide, 411480, 182880, 11338560, 384048)
    set_text(tb.text_frame, f"UC{uc_num:02d} | {title} | {subtitle}", TITLE_SIZE, WHITE, bold=True)

    # ── Left column: CHALLENGE ──
    add_shape(slide, 457200, 713232, 54864, 201168, RED)
    tb = add_text_box(slide, 566928, 694944, 5559552, 237744)
    set_text(tb.text_frame, "CHALLENGE", SECTION_SIZE, RED, bold=True)
    tb = add_text_box(slide, 566928, 969264, 5559552, 700000)
    set_text(tb.text_frame, challenges[0], BODY_SIZE, DARK_TEXT)
    for c in challenges[1:]:
        add_para(tb.text_frame, c, BODY_SIZE, DARK_TEXT)

    # ── SOLUTION ──
    sol_top = 1664208
    add_shape(slide, 457200, sol_top, 54864, 201168, GREEN)
    tb = add_text_box(slide, 566928, sol_top - 18288, 5559552, 237744)
    set_text(tb.text_frame, "SOLUTION", SECTION_SIZE, GREEN, bold=True)
    tb = add_text_box(slide, 566928, sol_top + 256032, 5559552, 700000)
    set_text(tb.text_frame, solutions[0], BODY_SIZE, DARK_TEXT)
    for s in solutions[1:]:
        add_para(tb.text_frame, s, BODY_SIZE, DARK_TEXT)

    # ── GOVERNANCE & SECURITY ──
    gov_top = 2615184
    add_shape(slide, 457200, gov_top, 54864, 201168, NAVY)
    tb = add_text_box(slide, 566928, gov_top - 18288, 5559552, 237744)
    set_text(tb.text_frame, "GOVERNANCE & SECURITY", SECTION_SIZE, NAVY, bold=True)
    tb = add_text_box(slide, 566928, gov_top + 256032, 5559552, 500000)
    set_text(tb.text_frame, governance[0], BODY_SIZE, DARK_TEXT)
    for g in governance[1:]:
        add_para(tb.text_frame, g, BODY_SIZE, DARK_TEXT)

    # ── YC COMPETITIVE LANDSCAPE ──
    yc_top = 3410712
    add_shape(slide, 457200, yc_top, 54864, 201168, MAGENTA)
    tb = add_text_box(slide, 566928, yc_top - 18288, 5559552, 237744)
    set_text(tb.text_frame, "YC COMPETITIVE LANDSCAPE", SECTION_SIZE, MAGENTA, bold=True)
    tb = add_text_box(slide, 566928, yc_top + 256032, 5559552, 621792)
    set_text(tb.text_frame, yc_entries[0], SMALL_SIZE, DARK_TEXT)
    for y in yc_entries[1:]:
        add_para(tb.text_frame, y, SMALL_SIZE, DARK_TEXT)

    # ── KPI boxes (right column, 2x2 grid) ──
    kpi_positions = [
        (6400800, 713232), (9052560, 713232),
        (6400800, 1673352), (9052560, 1673352),
    ]
    for idx, (kx, ky) in enumerate(kpi_positions):
        if idx >= len(kpis):
            break
        num, label = kpis[idx]
        add_shape(slide, kx, ky, 2468880, 777240, LIGHT_BG)
        tb = add_text_box(slide, kx, ky + 36576, 2468880, 388620)
        set_text(tb.text_frame, num, KPI_NUM_SIZE, RED, bold=True, alignment=PP_ALIGN.CENTER)
        tb = add_text_box(slide, kx + 45720, ky + 373075, 2377440, 373075)
        set_text(tb.text_frame, label, KPI_LABEL_SIZE, GRAY_TEXT, alignment=PP_ALIGN.CENTER)

    # ── SYSTEMS INTEGRATED ──
    sys_top = 2633472
    add_shape(slide, 6400800, sys_top, 54864, 201168, NAVY)
    tb = add_text_box(slide, 6510528, sys_top - 18288, 5193792, 237744)
    set_text(tb.text_frame, "SYSTEMS INTEGRATED", SECTION_SIZE, NAVY, bold=True)

    sys_x = 6492240
    sys_y = sys_top + 274320
    for i, sys_name in enumerate(systems):
        w = max(640080, len(sys_name) * 70000)
        add_shape(slide, sys_x, sys_y, w, 219456, LIGHT_BG)
        tb = add_text_box(slide, sys_x, sys_y, w, 219456)
        set_text(tb.text_frame, sys_name, SMALL_SIZE, NAVY, bold=True, alignment=PP_ALIGN.CENTER)
        sys_x += w + 91440

    # ── TARGET USERS ──
    tgt_top = 3227832
    add_shape(slide, 6400800, tgt_top, 54864, 201168, AMBER)
    tb = add_text_box(slide, 6510528, tgt_top - 18288, 5193792, 237744)
    set_text(tb.text_frame, "TARGET USERS", SECTION_SIZE, AMBER, bold=True)
    tb = add_text_box(slide, 6510528, tgt_top + 256032, 5193792, 201168)
    set_text(tb.text_frame, target_users, BODY_SIZE, DARK_TEXT)

    # ── SOLUTION STACK (4 columns) ──
    stk_top = 3776472
    add_shape(slide, 6400800, stk_top, 54864, 201168, NAVY)
    tb = add_text_box(slide, 6510528, stk_top - 18288, 5193792, 237744)
    set_text(tb.text_frame, "SOLUTION STACK", SECTION_SIZE, NAVY, bold=True)

    col_x = 6400800
    col_w = 1257300
    for col_title, col_items in stack:
        # Header
        add_shape(slide, col_x, stk_top + 274320, col_w, 201168, DARK_BAR)
        tb = add_text_box(slide, col_x, stk_top + 274320, col_w, 201168)
        set_text(tb.text_frame, col_title, STACK_SIZE, WHITE, bold=True, alignment=PP_ALIGN.CENTER)
        # Body
        add_shape(slide, col_x, stk_top + 475488, col_w, 502920, STACK_BG)
        tb = add_text_box(slide, col_x + 36576, stk_top + 493776, col_w - 73152, 457200)
        set_text(tb.text_frame, col_items[0], STACK_SIZE, DARK_TEXT)
        for item in col_items[1:]:
            add_para(tb.text_frame, item, STACK_SIZE, DARK_TEXT)
        col_x += col_w + 91440

    # ── Footer bar ──
    add_shape(slide, 0, 6263640, 12188952, 594360, DARK_BAR)
    tb = add_text_box(slide, 0, 6263640, 12188952, 594360)
    set_text(tb.text_frame, "AI Engineering Business Use Cases | Confidential", FOOTER_SIZE, WHITE, alignment=PP_ALIGN.CENTER)
    tb = add_text_box(slide, 11155680, 6263640, 914400, 594360)
    set_text(tb.text_frame, page_label, PAGE_NUM_SIZE, LIGHT_PAGE, alignment=PP_ALIGN.RIGHT)

    return slide


def update_page_numbers(prs, total):
    """Update page numbers on all slides."""
    for idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    text = para.text.strip()
                    if re.match(r'^\d+ / \d+$', text):
                        for run in para.runs:
                            run.text = f"{idx + 1} / {total}"
                    # Update title slide count
                    if "20 Production-Ready Use Cases" in text:
                        for run in para.runs:
                            if "20" in run.text:
                                run.text = run.text.replace("20 Production-Ready Use Cases Across 6 Verticals", "24 Production-Ready Use Cases Across 7 Verticals")
                    if "20\nUse Cases Ready" in text or text == "20":
                        if shape.name and "Text" in shape.name:
                            for run in para.runs:
                                if run.text.strip() == "20":
                                    run.text = "24"
                    if text == "6" and any(p.text.strip() == "Verticals Covered" for p in shape.text_frame.paragraphs):
                        for run in para.runs:
                            if run.text.strip() == "6":
                                run.text = "7"


def update_tech_stack(prs):
    """Add OpenHands to the tech stack slide (slide 4)."""
    slide = prs.slides[3]
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                if "LangGraph / CrewAI" in para.text:
                    for run in para.runs:
                        if "LangGraph" in run.text:
                            run.text = run.text.replace(
                                "LangGraph / CrewAI agent orchestrator",
                                "LangGraph / CrewAI / OpenHands agent orchestrator"
                            )
                if "Claude 3.5 Sonnet: reasoning" in para.text:
                    for run in para.runs:
                        if "Claude 3.5 Sonnet" in run.text:
                            run.text = run.text.replace(
                                "Claude 3.5 Sonnet: reasoning + generation",
                                "Claude 4.5 Opus: reasoning + generation"
                            )


def update_yc_landscape(prs):
    """Update the YC competitive landscape slide with Software Engineering vertical."""
    slide = prs.slides[24]  # Slide 25
    for shape in slide.shapes:
        if shape.has_text_frame:
            full = shape.text_frame.text
            if "AI Platforms" in full and "30+" in full:
                # Find the paragraph with AI Platforms row and add OpenHands context
                for para in shape.text_frame.paragraphs:
                    if "LangChain, CrewAI" in para.text:
                        for run in para.runs:
                            if "LangChain" in run.text:
                                run.text = run.text.replace(
                                    "LangChain, CrewAI, Temporal, various agent frameworks",
                                    "LangChain, CrewAI, OpenHands (74.6k★), Temporal, Devin, Factory AI"
                                )


def update_exec_summary(prs, total):
    """Update executive summary numbers."""
    slide = prs.slides[-1]  # Last slide
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                txt = para.text.strip()
                if "20 production-ready use cases across 6 verticals" in txt:
                    for run in para.runs:
                        run.text = run.text.replace(
                            "20 production-ready use cases across 6 verticals",
                            "24 production-ready use cases across 7 verticals"
                        )
                if txt == "20":
                    for run in para.runs:
                        if run.text.strip() == "20":
                            run.text = "24"
                if txt == "6":
                    # Check if any para in this shape says "Verticals Covered"
                    all_paras = list(shape.text_frame.paragraphs)
                    if any("Verticals" in p.text for p in all_paras):
                        for run in para.runs:
                            if run.text.strip() == "6":
                                run.text = "7"


def main():
    prs = Presentation("AI-Engineering-Business-Use-Cases.pptx")

    # Current: 32 slides. We'll add 4 new UC slides → 36 total.
    # Insert after slide 24 (UC20), before YC landscape (slide 25).
    total_slides = 36
    insert_at = 24  # 0-indexed, after UC20

    # ── UC21: AI-Powered Code Generation & Issue Resolution ──
    build_uc_slide(prs, insert_at, 21,
        title="AI-Powered Code Generation",
        subtitle="Autonomous Issue Resolution + PR Generation",
        challenges=[
            "Developer time wasted on routine bug fixes: 30-40% of engineering hours spent on low-complexity issues",
            "PR review bottleneck: average 2-day cycle time from issue to merged fix",
            "Legacy codebases accumulate 200+ open issues with no bandwidth for resolution",
            "Junior developer onboarding takes 3-6 months before meaningful code contributions",
        ],
        solutions=[
            "OpenHands-style autonomous agents: analyze GitHub issues, write fixes, open PRs for human review",
            "Sandboxed execution: every agent runs in isolated Docker container with full dev environment",
            "Event-sourced architecture: deterministic replay, full audit trail of every agent action",
            "Self-improving pipeline: 37% of agent's own codebase commits written by the agent itself",
        ],
        governance=[
            "All AI-generated code marked as AI-assisted; human approval required before merge",
            "Sandboxed execution prevents host system access; secrets masked in all outputs",
            "SecurityAnalyzer rates tool calls LOW/MEDIUM/HIGH risk with confirmation policies",
        ],
        yc_entries=[
            "OpenHands / All Hands AI (74.6k★) - open-source autonomous dev agents",
            "Devin / Cognition (funded $175M) - commercial AI developer",
            "Factory AI (S24) - autonomous code agents",
            "Sweep AI (S23) - automated PR generation",
        ],
        kpis=[
            ("77.6%", "SWE-Bench Resolve Rate"),
            ("~$3", "Cost per Generated PR"),
            ("37%", "Self-Written Commits"),
            ("2-4 wk", "Deployment Timeline"),
        ],
        systems=["GitHub", "GitLab", "Docker", "CI/CD"],
        target_users="Engineering Leads  |  DevOps Managers  |  VP Engineering",
        stack=[
            ("AGENT / SDK", ["OpenHands SDK", "CodeAct agent"]),
            ("COMPUTE / AI", ["Claude 4.5 Opus", "GPT-5.2 Codex"]),
            ("INTEGRATION", ["GitHub Actions", "MCP connectors"]),
            ("UX / DECISION", ["PR review portal", "Agent dashboard"]),
        ],
        total_slides=total_slides,
    )

    # ── UC22: Automated Testing & Quality Assurance ──
    build_uc_slide(prs, insert_at + 1, 22,
        title="Automated Test Generation",
        subtitle="AI Agents for Test Coverage & Bug Detection",
        challenges=[
            "Legacy codebases average 35% test coverage; manual test writing is slowest dev task",
            "Regression bugs escape to production: 15% of deployments cause incidents in first 24 hours",
            "Test maintenance burden: 20% of test suites break with each major refactor",
            "Security vulnerability testing requires specialized expertise most teams lack",
        ],
        solutions=[
            "AI agents identify bugs and generate comprehensive test suites (SWT-Bench validated)",
            "Multi-agent fan-out: parallel test generation across unit, integration, and E2E layers",
            "Automated test maintenance: agents detect broken tests and auto-fix after refactors",
            "Security-focused test generation: OWASP Top 10 coverage with automated pen-test scenarios",
        ],
        governance=[
            "Generated tests reviewed by senior engineer before CI integration",
            "Test data isolation: no production PII in test fixtures; synthetic data generation",
            "Coverage metrics tracked per sprint; minimum 80% threshold enforced via CI gates",
        ],
        yc_entries=[
            "QA Wolf (W19, team 80) - end-to-end testing as a service",
            "Carbonate (S23) - AI test generation",
            "Momentic (S23) - autonomous E2E testing",
            "Sapient AI (W24) - unit test generation",
        ],
        kpis=[
            ("35→85%", "Test Coverage Lift"),
            ("60%", "Fewer Prod Regressions"),
            ("10x", "Test Generation Speed"),
            ("1-2 wk", "Setup Timeline"),
        ],
        systems=["GitHub", "Jest/Pytest", "CI/CD", "SAST Tools"],
        target_users="QA Engineers  |  Engineering Managers  |  Security Teams",
        stack=[
            ("AGENT / SDK", ["OpenHands agents", "SWT-Bench model"]),
            ("COMPUTE / AI", ["Claude reasoning", "Code analysis"]),
            ("INTEGRATION", ["CI/CD hooks", "Coverage APIs"]),
            ("UX / DECISION", ["Coverage dashboard", "Risk heatmap"]),
        ],
        total_slides=total_slides,
    )

    # ── UC23: Code Modernization & Tech Debt ──
    build_uc_slide(prs, insert_at + 2, 23,
        title="Code Modernization & Tech Debt",
        subtitle="Autonomous Refactoring + Framework Migration",
        challenges=[
            "Technical debt compounds: 40% of dev time spent navigating and working around legacy code",
            "Framework migrations (e.g., Angular→React, Python 2→3) take 6-18 months manually",
            "Dependency upgrades deferred due to risk: average enterprise has 200+ outdated packages",
            "Monolith decomposition requires deep architectural knowledge often lost with attrition",
        ],
        solutions=[
            "AI-powered multi-repo dependency upgrades at ~$3 per PR across hundreds of services",
            "Autonomous framework migration: agent analyzes patterns, generates idiomatic code in target framework",
            "Monolith decomposition: agent identifies service boundaries, extracts and tests independently",
            "Greenfield scaffolding: commit0-validated app development from specs to working code",
        ],
        governance=[
            "All migration PRs include automated regression test results before review",
            "Dependency upgrade policy: security patches auto-merged, major versions require human approval",
            "Architecture decision records (ADRs) auto-generated for each decomposition step",
        ],
        yc_entries=[
            "Grit.io (W22) - automated code migrations",
            "CodeMod (W24) - codemod generation",
            "Moderne (S21, team 50) - large-scale code refactoring",
            "Sourcegraph Cody (S14, team 300+) - code intelligence",
        ],
        kpis=[
            ("~$3", "Cost per Migration PR"),
            ("80%", "Tech Debt Reduction"),
            ("6→1 mo", "Migration Timeline"),
            ("100+", "Repos per Sprint"),
        ],
        systems=["GitHub", "npm/pip/maven", "Docker", "Terraform"],
        target_users="Platform Engineers  |  Tech Leads  |  CTOs",
        stack=[
            ("ANALYSIS", ["Dependency graph", "Dead code scan"]),
            ("COMPUTE / AI", ["Claude Opus", "Multi-agent chain"]),
            ("INTEGRATION", ["Package registries", "CI validation"]),
            ("UX / DECISION", ["Migration tracker", "Risk scoring"]),
        ],
        total_slides=total_slides,
    )

    # ── UC24: DevOps & Incident Response Automation ──
    build_uc_slide(prs, insert_at + 3, 24,
        title="DevOps & Incident Response",
        subtitle="AI Agents for CI/CD, Log Analysis & Auto-Remediation",
        challenges=[
            "Mean time to resolution (MTTR) averages 4+ hours for production incidents",
            "On-call engineers spend 60% of incident time on log correlation and root cause triage",
            "CI/CD pipeline failures block 15-20% of deployments, requiring manual debugging",
            "Infrastructure drift: Terraform state diverges from reality across 50+ microservices",
        ],
        solutions=[
            "AI agents analyze logs, pinpoint root causes, and generate fix PRs within minutes",
            "Automated CI/CD debugging: agent reads build logs, identifies failures, pushes fixes",
            "Infrastructure-as-code auto-remediation: drift detection → Terraform PR → validated apply",
            "Runbook automation: agent executes incident playbooks with human-in-the-loop escalation",
        ],
        governance=[
            "Production access scoped read-only for agents; write actions require human approval",
            "Incident response audit trail: every agent action logged with timestamp and rationale",
            "Blast radius controls: auto-remediation limited to non-critical services without approval",
        ],
        yc_entries=[
            "Rootly (S21, team 45) - incident management",
            "incident.io (S21, team 120) - incident response",
            "Firehydrant (W20, team 90) - incident management",
            "Airplane (W22, team 40) - internal tooling + runbooks",
        ],
        kpis=[
            ("4hr→15m", "Mean Time to Resolution"),
            ("70%", "Auto-Resolved Incidents"),
            ("85%", "CI/CD Fix Rate"),
            ("24/7", "Always-On Coverage"),
        ],
        systems=["PagerDuty", "DataDog", "Terraform", "GitHub Actions"],
        target_users="SRE Teams  |  DevOps Engineers  |  Incident Commanders",
        stack=[
            ("OBSERVE", ["DataDog logs", "PagerDuty alerts"]),
            ("COMPUTE / AI", ["Log analysis LLM", "Root cause agent"]),
            ("INTEGRATION", ["Terraform API", "K8s API"]),
            ("UX / DECISION", ["Incident dashboard", "Runbook executor"]),
        ],
        total_slides=total_slides,
    )

    # ── Update existing slides ──
    update_tech_stack(prs)
    update_yc_landscape(prs)

    # Update page numbers across all slides
    update_page_numbers(prs, total_slides)
    update_exec_summary(prs, total_slides)

    # Add "Software Engineering" to title slide vertical tags
    slide1 = prs.slides[0]
    for shape in slide1.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                if para.text.strip() == "AI Platforms":
                    # Add a new vertical tag below
                    # Find the shape position and add new one
                    sx, sy = shape.left, shape.top
                    sw, sh = shape.width, shape.height
                    new_shape = add_shape(slide1, sx, sy + 502920, sw, sh, NAVY)
                    # Need to add text - use the shape's text frame
                    new_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
                    r = new_shape.text_frame.paragraphs[0].add_run()
                    r.text = "Software Engineering"
                    r.font.name = FONT
                    r.font.size = 165100
                    r.font.bold = True
                    r.font.color.rgb = WHITE
                    break

    # Save
    out_path = "AI-Engineering-Business-Use-Cases.pptx"
    prs.save(out_path)
    print(f"✓ Saved enriched deck: {out_path}")
    print(f"  → 4 new use cases added (UC21-UC24): AI Code Gen, Test Gen, Code Modernization, DevOps/Incident")
    print(f"  → Tech stack updated with OpenHands")
    print(f"  → YC landscape updated with OpenHands (74.6k★)")
    print(f"  → Software Engineering vertical added to title")
    print(f"  → Total slides: {total_slides}")


if __name__ == "__main__":
    main()
