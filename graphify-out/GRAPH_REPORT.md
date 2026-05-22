# Graph Report - /mnt/c/Users/sheke/Documents/hyundai-ai-vault/content-research/github  (2026-05-21)

## Corpus Check
- Corpus is ~1,354 words - fits in a single context window. You may not need a graph.

## Summary
- 41 nodes · 58 edges · 8 communities (6 shown, 2 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_OpenHands AI Platform & Competitors|OpenHands AI Platform & Competitors]]
- [[_COMMUNITY_Video Ingestion Pipeline|Video Ingestion Pipeline]]
- [[_COMMUNITY_Bidah Onboarding & Animation|Bidah Onboarding & Animation]]
- [[_COMMUNITY_Claude Code Guide & Practices|Claude Code Guide & Practices]]
- [[_COMMUNITY_Content Research Index|Content Research Index]]
- [[_COMMUNITY_Claude Code Skills Format|Claude Code Skills Format]]
- [[_COMMUNITY_Claude Code (Cross-Source)|Claude Code (Cross-Source)]]
- [[_COMMUNITY_Screenshot-to-Media Techniques|Screenshot-to-Media Techniques]]

## God Nodes (most connected - your core abstractions)
1. `OpenHands` - 11 edges
2. `create-onboarding-video Skill` - 10 edges
3. `Claude Code Guide by Ruben Hassid` - 9 edges
4. `/watch Video Analysis Skill` - 8 edges
5. `Screenshots to Animated Onboarding Video LinkedIn Post` - 7 edges
6. `Claude Code` - 6 edges
7. `bidah/skill-set` - 5 edges
8. `bidah/skill-set GitHub Repository` - 4 edges
9. `My Claude Code Can INSTANTLY Watch Any Video` - 4 edges
10. `Content Research Map of Content` - 4 edges

## Surprising Connections (you probably didn't know these)
- `/watch Video Analysis Skill` --semantically_similar_to--> `create-onboarding-video Skill`  [INFERRED] [semantically similar]
  youtube/claude-video-skill-brad.md → github/bidah-skill-set.md
- `SKILL.md Skill Definition Format` --semantically_similar_to--> `CLAUDE.md Memory File`  [INFERRED] [semantically similar]
  github/bidah-skill-set.md → web/ruben-claude-code-guide.md
- `Claude Code` --semantically_similar_to--> `Claude Code (OpenHands context)`  [INFERRED] [semantically similar]
  github/bidah-skill-set.md → content-research/github/openhands-ai-driven-development.md
- `Screenshot-Based Prompting` --semantically_similar_to--> `Screenshot-to-Video Workflow`  [INFERRED] [semantically similar]
  web/ruben-claude-code-guide.md → linkedin/bidah-create-onboarding-video-skill.md
- `Screenshots to Animated Onboarding Video LinkedIn Post` --references--> `Remotion (React Video Framework)`  [EXTRACTED]
  linkedin/bidah-create-onboarding-video-skill.md → github/bidah-skill-set.md

## Hyperedges (group relationships)
- **AI Coding Tool Ecosystem** — github_openhands_ai_driven_development_openhands, github_openhands_ai_driven_development_claude_code, github_openhands_ai_driven_development_codex, github_openhands_ai_driven_development_devin, github_openhands_ai_driven_development_jules, github_openhands_ai_driven_development_cursor [EXTRACTED 1.00]
- **Claude Code Skills Ecosystem** — github_bidah_skill_set_bidah_skill_set, github_bidah_skill_set_claude_code, github_bidah_skill_set_skill_md_format, github_bidah_skill_set_create_onboarding_video [EXTRACTED 1.00]
- **OpenHands Modular Product Surface** — github_openhands_ai_driven_development_openhands, github_openhands_ai_driven_development_software_agent_sdk, github_openhands_ai_driven_development_product_ladder, github_openhands_ai_driven_development_llm_agnostic [EXTRACTED 1.00]

## Communities (8 total, 2 thin omitted)

### Community 0 - "OpenHands AI Platform & Competitors"
Cohesion: 0.20
Nodes (10): Codex, Cursor, Devin, MIT + Enterprise Dual License Model, Jules, LLM-Agnostic Design, OpenHands, Product Ladder Strategy (+2 more)

### Community 1 - "Video Ingestion Pipeline"
Cohesion: 0.25
Nodes (9): Brad (AI & Automation), ffmpeg (Frame/Audio Extraction), Frames + Transcript Decomposition, Groq Whisper Transcription, OpenAI Whisper (Fallback), Second Brain Auto-Feed Use Case, My Claude Code Can INSTANTLY Watch Any Video, /watch Video Analysis Skill (+1 more)

### Community 2 - "Bidah Onboarding & Animation"
Cohesion: 0.40
Nodes (6): create-onboarding-video Skill, Cursor Animation Rules, Intake-First Workflow, Pieces Not Screens Philosophy, Remotion (React Video Framework), Spring-Based Animation

### Community 3 - "Claude Code Guide & Practices"
Cohesion: 0.40
Nodes (5): Claude Code Guide by Ruben Hassid, CLAUDE.md Memory File, Outcome-Focused Briefs, Ruben Hassid, Vibecoding Method

### Community 4 - "Content Research Index"
Cohesion: 0.67
Nodes (4): Content Research Map of Content, bidah/skill-set GitHub Repository, Screenshots to Animated Onboarding Video LinkedIn Post, Claude Code Skills as Distribution Channel

### Community 5 - "Claude Code Skills Format"
Cohesion: 0.67
Nodes (3): bidah/skill-set, ruben-claude-code-guide, SKILL.md Skill Definition Format

## Knowledge Gaps
- **12 isolated node(s):** `Spring-Based Animation`, `Ruben Hassid`, `Brad (AI & Automation)`, `yt-dlp (Video Downloader)`, `ffmpeg (Frame/Audio Extraction)` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OpenHands` connect `OpenHands AI Platform & Competitors` to `Claude Code Skills Format`, `Claude Code (Cross-Source)`?**
  _High betweenness centrality (0.406) - this node is a cross-community bridge._
- **Why does `Claude Code` connect `Claude Code (Cross-Source)` to `Video Ingestion Pipeline`, `Bidah Onboarding & Animation`, `Claude Code Guide & Practices`, `Content Research Index`, `Claude Code Skills Format`?**
  _High betweenness centrality (0.331) - this node is a cross-community bridge._
- **Why does `create-onboarding-video Skill` connect `Bidah Onboarding & Animation` to `Video Ingestion Pipeline`, `Content Research Index`, `Claude Code Skills Format`, `Claude Code (Cross-Source)`?**
  _High betweenness centrality (0.317) - this node is a cross-community bridge._
- **What connects `Spring-Based Animation`, `Ruben Hassid`, `Brad (AI & Automation)` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._