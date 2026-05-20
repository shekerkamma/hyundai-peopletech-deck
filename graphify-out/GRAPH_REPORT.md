# Graph Report - /mnt/c/Users/sheke/Documents/hyundai-ai-vault/content-research  (2026-05-20)

## Corpus Check
- Corpus is ~2,263 words - fits in a single context window. You may not need a graph.

## Summary
- 28 nodes · 42 edges · 6 communities (5 shown, 1 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.75)
- Token cost: 46,380 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Onboarding Video Skill|Onboarding Video Skill]]
- [[_COMMUNITY_Video Watch Pipeline|Video Watch Pipeline]]
- [[_COMMUNITY_Claude Code Guide|Claude Code Guide]]
- [[_COMMUNITY_Content Research Hub|Content Research Hub]]
- [[_COMMUNITY_Brad Video Analysis|Brad Video Analysis]]
- [[_COMMUNITY_Screenshot Prompting|Screenshot Prompting]]

## God Nodes (most connected - your core abstractions)
1. `create-onboarding-video Skill` - 9 edges
2. `Claude Code Guide by Ruben Hassid` - 9 edges
3. `/watch Video Analysis Skill` - 8 edges
4. `Screenshots to Animated Onboarding Video LinkedIn Post` - 7 edges
5. `bidah/skill-set GitHub Repository` - 4 edges
6. `Claude Code` - 4 edges
7. `My Claude Code Can INSTANTLY Watch Any Video` - 4 edges
8. `Content Research Map of Content` - 4 edges
9. `Claude Code Skills as Distribution Channel` - 3 edges
10. `Remotion (React Video Framework)` - 2 edges

## Surprising Connections (you probably didn't know these)
- `/watch Video Analysis Skill` --semantically_similar_to--> `create-onboarding-video Skill`  [INFERRED] [semantically similar]
  youtube/claude-video-skill-brad.md → github/bidah-skill-set.md
- `SKILL.md Skill Definition Format` --semantically_similar_to--> `CLAUDE.md Memory File`  [INFERRED] [semantically similar]
  github/bidah-skill-set.md → web/ruben-claude-code-guide.md
- `Screenshot-Based Prompting` --semantically_similar_to--> `Screenshot-to-Video Workflow`  [INFERRED] [semantically similar]
  web/ruben-claude-code-guide.md → linkedin/bidah-create-onboarding-video-skill.md
- `Screenshots to Animated Onboarding Video LinkedIn Post` --references--> `Remotion (React Video Framework)`  [EXTRACTED]
  linkedin/bidah-create-onboarding-video-skill.md → github/bidah-skill-set.md
- `Intake-First Workflow` --conceptually_related_to--> `Outcome-Focused Briefs`  [INFERRED]
  github/bidah-skill-set.md → web/ruben-claude-code-guide.md

## Hyperedges (group relationships)
- **Claude Code Skills Ecosystem** — github_bidah_skill_set_claude_code, github_bidah_skill_set_create_onboarding_video, youtube_claude_video_skill_brad_watch_skill, github_bidah_skill_set_skill_md_format, web_ruben_claude_code_guide_claude_md [INFERRED 0.85]
- **Onboarding Video Production Pipeline** — github_bidah_skill_set_create_onboarding_video, github_bidah_skill_set_remotion, github_bidah_skill_set_spring_animation, github_bidah_skill_set_cursor_animation, github_bidah_skill_set_pieces_not_screens [EXTRACTED 1.00]
- **Video Watch Pipeline** — youtube_claude_video_skill_brad_watch_skill, youtube_claude_video_skill_brad_yt_dlp, youtube_claude_video_skill_brad_ffmpeg, youtube_claude_video_skill_brad_groq_whisper, youtube_claude_video_skill_brad_frames_plus_transcript [EXTRACTED 1.00]
- **Content Research Cross-Source Cluster (May 2026)** — _index_content_research_moc, github_bidah_skill_set_repo, linkedin_bidah_create_onboarding_video_skill_post, web_ruben_claude_code_guide_article, youtube_claude_video_skill_brad_video [EXTRACTED 1.00]

## Communities (6 total, 1 thin omitted)

### Community 0 - "Onboarding Video Skill"
Cohesion: 0.33
Nodes (7): create-onboarding-video Skill, Cursor Animation Rules, Intake-First Workflow, Pieces Not Screens Philosophy, Remotion (React Video Framework), SKILL.md Skill Definition Format, Spring-Based Animation

### Community 1 - "Video Watch Pipeline"
Cohesion: 0.33
Nodes (7): Claude Code, ffmpeg (Frame/Audio Extraction), Frames + Transcript Decomposition, Groq Whisper Transcription, OpenAI Whisper (Fallback), /watch Video Analysis Skill, yt-dlp (Video Downloader)

### Community 2 - "Claude Code Guide"
Cohesion: 0.40
Nodes (5): Claude Code Guide by Ruben Hassid, CLAUDE.md Memory File, Outcome-Focused Briefs, Ruben Hassid, Vibecoding Method

### Community 3 - "Content Research Hub"
Cohesion: 0.67
Nodes (4): Content Research Map of Content, bidah/skill-set GitHub Repository, Screenshots to Animated Onboarding Video LinkedIn Post, Claude Code Skills as Distribution Channel

### Community 4 - "Brad Video Analysis"
Cohesion: 0.67
Nodes (3): Brad (AI & Automation), Second Brain Auto-Feed Use Case, My Claude Code Can INSTANTLY Watch Any Video

## Knowledge Gaps
- **5 isolated node(s):** `Spring-Based Animation`, `Ruben Hassid`, `Brad (AI & Automation)`, `yt-dlp (Video Downloader)`, `ffmpeg (Frame/Audio Extraction)`
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `/watch Video Analysis Skill` connect `Video Watch Pipeline` to `Onboarding Video Skill`, `Brad Video Analysis`?**
  _High betweenness centrality (0.400) - this node is a cross-community bridge._
- **Why does `create-onboarding-video Skill` connect `Onboarding Video Skill` to `Video Watch Pipeline`, `Content Research Hub`?**
  _High betweenness centrality (0.360) - this node is a cross-community bridge._
- **Why does `Claude Code Guide by Ruben Hassid` connect `Claude Code Guide` to `Video Watch Pipeline`, `Content Research Hub`, `Screenshot Prompting`?**
  _High betweenness centrality (0.282) - this node is a cross-community bridge._
- **What connects `Spring-Based Animation`, `Ruben Hassid`, `Brad (AI & Automation)` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._