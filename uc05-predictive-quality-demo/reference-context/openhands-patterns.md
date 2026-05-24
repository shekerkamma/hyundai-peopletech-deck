# OpenHands Patterns Used By This Demo

This is not a vendored copy of OpenHands. It is a compact reference pack for
prompting an agent to build the UC05 demo with OpenHands-style discipline.

## Repository Guidance Pattern

OpenHands uses an `AGENTS.md` file to tell agents how the repository is
structured, how to run setup, and which checks matter before pushing. For this
repo, the equivalent inputs are:

- `CLAUDE.md`
- `CODEBASE_MAP.md`
- `tooling/peopletech-ai-layer/skills/customer-facing-review/SKILL.md`
- this demo's `README.md`

## Skills / Microagent Pattern

OpenHands describes microagents as markdown files with optional frontmatter and
trigger keywords. This maps directly to the public `SKILL.md` examples from the
agentic engineering workflow:

- use skills to inject domain knowledge only when relevant,
- keep the skill concise enough for the agent to actually use,
- reference source code or exact files instead of broad prose summaries.

## Demo Build Mapping

- CodeAct-style agent: generate the station scoring and MES decision mechanics.
- Docker workspace idea: keep generated ML experiments isolated from customer
  presentation materials.
- Multi-agent delegation: split schema, training, edge optimization, connector,
  and review tasks.
- Review loop: iterate only on the UC05 diff until objective checks pass.

## Prompt Rule

Before coding, inspect the smallest relevant local files:

```md
Read:
- hyundai-ml-pipeline-strategy.md
- build_ml_pipeline_deck.js
- second-brain/github/openhands-openhands.md
- uc05-predictive-quality-demo/reference-context/openhands-patterns.md

Then implement one reviewable change.
```
