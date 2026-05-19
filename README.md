# Hyundai × PeopleTech — AI for Plant Operations

A complete pre-sales bundle for PeopleTech's engagement with Hyundai, covering 8 AI use cases for plant operations: visual inspection, variant confirmation, seating validation, SOP compliance, predictive quality, predictive maintenance, safety monitoring, and digital traceability.

Contextualized for Hyundai's actual plant network — Ulsan, Asan, HMGMA Metaplant America (IONIQ 5 / IONIQ 9), HMMA, HMMC, HMI — with explicit recommended pilot anchors and Hyundai-specific positioning against AIRS Company, HMGICS, and Boston Dynamics.

## Bundle contents

| File | What it is | Use it for |
|------|-----------|-----------|
| `executive_brief.docx` | One-page Word memo (~900 words) | **Email this first** to the Hyundai sponsor 5 minutes before the meeting |
| `executive_brief.md` | Same brief, markdown source | Edit / port to other formats |
| `index.html` | 17-slide HTML deck (incl. 2 architecture appendix slides) | Best-fidelity browser preview, PDF export, design source of truth |
| `Hyundai_PeopleTech_AI_Plant_Operations.pptx` | 17-slide native PowerPoint, 16:9 | Email, edit in PowerPoint / Keynote / Google Slides, in-meeting walkthrough |
| `ROI_Calculator_Hyundai.xlsx` | Interactive Excel workbook | **Open with finance / ops in the room.** Yellow input cells; live recalculation; per-pilot value + 3-year NPV |
| `architecture_visual_inspection.svg` (+ .png) | Pilot 1 reference architecture | Send to plant-floor engineers; pin to a printed wall in the war room |
| `architecture_predictive_maintenance.svg` (+ .png) | Pilot 2 reference architecture | Same — print and walk it with the maintenance team |

Generators: `build_pptx.py`, `build_docx.py`, `build_roi.py`. Run any of these to regenerate the corresponding artifact after content edits.

## Recommended distribution flow

1. **T-1 day:** email **`executive_brief.docx`** to the Hyundai sponsor
2. **In the meeting:** walk the **PowerPoint** (or HTML if projecting from a laptop)
3. **During Q&A on value:** open **`ROI_Calculator_Hyundai.xlsx`** and let Hyundai overwrite the yellow input cells with their own line economics — recalculates live
4. **For engineering follow-up:** send the **2 architecture SVGs** to the plant-floor team
5. **For the scoping workshop:** all artifacts together as a single zip / SharePoint folder

## View the HTML deck

```bash
# Open directly in browser
xdg-open index.html        # Linux / WSL
open index.html            # macOS
start index.html           # Windows

# Or serve over HTTP (recommended — some browsers restrict file:// for fonts)
python3 -m http.server 8765
# then visit http://127.0.0.1:8765
```

**Keyboard navigation:** `← →` or `↑ ↓` or `PageUp / PageDown` to move; `Home` / `End` to jump to first / last slide; or just scroll.

## Export to PDF

```bash
# Headless Chrome (best — preserves CSS gradients and shadows)
chromium --headless --disable-gpu --no-sandbox \
  --print-to-pdf=hyundai-peopletech-deck.pdf \
  --print-to-pdf-no-header --no-pdf-header-footer \
  --virtual-time-budget=5000 \
  http://127.0.0.1:8765/

# Or print from a regular browser (Cmd/Ctrl + P) — pick "Save as PDF"
```

## Deck structure (17 slides)

| # | Slide | Purpose |
|---|-------|---------|
| 01 | Cover | Title, partners, outcome chips |
| 02 | Why PeopleTech for Hyundai | Pre-sales positioning + HMGICS / AIRS / Boston Dynamics complement |
| 03 | Engagement Approach | Discovery → Pilot → Scale → Run, scaled to Ulsan + HMGMA cadence |
| 04 | UC-01: AI-based Visual Inspection | + Recommended Hyundai start: HMGMA IONIQ paint shop |
| 05 | UC-02: Model & Variant Confirmation | VIN/barcode + BOM matching |
| 06 | UC-03: Seating & Component Validation | Vision AI fitment |
| 07 | UC-04: SOP Compliance Monitoring | Pose estimation + workflow match |
| 08 | UC-05: Predictive Quality Analytics | Sensor ML for defect prediction |
| 09 | UC-06: Predictive Maintenance | + Recommended Hyundai start: Ulsan stamping + Asan welding |
| 10 | UC-07: AI Safety Monitoring | PPE + restricted zones |
| 11 | UC-08: Digital Traceability & Tracking | RFID + vision + genealogy graph |
| 12 | Reference Case Studies | 4 anonymized engagement summaries |
| 13 | Accelerators & Frameworks | 6 reusable PeopleTech assets |
| 14 | AI Computer Vision Capabilities | Model × maturity × use case matrix |
| 15 | Strategic Summary + CTA | Recommended pilots anchored at HMGMA + Ulsan / Asan |
| 16 | **Appendix · Pilot 1 Architecture** | Full reference architecture for Visual Inspection |
| 17 | **Appendix · Pilot 2 Architecture** | Full reference architecture for Predictive Maintenance |

Each use case slide extends the original reference template with a **Solution Stack & Architecture** strip spanning the bottom — four columns mapping Edge / Capture → Compute / AI Models → Integration → UX / Decision. Slides 04 and 09 additionally show a **Recommended Hyundai Start** card identifying the specific plant / line PeopleTech recommends as the pilot site.

## ROI Calculator usage

`ROI_Calculator_Hyundai.xlsx` contains four sheets:

1. **Inputs** — Yellow cells: edit Hyundai's actual line economics (vehicles/day, ASP, downtime cost, defect rate, etc.). Pre-filled with Ulsan-scale defaults (~1,600 vehicles/day single line).
2. **Pilot Sizing** — Per-line value math for the two recommended pilots, payback months, and combined 3-year NPV.
3. **Full Use Cases** — All 8 use cases parametrized with the improvement % from the deck benchmarks.
4. **Notes** — Assumptions, sources, sensitivity, and instructions for using this in the meeting.

The single largest swing variable is **unplanned downtime cost per minute** — sensitivity discussion in the Notes sheet.

## Editing

Each artifact has a generator script. Edit content, then regenerate:

```bash
python3 build_pptx.py   # → Hyundai_PeopleTech_AI_Plant_Operations.pptx
python3 build_docx.py   # → executive_brief.docx
python3 build_roi.py    # → ROI_Calculator_Hyundai.xlsx

# Architecture SVGs are hand-authored; to update PNGs after editing SVGs:
python3 -c "import cairosvg; cairosvg.svg2png(url='architecture_visual_inspection.svg', write_to='architecture_visual_inspection.png', output_width=2400); cairosvg.svg2png(url='architecture_predictive_maintenance.svg', write_to='architecture_predictive_maintenance.png', output_width=2400)"
```

The HTML deck (`index.html`) is hand-edited — search for `<!-- SLIDE N -->` to find the section you want.

Design tokens (top of HTML `<style>` and top of each Python generator):

```
navy-800  #1a2754   primary brand
teal      #14a085   accent 1 (Visual Inspection, traceability, Hyundai-start highlight)
orange    #d97706   accent 2 (Variant Confirmation)
purple    #7c3aed   accent 3 (Seating Validation)
red       #dc2626   accent 4 (Predictive Quality)
```

## Confidentiality

Footer reads "CONFIDENTIAL" on every slide. All Hyundai references are derived from publicly available information (Hyundai's announced plants, the IONIQ E-GMP platform, the HMGICS facility, AIRS Company, Boston Dynamics acquisition). Replace or remove "CONFIDENTIAL" footer per PeopleTech's distribution policy.
