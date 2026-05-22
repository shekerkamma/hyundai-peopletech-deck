---
name: deck-builder
description: >-
  Use when creating or modifying PowerPoint build scripts (build_pptx.py,
  build_deck_v2.py, build_architecture_pptx.js, etc.). Enforces PeopleTech's
  deck conventions and Hyundai framing rules.
paths:
  - build_*.py
  - build_*.js
  - build_*.sh
---

# Deck Builder

Activates for work on any build script that generates presentation artifacts.

## Rules (load these every time)

1. **Customer framing only.** Every slide frames AI capabilities as solving
   Hyundai plant problems. Never mention PeopleTech internal tools, research
   methodology, or knowledge graphs.
2. **Use python-pptx for .pptx generation in Python.** Node scripts use
   `pptxgenjs`. Do not mix the two in one script.
3. **Hyundai plant anchors.** Reference specific plants (Ulsan, Asan, HMGMA
   Metaplant America, HMMA, HMMC, HMI) in examples and deployment scenarios.
4. **ROI figures come from the calculator.** Never hard-code cost/benefit
   numbers. Reference `ROI_Calculator_Hyundai.xlsx` or `build_roi.py` for
   the source of truth.
5. **One script = one deliverable.** Each build script produces exactly one
   output file. Scripts are not libraries — do not import between them.

## When you need the detail

For the full slide structure conventions and color palette, read
[references/deck-conventions.md](references/deck-conventions.md).
