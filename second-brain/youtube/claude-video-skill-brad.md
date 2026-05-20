---
title: "My Claude Code Can INSTANTLY Watch Any Video"
source: https://www.youtube.com/watch?v=QZMljuD10sU
creator: Brad | AI & Automation
duration: "08:36"
date_watched: 2026-05-20
tags: [claude-code, skill, video-analysis, yt-dlp, ffmpeg, whisper, groq, content-research, second-brain]
---

# My Claude Code Can INSTANTLY Watch Any Video (Here's How)

## Core Idea
A free Claude Code skill (`/watch`) that lets Claude "watch" videos by decomposing them into frames + transcript. Since Anthropic has no native video model, the skill splits video into two things Claude already understands: **images** and **text**.

## How It Works (Pipeline)
1. **yt-dlp** downloads the video (supports 1,000+ sites)
2. **ffmpeg** extracts frames at auto-scaled rate + pulls audio
3. **Captions** pulled free from YouTube (or Whisper API fallback)
4. Claude **reads frames as images** + timestamped transcript
5. Claude answers grounded in what it actually **saw** and **heard**

## Key Insight
> "Half of the interesting stuff in video isn't said out loud. It happens on screen." — Brad

Most existing video tools only pull the transcript. This skill gives Claude the frames AND audio together, so it catches graphs, UI changes, on-screen text, and visual context that transcript-only tools miss.

## Frame Budget & Cost
| Duration | Frames | Cost |
|----------|--------|------|
| ≤30s | ~30 | Cheap |
| 30s-1min | ~40 | Cheap |
| 1-3min | ~60 | Moderate |
| 3-10min | ~80 | ~$1 |
| >10min | 100 (sparse) | ~$1 |

- Hard caps: 2 fps, 100 frames max
- 30-min and 1-hour videos cost roughly the same (~$1 on API pricing)
- On Max subscription plan: $0 additional cost

## Transcription Cost
- **YouTube captions** = free (majority of public videos)
- **Groq Whisper** = free tier covers 2 hours of transcription per hour
- **OpenAI Whisper** = standard pricing (fallback)
- Whisper only needed for: local files, TikToks, Looms, caption-less uploads

## Tools Used (battle-tested, free)
- **yt-dlp** — video downloader, works on 1,000+ sites
- **ffmpeg** — frame extraction + audio extraction
- **Groq API** — hosted Whisper transcription (preferred, cheapest)
- No MCPs, no third-party wrappers, no expensive video models

## Use Cases

### 1. Content Research / Hook Analysis
- Paste a winning video URL
- Claude breaks down: visual setup, exact words, pattern interrupt timing, what's on screen at hook moment
- Replaces 10 min of manual pause-and-scrub per video

### 2. Bug Debugging from Screen Recordings
- Drop a 30-second screen recording
- Claude finds the exact frame where the issue starts
- Identifies state changes visually without you ever opening the file

### 3. Focused Analysis (--start / --end)
- Zoom into a 10-second segment of a 2-hour video
- Denser frame rate on the focused window
- Saves context window vs sparse full-video scan

### 4. Second Brain Auto-Feed (Brad's personal favorite)
- Give Claude a list of competitor/creator channels
- Claude watches each video automatically
- Generates structured notes: what made the video work, structure, hooks
- Feeds directly into Obsidian knowledge base
- Compounds over time — more videos → more context → smarter notes

## Quotable Insights
- "It's like Neo plugging into the Matrix. By the time you've hit play, Claude's already watched the whole thing."
- "You're not watching content anymore. You're downloading context automatically and putting it to work."
- "A video is just two things: a bunch of frames and the transcript. That's it."
- "I ran every test in this video three times in parallel and burned less than 10% of my session — over 5 hours of video."

## Limitations
- Best accuracy under 10 minutes
- No private/auth-required platforms
- Whisper upload limit: 25 MB (~50 min audio)
- Sparse scan warning on long videos — use --start/--end instead

## Related
- Brad's "Second Brain in Obsidian" video (referenced, not linked)
- Universal Context Layer (mentioned as built using this skill)
- GitHub: bradautomates/claude-video (MIT license)
