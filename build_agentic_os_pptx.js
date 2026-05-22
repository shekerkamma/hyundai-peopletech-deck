const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

// ─── Theme ───
const C = {
  WHITE: 'FFFFFF', CHARCOAL: '1A1A1A', NAVY_DEEP: '1F3B6E',
  NAVY_CARD: '0D3B5E', RED: 'E31837', LIGHT_BG: 'F5F7FA',
  BORDER: 'D0D5DD', MUTED: '6B7280', CODE_BG: 'F0F2F5'
};

pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'PeopleTech AI Engineering';
pptx.title = 'Agentic OS Architecture';

// ─── Helpers ───
function addTitle(slide, text, subtitle) {
  slide.addText(text, { x: 0.5, y: 0.25, w: 12.5, h: 0.7,
    fontSize: 38, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
  if (subtitle) slide.addText(subtitle, { x: 0.5, y: 0.9, w: 12.5, h: 0.4,
    fontSize: 15, color: C.MUTED, fontFace: 'Calibri' });
}

function addCard(slide, x, y, w, h, header, body, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h,
    line: { color: C.BORDER, width: 1 }, fill: { color: opts.fill || C.WHITE },
    rectRadius: 0.08 });
  if (header) {
    slide.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.38,
      fill: { color: opts.headerColor || C.NAVY_CARD }, line: { color: opts.headerColor || C.NAVY_CARD, width: 0 },
      rectRadius: 0.08 });
    slide.addText(header, { x: x + 0.12, y: y + 0.06, w: w - 0.24, h: 0.28,
      fontSize: 12, bold: true, color: C.WHITE, fontFace: 'Calibri' });
  }
  const bodyY = header ? y + 0.44 : y + 0.12;
  const bodyH = header ? h - 0.56 : h - 0.24;
  if (typeof body === 'string') {
    slide.addText(body, { x: x + 0.12, y: bodyY, w: w - 0.24, h: bodyH,
      fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri', valign: 'top', wrap: true });
  } else {
    slide.addText(body, { x: x + 0.12, y: bodyY, w: w - 0.24, h: bodyH,
      fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri', valign: 'top', wrap: true });
  }
}

function addMetric(slide, x, y, w, value, label) {
  slide.addText(value, { x, y, w, h: 1.1, fontSize: 72, bold: true,
    color: C.RED, fontFace: 'Calibri', align: 'left' });
  slide.addText(label, { x, y: y + 1.0, w, h: 0.5, fontSize: 13,
    color: C.CHARCOAL, fontFace: 'Calibri', align: 'left' });
}

function addCodeBlock(slide, x, y, w, h, code) {
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h,
    fill: { color: C.CODE_BG }, line: { color: C.BORDER, width: 1 },
    rectRadius: 0.06 });
  slide.addText(code, { x: x + 0.12, y: y + 0.1, w: w - 0.24, h: h - 0.2,
    fontSize: 11, color: C.CHARCOAL, fontFace: 'Courier New', valign: 'top', wrap: true });
}

function addBanner(slide, text) {
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 6.85, w: 13.33, h: 0.65,
    fill: { color: C.NAVY_CARD }, line: { color: C.NAVY_CARD, width: 0 } });
  slide.addText(text, { x: 0.4, y: 6.88, w: 12.5, h: 0.58,
    fontSize: 15, bold: true, color: C.WHITE, fontFace: 'Calibri',
    align: 'center', valign: 'middle' });
}

function addNumberCircle(slide, x, y, num, color) {
  slide.addShape(pptx.ShapeType.ellipse, { x, y, w: 0.35, h: 0.35,
    fill: { color: color || C.NAVY_DEEP }, line: { color: color || C.NAVY_DEEP, width: 0 } });
  slide.addText(String(num), { x, y, w: 0.35, h: 0.35,
    fontSize: 13, bold: true, color: C.WHITE, fontFace: 'Calibri',
    align: 'center', valign: 'middle' });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 1 — Title
// ═══════════════════════════════════════════════════════════
let s1 = pptx.addSlide();
s1.background = { fill: C.WHITE };
s1.addText('Agentic OS', { x: 0.5, y: 1.5, w: 7, h: 1.2,
  fontSize: 48, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
s1.addText('System Architecture', { x: 0.5, y: 2.6, w: 7, h: 0.6,
  fontSize: 28, color: C.CHARCOAL, fontFace: 'Calibri' });
s1.addText('An operating system for AI-powered work:\nshared context, client isolation, persistent memory, autonomous execution', {
  x: 0.5, y: 3.4, w: 7, h: 0.8,
  fontSize: 14, color: C.MUTED, fontFace: 'Calibri', lineSpacing: 22 });
// Accent pill
s1.addShape(pptx.ShapeType.roundRect, { x: 0.5, y: 4.5, w: 2.8, h: 0.38,
  fill: { color: C.RED }, rectRadius: 0.1 });
s1.addText('4 Layers  |  136 Skills  |  Always On', { x: 0.5, y: 4.5, w: 2.8, h: 0.38,
  fontSize: 10, bold: true, color: C.WHITE, fontFace: 'Calibri', align: 'center', valign: 'middle' });
// Right side icon grid
const icons = [
  { emoji: 'Shared\nContext', c: 'E8C872' },
  { emoji: 'Client\nContext', c: '4A9EDE' },
  { emoji: 'Memory\nLayer', c: 'E57373' },
  { emoji: 'Execution\nLayer', c: '81C784' }
];
icons.forEach((ic, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const ix = 8.5 + col * 2.2;
  const iy = 1.8 + row * 2.2;
  s1.addShape(pptx.ShapeType.roundRect, { x: ix, y: iy, w: 1.8, h: 1.6,
    fill: { color: C.LIGHT_BG }, line: { color: ic.c, width: 2 }, rectRadius: 0.12 });
  s1.addText(ic.emoji, { x: ix, y: iy + 0.3, w: 1.8, h: 1.0,
    fontSize: 14, bold: true, color: ic.c, fontFace: 'Calibri',
    align: 'center', valign: 'middle' });
});
addBanner(s1, 'From single conversations to a fully staffed AI department');

// ═══════════════════════════════════════════════════════════
// SLIDE 2 — What is Agentic OS?
// ═══════════════════════════════════════════════════════════
let s2 = pptx.addSlide();
s2.background = { fill: C.WHITE };
addTitle(s2, 'What is Agentic OS?', 'An operating system architecture for AI-powered work');

addCard(s2, 0.5, 1.6, 3.8, 2.8, 'Context Layer',
  'Universal knowledge, skills, and brand standards that every project inherits automatically. Your CLAUDE.md, skills library, and brand identity.');
addCard(s2, 4.6, 1.6, 3.8, 2.8, 'Isolation Layer',
  'Per-client workspaces that override shared defaults. Each client gets their own CLAUDE.md, skills, brand context, and project plans. No cross-contamination.');
addCard(s2, 8.7, 1.6, 3.8, 2.8, 'Intelligence Layer',
  'Persistent memory that survives across sessions. Always-loaded learnings plus on-demand semantic search, relational lookup, and cross-tool retrieval.');

s2.addText('The result: an AI that scales across clients while maintaining deep, personalized context for each one.', {
  x: 0.5, y: 4.8, w: 12.0, h: 0.5, fontSize: 13, italic: true, color: C.MUTED, fontFace: 'Calibri' });

addBanner(s2, 'Not a chatbot. An operating system.');

// ═══════════════════════════════════════════════════════════
// SLIDE 3 — The Problem
// ═══════════════════════════════════════════════════════════
let s3 = pptx.addSlide();
s3.background = { fill: C.WHITE };
addTitle(s3, 'The Problem', 'Why a single AI conversation is not enough');

// Flow: Before
s3.addText('Today: Fragmented AI Usage', { x: 0.5, y: 1.5, w: 12, h: 0.3,
  fontSize: 16, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

const problems = [
  { h: 'No Memory', b: 'Every conversation starts from zero. The AI forgets your preferences, brand voice, and past decisions.' },
  { h: 'No Isolation', b: 'Client A\'s confidential data leaks into Client B\'s context. Brand voices bleed together.' },
  { h: 'No Automation', b: 'Every task requires manual invocation. No scheduled workflows, no chained skills, no background processing.' }
];
problems.forEach((p, i) => {
  addCard(s3, 0.5 + i * 4.1, 2.0, 3.8, 2.6, p.h, p.b, { headerColor: 'B91C1C' });
});

s3.addShape(pptx.ShapeType.rect, { x: 0.5, y: 5.0, w: 12.3, h: 0.04,
  fill: { color: C.BORDER } });

s3.addText('Agentic OS solves all three: persistent context + client isolation + autonomous execution', {
  x: 0.5, y: 5.2, w: 12.0, h: 0.4, fontSize: 13, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

// ═══════════════════════════════════════════════════════════
// SLIDE 4 — Architecture Overview
// ═══════════════════════════════════════════════════════════
let s4 = pptx.addSlide();
s4.background = { fill: C.WHITE };
addTitle(s4, 'Architecture Overview', 'Four layers, one system');

// Left: layer diagram
const layers = [
  { label: 'Shared Context', sub: 'CLAUDE.md, Skills, Brand, Planning', color: 'E8C872', bg: 'FFF8E1' },
  { label: 'Client Context', sub: 'Per-client overrides, isolated workspaces', color: '4A9EDE', bg: 'E8F4FD' },
  { label: 'Memory Layer', sub: 'Learnings + on-demand retrieval', color: 'E57373', bg: 'FDE8E8' },
  { label: 'Execution Layer', sub: 'Skills, Cron, Always-On, Channels', color: '81C784', bg: 'ECFDF5' }
];
layers.forEach((l, i) => {
  const ly = 1.6 + i * 1.2;
  s4.addShape(pptx.ShapeType.roundRect, { x: 0.5, y: ly, w: 7.5, h: 0.95,
    fill: { color: l.bg }, line: { color: l.color, width: 2 }, rectRadius: 0.1 });
  addNumberCircle(s4, 0.7, ly + 0.3, i + 1, l.color);
  s4.addText(l.label, { x: 1.2, y: ly + 0.1, w: 5, h: 0.4,
    fontSize: 16, bold: true, color: C.CHARCOAL, fontFace: 'Calibri' });
  s4.addText(l.sub, { x: 1.2, y: ly + 0.5, w: 6, h: 0.35,
    fontSize: 11, color: C.MUTED, fontFace: 'Calibri' });
});

// Right: flow
s4.addText('Data Flow', { x: 8.5, y: 1.6, w: 4, h: 0.35,
  fontSize: 16, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

const flows = [
  'Shared standards flow to all clients',
  'Client context overrides shared defaults',
  'Memory loaded at session start',
  'On-demand retrieval for deep context',
  'Skills chain into multi-step workflows',
  'Cron triggers run autonomously',
  'Outputs delivered via any channel'
];
flows.forEach((f, i) => {
  addNumberCircle(s4, 8.5, 2.15 + i * 0.55, i + 1, C.NAVY_DEEP);
  s4.addText(f, { x: 9.0, y: 2.15 + i * 0.55, w: 4, h: 0.4,
    fontSize: 11, color: C.CHARCOAL, fontFace: 'Calibri', valign: 'middle' });
});

// ═══════════════════════════════════════════════════════════
// SLIDE 5 — Components Deep Dive
// ═══════════════════════════════════════════════════════════
let s5 = pptx.addSlide();
s5.background = { fill: C.WHITE };
addTitle(s5, 'Components Deep Dive', 'What lives in each layer');

addCard(s5, 0.5, 1.5, 5.8, 2.2, 'Shared Context',
  'Work Preferences: CLAUDE.md, SOUL.md, user.md\nSkills: research, copywriting, video, cron\nBrand Context: voice-profile, ICP, positioning, assets\nPlanning Frameworks: quick task, planned project, full biz\nOutput Storage: projects/ > category/ > date/');

addCard(s5, 6.7, 1.5, 5.8, 2.2, 'Client/Project Context',
  'Client CLAUDE.md overrides root rules\nClient-specific skills (taste-skill, design-skill)\nIsolated brand context per client\nProject plans and deliverable trackers\nContext Overwrites: client version always wins');

addCard(s5, 0.5, 4.0, 5.8, 2.2, 'Memory Layer',
  'Fed Every Time: learnings.md, memory/ (dated), hooks\nOn-Demand: MCP-SEARCH (semantic), MEMHULCE (exact)\nRelational: LLM Wiki, Obsidian knowledge graphs\nCross-tool: OpenBrain spans Notion, Slack, email\nTwo-tier design: fast context + deep archive');

addCard(s5, 6.7, 4.0, 5.8, 2.2, 'Execution Layer',
  'Skill Systems: multi-step chained workflows\nCron Jobs: scheduled, event-driven automation\nUPS / Always On: 24/7 cloud, no laptop needed\nChannels: CLI, desktop, mobile, web, Slack\nModular: adopt what you need, skip the rest');

// ═══════════════════════════════════════════════════════════
// SLIDE 6 — Comparison: Before vs After
// ═══════════════════════════════════════════════════════════
let s6 = pptx.addSlide();
s6.background = { fill: C.WHITE };
addTitle(s6, 'Before vs After Agentic OS', 'What changes when you adopt the system');

const tableRows = [
  ['Capability', 'Without Agentic OS', 'With Agentic OS'],
  ['Context', 'Starts from zero every session', 'Persistent memory + learnings'],
  ['Client Work', 'Brand voices bleed together', 'Fully isolated per client'],
  ['Skills', 'Re-explain every task', 'Invoke /skill-name instantly'],
  ['Automation', 'Manual every time', 'Cron + chained workflows'],
  ['Availability', 'Only when laptop is open', '24/7 cloud execution'],
  ['Scalability', 'One conversation at a time', 'Parallel client workstreams']
];

const colWidths = [2.5, 4.5, 4.5];
tableRows.forEach((row, ri) => {
  const ry = 1.5 + ri * 0.62;
  row.forEach((cell, ci) => {
    const cx = 0.5 + colWidths.slice(0, ci).reduce((a, b) => a + b, 0);
    const isHeader = ri === 0;
    const isWinner = ci === 2 && ri > 0;
    const fillColor = isHeader ? C.NAVY_DEEP : (isWinner ? 'FEE2E2' : (ri % 2 === 0 ? C.LIGHT_BG : C.WHITE));
    const textColor = isHeader ? C.WHITE : (isWinner ? C.RED : C.CHARCOAL);

    s6.addShape(pptx.ShapeType.rect, { x: cx, y: ry, w: colWidths[ci], h: 0.55,
      fill: { color: fillColor }, line: { color: C.BORDER, width: 0.5 } });
    s6.addText(cell, { x: cx + 0.1, y: ry + 0.05, w: colWidths[ci] - 0.2, h: 0.45,
      fontSize: isHeader ? 12 : 11, bold: isHeader || ci === 0, color: textColor,
      fontFace: 'Calibri', valign: 'middle', wrap: true });
  });
});

// ═══════════════════════════════════════════════════════════
// SLIDE 7 — Directory Structure
// ═══════════════════════════════════════════════════════════
let s7 = pptx.addSlide();
s7.background = { fill: C.WHITE };
addTitle(s7, 'Directory Structure', 'Files over databases — inspectable, versionable, portable');

s7.addText('Shared Context', { x: 0.5, y: 1.5, w: 5, h: 0.3,
  fontSize: 14, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

addCodeBlock(s7, 0.5, 1.9, 5.5, 2.8,
  'agentic-os/\n' +
  '├── CLAUDE.md          # Root rules\n' +
  '├── SOUL.md            # Personality & tone\n' +
  '├── user.md            # User preferences\n' +
  '├── context/\n' +
  '│   ├── brand_context/ # Voice, ICP, positioning\n' +
  '│   ├── learnings.md   # Accumulated insights\n' +
  '│   └── memory/        # Dated entries\n' +
  '├── projects/          # Output storage\n' +
  '└── .claude/skills/    # Skill definitions');

s7.addText('Client Context (isolated)', { x: 7, y: 1.5, w: 5.5, h: 0.3,
  fontSize: 14, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

addCodeBlock(s7, 7, 1.9, 5.5, 2.8,
  'clients/client-one/\n' +
  '├── CLAUDE.md          # Overrides root\n' +
  '├── brand_context/     # Client brand\n' +
  '├── context/\n' +
  '│   ├── learnings.md   # Client learnings\n' +
  '│   └── memory/        # Client memory\n' +
  '├── projects/          # Client outputs\n' +
  '└── .claude/skills/    # Client skills');

s7.addText('Key Principle: Everything is a file. Git tracks changes. Copy to move.', {
  x: 0.5, y: 5.2, w: 12, h: 0.4, fontSize: 13, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

// ═══════════════════════════════════════════════════════════
// SLIDE 8 — Key Metrics
// ═══════════════════════════════════════════════════════════
let s8 = pptx.addSlide();
s8.background = { fill: C.WHITE };
addTitle(s8, 'Key Metrics', 'What Agentic OS delivers');

addMetric(s8, 0.5, 1.8, 3.5, '136', 'Skills available globally\nacross all projects');
addMetric(s8, 4.5, 1.8, 3.5, '4', 'Layers working together:\ncontext, isolation, memory, execution');
addMetric(s8, 8.5, 1.8, 3.5, '24/7', 'Always-on execution\nno laptop dependency');

s8.addShape(pptx.ShapeType.rect, { x: 0.5, y: 4.2, w: 12, h: 0.04,
  fill: { color: C.BORDER } });

addCard(s8, 0.5, 4.5, 3.8, 1.5, 'Context Retention',
  'Memory persists across sessions. Learnings compound. The AI gets better at your work over time.');
addCard(s8, 4.6, 4.5, 3.8, 1.5, 'Client Isolation',
  'Zero cross-contamination. Delete one client folder without affecting any other. Full data sovereignty.');
addCard(s8, 8.7, 4.5, 3.8, 1.5, 'Skill Reuse',
  'Build once, invoke everywhere. Skills work across all clients with consistent quality and format.');

// ═══════════════════════════════════════════════════════════
// SLIDE 9 — Data Flow
// ═══════════════════════════════════════════════════════════
let s9 = pptx.addSlide();
s9.background = { fill: C.WHITE };
addTitle(s9, 'Key Data Flow', 'How a typical session works end to end');

const steps = [
  { n: 1, label: 'Session\nStarts', sub: 'Hooks fire', color: 'E8C872' },
  { n: 2, label: 'Shared\nContext', sub: 'Rules load', color: 'E8C872' },
  { n: 3, label: 'Client\nOverride', sub: 'Scope set', color: '4A9EDE' },
  { n: 4, label: 'Skill\nInvoked', sub: '/command', color: '4A9EDE' },
  { n: 5, label: 'Memory\nQueried', sub: 'Context found', color: 'E57373' },
  { n: 6, label: 'Output\nGenerated', sub: 'Deliverable', color: '81C784' },
  { n: 7, label: 'Session\nEnds', sub: 'Learnings saved', color: 'E57373' }
];

steps.forEach((st, i) => {
  const sx = 0.3 + i * 1.8;
  const sy = 2.0;
  // Box
  s9.addShape(pptx.ShapeType.roundRect, { x: sx, y: sy, w: 1.5, h: 2.2,
    fill: { color: C.WHITE }, line: { color: st.color, width: 2 }, rectRadius: 0.1 });
  // Number circle
  addNumberCircle(s9, sx + 0.575, sy + 0.15, st.n, st.color);
  // Label
  s9.addText(st.label, { x: sx, y: sy + 0.6, w: 1.5, h: 0.7,
    fontSize: 13, bold: true, color: C.CHARCOAL, fontFace: 'Calibri',
    align: 'center', valign: 'middle' });
  // Sub
  s9.addText(st.sub, { x: sx, y: sy + 1.4, w: 1.5, h: 0.4,
    fontSize: 10, color: C.MUTED, fontFace: 'Calibri', align: 'center' });
  // Arrow (except last)
  if (i < steps.length - 1) {
    s9.addShape(pptx.ShapeType.rightArrow, {
      x: sx + 1.55, y: sy + 0.85, w: 0.2, h: 0.35,
      fill: { color: C.BORDER }, line: { color: C.BORDER, width: 0 }
    });
  }
});

addBanner(s9, 'Every session starts informed and ends smarter');

// ═══════════════════════════════════════════════════════════
// SLIDE 10 — Summary / CTA
// ═══════════════════════════════════════════════════════════
let s10 = pptx.addSlide();
s10.background = { fill: C.WHITE };
addTitle(s10, 'Summary', 'Three principles that make Agentic OS work');

addCard(s10, 0.5, 1.6, 3.8, 3.0, 'Files Over Databases',
  'All context stored as markdown in a directory tree. Inspectable with cat, versionable with git, portable by copying a folder.\n\nNo vendor lock-in. No proprietary formats. Your AI knowledge base is just files.');

addCard(s10, 4.6, 1.6, 3.8, 3.0, 'Override Over Merge',
  'Client context doesn\'t merge with shared context — it overwrites. This prevents subtle bugs where a client inherits an unwanted rule.\n\nExplicit is better than implicit.');

addCard(s10, 8.7, 1.6, 3.8, 3.0, 'Skills Over Prompts',
  'Each capability is a reusable, versioned, composable skill — not a fragile system prompt.\n\nBuild once, invoke everywhere. Chain into workflows. Share via marketplace.');

addBanner(s10, 'Shared standards + local autonomy + persistent memory = AI that scales like a chain but feels boutique');

// ─── Generate ───
const outPath = 'agentic-os-architecture.pptx';
pptx.writeFile({ fileName: outPath })
  .then(() => console.log(`Created: ${outPath}`))
  .catch(err => console.error(err));
