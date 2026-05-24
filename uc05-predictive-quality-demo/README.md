# UC05 Predictive Quality Demo

Interactive static implementation demo for realizing one Hyundai/PeopleTech use
case: UC05 Predictive Quality for Software-Defined Factory lines.

Open `index.html` in a browser. No build step is required.

For the full-stack version, run the backend too:

```bash
python3 backend/server.py
```

Then use the **Real backend** panel in the UI to check the API, score events
through SQLite-backed endpoints, and load persisted plant data.

## Demo Story

The buyer sees a simulated SDF line where active vehicle variants change quality
thresholds in real time. The app scores actual synthetic vehicle events through
`quality-engine.js`, records MES gate decisions, and exports the event log as
JSON.

Core mechanics:

- variant-specific station tolerance schema in `demo-data.js`,
- synthetic unit generation with line-speed pressure and transition drift,
- station-level z-score, threshold, volatility, and drift scoring,
- aggregate MES decision: continue, inspect next unit, or hold and rework,
- live vehicle-event table and JSON export.
- generated incident reports and retraining briefs in `artifact-service.js`,
- threshold/model version history for governance-style review,
- an agent build console that mirrors the plan, implement, cleanup, review loop.

The right side of the app shows how an OpenHands-inspired agent workflow would
build this faster:

- schema agent,
- training agent,
- edge optimization agent,
- MES connector agent,
- review loop agent.

## Local Source Inputs

- `hyundai-ml-pipeline-strategy.md`
- `hyundai-ml-pipeline-meeting-prep.md`
- `build_ml_pipeline_deck.js`
- `second-brain/github/openhands-openhands.md`
- `uc05-predictive-quality-demo/reference-context/openhands-patterns.md`

## External References

- https://github.com/OpenHands/OpenHands
- https://github.com/OpenHands/OpenHands/blob/main/AGENTS.md
- https://github.com/pawel-cell/micky-podcast-agentic-engineering/blob/main/skills/agentic-engineering-workflow/SKILL.md
- https://github.com/pawel-cell/micky-podcast-agentic-engineering/blob/main/skills/code-structure-cleanup/SKILL.md
- https://github.com/pawel-cell/micky-podcast-agentic-engineering/blob/main/skills/grep-loop-review-workflow/SKILL.md
