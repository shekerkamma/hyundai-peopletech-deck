---
name: architecture-diagram
description: >-
  Use when creating or modifying draw.io architecture diagrams for use cases
  (uc01-uc08) or platform-level architecture. Enforces diagram conventions.
paths:
  - "*.drawio"
  - ai-plant-operations-architecture.*
  - mlops-pipeline-architecture.*
---

# Architecture Diagram

Activates for work on draw.io diagram files.

## Rules

1. **Draw.io XML format.** All architecture diagrams are `.drawio` files
   (standard draw.io/diagrams.net XML). Do not use other diagram formats.
2. **Layer structure.** Use named layers: `Infrastructure`, `Data Flow`,
   `AI/ML Pipeline`, `Integration`, `Annotations`.
3. **Use case naming.** Files follow `uc0X-<name>-architecture.drawio` pattern.
   Keep the numbering consistent with the 8 use cases.
4. **Edge labels.** Every data flow arrow must have a label describing what
   moves (e.g., "sensor telemetry", "inference results", "alert notification").
5. **Hyundai systems.** Reference real Hyundai systems where possible: MES,
   GQMS (Global Quality Management System), HMG Connect, Ioniq platform.

## Reference

For the full list of use cases and their architecture patterns, read
[references/use-case-index.md](references/use-case-index.md).
