---
name: customer-facing-review
description: >-
  Use before finalizing any customer-facing deliverable. Reviews deck content,
  architecture slides, and executive briefs for internal tool leaks and
  Hyundai framing compliance.
paths:
  - build_*.py
  - build_*.js
  - "*.drawio"
  - executive_brief.*
---

# Customer-Facing Review

Pre-ship review skill. Run this before any deliverable goes to Hyundai.

## Checklist

1. **No internal tool mentions.** Search all output text for: graphify,
   knowledge graph, nodes indexed, Obsidian, second brain, content research,
   ingestion pipeline. None of these should appear.
2. **Hyundai framing.** Every capability should be framed as solving a Hyundai
   plant problem, not as a generic AI feature.
3. **ROI consistency.** All cost/benefit figures must trace back to
   `ROI_Calculator_Hyundai.xlsx`. No invented numbers.
4. **Plant specificity.** At least 3 slides should reference specific Hyundai
   plants by name with relevant use case examples.
5. **Architecture accuracy.** Diagram references in slides must match the
   current `.drawio` source files. No stale screenshots.
6. **Confidentiality footer.** Every slide must include "Confidential -
   PeopleTech" in the footer.

## How to run

Read through the build script output strings and flag any violations.
Report findings as a numbered list with file:line references.
