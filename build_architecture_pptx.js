const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

// ============================================================================
// ENTERPRISE CONSULTING THEME
// ============================================================================
const C = {
  WHITE: 'FFFFFF', CHARCOAL: '1A1A1A', NAVY_DEEP: '1F3B6E',
  NAVY_CARD: '0D3B5E', RED: 'E31837', LIGHT_BG: 'F5F7FA',
  BORDER: 'D0D5DD', MUTED: '6B7280', CODE_BG: 'F0F2F5'
};

pptx.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5

// ============================================================================
// HELPERS
// ============================================================================
function addCard(slide, x, y, w, h, header, body, opts = {}) {
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h,
    line: { color: C.BORDER, width: 1 }, fill: { color: opts.fill || C.WHITE } });
  if (header) {
    slide.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.38,
      fill: { color: C.NAVY_CARD }, line: { color: C.NAVY_CARD, width: 0 } });
    slide.addText(header, { x: x + 0.12, y: y + 0.06, w: w - 0.24, h: 0.28,
      fontSize: 12, bold: true, color: C.WHITE, fontFace: 'Calibri' });
  }
  if (typeof body === 'string') {
    slide.addText(body, { x: x + 0.12, y: y + (header ? 0.44 : 0.12), w: w - 0.24,
      h: h - (header ? 0.56 : 0.24), fontSize: 12, color: C.CHARCOAL,
      fontFace: 'Calibri', valign: 'top', wrap: true });
  } else if (Array.isArray(body)) {
    const rows = body.map(b => ({ text: b, options: { bullet: true, fontSize: 11, color: C.CHARCOAL, fontFace: 'Calibri' } }));
    slide.addText(rows, { x: x + 0.12, y: y + (header ? 0.44 : 0.12), w: w - 0.24,
      h: h - (header ? 0.56 : 0.24), valign: 'top', wrap: true });
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
    fill: { color: C.CODE_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addText(code, { x: x + 0.12, y: y + 0.1, w: w - 0.24, h: h - 0.2,
    fontSize: 11, color: C.CHARCOAL, fontFace: 'Courier New',
    valign: 'top', wrap: true });
}

function addTableRow(slide, x, y, w, rowH, cols, highlightCol = null) {
  const colW = w / cols.length;
  cols.forEach((text, i) => {
    const fill = (i === highlightCol) ? 'FEE2E2' : (i === 0 ? C.LIGHT_BG : C.WHITE);
    const textColor = (i === highlightCol) ? C.RED : C.CHARCOAL;
    slide.addShape(pptx.ShapeType.rect, { x: x + i * colW, y, w: colW, h: rowH,
      fill: { color: fill }, line: { color: C.BORDER, width: 0.5 } });
    slide.addText(text, { x: x + i * colW + 0.1, y: y + 0.05, w: colW - 0.2, h: rowH - 0.1,
      fontSize: 12, color: textColor, fontFace: 'Calibri',
      bold: (i === 0), valign: 'middle', wrap: true });
  });
}

function addBanner(slide, text) {
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 6.8, w: 13.33, h: 0.7,
    fill: { color: C.NAVY_CARD }, line: { color: C.NAVY_CARD, width: 0 } });
  slide.addText(text, { x: 0.4, y: 6.85, w: 12.53, h: 0.6,
    fontSize: 15, bold: true, color: C.WHITE, fontFace: 'Calibri',
    align: 'center', valign: 'middle' });
}

function addTitle(slide, text, subtitle = '') {
  slide.addText(text, { x: 0.5, y: 0.25, w: 12.33, h: 0.7,
    fontSize: 38, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
  if (subtitle) slide.addText(subtitle, { x: 0.5, y: 0.9, w: 12.33, h: 0.4,
    fontSize: 15, color: C.MUTED, fontFace: 'Calibri' });
}

// ============================================================================
// SLIDE 1 — TITLE
// ============================================================================
let slide = pptx.addSlide();
slide.background = { color: C.WHITE };

// Left 60%
slide.addText('AI PLANT OPERATIONS PLATFORM', { x: 0.5, y: 0.8, w: 7.5, h: 0.4,
  fontSize: 14, bold: true, color: C.MUTED, fontFace: 'Calibri', letterSpacing: 3 });
slide.addText('Architecture Guide', { x: 0.5, y: 1.4, w: 7.5, h: 1.2,
  fontSize: 42, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
slide.addText('Hyundai  ×  PeopleTech', { x: 0.5, y: 2.7, w: 7.5, h: 0.6,
  fontSize: 24, color: C.MUTED, fontFace: 'Calibri' });
// RED tagline pill
slide.addShape(pptx.ShapeType.roundRect, { x: 0.5, y: 3.6, w: 4.5, h: 0.45,
  fill: { color: 'FEE2E2' }, line: { color: C.RED, width: 1 }, rectRadius: 0.1 });
slide.addText('Edge-to-Cloud · 8 Use Cases · Integration-First', { x: 0.6, y: 3.6, w: 4.3, h: 0.45,
  fontSize: 12, bold: true, color: C.RED, fontFace: 'Calibri', valign: 'middle' });
// Subtitle
slide.addText('End-to-end platform architecture for AI-driven manufacturing\nacross Hyundai\'s global plant network', { x: 0.5, y: 4.3, w: 7, h: 0.8,
  fontSize: 14, color: C.CHARCOAL, fontFace: 'Calibri', lineSpacingMultiple: 1.4 });

// Right 40% — icon representation (4 layer boxes)
const layers = ['Plant Floor / Edge', 'Streaming & Integration', 'AI / ML Compute', 'Application & UX'];
const layerColors = [C.NAVY_DEEP, 'C2410C', '15803D', 'BE185D'];
layers.forEach((lbl, i) => {
  const ly = 1.0 + i * 1.3;
  slide.addShape(pptx.ShapeType.rect, { x: 8.5, y: ly, w: 4.3, h: 1.0,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addShape(pptx.ShapeType.rect, { x: 8.5, y: ly, w: 0.08, h: 1.0,
    fill: { color: layerColors[i] }, line: { color: layerColors[i], width: 0 } });
  slide.addText(lbl, { x: 8.75, y: ly, w: 3.9, h: 1.0,
    fontSize: 13, bold: true, color: C.CHARCOAL, fontFace: 'Calibri', valign: 'middle' });
});

addBanner(slide, 'Hyundai × PeopleTech · AI Manufacturing Practice · May 2026');

// ============================================================================
// SLIDE 2 — WHAT IS IT?
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'What is the AI Plant Operations Platform?', 'One platform, eight use cases, shared infrastructure');

addCard(slide, 0.5, 1.5, 3.8, 3.5, 'Edge-to-Cloud',
  'Connects plant-floor sensors, cameras, and scanners through edge compute to cloud AI models. Sub-200ms line-side latency for real-time decisions. Runs on NVIDIA Jetson, Hailo, and Intel edge with AWS IoT Greengrass / Azure IoT Edge.');
addCard(slide, 4.6, 1.5, 3.8, 3.5, 'Integration-First',
  'Plugs into Hyundai\'s existing SAP MES/ERP, SAP PM, AVEVA PI historian — no rip-and-replace. Pre-built connector library with standardized event schemas for line-hold, work-order generation, and quality events.');
addCard(slide, 8.7, 1.5, 4.1, 3.5, '8 AI Use Cases',
  ['Visual Inspection — CNN defect detection',
   'Variant Confirmation — VIN/BOM match',
   'Seating Validation — fitment checks',
   'SOP Compliance — pose estimation',
   'Predictive Quality — sensor fusion ML',
   'Predictive Maintenance — anomaly detection',
   'Safety Monitoring — PPE/zone AI',
   'Digital Traceability — genealogy graph']);

slide.addText('Designed to pilot on one line and scale across Ulsan, Asan, HMGMA, HMMA, HMMC, HMI.', {
  x: 0.5, y: 5.3, w: 12.33, h: 0.5, fontSize: 13, italic: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

addBanner(slide, 'Shared infrastructure · Shared MLOps · Scale from 1 line to enterprise');

// ============================================================================
// SLIDE 3 — THE PROBLEM
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'The Problem', 'Why siloed solutions fail at plant scale');

// Top flow: Siloed → Fragmented → Slow → Costly
const flowLabels = ['Siloed Point\nSolutions', 'Fragmented\nData', 'Slow Response\nTimes', 'High Cost of\nQuality Failures'];
flowLabels.forEach((lbl, i) => {
  const fx = 0.5 + i * 3.15;
  slide.addShape(pptx.ShapeType.rect, { x: fx, y: 1.5, w: 2.8, h: 0.8,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addText(lbl, { x: fx, y: 1.5, w: 2.8, h: 0.8,
    fontSize: 12, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  if (i < 3) {
    slide.addText('→', { x: fx + 2.8, y: 1.5, w: 0.35, h: 0.8,
      fontSize: 18, color: C.RED, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  }
});

// 3 problem cards
addCard(slide, 0.5, 2.7, 3.9, 2.5, 'No Shared Platform',
  'Each use case built on its own stack. Separate cameras, separate databases, separate dashboards. No cross-use-case data fusion. Infrastructure cost multiplied by 8.');
addCard(slide, 4.7, 2.7, 3.9, 2.5, 'Integration Gap',
  'AI models produce insights that never reach operators. Manual hand-offs between AI outputs and SAP/MES. No automated line-hold, work-order generation, or escalation.');
addCard(slide, 8.9, 2.7, 3.9, 2.5, 'Latency & Scale',
  'Cloud-only inference adds 500ms–2s latency — too slow for line-side decisions. Models trained once, never retrained. No OTA update path. Scaling from 1 line to 50 requires re-architecture.');

addBanner(slide, 'The platform approach: one infrastructure, eight use cases, one integration layer');

// ============================================================================
// SLIDE 4 — ARCHITECTURE OVERVIEW
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Architecture Overview', 'Four-layer edge-to-cloud platform');

// Left 65%: simplified architecture diagram representation
// Layer 1 - Edge
slide.addShape(pptx.ShapeType.rect, { x: 0.5, y: 1.5, w: 7.8, h: 1.1,
  fill: { color: 'F0F9FF' }, line: { color: 'BAE6FD', width: 1 } });
slide.addText('PLANT FLOOR / EDGE CAPTURE', { x: 0.6, y: 1.55, w: 3, h: 0.3,
  fontSize: 10, bold: true, color: '0369A1', fontFace: 'Calibri' });
const edgeItems = ['Vision Cameras\n(Cognex, Basler)', 'IoT Sensors\n(Vib, Acoustic)', 'RFID / Barcode\nScanners', 'Edge Compute\n(Jetson, Hailo)'];
edgeItems.forEach((lbl, i) => {
  slide.addShape(pptx.ShapeType.rect, { x: 0.7 + i * 1.9, y: 1.9, w: 1.7, h: 0.6,
    fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 } });
  slide.addText(lbl, { x: 0.7 + i * 1.9, y: 1.9, w: 1.7, h: 0.6,
    fontSize: 9, color: C.CHARCOAL, fontFace: 'Calibri', align: 'center', valign: 'middle' });
});

// Layer 2 - Streaming
slide.addShape(pptx.ShapeType.rect, { x: 0.5, y: 2.8, w: 7.8, h: 1.1,
  fill: { color: 'FFF7ED' }, line: { color: 'FED7AA', width: 1 } });
slide.addText('STREAMING & INTEGRATION', { x: 0.6, y: 2.85, w: 3, h: 0.3,
  fontSize: 10, bold: true, color: 'C2410C', fontFace: 'Calibri' });
const streamItems = ['Kafka Event\nStream', 'SAP MES / ERP\nConnectors', 'AVEVA PI\nHistorian', 'Quality DB\nNeo4j Graph'];
streamItems.forEach((lbl, i) => {
  slide.addShape(pptx.ShapeType.rect, { x: 0.7 + i * 1.9, y: 3.2, w: 1.7, h: 0.6,
    fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 } });
  slide.addText(lbl, { x: 0.7 + i * 1.9, y: 3.2, w: 1.7, h: 0.6,
    fontSize: 9, color: C.CHARCOAL, fontFace: 'Calibri', align: 'center', valign: 'middle' });
});

// Layer 3 - AI
slide.addShape(pptx.ShapeType.rect, { x: 0.5, y: 4.1, w: 7.8, h: 1.1,
  fill: { color: 'F0FDF4' }, line: { color: 'BBF7D0', width: 1 } });
slide.addText('AI / ML COMPUTE (CLOUD)', { x: 0.6, y: 4.15, w: 3, h: 0.3,
  fontSize: 10, bold: true, color: '15803D', fontFace: 'Calibri' });
const aiItems = ['SageMaker /\nAzure ML', '8 Use Case\nModel Groups', 'MLOps\nPipeline', 'Data Lake /\nFeature Store'];
aiItems.forEach((lbl, i) => {
  slide.addShape(pptx.ShapeType.rect, { x: 0.7 + i * 1.9, y: 4.5, w: 1.7, h: 0.6,
    fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 } });
  slide.addText(lbl, { x: 0.7 + i * 1.9, y: 4.5, w: 1.7, h: 0.6,
    fontSize: 9, color: C.CHARCOAL, fontFace: 'Calibri', align: 'center', valign: 'middle' });
});

// Layer 4 - App
slide.addShape(pptx.ShapeType.rect, { x: 0.5, y: 5.4, w: 7.8, h: 1.1,
  fill: { color: 'FDF2F8' }, line: { color: 'FBCFE8', width: 1 } });
slide.addText('APPLICATION & UX', { x: 0.6, y: 5.45, w: 3, h: 0.3,
  fontSize: 10, bold: true, color: 'BE185D', fontFace: 'Calibri' });
const uxItems = ['Quality\nDashboard', 'Asset Health\nDashboard', 'EHS / Safety\nWall', 'Executive BI\n& Alerts'];
uxItems.forEach((lbl, i) => {
  slide.addShape(pptx.ShapeType.rect, { x: 0.7 + i * 1.9, y: 5.8, w: 1.7, h: 0.6,
    fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 } });
  slide.addText(lbl, { x: 0.7 + i * 1.9, y: 5.8, w: 1.7, h: 0.6,
    fontSize: 9, color: C.CHARCOAL, fontFace: 'Calibri', align: 'center', valign: 'middle' });
});

// Right 35%: 5-step flow
slide.addText('5-Step Data Flow', { x: 8.6, y: 1.5, w: 4.2, h: 0.4,
  fontSize: 20, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const steps = [
  '1. Capture — cameras, sensors, RFID scan production line',
  '2. Edge Inference — local GPU runs models in <200ms',
  '3. Event Stream — Kafka routes scored events to integration layer',
  '4. AI + Enterprise — cloud models train; SAP/MES act on events',
  '5. UX — dashboards, alerts, and mobile push to operators'
];
steps.forEach((s, i) => {
  slide.addShape(pptx.ShapeType.rect, { x: 8.6, y: 2.1 + i * 0.85, w: 4.2, h: 0.7,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addShape(pptx.ShapeType.rect, { x: 8.6, y: 2.1 + i * 0.85, w: 0.06, h: 0.7,
    fill: { color: C.NAVY_DEEP }, line: { color: C.NAVY_DEEP, width: 0 } });
  slide.addText(s, { x: 8.8, y: 2.1 + i * 0.85, w: 3.9, h: 0.7,
    fontSize: 11, color: C.CHARCOAL, fontFace: 'Calibri', valign: 'middle', wrap: true });
});

// ============================================================================
// SLIDE 5 — COMPONENTS DEEP DIVE (2×2 cards)
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Components Deep Dive', 'What each layer does and why');

addCard(slide, 0.5, 1.4, 5.9, 2.5, 'Plant Floor / Edge Capture',
  ['Vision cameras (Cognex, Basler, Keyence) — multi-angle, high-res surface capture',
   'IoT sensors — vibration, acoustic, thermal, pressure for machine health',
   'RFID & barcode scanners — component tracking and VIN verification',
   'Edge compute (NVIDIA Jetson, Hailo) — <200ms local inference',
   'OPC-UA bus + edge gateway — protocol translation and local resilience']);
addCard(slide, 6.8, 1.4, 5.9, 2.5, 'Streaming & Integration',
  ['Kafka event bus — real-time quality, maintenance, safety event routing',
   'MES / SAP Connector Library — pre-built line-hold and work-order integration',
   'SAP MES/ERP + SAP PM/CMMS — production orders, maintenance scheduling',
   'AVEVA PI historian — time-series sensor storage',
   'Neo4j genealogy graph — component-to-vehicle traceability']);
addCard(slide, 0.5, 4.2, 5.9, 2.5, 'AI / ML Compute (Cloud)',
  ['AWS SageMaker / Azure ML — training, tuning, model registry',
   '8 model groups: CNN (visual), YOLO (detection), LSTM (time-series), Autoencoder (anomaly)',
   'MLOps: MLflow + CI/CD + drift detection + auto-retraining',
   'Model optimization: TensorRT / ONNX → edge OTA deployment',
   'Data lake (S3 / ADLS) with Parquet / Delta Lake feature store']);
addCard(slide, 6.8, 4.2, 5.9, 2.5, 'Application & UX',
  ['Quality dashboard — real-time defect monitoring by station/shift',
   'Asset health dashboard — risk-prioritized maintenance work queue',
   'EHS live wall — PPE compliance, zone alerts, incident reports',
   'Operator station UI — pass/fail cues, hold-station controls',
   'Alerting (Slack/Teams/Andon) + Executive BI (Power BI/Tableau)']);

// ============================================================================
// SLIDE 6 — COMPARISON / DECISION MATRIX
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Platform vs. Point Solutions', 'Why a unified architecture wins');

// Table header
addTableRow(slide, 0.5, 1.5, 12.33, 0.5,
  ['Dimension', 'Siloed Point Solutions', 'Unified Platform (Ours)'], 2);
// Rows
const rows = [
  ['Infrastructure cost', '8× separate stacks, cameras, DBs', 'Shared edge fleet + one data lake'],
  ['Integration effort', 'Custom connectors per use case', 'Pre-built SAP/MES library, Kafka bus'],
  ['Latency', 'Cloud-only: 500ms–2s', 'Edge-first: <200ms'],
  ['Model retraining', 'Manual, ad-hoc per model', 'Unified MLOps: drift detect → auto-retrain → OTA'],
  ['Time to add use case', '3–6 months from scratch', '4–6 weeks (deploy model to existing infra)'],
  ['Cross-UC data fusion', 'Not possible', 'Shared data lake enables sensor + vision fusion'],
  ['Scale path', 'Re-architect per plant', 'Add edge nodes, same stack'],
];
rows.forEach((r, i) => {
  addTableRow(slide, 0.5, 2.05 + i * 0.6, 12.33, 0.55, r, 2);
});

// ============================================================================
// SLIDE 7 — IMPLEMENTATION / CODE VIEW
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Implementation View', 'Edge inference + MLOps pipeline');

// Left: explanation
slide.addText('Edge Inference Pipeline', { x: 0.5, y: 1.4, w: 5.5, h: 0.4,
  fontSize: 20, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const implBullets = [
  { text: 'Camera captures frame → edge GPU runs TensorRT-optimized model', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Anomaly score + metadata published to Kafka topic', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'If score > threshold → MES connector triggers SAP line-hold', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Defect record persisted to PostgreSQL with full traceability', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Dashboard updates in real time; operator sees pass/fail', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
];
slide.addText(implBullets, { x: 0.5, y: 1.9, w: 5.5, h: 2.5, valign: 'top' });

slide.addText('MLOps Retraining Loop', { x: 0.5, y: 4.5, w: 5.5, h: 0.4,
  fontSize: 20, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const mlopsBullets = [
  { text: 'Rework-confirmed defects feed back to SageMaker weekly', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'MLflow tracks experiments, model registry versions artifacts', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'TensorRT optimization → OTA push to edge fleet via Greengrass', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
];
slide.addText(mlopsBullets, { x: 0.5, y: 5.0, w: 5.5, h: 1.5, valign: 'top' });

// Right: code block
addCodeBlock(slide, 6.5, 1.4, 6.3, 5.2,
`# Edge Inference Pipeline (simplified)
# ─────────────────────────────────────

frame = camera.capture()           # Cognex/Basler
tensor = preprocess(frame)         # Resize, normalize
score = model.infer(tensor)        # TensorRT on Jetson

event = {
  "station_id": STATION,
  "score": score,
  "timestamp": now(),
  "image_ref": s3_upload(frame),
  "vin": rfid_reader.last_scan()
}

kafka.publish("quality.defects", event)

if score > THRESHOLD:
  mes_connector.trigger_line_hold(
    station=STATION,
    reason="AI defect detected",
    score=score
  )
  quality_db.insert(event)
  alerting.notify(SUPERVISOR, event)

# ── Weekly retraining loop ──
rework_data = quality_db.get_confirmed()
sagemaker.train(
  dataset=rework_data,
  base_model="resnet50-v3.2",
  output="s3://models/resnet50-v3.3"
)
iot_greengrass.ota_deploy("resnet50-v3.3")`);

// ============================================================================
// SLIDE 8 — KEY METRICS / RESULTS
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Expected Outcomes', 'Measured results from peer-OEM deployments');

// Left: simplified architecture representation
slide.addShape(pptx.ShapeType.rect, { x: 0.5, y: 1.5, w: 5.5, h: 5.0,
  fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
slide.addText('Platform Impact Areas', { x: 0.7, y: 1.6, w: 5.1, h: 0.4,
  fontSize: 16, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

const impactAreas = [
  { label: 'Visual Inspection', detail: 'CNN defect detection → −45% rework, −60% escapes', color: '14A085' },
  { label: 'Predictive Maintenance', detail: 'Anomaly detection → −40% downtime, 5:1 ROI', color: '1A2754' },
  { label: 'Safety & SOP', detail: 'Pose estimation → −55% incidents, 98% PPE compliance', color: '0E7B6A' },
  { label: 'Traceability', detail: 'Genealogy graph → 100% tracking, recall in days', color: '7C3AED' },
];
impactAreas.forEach((area, i) => {
  const ay = 2.2 + i * 1.0;
  slide.addShape(pptx.ShapeType.rect, { x: 0.7, y: ay, w: 5.1, h: 0.8,
    fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 } });
  slide.addShape(pptx.ShapeType.rect, { x: 0.7, y: ay, w: 0.06, h: 0.8,
    fill: { color: area.color }, line: { color: area.color, width: 0 } });
  slide.addText(area.label, { x: 0.9, y: ay + 0.08, w: 4.7, h: 0.3,
    fontSize: 13, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
  slide.addText(area.detail, { x: 0.9, y: ay + 0.4, w: 4.7, h: 0.3,
    fontSize: 11, color: C.MUTED, fontFace: 'Calibri' });
});

// Right: 3 large stats
addMetric(slide, 6.8, 1.5, 5.5, '<200ms', 'Edge inference latency — line-side decisions in real time');
addMetric(slide, 6.8, 3.2, 5.5, '3–5×', 'Measured ROI within first year of deployment');
addMetric(slide, 6.8, 4.9, 5.5, '40–60%', 'Faster time-to-pilot with PeopleTech accelerators');

// ============================================================================
// SLIDE 9 — KEY DATA FLOW (timeline)
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Key Data Flow', 'How a defect detection event moves through the platform');

// 7 steps as horizontal timeline
const flowSteps = [
  { n: '1', label: 'Camera\nCapture', detail: 'High-res frame\nin light tunnel' },
  { n: '2', label: 'Edge\nInference', detail: 'CNN model\n<200ms' },
  { n: '3', label: 'Event\nPublish', detail: 'Kafka topic\nwith score' },
  { n: '4', label: 'MES\nLine-Hold', detail: 'SAP API\nauto-trigger' },
  { n: '5', label: 'Quality DB\nWrite', detail: 'PostgreSQL\ntraceability' },
  { n: '6', label: 'Dashboard\nUpdate', detail: 'Real-time\noperator UI' },
  { n: '7', label: 'Retrain\n& OTA', detail: 'SageMaker\n→ Edge push' },
];
const stepW = 1.55;
const startX = 0.5;
const stepY = 2.0;

flowSteps.forEach((s, i) => {
  const sx = startX + i * (stepW + 0.25);
  // Number circle
  slide.addShape(pptx.ShapeType.ellipse, { x: sx + 0.55, y: stepY, w: 0.45, h: 0.45,
    fill: { color: C.NAVY_DEEP }, line: { color: C.NAVY_DEEP, width: 0 } });
  slide.addText(s.n, { x: sx + 0.55, y: stepY, w: 0.45, h: 0.45,
    fontSize: 16, bold: true, color: C.WHITE, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  // Step box
  slide.addShape(pptx.ShapeType.rect, { x: sx, y: stepY + 0.6, w: stepW, h: 1.4,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addText(s.label, { x: sx + 0.1, y: stepY + 0.65, w: stepW - 0.2, h: 0.6,
    fontSize: 12, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  slide.addText(s.detail, { x: sx + 0.1, y: stepY + 1.25, w: stepW - 0.2, h: 0.65,
    fontSize: 10, color: C.MUTED, fontFace: 'Calibri', align: 'center', valign: 'top' });
  // Arrow between steps
  if (i < flowSteps.length - 1) {
    slide.addText('→', { x: sx + stepW, y: stepY + 0.95, w: 0.25, h: 0.4,
      fontSize: 18, color: C.RED, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  }
});

// Predictive Maintenance flow below
slide.addText('Predictive Maintenance Flow', { x: 0.5, y: 4.5, w: 12.33, h: 0.4,
  fontSize: 20, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

const maintSteps = [
  { n: '1', label: 'Sensor\nStream', detail: 'Vibration, acoustic\nthermal data' },
  { n: '2', label: 'Edge\nAggregate', detail: 'Windowed\nfeatures' },
  { n: '3', label: 'Anomaly\nDetect', detail: 'Autoencoder\n+ survival model' },
  { n: '4', label: 'Work Order\nGenerate', detail: 'SAP PM\nauto-create' },
  { n: '5', label: 'Technician\nNotify', detail: 'Mobile push\n+ risk queue' },
];
const mStepW = 2.1;
const mStartX = 0.5;
const mStepY = 5.0;

maintSteps.forEach((s, i) => {
  const sx = mStartX + i * (mStepW + 0.3);
  slide.addShape(pptx.ShapeType.ellipse, { x: sx + 0.8, y: mStepY, w: 0.4, h: 0.4,
    fill: { color: C.NAVY_DEEP }, line: { color: C.NAVY_DEEP, width: 0 } });
  slide.addText(s.n, { x: sx + 0.8, y: mStepY, w: 0.4, h: 0.4,
    fontSize: 14, bold: true, color: C.WHITE, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  slide.addShape(pptx.ShapeType.rect, { x: sx, y: mStepY + 0.5, w: mStepW, h: 1.1,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addText(s.label, { x: sx + 0.1, y: mStepY + 0.52, w: mStepW - 0.2, h: 0.45,
    fontSize: 11, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  slide.addText(s.detail, { x: sx + 0.1, y: mStepY + 0.95, w: mStepW - 0.2, h: 0.55,
    fontSize: 10, color: C.MUTED, fontFace: 'Calibri', align: 'center', valign: 'top' });
  if (i < maintSteps.length - 1) {
    slide.addText('→', { x: sx + mStepW, y: mStepY + 0.75, w: 0.3, h: 0.4,
      fontSize: 16, color: C.RED, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  }
});

// ============================================================================
// SLIDE 10 — SUMMARY / CTA
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Summary & Next Steps');

// 3 takeaway cards
addCard(slide, 0.5, 1.5, 3.9, 2.8, 'Unified Platform',
  'One infrastructure for 8 use cases. Shared edge compute, event bus, data lake, and MLOps pipeline. Adding a new use case is a model deployment — not an infrastructure project. Amortize cost across the entire program.');
addCard(slide, 4.7, 1.5, 3.9, 2.8, 'Integration-First',
  'Plugs into SAP MES/ERP, SAP PM, AVEVA PI — no rip-and-replace. AI outputs flow into the systems operators already use. Automated line-hold, work-order generation, and escalation. Pre-built connector library cuts integration time 40–60%.');
addCard(slide, 8.9, 1.5, 3.9, 2.8, 'Pilot-First Scale',
  'Start with 2 pilots on one line: Visual Inspection at HMGMA (IONIQ paint) + Predictive Maintenance at Ulsan stamping. Prove ROI in 12 weeks. Scale to plant-wide without re-architecture. Go/no-go gate before any commitment to expand.');

// Design decisions
slide.addText('Key Design Decisions', { x: 0.5, y: 4.6, w: 12.33, h: 0.4,
  fontSize: 18, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const decisions = [
  { text: 'Edge-first inference — <200ms latency for real-time line-side decisions', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Cloud retraining — weekly model improvement with drift detection and auto-retrain', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Shared data lake — enables cross-use-case fusion (e.g., vision + sensor for predictive quality)', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Modular add-a-use-case — deploy model to existing infra in 4–6 weeks vs. 3–6 months from scratch', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
];
slide.addText(decisions, { x: 0.5, y: 5.1, w: 12.33, h: 1.5, valign: 'top' });

addBanner(slide, 'Next step: Pilot Scoping Workshop — walk the line, agree the baseline, lock dates.');

// ============================================================================
// SAVE
// ============================================================================
pptx.writeFile({ fileName: 'ai-plant-operations-architecture.pptx' })
  .then(() => console.log('Saved: ai-plant-operations-architecture.pptx'))
  .catch(err => console.error(err));
