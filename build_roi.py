"""Build the ROI calculator workbook for the Hyundai pilot conversation.

Outputs: ROI_Calculator_Hyundai.xlsx

Sheets:
  - Inputs       — plant + line economics. Hyundai stakeholders edit yellow cells.
  - Pilot Sizing — the 2 recommended pilots (Visual Inspection + Predictive Maintenance)
                   with per-line value math, payback months, and 3-year NPV.
  - Full Use Cases — all 8 use cases with parametrized savings ranges.
  - Notes        — assumptions, sources, sensitivities.

Pre-filled defaults are Ulsan-scale public figures for a single high-volume line.
"""
from openpyxl import Workbook
from openpyxl.styles import (Font, PatternFill, Alignment, Border, Side, NamedStyle)
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

NAVY = "1A2754"
TEAL = "14A085"
ORANGE = "D97706"
RED = "DC2626"
SLATE_50 = "F8FAFC"
SLATE_200 = "E2E8F0"
INK = "1E293B"
INK_MUTE = "64748B"
YELLOW_INPUT = "FEF9C3"

wb = Workbook()

# ============================================================================
# STYLES
# ============================================================================
thin = Side(style="thin", color="CBD5E1")
border_all = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_header(cell, fill=NAVY, color="FFFFFF", size=11):
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(name="Calibri", size=size, bold=True, color=color)
    cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    cell.border = border_all

def style_label(cell, bold=False):
    cell.font = Font(name="Calibri", size=11, bold=bold, color=INK)
    cell.alignment = Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
    cell.border = border_all

def style_input(cell, fmt=None):
    cell.fill = PatternFill("solid", fgColor=YELLOW_INPUT)
    cell.font = Font(name="Calibri", size=11, bold=True, color=INK)
    cell.alignment = Alignment(horizontal="right", vertical="center", indent=1)
    cell.border = border_all
    if fmt:
        cell.number_format = fmt

def style_calc(cell, fmt=None, bold=False, color=INK):
    cell.fill = PatternFill("solid", fgColor=SLATE_50)
    cell.font = Font(name="Calibri", size=11, bold=bold, color=color)
    cell.alignment = Alignment(horizontal="right", vertical="center", indent=1)
    cell.border = border_all
    if fmt:
        cell.number_format = fmt

def style_output(cell, fmt=None, fill=TEAL):
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    cell.alignment = Alignment(horizontal="right", vertical="center", indent=1)
    cell.border = border_all
    if fmt:
        cell.number_format = fmt

def title_row(ws, row, text, span=6, fill=NAVY):
    ws.cell(row=row, column=1, value=text)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    c = ws.cell(row=row, column=1)
    c.fill = PatternFill("solid", fgColor=fill)
    c.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 30

def section_row(ws, row, text, span=6, fill="E2E8F0"):
    ws.cell(row=row, column=1, value=text)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    c = ws.cell(row=row, column=1)
    c.fill = PatternFill("solid", fgColor=fill)
    c.font = Font(name="Calibri", size=11, bold=True, color=NAVY)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 22

# ============================================================================
# SHEET 1: INPUTS
# ============================================================================
ws = wb.active
ws.title = "Inputs"
ws.column_dimensions["A"].width = 42
ws.column_dimensions["B"].width = 18
ws.column_dimensions["C"].width = 14
ws.column_dimensions["D"].width = 46

title_row(ws, 1, "ROI INPUTS  ·  Yellow cells = edit these", span=4)

section_row(ws, 3, "Plant & Line Economics", span=4)

inputs = [
    # (label, default, format, note)
    ("Vehicles produced per day (single line)",   1600,    "#,##0",      "Ulsan single line, 2 shifts. ~400K/yr per line."),
    ("Production days per year",                  300,     "#,##0",      "~6 days/week, planned shutdowns excluded."),
    ("Average vehicle revenue (USD)",             30000,   '"$"#,##0',   "Mix of Tucson, Santa Fe, IONIQ — use your blended ASP."),
    ("Average warranty cost per defect escape (USD)", 450,  '"$"#,##0',   "Industry-standard $300–$800 depending on defect class."),
    ("Average rework cost per defect (USD)",      180,     '"$"#,##0',   "Includes labor + materials + line disruption."),
    ("Hourly fully-loaded line labor cost (USD)", 95,      '"$"#,##0',   "Per operator, includes benefits."),
    ("Unplanned downtime cost per minute (USD)",  22000,   '"$"#,##0',   "Industry-standard for high-volume automotive line."),
    ("Current unplanned downtime (hrs / week)",   6.4,     "0.0",        "Default from Global EV manufacturer baseline."),
    ("Current defect escape rate (% of vehicles)", 0.012,  "0.00%",      "1.2% — typical pre-AI baseline."),
    ("Current rework rate (% of vehicles)",       0.08,    "0.00%",      "8% pre-AI typical on premium SUV lines."),
    ("Discount rate (for NPV)",                   0.10,    "0.0%",       "Standard corporate discount rate."),
]

for i, (label, val, fmt, note) in enumerate(inputs):
    r = 4 + i
    ws.cell(row=r, column=1, value=label); style_label(ws.cell(row=r, column=1))
    ws.cell(row=r, column=2, value=val); style_input(ws.cell(row=r, column=2), fmt=fmt)
    ws.cell(row=r, column=3, value=""); style_calc(ws.cell(row=r, column=3))
    ws.cell(row=r, column=4, value=note); ws.cell(row=r, column=4).font = Font(name="Calibri", size=10, italic=True, color=INK_MUTE)
    ws.cell(row=r, column=4).alignment = Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
    ws.cell(row=r, column=4).border = border_all

# Named ranges for use in formulas
INP = {
    "veh_day": "Inputs!$B$4",
    "days_yr": "Inputs!$B$5",
    "asp":     "Inputs!$B$6",
    "warr":    "Inputs!$B$7",
    "rework":  "Inputs!$B$8",
    "labor":   "Inputs!$B$9",
    "dt_cost": "Inputs!$B$10",
    "dt_curr": "Inputs!$B$11",
    "esc_rate":"Inputs!$B$12",
    "rew_rate":"Inputs!$B$13",
    "wacc":    "Inputs!$B$14",
}

# ----- Pilot economics block -----
section_row(ws, 16, "Pilot Economics — PeopleTech engagement", span=4)
pilot_inputs = [
    ("Pilot duration (weeks)",                12,      "0",        "Discovery + delivery + measurement."),
    ("Pilot fixed fee per use case (USD)",    450000,  '"$"#,##0', "PeopleTech embedded pod, fixed-scope."),
    ("Per-line scale rollout cost (USD)",     200000,  '"$"#,##0', "Hardware + integration per additional line."),
    ("Annual managed-service / Run cost (USD)", 180000, '"$"#,##0',"Drift monitoring, retraining, 24×7 support per pilot."),
    ("Number of lines / assets in full rollout", 8,    "0",        "How many lines (Visual Inspection) or asset groups (PM) to scale to."),
]
for i, (label, val, fmt, note) in enumerate(pilot_inputs):
    r = 17 + i
    ws.cell(row=r, column=1, value=label); style_label(ws.cell(row=r, column=1))
    ws.cell(row=r, column=2, value=val); style_input(ws.cell(row=r, column=2), fmt=fmt)
    ws.cell(row=r, column=4, value=note); ws.cell(row=r, column=4).font = Font(name="Calibri", size=10, italic=True, color=INK_MUTE)
    ws.cell(row=r, column=4).alignment = Alignment(horizontal="left", vertical="center", indent=1, wrap_text=True)
    ws.cell(row=r, column=4).border = border_all

INP.update({
    "pilot_weeks":    "Inputs!$B$17",
    "pilot_fee":      "Inputs!$B$18",
    "scale_cost":     "Inputs!$B$19",
    "run_cost":       "Inputs!$B$20",
    "lines":          "Inputs!$B$21",
})

# ============================================================================
# SHEET 2: PILOT SIZING
# ============================================================================
ws2 = wb.create_sheet("Pilot Sizing")
ws2.column_dimensions["A"].width = 50
for c in ["B", "C", "D"]:
    ws2.column_dimensions[c].width = 18
ws2.column_dimensions["E"].width = 36

title_row(ws2, 1, "PILOT SIZING  ·  Two Recommended Pilots", span=5)

# --- PILOT 1: VISUAL INSPECTION ---
section_row(ws2, 3, "Pilot 1 — AI-based Visual Inspection (Recommended: HMGMA paint, IONIQ line)", span=5, fill="ECFDF5")
ws2.cell(row=4, column=1, value="Metric"); style_header(ws2.cell(row=4, column=1), fill=NAVY)
ws2.cell(row=4, column=2, value="Baseline"); style_header(ws2.cell(row=4, column=2), fill=NAVY)
ws2.cell(row=4, column=3, value="With AI"); style_header(ws2.cell(row=4, column=3), fill=NAVY)
ws2.cell(row=4, column=4, value="Annual Value"); style_header(ws2.cell(row=4, column=4), fill=NAVY)
ws2.cell(row=4, column=5, value="Logic"); style_header(ws2.cell(row=4, column=5), fill=NAVY)

vi_rows = [
    # (label, baseline_formula, ai_formula, value_formula, format, logic)
    ("Defect escapes per year",
     f"={INP['veh_day']}*{INP['days_yr']}*{INP['esc_rate']}",
     f"={INP['veh_day']}*{INP['days_yr']}*{INP['esc_rate']}*(1-0.60)",
     f"=(B5-C5)*{INP['warr']}",
     "#,##0",
     "−60% escape defects (deck benchmark)"),
    ("Rework events per year",
     f"={INP['veh_day']}*{INP['days_yr']}*{INP['rew_rate']}",
     f"={INP['veh_day']}*{INP['days_yr']}*{INP['rew_rate']}*(1-0.45)",
     f"=(B6-C6)*{INP['rework']}",
     "#,##0",
     "−45% rework cost (deck benchmark)"),
    ("Manual inspection labor (annualized USD)",
     f"=4*{INP['labor']}*8*{INP['days_yr']}",
     f"=2*{INP['labor']}*8*{INP['days_yr']}",
     f"=B7-C7",
     '"$"#,##0',
     "4 inspectors → 2 supervisors per shift"),
]
for i, (label, b, a, v, fmt, logic) in enumerate(vi_rows):
    r = 5 + i
    ws2.cell(row=r, column=1, value=label); style_label(ws2.cell(row=r, column=1))
    ws2.cell(row=r, column=2, value=b); style_calc(ws2.cell(row=r, column=2), fmt=fmt)
    ws2.cell(row=r, column=3, value=a); style_calc(ws2.cell(row=r, column=3), fmt=fmt)
    ws2.cell(row=r, column=4, value=v); style_calc(ws2.cell(row=r, column=4), fmt='"$"#,##0', bold=True, color=TEAL)
    ws2.cell(row=r, column=5, value=logic); style_label(ws2.cell(row=r, column=5))
    ws2.cell(row=r, column=5).font = Font(name="Calibri", size=10, italic=True, color=INK_MUTE)

# Pilot 1 summary
ws2.cell(row=9, column=1, value="Annual Value per Line (Pilot 1)"); style_label(ws2.cell(row=9, column=1), bold=True)
ws2.cell(row=9, column=4, value="=SUM(D5:D7)"); style_output(ws2.cell(row=9, column=4), fmt='"$"#,##0', fill=TEAL)

ws2.cell(row=10, column=1, value="Year-1 Investment (1 pilot)"); style_label(ws2.cell(row=10, column=1))
ws2.cell(row=10, column=4, value=f"={INP['pilot_fee']}"); style_calc(ws2.cell(row=10, column=4), fmt='"$"#,##0')

ws2.cell(row=11, column=1, value="Year-1 ROI (single-line pilot)"); style_label(ws2.cell(row=11, column=1), bold=True)
ws2.cell(row=11, column=4, value="=D9/D10"); style_output(ws2.cell(row=11, column=4), fmt='0.0"×"', fill=NAVY)

ws2.cell(row=12, column=1, value="Payback (months)"); style_label(ws2.cell(row=12, column=1))
ws2.cell(row=12, column=4, value="=D10/(D9/12)"); style_calc(ws2.cell(row=12, column=4), fmt='0.0" mo"', bold=True)

ws2.cell(row=13, column=1, value="Scaled value (full rollout, annual)"); style_label(ws2.cell(row=13, column=1), bold=True)
ws2.cell(row=13, column=4, value=f"=D9*{INP['lines']}"); style_output(ws2.cell(row=13, column=4), fmt='"$"#,##0', fill=TEAL)

# --- PILOT 2: PREDICTIVE MAINTENANCE ---
section_row(ws2, 15, "Pilot 2 — Predictive Maintenance (Recommended: Ulsan stamping + Asan welding)", span=5, fill="ECFDF5")
ws2.cell(row=16, column=1, value="Metric"); style_header(ws2.cell(row=16, column=1), fill=NAVY)
ws2.cell(row=16, column=2, value="Baseline"); style_header(ws2.cell(row=16, column=2), fill=NAVY)
ws2.cell(row=16, column=3, value="With AI"); style_header(ws2.cell(row=16, column=3), fill=NAVY)
ws2.cell(row=16, column=4, value="Annual Value"); style_header(ws2.cell(row=16, column=4), fill=NAVY)
ws2.cell(row=16, column=5, value="Logic"); style_header(ws2.cell(row=16, column=5), fill=NAVY)

pm_rows = [
    ("Unplanned downtime (hrs / year)",
     f"={INP['dt_curr']}*52",
     f"={INP['dt_curr']}*52*(1-0.40)",
     f"=(B17-C17)*60*{INP['dt_cost']}",
     "0.0",
     "−40% unplanned downtime (deck benchmark, 5:1 ROI)"),
    ("Reactive maintenance cost (annualized USD)",
     f"=12*8*{INP['labor']}*52",
     f"=12*8*{INP['labor']}*52*(1-0.30)",
     f"=B18-C18",
     '"$"#,##0',
     "−30% maintenance cost"),
    ("Asset lifespan extension (annualized USD)",
     "=2500000",
     "=2500000*(1+0.25)",
     "=C19-B19",
     '"$"#,##0',
     "+25% asset lifespan amortized over $2.5M typical asset"),
]
for i, (label, b, a, v, fmt, logic) in enumerate(pm_rows):
    r = 17 + i
    ws2.cell(row=r, column=1, value=label); style_label(ws2.cell(row=r, column=1))
    ws2.cell(row=r, column=2, value=b); style_calc(ws2.cell(row=r, column=2), fmt=fmt)
    ws2.cell(row=r, column=3, value=a); style_calc(ws2.cell(row=r, column=3), fmt=fmt)
    ws2.cell(row=r, column=4, value=v); style_calc(ws2.cell(row=r, column=4), fmt='"$"#,##0', bold=True, color=TEAL)
    ws2.cell(row=r, column=5, value=logic); style_label(ws2.cell(row=r, column=5))
    ws2.cell(row=r, column=5).font = Font(name="Calibri", size=10, italic=True, color=INK_MUTE)

ws2.cell(row=21, column=1, value="Annual Value per Line/Asset Group (Pilot 2)"); style_label(ws2.cell(row=21, column=1), bold=True)
ws2.cell(row=21, column=4, value="=SUM(D17:D19)"); style_output(ws2.cell(row=21, column=4), fmt='"$"#,##0', fill=TEAL)

ws2.cell(row=22, column=1, value="Year-1 Investment (1 pilot)"); style_label(ws2.cell(row=22, column=1))
ws2.cell(row=22, column=4, value=f"={INP['pilot_fee']}"); style_calc(ws2.cell(row=22, column=4), fmt='"$"#,##0')

ws2.cell(row=23, column=1, value="Year-1 ROI (single-pilot)"); style_label(ws2.cell(row=23, column=1), bold=True)
ws2.cell(row=23, column=4, value="=D21/D22"); style_output(ws2.cell(row=23, column=4), fmt='0.0"×"', fill=NAVY)

ws2.cell(row=24, column=1, value="Payback (months)"); style_label(ws2.cell(row=24, column=1))
ws2.cell(row=24, column=4, value="=D22/(D21/12)"); style_calc(ws2.cell(row=24, column=4), fmt='0.0" mo"', bold=True)

ws2.cell(row=25, column=1, value="Scaled value (full rollout, annual)"); style_label(ws2.cell(row=25, column=1), bold=True)
ws2.cell(row=25, column=4, value=f"=D21*{INP['lines']}"); style_output(ws2.cell(row=25, column=4), fmt='"$"#,##0', fill=TEAL)

# --- COMBINED 3-YEAR NPV ---
section_row(ws2, 27, "Combined 3-Year NPV — Both Pilots Scaled", span=5, fill="FEF3C7")
ws2.cell(row=28, column=1, value="Year"); style_header(ws2.cell(row=28, column=1), fill=NAVY)
ws2.cell(row=28, column=2, value="Investment"); style_header(ws2.cell(row=28, column=2), fill=NAVY)
ws2.cell(row=28, column=3, value="Annual Value"); style_header(ws2.cell(row=28, column=3), fill=NAVY)
ws2.cell(row=28, column=4, value="Net Cashflow"); style_header(ws2.cell(row=28, column=4), fill=NAVY)
ws2.cell(row=28, column=5, value="Discounted"); style_header(ws2.cell(row=28, column=5), fill=NAVY)

# Year 1: both pilots + initial scale rollout cost
ws2.cell(row=29, column=1, value="Year 1 (Pilots + initial scale)"); style_label(ws2.cell(row=29, column=1))
ws2.cell(row=29, column=2, value=f"=2*{INP['pilot_fee']}+{INP['scale_cost']}*{INP['lines']}"); style_calc(ws2.cell(row=29, column=2), fmt='"$"#,##0')
ws2.cell(row=29, column=3, value="=(D13+D25)/2"); style_calc(ws2.cell(row=29, column=3), fmt='"$"#,##0')  # half-year scaled value
ws2.cell(row=29, column=4, value="=C29-B29"); style_calc(ws2.cell(row=29, column=4), fmt='"$"#,##0')
ws2.cell(row=29, column=5, value=f"=D29/((1+{INP['wacc']})^1)"); style_calc(ws2.cell(row=29, column=5), fmt='"$"#,##0', bold=True)

ws2.cell(row=30, column=1, value="Year 2 (Full operation)"); style_label(ws2.cell(row=30, column=1))
ws2.cell(row=30, column=2, value=f"=2*{INP['run_cost']}"); style_calc(ws2.cell(row=30, column=2), fmt='"$"#,##0')
ws2.cell(row=30, column=3, value="=D13+D25"); style_calc(ws2.cell(row=30, column=3), fmt='"$"#,##0')
ws2.cell(row=30, column=4, value="=C30-B30"); style_calc(ws2.cell(row=30, column=4), fmt='"$"#,##0')
ws2.cell(row=30, column=5, value=f"=D30/((1+{INP['wacc']})^2)"); style_calc(ws2.cell(row=30, column=5), fmt='"$"#,##0', bold=True)

ws2.cell(row=31, column=1, value="Year 3 (Full operation)"); style_label(ws2.cell(row=31, column=1))
ws2.cell(row=31, column=2, value=f"=2*{INP['run_cost']}"); style_calc(ws2.cell(row=31, column=2), fmt='"$"#,##0')
ws2.cell(row=31, column=3, value="=D13+D25"); style_calc(ws2.cell(row=31, column=3), fmt='"$"#,##0')
ws2.cell(row=31, column=4, value="=C31-B31"); style_calc(ws2.cell(row=31, column=4), fmt='"$"#,##0')
ws2.cell(row=31, column=5, value=f"=D31/((1+{INP['wacc']})^3)"); style_calc(ws2.cell(row=31, column=5), fmt='"$"#,##0', bold=True)

ws2.cell(row=33, column=1, value="3-YEAR NPV (BOTH PILOTS, SCALED)"); style_label(ws2.cell(row=33, column=1), bold=True)
ws2.cell(row=33, column=5, value="=SUM(E29:E31)"); style_output(ws2.cell(row=33, column=5), fmt='"$"#,##0', fill=TEAL)
ws2.cell(row=33, column=5).font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
ws2.row_dimensions[33].height = 30

# ============================================================================
# SHEET 3: FULL USE CASES (parametric)
# ============================================================================
ws3 = wb.create_sheet("Full Use Cases")
ws3.column_dimensions["A"].width = 36
for c in ["B", "C", "D", "E", "F"]:
    ws3.column_dimensions[c].width = 16
ws3.column_dimensions["G"].width = 40

title_row(ws3, 1, "ALL 8 USE CASES  ·  Per-Line Annual Value Estimates", span=7)
ws3.cell(row=3, column=1, value="Use Case"); style_header(ws3.cell(row=3, column=1), fill=NAVY)
ws3.cell(row=3, column=2, value="Driver (per line)"); style_header(ws3.cell(row=3, column=2), fill=NAVY)
ws3.cell(row=3, column=3, value="Improvement %"); style_header(ws3.cell(row=3, column=3), fill=NAVY)
ws3.cell(row=3, column=4, value="Baseline Cost"); style_header(ws3.cell(row=3, column=4), fill=NAVY)
ws3.cell(row=3, column=5, value="Annual Value"); style_header(ws3.cell(row=3, column=5), fill=NAVY)
ws3.cell(row=3, column=6, value="Scaled (× lines)"); style_header(ws3.cell(row=3, column=6), fill=NAVY)
ws3.cell(row=3, column=7, value="Hyundai Anchor"); style_header(ws3.cell(row=3, column=7), fill=NAVY)

use_cases = [
    ("UC-01 Visual Inspection",
     "Escape defect warranty cost",
     0.60,
     f"={INP['veh_day']}*{INP['days_yr']}*{INP['esc_rate']}*{INP['warr']}",
     "HMGMA · IONIQ paint shop"),
    ("UC-02 Variant Confirmation",
     "Wrong-variant rework events",
     0.70,
     f"={INP['veh_day']}*{INP['days_yr']}*0.005*{INP['rework']}*4",
     "High-variant Tucson trim lines · Genesis"),
    ("UC-03 Seating & Component Validation",
     "Fitment-related recall risk",
     0.85,
     "=2000000",
     "Final assembly · all passenger lines"),
    ("UC-04 SOP Compliance",
     "Final-stage defect leakage",
     0.40,
     f"={INP['veh_day']}*{INP['days_yr']}*0.008*{INP['warr']}",
     "Complex assembly cells · Genesis"),
    ("UC-05 Predictive Quality",
     "Scrap + rework cost",
     0.35,
     f"={INP['veh_day']}*{INP['days_yr']}*{INP['rew_rate']}*{INP['rework']}",
     "Body-in-white · welding shops"),
    ("UC-06 Predictive Maintenance",
     "Unplanned downtime cost",
     0.40,
     f"={INP['dt_curr']}*52*60*{INP['dt_cost']}",
     "Ulsan stamping · Asan welding"),
    ("UC-07 Safety Monitoring",
     "Incident + EHS exposure",
     0.55,
     "=1500000",
     "Plant-wide · HMMA / HMI / HMMC rollout pattern"),
    ("UC-08 Digital Traceability",
     "Recall investigation + audit",
     0.70,
     "=3000000",
     "Cross-plant supply chain · component genealogy"),
]
for i, (uc, driver, pct, baseline, anchor) in enumerate(use_cases):
    r = 4 + i
    ws3.cell(row=r, column=1, value=uc); style_label(ws3.cell(row=r, column=1), bold=True)
    ws3.cell(row=r, column=2, value=driver); style_label(ws3.cell(row=r, column=2))
    ws3.cell(row=r, column=3, value=pct); style_calc(ws3.cell(row=r, column=3), fmt="0.0%", bold=True)
    ws3.cell(row=r, column=4, value=baseline); style_calc(ws3.cell(row=r, column=4), fmt='"$"#,##0')
    ws3.cell(row=r, column=5, value=f"=C{r}*D{r}"); style_calc(ws3.cell(row=r, column=5), fmt='"$"#,##0', bold=True, color=TEAL)
    ws3.cell(row=r, column=6, value=f"=E{r}*{INP['lines']}"); style_output(ws3.cell(row=r, column=6), fmt='"$"#,##0', fill=TEAL)
    ws3.cell(row=r, column=7, value=anchor); style_label(ws3.cell(row=r, column=7))
    ws3.cell(row=r, column=7).font = Font(name="Calibri", size=10, italic=True, color=INK_MUTE)

# Totals
total_row = 4 + len(use_cases) + 1
ws3.cell(row=total_row, column=1, value="TOTAL — All 8 Use Cases, Scaled"); style_label(ws3.cell(row=total_row, column=1), bold=True)
ws3.cell(row=total_row, column=5, value=f"=SUM(E4:E{4 + len(use_cases) - 1})"); style_output(ws3.cell(row=total_row, column=5), fmt='"$"#,##0', fill=NAVY)
ws3.cell(row=total_row, column=6, value=f"=SUM(F4:F{4 + len(use_cases) - 1})"); style_output(ws3.cell(row=total_row, column=6), fmt='"$"#,##0', fill=TEAL)
ws3.row_dimensions[total_row].height = 28

# ============================================================================
# SHEET 4: NOTES
# ============================================================================
ws4 = wb.create_sheet("Notes")
ws4.column_dimensions["A"].width = 110

title_row(ws4, 1, "ASSUMPTIONS  ·  SOURCES  ·  SENSITIVITY", span=1)

notes = [
    "",
    "PURPOSE",
    "This workbook lets Hyundai stakeholders enter their own line economics and see the resulting",
    "ROI for the two recommended pilots (Visual Inspection + Predictive Maintenance) and for all",
    "eight use cases in the AI for Plant Operations deck. Yellow cells in the Inputs tab are editable.",
    "All other cells are formulas.",
    "",
    "DEFAULT VALUES — SOURCES",
    "• Vehicles per day (1,600) — single high-volume line at Ulsan-scale plant; ~400K vehicles/year per line.",
    "• Production days (300) — standard automotive year less planned shutdowns.",
    "• Downtime cost ($22,000/min) — automotive industry standard for high-volume final-assembly lines.",
    "• Downtime baseline (6.4 hrs/week) — anchored on the Global EV manufacturer reference case from the deck.",
    "• Defect escape rate (1.2%) and rework rate (8%) — pre-AI baselines from Tier-1 OEM paint shop reference case.",
    "• Improvement percentages — taken from in-production outcome ranges of comparable AI deployments; same",
    "  ranges shown in the use case slides of the companion deck.",
    "",
    "WHAT THIS DOES NOT MODEL",
    "• One-time Hyundai-side capex on Hyundai-owned infrastructure (cameras, gateways) — varies by line and",
    "  is part of pilot scoping.",
    "• Brand / warranty halo from quality improvements — real but hard to quantify precisely; treat as upside.",
    "• Strategic optionality: foundation for the other six use cases. Pilots 1 & 2 create the data + integration",
    "  scaffolding that compresses time-to-deploy for UCs 02, 03, 04, 05, 07, 08.",
    "",
    "SENSITIVITY",
    "The single largest swing variable is unplanned downtime cost per minute. Halving it (to $11K) cuts",
    "Pilot 2's value roughly in half; doubling it (to $44K) roughly doubles it. The model is conservative",
    "against the industry-standard figure.",
    "",
    "USE IN THE MEETING",
    "Open this workbook with Hyundai's operations / finance counterpart present. Walk the Inputs sheet,",
    "let them overwrite defaults with their internal numbers, and watch the Pilot Sizing and Full Use Cases",
    "sheets recalculate live. Make the recommendation feel inevitable: 'These are your numbers, not ours.'",
]
for i, line in enumerate(notes):
    r = 3 + i
    c = ws4.cell(row=r, column=1, value=line)
    if line in ("PURPOSE", "DEFAULT VALUES — SOURCES", "WHAT THIS DOES NOT MODEL", "SENSITIVITY", "USE IN THE MEETING"):
        c.font = Font(name="Calibri", size=12, bold=True, color=NAVY)
    else:
        c.font = Font(name="Calibri", size=11, color=INK)
    c.alignment = Alignment(horizontal="left", vertical="top", indent=1, wrap_text=True)

# ============================================================================
# SAVE
# ============================================================================
out = "ROI_Calculator_Hyundai.xlsx"
wb.save(out)
print(f"Saved: {out}")
print(f"Sheets: {wb.sheetnames}")
