# Hyundai PeopleTech Deck — Codebase Map

A lightweight map so an agent can find where content lives before exploring.

## Top level

| Path | What it is |
|------|------------|
| Root `.py/.js/.sh` | Build scripts — each generates one deliverable |
| Root `.drawio` | Architecture diagram sources (draw.io XML) |
| Root `.pptx/.docx/.xlsx` | Generated presentation artifacts — outputs, not sources |
| `second-brain/` | Content research notes organized by source platform |
| `graphify-out/` | Knowledge graph outputs (internal only) |
| `helpline-reference/` | Reference example of AI Layer harness (coleam00/helpline) |

## Build scripts → outputs

| Script | Output | What it builds |
|--------|--------|----------------|
| `build_pptx.py` | `Hyundai_PeopleTech_AI_Plant_Operations.pptx` | Main capability deck |
| `build_deck_v2.py` | `PeopleTech_AI_Engineering_Team_Hyundai.pptx` | Engineering team deck |
| `build_architecture_pptx.js` | `ai-plant-operations-architecture.pptx` | Platform architecture slides |
| `build_mlops_pptx.js` | `mlops-pipeline-architecture.pptx` | MLOps pipeline slides |
| `build_uc_diagrams.sh` | `uc01–uc08` drawio files | 8 use case architecture diagrams |
| `build_docx.py` | `executive_brief.docx` | Executive summary document |
| `build_roi.py` | `ROI_Calculator_Hyundai.xlsx` | ROI calculation spreadsheet |

## second-brain/

| Subdirectory | Source | Content type |
|-------------|--------|--------------|
| `github/` | GitHub repos | Technical architecture notes |
| `linkedin/` | LinkedIn posts | Industry insights |
| `web/` | Web articles | Research and benchmarks |
| `youtube/` | YouTube videos | Tutorial and strategy notes |

## Architecture diagrams (use cases)

| File | Use case |
|------|----------|
| `uc01-visual-inspection-architecture.drawio` | Visual inspection |
| `uc02-variant-confirmation-architecture.drawio` | Variant confirmation |
| `uc03-seating-validation-architecture.drawio` | Seating validation |
| `uc04-sop-compliance-architecture.drawio` | SOP compliance |
| `uc05-predictive-quality-architecture.drawio` | Predictive quality |
| `uc06-predictive-maintenance-architecture.drawio` | Predictive maintenance |
| `uc07-safety-monitoring-architecture.drawio` | Safety monitoring |
| `uc08-digital-traceability-architecture-v2.drawio` | Digital traceability |

## Finding content

- **A deck or slide** → check `CODEBASE_MAP.md` build scripts table above
- **Architecture for a use case** → `uc0X-*.drawio` at root
- **Research on a topic** → `second-brain/<platform>/` notes
- **ROI or cost figures** → `ROI_Calculator_Hyundai.xlsx` + `build_roi.py`
