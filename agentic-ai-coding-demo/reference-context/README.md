# Reference Context Workspace

Use this folder for local copies of external repositories that should guide an
AI coding agent.

Suggested layout:

```text
reference-context/
  repos/
    micky-podcast-agentic-engineering/
      skills/
        agentic-engineering-workflow/SKILL.md
        code-structure-cleanup/SKILL.md
        grep-loop-review-workflow/SKILL.md
    michaelshimeles-skills/
      ...
```

When prompting an agent, reference the smallest relevant file or folder instead
of dumping an entire repository into context.

Example:

```md
Before editing, inspect:
- agentic-ai-coding-demo/reference-context/repos/micky-podcast-agentic-engineering/skills/code-structure-cleanup/SKILL.md
- tooling/peopletech-ai-layer/skills/customer-facing-review/SKILL.md

Then implement only the requested feature and run the relevant checks.
```
