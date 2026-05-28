#!/usr/bin/env node
/**
 * OpenHands Autonomous Coding Pipeline — Architecture Deck
 * Enterprise Consulting theme (white background, NAVY_DEEP + RED accents)
 * 10 slides following the standard architecture presentation structure
 */

const pptxgen = require("pptxgenjs");
const pptx = new pptxgen();

pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 inches
pptx.author = "PeopleTech AI Engineering";

// ── Color Constants ──
const C = {
  WHITE: "FFFFFF", CHARCOAL: "1A1A1A", NAVY_DEEP: "1F3B6E",
  NAVY_CARD: "0D3B5E", RED: "E31837", LIGHT_BG: "F5F7FA",
  BORDER: "D0D5DD", MUTED: "6B7280", CODE_BG: "F0F2F5",
  GREEN: "166534", LIGHT_GREEN: "F0FDF4", LIGHT_RED: "FEE2E2",
  LIGHT_BLUE: "EEF2FF", AMBER: "92400E", LIGHT_AMBER: "FEF3C7",
};

// ── Helper Functions ──
function addTitle(slide, text, subtitle) {
  slide.addText(text, {
    x: 0.5, y: 0.25, w: 12.33, h: 0.7,
    fontSize: 36, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.5, y: 0.9, w: 12.33, h: 0.4,
      fontSize: 14, color: C.MUTED, fontFace: "Calibri",
    });
  }
}

function addCard(slide, x, y, w, h, header, body, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w, h,
    line: { color: C.BORDER, width: 1 },
    fill: { color: opts.fill || C.WHITE },
    rectRadius: 0.05,
  });
  if (header) {
    slide.addShape(pptx.ShapeType.rect, {
      x, y, w, h: 0.38,
      fill: { color: opts.headerColor || C.NAVY_CARD },
      line: { width: 0 },
      rectRadius: 0.05,
    });
    slide.addText(header, {
      x: x + 0.12, y: y + 0.06, w: w - 0.24, h: 0.28,
      fontSize: 12, bold: true, color: C.WHITE, fontFace: "Calibri",
    });
  }
  if (typeof body === "string") {
    slide.addText(body, {
      x: x + 0.15, y: y + (header ? 0.44 : 0.12), w: w - 0.3,
      h: h - (header ? 0.56 : 0.24),
      fontSize: 12, color: C.CHARCOAL, fontFace: "Calibri",
      valign: "top", wrap: true, lineSpacingMultiple: 1.15,
    });
  } else if (Array.isArray(body)) {
    slide.addText(body, {
      x: x + 0.15, y: y + (header ? 0.44 : 0.12), w: w - 0.3,
      h: h - (header ? 0.56 : 0.24),
      valign: "top", wrap: true, lineSpacingMultiple: 1.15,
    });
  }
}

function addMetric(slide, x, y, w, value, label) {
  slide.addText(value, {
    x, y, w, h: 0.9,
    fontSize: 60, bold: true, color: C.RED, fontFace: "Calibri",
  });
  slide.addText(label, {
    x, y: y + 0.85, w, h: 0.45,
    fontSize: 13, color: C.CHARCOAL, fontFace: "Calibri",
    valign: "top",
  });
}

function addBanner(slide, text) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 6.85, w: 13.33, h: 0.65,
    fill: { color: C.NAVY_CARD }, line: { width: 0 },
  });
  slide.addText(text, {
    x: 0.4, y: 6.88, w: 12.53, h: 0.55,
    fontSize: 13, bold: true, color: C.WHITE, fontFace: "Calibri",
    align: "center", valign: "middle",
  });
}

function addCodeBlock(slide, x, y, w, h, code) {
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w, h,
    fill: { color: C.CODE_BG },
    line: { color: C.BORDER, width: 1 },
    rectRadius: 0.05,
  });
  slide.addText(code, {
    x: x + 0.12, y: y + 0.1, w: w - 0.24, h: h - 0.2,
    fontSize: 10, color: C.CHARCOAL, fontFace: "Courier New",
    valign: "top", wrap: true, lineSpacingMultiple: 1.3,
  });
}

function addFlowBox(slide, x, y, w, h, text, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w, h,
    fill: { color: opts.fill || C.WHITE },
    line: { color: opts.border || C.BORDER, width: 1.5 },
    rectRadius: 0.05,
  });
  slide.addText(text, {
    x: x + 0.08, y, w: w - 0.16, h,
    fontSize: opts.fontSize || 10, bold: opts.bold || false,
    color: opts.fontColor || C.CHARCOAL, fontFace: "Calibri",
    align: "center", valign: "middle", wrap: true,
  });
}

function addArrow(slide, x, y, w) {
  slide.addShape(pptx.ShapeType.rect, {
    x, y: y + 0.18, w, h: 0.04,
    fill: { color: C.BORDER }, line: { width: 0 },
  });
  // arrowhead
  slide.addText("▶", {
    x: x + w - 0.15, y: y + 0.06, w: 0.2, h: 0.28,
    fontSize: 10, color: C.BORDER, fontFace: "Calibri",
    align: "center", valign: "middle",
  });
}

function addNumberCircle(slide, x, y, num, color) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x, y, w: 0.28, h: 0.28,
    fill: { color: color || C.RED },
    line: { width: 0 },
  });
  slide.addText(String(num), {
    x, y, w: 0.28, h: 0.28,
    fontSize: 10, bold: true, color: C.WHITE, fontFace: "Calibri",
    align: "center", valign: "middle",
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 1: Title
// ═══════════════════════════════════════════════════════
let s1 = pptx.addSlide();
s1.background = { color: C.WHITE };

s1.addText("OpenHands\nAutonomous Coding Pipeline", {
  x: 0.5, y: 1.0, w: 7.5, h: 2.2,
  fontSize: 42, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri",
  lineSpacingMultiple: 1.1,
});
s1.addText("Architecture Guide", {
  x: 0.5, y: 3.2, w: 7.5, h: 0.5,
  fontSize: 22, color: C.MUTED, fontFace: "Calibri",
});

// Red tagline pill
s1.addShape(pptx.ShapeType.rect, {
  x: 0.5, y: 4.0, w: 4.8, h: 0.42,
  fill: { color: C.RED }, line: { width: 0 }, rectRadius: 0.2,
});
s1.addText("From issue to merged PR in minutes — every action auditable", {
  x: 0.7, y: 4.02, w: 4.4, h: 0.38,
  fontSize: 11, bold: true, color: C.WHITE, fontFace: "Calibri",
  align: "center", valign: "middle",
});

// Right side — stats column
const stats = [
  ["77.6%", "SWE-Bench Resolve Rate"],
  ["~$3", "Cost per Pull Request"],
  ["37%", "Self-Written Commits"],
  ["74.6k", "GitHub Stars (Open Source)"],
];
stats.forEach(([val, label], i) => {
  const sy = 1.2 + i * 1.35;
  s1.addText(val, {
    x: 9.0, y: sy, w: 3.8, h: 0.7,
    fontSize: 44, bold: true, color: C.RED, fontFace: "Calibri",
  });
  s1.addText(label, {
    x: 9.0, y: sy + 0.65, w: 3.8, h: 0.35,
    fontSize: 12, color: C.MUTED, fontFace: "Calibri",
  });
});

addBanner(s1, "AI Engineering Business Use Cases | Architecture Guide");

// ═══════════════════════════════════════════════════════
// SLIDE 2: What Is It? (3 icon cards)
// ═══════════════════════════════════════════════════════
let s2 = pptx.addSlide();
s2.background = { color: C.WHITE };
addTitle(s2, "What is the OpenHands Coding Pipeline?", "An AI platform that turns GitHub issues into production-ready pull requests autonomously");

addCard(s2, 0.5, 1.6, 3.8, 2.8, "Autonomous Agent",
  "An AI agent reads a GitHub issue, understands the codebase, writes code and tests, and opens a PR — all without human intervention. Powered by CodeAct, a stateless event processor that unifies reasoning and execution.",
);
addCard(s2, 4.6, 1.6, 3.8, 2.8, "Sandboxed Execution",
  "Every agent runs in an isolated Docker container with its own shell, Python interpreter, browser, and file system. No host access. No cross-contamination. Full audit trail of every action.",
);
addCard(s2, 8.7, 1.6, 3.8, 2.8, "Model-Agnostic",
  "100+ LLM providers via LiteLLM. Claude 4.5 Opus for reasoning, GPT-5.2 Codex for greenfield tasks. Swap models in config, not code. No vendor lock-in.",
);

addCard(s2, 0.5, 4.8, 12.0, 1.4, null, [
  { text: "Key insight: ", options: { fontSize: 13, bold: true, color: C.RED, fontFace: "Calibri" }},
  { text: "OpenHands is not a copilot — it executes real engineering work end-to-end. 37% of its own codebase commits are written by the agent itself.", options: { fontSize: 13, color: C.CHARCOAL, fontFace: "Calibri" }},
], { fill: C.LIGHT_BG });

addBanner(s2, "Open source (74.6k ★) · Trusted by engineers at TikTok, VMware, Roche, Amazon, Netflix, Apple, NVIDIA");

// ═══════════════════════════════════════════════════════
// SLIDE 3: The Problem
// ═══════════════════════════════════════════════════════
let s3 = pptx.addSlide();
s3.background = { color: C.WHITE };
addTitle(s3, "The Problem", "Engineering teams waste 30-40% of capacity on low-complexity, repetitive work");

// Problem flow
addFlowBox(s3, 0.5, 1.5, 2.5, 0.5, "200+ open issues backlogged", { fill: C.LIGHT_RED, border: C.RED, fontColor: C.RED, bold: true });
addArrow(s3, 3.0, 1.5, 0.6);
addFlowBox(s3, 3.6, 1.5, 2.5, 0.5, "4hr avg resolution time", { fill: C.LIGHT_RED, border: C.RED, fontColor: C.RED, bold: true });
addArrow(s3, 6.1, 1.5, 0.6);
addFlowBox(s3, 6.7, 1.5, 2.5, 0.5, "2-day PR cycle time", { fill: C.LIGHT_RED, border: C.RED, fontColor: C.RED, bold: true });
addArrow(s3, 9.2, 1.5, 0.6);
addFlowBox(s3, 9.8, 1.5, 2.5, 0.5, "$180K+ annual cost", { fill: C.LIGHT_RED, border: C.RED, fontColor: C.RED, bold: true });

// 3 problem cards
addCard(s3, 0.5, 2.5, 3.8, 2.5, "Bug Fix Bottleneck",
  "• 30-40% of engineering hours on low-complexity issues\n• Junior devs take 3-6 months to contribute meaningfully\n• Knowledge silos: only 1-2 people can fix each area"
);
addCard(s3, 4.6, 2.5, 3.8, 2.5, "Test & Quality Gap",
  "• Legacy codebases average 35% test coverage\n• 15% of deployments cause incidents in first 24 hours\n• Test maintenance breaks 20% of suites per refactor"
);
addCard(s3, 8.7, 2.5, 3.8, 2.5, "Tech Debt Compounds",
  "• 40% of dev time navigating legacy code\n• Framework migrations take 6-18 months manually\n• 200+ outdated dependencies per enterprise avg"
);

addBanner(s3, "The cost of NOT automating: $2M+ annually in a 50-engineer org");

// ═══════════════════════════════════════════════════════
// SLIDE 4: Architecture Overview
// ═══════════════════════════════════════════════════════
let s4 = pptx.addSlide();
s4.background = { color: C.WHITE };
addTitle(s4, "Architecture Overview", "Five layers + cross-cutting security and observability");

// Diagram area (left 65%)
const layers = [
  { label: "TRIGGER", boxes: ["GitHub Issue", "Webhook", "Agent Server"], y: 1.5, fill: C.LIGHT_BG },
  { label: "AGENT", boxes: ["CodeAct Agent", "LLM Router", "Claude / GPT"], y: 2.6, fill: C.LIGHT_BG },
  { label: "SANDBOX", boxes: ["Docker Container", "Bash + Python", "Chromium + VS Code"], y: 3.7, fill: C.LIGHT_BG },
  { label: "OUTPUT", boxes: ["Git Ops + PR", "CI/CD Pipeline", "Review Gate"], y: 4.8, fill: C.LIGHT_BG },
];

layers.forEach((layer) => {
  // Layer label
  s4.addText(layer.label, {
    x: 0.3, y: layer.y + 0.12, w: 0.95, h: 0.36,
    fontSize: 9, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri",
    align: "right",
  });

  // Background zone
  s4.addShape(pptx.ShapeType.rect, {
    x: 1.35, y: layer.y, w: 6.8, h: 0.65,
    fill: { color: layer.fill }, line: { color: C.BORDER, width: 0.5 },
    rectRadius: 0.04,
  });

  // Boxes
  layer.boxes.forEach((box, i) => {
    const bx = 1.55 + i * 2.25;
    const isCoreBox = ["Agent Server", "CodeAct Agent", "Docker Container", "Git Ops + PR"].includes(box);
    addFlowBox(s4, bx, layer.y + 0.1, 1.9, 0.45, box, {
      fill: isCoreBox ? C.NAVY_CARD : C.WHITE,
      border: isCoreBox ? C.NAVY_CARD : C.BORDER,
      fontColor: isCoreBox ? C.WHITE : C.CHARCOAL,
      bold: isCoreBox,
      fontSize: 9,
    });

    // Arrows between boxes
    if (i < layer.boxes.length - 1) {
      s4.addText("→", {
        x: bx + 1.9, y: layer.y + 0.1, w: 0.35, h: 0.45,
        fontSize: 14, color: C.BORDER, align: "center", valign: "middle",
      });
    }
  });
});

// Vertical arrows between layers
[1.95, 3.05, 4.15].forEach((ay) => {
  s4.addText("▼", {
    x: 3.5, y: ay, w: 0.4, h: 0.45,
    fontSize: 12, color: C.BORDER, align: "center", valign: "middle",
  });
});

// Right panel — numbered flow
s4.addText("12-Step Data Flow", {
  x: 8.7, y: 1.4, w: 4.0, h: 0.35,
  fontSize: 16, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri",
});

const flowSteps = [
  "Issue created (label: fix-me)",
  "Webhook routes to Agent Server",
  "Server spawns CodeAct Agent",
  "Agent queries LLM via LiteLLM",
  "LLM returns reasoning + actions",
  "Code executes in Docker sandbox",
  "Agent invokes registered tools",
  "Changes committed to git branch",
  "PR opened with summary",
  "CI/CD runs tests + SAST + lint",
  "Confidence scored at review gate",
  "Auto-merge or human review",
];

flowSteps.forEach((step, i) => {
  const fy = 1.85 + i * 0.38;
  addNumberCircle(s4, 8.7, fy, i + 1, i < 6 ? C.RED : C.NAVY_DEEP);
  s4.addText(step, {
    x: 9.1, y: fy, w: 3.7, h: 0.32,
    fontSize: 10, color: C.CHARCOAL, fontFace: "Calibri",
    valign: "middle",
  });
});

addBanner(s4, "Event-sourced architecture: every action logged, deterministic replay, full audit trail");

// ═══════════════════════════════════════════════════════
// SLIDE 5: Components Deep Dive (2x2 grid)
// ═══════════════════════════════════════════════════════
let s5 = pptx.addSlide();
s5.background = { color: C.WHITE };
addTitle(s5, "Components Deep Dive", "Core platform components powering the autonomous pipeline");

addCard(s5, 0.5, 1.5, 5.9, 2.4, "CodeAct Agent",
  "• Stateless event processor — unifies reasoning and execution\n• Two modes: natural language conversation + code execution\n• Function calling for precise tool specification (CodeAct 2.1)\n• Sub-agent delegation: spawn parallel child agents\n• Context: skills, prompts, security policies, tool specs"
);
addCard(s5, 6.7, 1.5, 5.9, 2.4, "Docker Sandbox Runtime",
  "• Isolated container per agent session — no host access\n• Full dev environment: bash, Python, Chromium, VS Code\n• Overlay filesystem for non-destructive modifications\n• Three-tier image tagging for incremental builds\n• Plugin system: Jupyter, Agent Skills extensions"
);
addCard(s5, 0.5, 4.2, 5.9, 2.2, "LLM Router (LiteLLM)",
  "• 100+ providers — Claude, GPT, Gemini, DeepSeek, open-weight\n• Native reasoning support (Anthropic thinking, OpenAI reasoning)\n• NonNativeToolCallingMixin for basic models\n• Model swap via config change, no code changes\n• Cost optimization: route by task complexity"
);
addCard(s5, 6.7, 4.2, 5.9, 2.2, "Event Store + Audit",
  "• Append-only immutable event log\n• Deterministic replay of any session\n• Session recovery after interruption\n• SecurityAnalyzer: LOW/MEDIUM/HIGH risk rating\n• Secret Registry: per-conversation isolation, masked outputs"
);

addBanner(s5, "Every component is modular — swap, scale, or replace independently");

// ═══════════════════════════════════════════════════════
// SLIDE 6: Comparison / Decision Matrix
// ═══════════════════════════════════════════════════════
let s6 = pptx.addSlide();
s6.background = { color: C.WHITE };
addTitle(s6, "Platform Comparison", "OpenHands vs. commercial and open-source alternatives");

const tableX = 0.5;
const tableY = 1.5;
const colW = 2.42;
const rowH = 0.55;
const headers = ["Capability", "OpenHands", "Devin", "Copilot", "Cursor"];
const rows = [
  ["SWE-Bench Score", "77.6%", "~70%", "N/A", "N/A"],
  ["Cost per PR", "~$3", "$500/mo seat", "Free–$39/mo", "$20/mo"],
  ["Open Source", "Yes (74.6k★)", "No", "No", "No"],
  ["Self-Hosted / Air-Gap", "Yes (K8s)", "No", "No", "No"],
  ["Model Agnostic", "100+ providers", "Proprietary", "GPT only", "Multi-model"],
  ["Sandboxed Execution", "Docker per agent", "Cloud sandbox", "In-editor", "In-editor"],
  ["MCP Integration", "Native", "No", "No", "Partial"],
  ["Audit Trail", "Event-sourced", "Logs only", "Minimal", "Minimal"],
  ["Multi-Agent", "Sub-agent delegation", "Single agent", "Single agent", "Single agent"],
];

// Header row
headers.forEach((h, i) => {
  const fill = i === 1 ? C.RED : C.NAVY_CARD;
  s6.addShape(pptx.ShapeType.rect, {
    x: tableX + i * colW, y: tableY, w: colW, h: 0.42,
    fill: { color: fill }, line: { color: fill, width: 0 },
  });
  s6.addText(h, {
    x: tableX + i * colW + 0.08, y: tableY + 0.04, w: colW - 0.16, h: 0.34,
    fontSize: 11, bold: true, color: C.WHITE, fontFace: "Calibri",
    valign: "middle",
  });
});

// Data rows
rows.forEach((row, ri) => {
  row.forEach((cell, ci) => {
    const ry = tableY + 0.42 + ri * rowH;
    const fill = ci === 1 ? C.LIGHT_RED : (ci === 0 ? C.LIGHT_BG : C.WHITE);
    const textColor = ci === 1 ? C.RED : C.CHARCOAL;
    s6.addShape(pptx.ShapeType.rect, {
      x: tableX + ci * colW, y: ry, w: colW, h: rowH,
      fill: { color: fill },
      line: { color: C.BORDER, width: 0.5 },
    });
    s6.addText(cell, {
      x: tableX + ci * colW + 0.08, y: ry + 0.04, w: colW - 0.16, h: rowH - 0.08,
      fontSize: 10, bold: ci === 0, color: textColor, fontFace: "Calibri",
      valign: "middle", wrap: true,
    });
  });
});

addBanner(s6, "OpenHands: enterprise-grade autonomy at open-source economics");

// ═══════════════════════════════════════════════════════
// SLIDE 7: Implementation / Code View
// ═══════════════════════════════════════════════════════
let s7 = pptx.addSlide();
s7.background = { color: C.WHITE };
addTitle(s7, "Implementation", "Three deployment modes — CLI, SDK, or GitHub Action");

// Left: explanation
s7.addText("GitHub Action (Resolver)", {
  x: 0.5, y: 1.5, w: 5.5, h: 0.35,
  fontSize: 18, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri",
});
s7.addText(
  "• Label any issue with fix-me — agent auto-triages and opens a PR\n" +
  "• Mention @openhands on a PR for automated review and fixes\n" +
  "• Works with any GitHub repo — setup in 5 minutes\n" +
  "• 37% of the resolver's own commits are AI-generated",
  {
    x: 0.5, y: 1.95, w: 5.5, h: 1.5,
    fontSize: 12, color: C.CHARCOAL, fontFace: "Calibri",
    valign: "top", lineSpacingMultiple: 1.4,
  }
);

s7.addText("SDK (Programmatic)", {
  x: 0.5, y: 3.6, w: 5.5, h: 0.35,
  fontSize: 18, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri",
});
s7.addText(
  "• Composable Python library — define agents in code\n" +
  "• Run locally or scale to thousands in the cloud\n" +
  "• openhands.sdk: Agent, Conversation, LLM, Tool, MCP\n" +
  "• openhands.workspace: Docker or hosted API execution",
  {
    x: 0.5, y: 4.05, w: 5.5, h: 1.5,
    fontSize: 12, color: C.CHARCOAL, fontFace: "Calibri",
    valign: "top", lineSpacingMultiple: 1.4,
  }
);

// Right: code blocks
addCodeBlock(s7, 6.5, 1.5, 6.3, 2.0,
  "# .github/workflows/openhands-resolver.yml\n" +
  "name: OpenHands Resolver\n" +
  "on:\n" +
  "  issues:\n" +
  "    types: [labeled]\n" +
  "jobs:\n" +
  "  resolve:\n" +
  "    if: github.event.label.name == 'fix-me'\n" +
  "    uses: all-hands-ai/openhands-resolver@main\n" +
  "    with:\n" +
  "      llm-model: claude-opus-4-6"
);

addCodeBlock(s7, 6.5, 3.8, 6.3, 2.2,
  "# SDK usage\n" +
  "from openhands.sdk import Agent, Conversation\n" +
  "from openhands.workspace import DockerWorkspace\n\n" +
  "agent = Agent(\n" +
  "    model='claude-opus-4-6',\n" +
  "    tools=['file_ops', 'shell', 'git'],\n" +
  "    security_policy='medium'\n" +
  ")\n" +
  "workspace = DockerWorkspace(repo='my-org/my-repo')\n" +
  "result = agent.resolve(issue_id=123, workspace=workspace)"
);

addBanner(s7, "Setup in 5 minutes: copy YAML, set API key, label an issue");

// ═══════════════════════════════════════════════════════
// SLIDE 8: Key Metrics / Results
// ═══════════════════════════════════════════════════════
let s8 = pptx.addSlide();
s8.background = { color: C.WHITE };
addTitle(s8, "Proven Results", "Benchmarked and battle-tested in production");

addMetric(s8, 0.5, 1.5, 3.5, "77.6%", "SWE-Bench Verified resolve rate — highest among open-source agents (May 2026)");
addMetric(s8, 4.5, 1.5, 3.5, "~$3", "Cost per generated PR — real-world Go microservice upgrades across 50 services");
addMetric(s8, 8.5, 1.5, 3.5, "37%", "Self-written commits — the resolver writes its own codebase improvements");

// Secondary metrics row
addCard(s8, 0.5, 3.8, 3.8, 1.8, "Benchmark Performance", [
  { text: "#1 Claude 4.5 Opus", options: { fontSize: 11, bold: true, color: C.RED, fontFace: "Calibri", breakType: "none" }},
  { text: " — top in issue resolution, frontend, testing\n", options: { fontSize: 11, color: C.CHARCOAL, fontFace: "Calibri" }},
  { text: "#2 GPT-5.2 Codex", options: { fontSize: 11, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri", breakType: "none" }},
  { text: " — best at long-horizon greenfield tasks\n", options: { fontSize: 11, color: C.CHARCOAL, fontFace: "Calibri" }},
  { text: "Cost-effective: ", options: { fontSize: 11, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri", breakType: "none" }},
  { text: "Gemini 3 Flash, DeepSeek-v3.2", options: { fontSize: 11, color: C.CHARCOAL, fontFace: "Calibri" }},
]);

addCard(s8, 4.6, 3.8, 3.8, 1.8, "Production Proof Points",
  "• Used at TikTok, VMware, Roche, Amazon, Netflix, Apple, NVIDIA\n• 74.6k GitHub stars, 9.5k forks\n• Go microservice upgrades: $150 total vs $180K manual\n• 70% of routine issues auto-resolved"
);

addCard(s8, 8.7, 3.8, 3.8, 1.8, "Enterprise Readiness",
  "• K8s self-hosted for air-gapped environments\n• RBAC + audit logging + secrets management\n• Slack, Jira, Linear integrations\n• SOC 2 / HIPAA compatible architecture"
);

addBanner(s8, "These results are reproducible: open-source, model-agnostic, deployable on-premise");

// ═══════════════════════════════════════════════════════
// SLIDE 9: Key Data Flow (horizontal timeline)
// ═══════════════════════════════════════════════════════
let s9 = pptx.addSlide();
s9.background = { color: C.WHITE };
addTitle(s9, "Issue-to-PR Data Flow", "12 steps from GitHub issue to merged pull request");

const steps = [
  { num: 1, label: "Issue\nCreated", desc: "Developer labels\nissue fix-me" },
  { num: 2, label: "Webhook\nFires", desc: "GitHub sends\nevent payload" },
  { num: 3, label: "Session\nSpawned", desc: "Docker sandbox\nspins up" },
  { num: 4, label: "Codebase\nAnalyzed", desc: "Agent reads repo\nand issue" },
  { num: 5, label: "LLM\nReasoning", desc: "Claude plans\napproach" },
  { num: 6, label: "Code\nExecuted", desc: "Writes + runs\nin sandbox" },
];
const steps2 = [
  { num: 7, label: "Tools\nInvoked", desc: "Native + MCP\ntool calls" },
  { num: 8, label: "Git\nCommit", desc: "Changes on\nnew branch" },
  { num: 9, label: "PR\nOpened", desc: "Summary +\nissue link" },
  { num: 10, label: "CI/CD\nRuns", desc: "Tests + SAST\n+ lint" },
  { num: 11, label: "Confidence\nScored", desc: "Review gate\nevaluates" },
  { num: 12, label: "Merge /\nReview", desc: "Auto or\nhuman gate" },
];

[steps, steps2].forEach((row, ri) => {
  const baseY = 1.6 + ri * 2.6;
  row.forEach((step, i) => {
    const bx = 0.4 + i * 2.1;
    // Number circle
    addNumberCircle(s9, bx + 0.55, baseY, step.num, C.RED);
    // Box
    addFlowBox(s9, bx, baseY + 0.45, 1.6, 0.85, step.label, {
      fill: step.num <= 3 || step.num >= 11 ? C.LIGHT_BG : C.WHITE,
      border: step.num === 12 ? C.GREEN : C.BORDER,
      bold: true, fontSize: 11,
    });
    // Description
    s9.addText(step.desc, {
      x: bx, y: baseY + 1.35, w: 1.6, h: 0.6,
      fontSize: 9, color: C.MUTED, fontFace: "Calibri",
      align: "center", valign: "top", wrap: true,
    });
    // Arrow
    if (i < row.length - 1) {
      s9.addText("→", {
        x: bx + 1.6, y: baseY + 0.6, w: 0.5, h: 0.55,
        fontSize: 16, color: C.BORDER, align: "center", valign: "middle",
      });
    }
  });
});

addBanner(s9, "Typical resolution time: 5-15 minutes for common bug fixes | ~$3 per PR");

// ═══════════════════════════════════════════════════════
// SLIDE 10: Summary / CTA
// ═══════════════════════════════════════════════════════
let s10 = pptx.addSlide();
s10.background = { color: C.WHITE };
addTitle(s10, "Summary & Next Steps");

addCard(s10, 0.5, 1.4, 3.8, 2.6, "Why OpenHands?",
  "• 77.6% SWE-Bench — state-of-the-art resolve rate\n• Open source (74.6k★) — no vendor lock-in\n• Model-agnostic — 100+ LLM providers\n• Sandboxed — isolated Docker per agent\n• Event-sourced — full audit trail\n• Self-hosted — air-gapped K8s support"
);
addCard(s10, 4.6, 1.4, 3.8, 2.6, "ROI Case",
  "• ~$3 per PR vs $350/hr developer time\n• 70% of routine issues auto-resolved\n• Go microservices: $150 vs $180K manual\n• 37% autonomous commits (dogfooding)\n• MTTR: 4 hours → 15 minutes\n• Test coverage: 35% → 85%"
);
addCard(s10, 8.7, 1.4, 3.8, 2.6, "Getting Started",
  "Week 1: GitHub Action setup (5 min)\nWeek 2: Label 10 issues as fix-me\nWeek 3: Review agent PRs, tune threshold\nWeek 4: Enable auto-merge for high-confidence\nMonth 2: SDK integration for custom workflows\nMonth 3: Enterprise K8s deployment"
);

// CTA box
s10.addShape(pptx.ShapeType.rect, {
  x: 0.5, y: 4.5, w: 12.0, h: 1.6,
  fill: { color: C.LIGHT_BG },
  line: { color: C.BORDER, width: 1 },
  rectRadius: 0.08,
});
s10.addText("Recommended Next Step", {
  x: 0.7, y: 4.6, w: 11.6, h: 0.4,
  fontSize: 18, bold: true, color: C.NAVY_DEEP, fontFace: "Calibri",
});
s10.addText(
  "Start with the GitHub Action Resolver on one repository. Label 10 low-priority issues as fix-me. " +
  "Review the agent's PRs for 2 weeks — this builds confidence in the system before expanding. " +
  "Typical time to first value: under 1 hour.",
  {
    x: 0.7, y: 5.05, w: 11.6, h: 0.9,
    fontSize: 13, color: C.CHARCOAL, fontFace: "Calibri",
    valign: "top", wrap: true, lineSpacingMultiple: 1.3,
  }
);

addBanner(s10, "From issue to merged PR in minutes — every action sandboxed, logged, auditable");

// ── Save ──
const outPath = "openhands-autonomous-coding-pipeline-architecture.pptx";
pptx.writeFile({ fileName: outPath }).then(() => {
  console.log(`✓ Saved: ${outPath} (10 slides, Enterprise Consulting theme)`);
});
