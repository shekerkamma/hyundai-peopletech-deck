# Hyundai PeopleTech Deck

Pre-sales capability deck workspace for PeopleTech's AI plant operations pitch to Hyundai Motor Group. Monorepo: build scripts, architecture diagrams, research notes, and presentation outputs.

This root file is intentionally lean — it holds only what's true everywhere.
Each subdirectory has its own `CLAUDE.md` with local conventions;
Claude loads them automatically as it moves into that directory.

## Where things live

See `CODEBASE_MAP.md` for the full tree. Top level:

- `second-brain/` — content research notes ingested from YouTube, LinkedIn, GitHub, web
- `graphify-out/` — knowledge graph outputs (internal tooling, never customer-facing)
- Root `.py` / `.js` / `.sh` — build scripts that generate `.pptx`, `.docx`, `.xlsx`
- Root `.drawio` — editable architecture diagrams (draw.io XML)
- Root `.pptx` / `.docx` / `.xlsx` — generated presentation artifacts

## Critical gotchas (repo-wide)

- **Customer-facing materials must NEVER mention internal tools.** No graphify, knowledge graphs, nodes indexed, Obsidian, or internal research methodology. These are invisible accelerators — the audience sees PeopleTech capabilities and Hyundai solutions only.
- **Money and ROI figures use the ROI Calculator.** `ROI_Calculator_Hyundai.xlsx` is the single source of truth for all cost/benefit claims in decks.
- **Architecture diagrams come in pairs.** `.drawio` (editable source) + `.pptx` or `.png` (generated output). Edit the `.drawio`, regenerate the output.
- **Build scripts are one-shot generators.** `build_pptx.py`, `build_deck_v2.py`, `build_architecture_pptx.js`, etc. each produce a specific `.pptx`. They are not libraries — do not import them from each other.
- **Navigate by content type, not by service.** This is a presentation workspace, not a running application. Find things by what they produce (deck, diagram, research note).

## Commands

```bash
python build_pptx.py                    # main deck
python build_deck_v2.py                 # v2 engineering team deck
node build_architecture_pptx.js         # architecture slides
node build_mlops_pptx.js                # MLOps pipeline slides
bash build_uc_diagrams.sh               # all 8 use case diagrams
python build_docx.py                    # executive brief
python build_roi.py                     # ROI calculator
```
