---
title: "bidah/skill-set"
source: https://github.com/bidah/skill-set
source_type: github-repo
owner: bidah
stars: 221
language: null
license: null
date_watched: 2026-05-20
tags: [content-research, github, claude-code, skills, remotion, onboarding, video, source/github]
---

# bidah/skill-set

## TL;DR
A collection of Claude Code skills by @bidah. Currently contains one skill — `create-onboarding-video` — which produces short, punchy iOS-style onboarding videos using Remotion by animating cropped UI components from screenshots.

## What It Does
Provides reusable Claude Code skills that can be dropped into `~/.claude/skills/` or a project's `.claude/skills/` directory. The flagship skill (`create-onboarding-video`) takes app screenshots and produces animated MP4 videos suitable for App Store previews or in-app onboarding flows.

### create-onboarding-video Skill
- **Input**: 2-4 screenshots per screen (resting, mid-interaction, result states)
- **Output**: Remotion project → MP4 video (1080x1920 portrait default)
- **Style**: UI-first, never full-screen — isolates/crops individual UI components (buttons, cards, fields) and animates them with spring-based transitions
- **Length**: 3-8 seconds per beat, ~30s total max
- **Features**:
  - Cursor animation (fade-in at center, straight-line glide to target)
  - Top-anchored captions with rise-from-below animation
  - Spring-based motion, masked reveals, shared-element morphs
  - Cross-fade transitions between beats

## Tech Stack
- **Framework**: [[Remotion]] (React-based video framework)
- **Language**: JavaScript/TypeScript (Remotion components)
- **Animation**: Spring physics, Easing.bezier curves
- **Output**: MP4 via Remotion renderer

## Traction
- **Stars**: 221 | **Forks**: 30 | **Age**: ~11 days (created 2026-05-09)
- **Star velocity**: ~20 stars/day — strong early traction
- **Recent activity**: Last push 2026-05-09

## Architecture
```
skill-set/
├── README.md
└── skills/
    └── create-onboarding-video/
        ├── SKILL.md          ← main skill definition
        └── resources/
            └── cursor-component.md  ← reusable pointer component
```

## Key Design Decisions
- **Pieces not screens**: Each beat shows a cropped UI component, not a full screenshot — the viewer sees the feature in action, not a screen tour
- **Cursor-led interactions**: Every tap must be preceded by visible cursor movement — no teleporting
- **Caption positioning**: Fixed top-of-frame band, consistent across all beats
- **Delegates to remotion-best-practices**: The skill invokes another skill for Remotion code quality
- **Intake-first workflow**: Won't start rendering until it has stills + intent for every screen

## Integration Potential
- **Use case for us**: Could create onboarding videos for Hyundai plant ops mobile interfaces or training apps
- **Effort to integrate**: Low — copy skill folder to `.claude/skills/`, provide screenshots
- **License**: None specified (no license file)

## Steal-Worthy Elements
- The SKILL.md format is an excellent template for writing Claude Code skills — detailed operating rules, workflow steps, and forbidden patterns
- "Pieces not screens" philosophy could apply to any demo/presentation work
- The cursor animation rules (fade-in at center, single straight-line moves, no teleporting) are well-thought-out UX patterns

## Backlinks
- [[bidah-create-onboarding-video-skill]] — LinkedIn post that surfaced this repo
- [[Claude Code]] — the platform these skills run on
- [[Remotion]] — the underlying video framework
- [[ruben-claude-code-guide]] — guide referenced alongside this repo
