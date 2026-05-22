---
name: content-research-ingest
description: >-
  Use when ingesting new research content into second-brain/ from YouTube,
  LinkedIn, GitHub, or web sources. Enforces note formatting and filing.
paths:
  - second-brain/**
---

# Content Research Ingest

Activates for work in the `second-brain/` research directory.

## Rules

1. **One file per source.** Each ingested piece of content gets its own markdown
   file in the appropriate platform subdirectory.
2. **File naming.** Use kebab-case slugs: `topic-name.md` or
   `author-topic-name.md`.
3. **Frontmatter.** Every note should start with source URL, date ingested,
   and a 1-line summary.
4. **Extract actionable insights.** Focus on: technical architecture details,
   ROI data points, competitor approaches, integration patterns, and Hyundai-
   relevant manufacturing AI examples.
5. **Flag customer-usable content.** Mark sections that can inform deck slides
   with `<!-- deck-usable -->` comments.
6. **Internal tools stay invisible.** Notes may reference how graphify or
   knowledge graphs were used to process the content, but tag those sections
   with `<!-- internal-only -->` so they are never pulled into deck materials.

## Platform subdirectories

| Directory | Source | Focus |
|-----------|--------|-------|
| `github/` | GitHub repos, READMEs | Technical architecture, code patterns |
| `linkedin/` | LinkedIn posts, articles | Industry trends, competitor moves |
| `web/` | Blog posts, documentation | Benchmarks, case studies |
| `youtube/` | Video transcripts | Tutorials, strategy talks |
