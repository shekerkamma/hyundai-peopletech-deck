# Hyundai × PeopleTech — AI for Plant Operations

A 15-slide HTML pitch deck for PeopleTech's pre-sales engagement with Hyundai, covering 8 AI use cases for plant operations: visual inspection, variant confirmation, seating validation, SOP compliance, predictive quality, predictive maintenance, safety monitoring, and digital traceability.

Self-contained single-file deck. No build step, no dependencies.

## View

```bash
# Open directly in browser
xdg-open index.html        # Linux
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
# Each slide will land on its own page via @page CSS rules
```

## Deck structure

| # | Slide | Purpose |
|---|-------|---------|
| 01 | Cover | Title, partners, outcome chips |
| 02 | Why PeopleTech for Hyundai | Pre-sales positioning |
| 03 | Engagement Approach | Discovery → Pilot → Scale → Run |
| 04 | UC-01: AI-based Visual Inspection | Computer Vision + Deep Learning |
| 05 | UC-02: Model & Variant Confirmation | VIN/barcode + BOM matching |
| 06 | UC-03: Seating & Component Validation | Vision AI fitment |
| 07 | UC-04: SOP Compliance Monitoring | Pose estimation + workflow match |
| 08 | UC-05: Predictive Quality Analytics | Sensor ML for defect prediction |
| 09 | UC-06: Predictive Maintenance | Vibration + acoustic ML |
| 10 | UC-07: AI Safety Monitoring | PPE + restricted zones |
| 11 | UC-08: Digital Traceability & Tracking | RFID + vision + genealogy graph |
| 12 | Reference Case Studies | 4 anonymized engagement summaries |
| 13 | Accelerators & Frameworks | 6 reusable PeopleTech assets |
| 14 | AI Computer Vision Capabilities | Model × maturity × use case matrix |
| 15 | Strategic Summary + CTA | Recommended pilot + next step |

Each use case slide extends the original reference template with a **Solution Stack & Architecture** strip spanning the bottom — four columns mapping Edge / Capture → Compute / AI Models → Integration → UX / Decision.

## Editing

The entire deck is in `index.html` (one file, ~67 KB). To change a slide, search for the `<!-- SLIDE N -->` comment and edit the section below it. Design tokens are at the top of the `<style>` block:

```css
:root {
  --navy-800: #1a2754;   /* primary brand */
  --teal:     #14a085;   /* accent 1 */
  --orange:   #d97706;   /* accent 2 */
  --purple:   #7c3aed;   /* accent 3 */
  --red:      #dc2626;   /* accent 4 */
}
```

## Confidentiality

Footer reads "CONFIDENTIAL" on every slide. Replace or remove in the `.uc-footer` rules / per-slide footers if making this a public artifact.
