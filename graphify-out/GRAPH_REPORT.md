# Graph Report - second-brain/github  (2026-05-22)

## Corpus Check
- Corpus is ~2,656 words - fits in a single context window. You may not need a graph.

## Summary
- 54 nodes · 73 edges · 5 communities
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_OpenHands Platform & SDK|OpenHands Platform & SDK]]
- [[_COMMUNITY_Content Creation Skills|Content Creation Skills]]
- [[_COMMUNITY_Knowledge Management Pipeline|Knowledge Management Pipeline]]
- [[_COMMUNITY_AI Coding Agent Landscape|AI Coding Agent Landscape]]
- [[_COMMUNITY_Video Processing & Research|Video Processing & Research]]

## God Nodes (most connected - your core abstractions)
1. `create-onboarding-video Skill` - 12 edges
2. `OpenHands` - 11 edges
3. `Claude Code Guide by Ruben Hassid` - 9 edges
4. `OpenHands Platform (Upstream)` - 9 edges
5. `/watch Video Analysis Skill` - 8 edges
6. `Screenshots to Animated Onboarding Video LinkedIn Post` - 7 edges
7. `Claude Code` - 6 edges
8. `bidah/skill-set` - 5 edges
9. `bidah/skill-set GitHub Repository` - 4 edges
10. `SKILL.md Skill Definition Format` - 4 edges

## Surprising Connections (you probably didn't know these)
- `/watch Video Analysis Skill` --semantically_similar_to--> `create-onboarding-video Skill`  [INFERRED] [semantically similar]
  youtube/claude-video-skill-brad.md → github/bidah-skill-set.md
- `OpenHands Skills System` --semantically_similar_to--> `create-onboarding-video Skill`  [INFERRED] [semantically similar]
  second-brain/github/openhands-openhands.md → github/bidah-skill-set.md
- `SKILL.md Skill Definition Format` --semantically_similar_to--> `CLAUDE.md Memory File`  [INFERRED] [semantically similar]
  github/bidah-skill-set.md → web/ruben-claude-code-guide.md
- `OpenHands Skills System` --semantically_similar_to--> `SKILL.md Skill Definition Format`  [INFERRED] [semantically similar]
  second-brain/github/openhands-openhands.md → github/bidah-skill-set.md
- `Claude Code` --semantically_similar_to--> `Claude Code (OpenHands context)`  [INFERRED] [semantically similar]
  github/bidah-skill-set.md → content-research/github/openhands-ai-driven-development.md

## Hyperedges (group relationships)
- **AI Coding Agent Ecosystem** — github_openhands_openhands_openhands_platform, github_openhands_openhands_claude_code, github_openhands_openhands_codeact_agent, github_openhands_openhands_software_agent_sdk [EXTRACTED 0.95]
- **Markdown-Based Skills/Microagent Pattern** — github_openhands_openhands_skills_system, github_bidah_skill_set_skill_md_format, github_bidah_skill_set_create_onboarding_video [INFERRED 0.85]
- **OpenHands Product Ladder (SDK → CLI → GUI → Cloud → Enterprise)** — github_openhands_openhands_software_agent_sdk, github_openhands_openhands_enterprise_tier, github_openhands_openhands_sdk_first_architecture, github_openhands_openhands_dual_license [EXTRACTED 0.95]

## Communities (5 total, 0 thin omitted)

### Community 0 - "OpenHands Platform & SDK"
Cohesion: 0.15
Nodes (13): bidah/skill-set, OpenHands Platform (Fork Notes), Claude Code, CodeAct Agent, Docker Sandbox Execution, MIT + Enterprise Dual License Model, OpenHands Enterprise (K8s Self-Hosted), Model-Agnostic LLM Support (+5 more)

### Community 1 - "Content Creation Skills"
Cohesion: 0.24
Nodes (11): bidah/skill-set, Claude Code, create-onboarding-video Skill, Cursor Animation Rules, Intake-First Workflow, Pieces Not Screens Philosophy, Remotion (React Video Framework), ruben-claude-code-guide (+3 more)

### Community 2 - "Knowledge Management Pipeline"
Cohesion: 0.27
Nodes (11): Content Research Map of Content, bidah/skill-set GitHub Repository, Screenshots to Animated Onboarding Video LinkedIn Post, Screenshot-to-Video Workflow, Claude Code Skills as Distribution Channel, Claude Code Guide by Ruben Hassid, CLAUDE.md Memory File, Outcome-Focused Briefs (+3 more)

### Community 3 - "AI Coding Agent Landscape"
Cohesion: 0.20
Nodes (10): Codex, Cursor, Devin, MIT + Enterprise Dual License Model, Jules, LLM-Agnostic Design, OpenHands, Product Ladder Strategy (+2 more)

### Community 4 - "Video Processing & Research"
Cohesion: 0.25
Nodes (9): Brad (AI & Automation), ffmpeg (Frame/Audio Extraction), Frames + Transcript Decomposition, Groq Whisper Transcription, OpenAI Whisper (Fallback), Second Brain Auto-Feed Use Case, My Claude Code Can INSTANTLY Watch Any Video, /watch Video Analysis Skill (+1 more)

## Knowledge Gaps
- **15 isolated node(s):** `Spring-Based Animation`, `Ruben Hassid`, `Brad (AI & Automation)`, `yt-dlp (Video Downloader)`, `ffmpeg (Frame/Audio Extraction)` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `create-onboarding-video Skill` connect `Content Creation Skills` to `OpenHands Platform & SDK`, `Knowledge Management Pipeline`, `Video Processing & Research`?**
  _High betweenness centrality (0.482) - this node is a cross-community bridge._
- **Why does `OpenHands` connect `AI Coding Agent Landscape` to `Content Creation Skills`?**
  _High betweenness centrality (0.314) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `create-onboarding-video Skill` (e.g. with `/watch Video Analysis Skill` and `OpenHands Skills System`) actually correct?**
  _`create-onboarding-video Skill` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Spring-Based Animation`, `Ruben Hassid`, `Brad (AI & Automation)` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._