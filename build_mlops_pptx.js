const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

const C = {
  WHITE: 'FFFFFF', CHARCOAL: '1A1A1A', NAVY_DEEP: '1F3B6E',
  NAVY_CARD: '0D3B5E', RED: 'E31837', LIGHT_BG: 'F5F7FA',
  BORDER: 'D0D5DD', MUTED: '6B7280', CODE_BG: 'F0F2F5'
};

pptx.layout = 'LAYOUT_WIDE';

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
      fontSize: 11, color: textColor, fontFace: 'Calibri',
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

slide.addText('MLOPS PIPELINE', { x: 0.5, y: 0.8, w: 7.5, h: 0.4,
  fontSize: 14, bold: true, color: C.MUTED, fontFace: 'Calibri', charSpacing: 3 });
slide.addText('Training to Edge\nDeployment', { x: 0.5, y: 1.4, w: 7.5, h: 1.4,
  fontSize: 42, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri', lineSpacingMultiple: 1.1 });
slide.addText('Hyundai  ×  PeopleTech', { x: 0.5, y: 2.9, w: 7.5, h: 0.6,
  fontSize: 24, color: C.MUTED, fontFace: 'Calibri' });

slide.addShape(pptx.ShapeType.roundRect, { x: 0.5, y: 3.8, w: 5.5, h: 0.45,
  fill: { color: 'FEE2E2' }, line: { color: C.RED, width: 1 }, rectRadius: 0.1 });
slide.addText('Closed-Loop Model Lifecycle · 8 Use Cases · Auto-Retrain on Drift', { x: 0.6, y: 3.8, w: 5.3, h: 0.45,
  fontSize: 12, bold: true, color: C.RED, fontFace: 'Calibri', valign: 'middle' });

slide.addText('How every AI model in the plant gets trained, optimized,\ndeployed to edge, monitored, and automatically retrained.', { x: 0.5, y: 4.5, w: 7, h: 0.8,
  fontSize: 14, color: C.CHARCOAL, fontFace: 'Calibri', lineSpacingMultiple: 1.4 });

// Right: 4 stage boxes
const stages = ['1. Data Collection', '2. Training & Registry', '3. Edge Deployment', '4. Monitor & Retrain'];
const stageColors = ['0369A1', '15803D', 'C2410C', 'BE185D'];
stages.forEach((lbl, i) => {
  const ly = 1.2 + i * 1.25;
  slide.addShape(pptx.ShapeType.rect, { x: 8.5, y: ly, w: 4.3, h: 0.95,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addShape(pptx.ShapeType.rect, { x: 8.5, y: ly, w: 0.08, h: 0.95,
    fill: { color: stageColors[i] }, line: { color: stageColors[i], width: 0 } });
  slide.addText(lbl, { x: 8.75, y: ly, w: 3.9, h: 0.95,
    fontSize: 14, bold: true, color: C.CHARCOAL, fontFace: 'Calibri', valign: 'middle' });
  if (i < 3) {
    slide.addText('↓', { x: 10.2, y: ly + 0.85, w: 0.5, h: 0.35,
      fontSize: 16, color: C.NAVY_DEEP, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  }
});
// Retrain loop arrow
slide.addText('↻ Auto-retrain loop', { x: 8.5, y: 6.3, w: 4.3, h: 0.3,
  fontSize: 11, italic: true, color: C.RED, fontFace: 'Calibri', align: 'center' });

addBanner(slide, 'Hyundai × PeopleTech · MLOps for AI Plant Operations · May 2026');

// ============================================================================
// SLIDE 2 — WHAT IS IT?
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'What is the MLOps Pipeline?', 'Closed-loop model lifecycle from data to edge to retraining');

addCard(slide, 0.5, 1.5, 3.8, 3.5, 'Automated Training',
  'Sensor data, inference logs, and human feedback flow into a feature store. GPU training on SageMaker / Azure ML with MLflow experiment tracking. Models evaluated against the champion before promotion to the registry.');
addCard(slide, 4.6, 1.5, 3.8, 3.5, 'Edge-First Deployment',
  'Models optimized for edge hardware (TensorRT, ONNX, INT8 quantization) to meet <200ms latency. Containerized and deployed via OTA to Jetson/Hailo edge fleet. Canary deployment with auto-rollback protects the line.');
addCard(slide, 8.7, 1.5, 4.1, 3.5, 'Auto-Retrain on Drift',
  ['Performance monitored per model, per plant, per shift',
   'Data drift (KL divergence) + concept drift (accuracy decay)',
   'Threshold breach → auto-retrain trigger',
   'No manual intervention for routine model refresh',
   'Emergency retrain for sudden degradation',
   'Full audit trail for IATF/ISO compliance']);

slide.addText('One pipeline manages all model types: CNN, YOLO, Pose, XGBoost, LSTM, Autoencoder, Graph ML, OCR.', {
  x: 0.5, y: 5.3, w: 12.33, h: 0.5, fontSize: 13, italic: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

addBanner(slide, 'From plant floor data to production models in hours, not months');

// ============================================================================
// SLIDE 3 — THE PROBLEM
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'The Problem', 'Why traditional ML deployment fails in manufacturing');

const flowLabels = ['Train Once,\nDeploy Forever', 'Model Decay\nGoes Unnoticed', 'Manual Retrain\n(Weeks)', 'Quality Escapes\nIncrease'];
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

addCard(slide, 0.5, 2.7, 3.9, 2.5, 'No Drift Detection',
  'Models trained on historical data degrade when conditions change — new paint formulations, seasonal temperature shifts, model year changeovers. Without monitoring, accuracy silently drops and defects escape.');
addCard(slide, 4.7, 2.7, 3.9, 2.5, 'Manual Deployment',
  'Data scientists retrain manually on laptops. No versioning, no A/B testing, no canary rollout. Edge devices updated by walking the plant floor with USB drives. Weeks of lead time for a model fix.');
addCard(slide, 8.9, 2.7, 3.9, 2.5, 'No Governance',
  'No audit trail for which model is running where. Safety-critical models (PPE, SOP) deployed without review gates. Compliance teams can\'t trace a prediction back to its training data. IATF/ISO audit risk.');

addBanner(slide, 'The MLOps pipeline eliminates all three failure modes');

// ============================================================================
// SLIDE 4 — ARCHITECTURE OVERVIEW
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Pipeline Architecture', 'Four-stage closed-loop model lifecycle');

// Left 65%: 4 horizontal layers
const layers = [
  { label: 'DATA COLLECTION', color: '0369A1', bg: 'F0F9FF', border: 'BAE6FD',
    items: ['Plant Sensors', 'Inference Logs', 'Human Feedback', 'Labeling + DVC'] },
  { label: 'TRAINING & REGISTRY', color: '15803D', bg: 'F0FDF4', border: 'BBF7D0',
    items: ['Feature Store', 'GPU Training', 'MLflow Tracking', 'Model Registry'] },
  { label: 'PACKAGING & DEPLOY', color: 'C2410C', bg: 'FFF7ED', border: 'FED7AA',
    items: ['TensorRT/ONNX', 'Container Build', 'CI/CD Pipeline', 'Edge OTA'] },
  { label: 'MONITOR & RETRAIN', color: 'BE185D', bg: 'FDF2F8', border: 'FBCFE8',
    items: ['Perf Monitor', 'Drift Detection', 'Alert Engine', 'Governance'] },
];

layers.forEach((l, li) => {
  const ly = 1.5 + li * 1.25;
  slide.addShape(pptx.ShapeType.rect, { x: 0.5, y: ly, w: 7.8, h: 1.05,
    fill: { color: l.bg }, line: { color: l.border, width: 1 } });
  slide.addText(l.label, { x: 0.6, y: ly + 0.05, w: 2.5, h: 0.25,
    fontSize: 10, bold: true, color: l.color, fontFace: 'Calibri' });
  l.items.forEach((item, ii) => {
    slide.addShape(pptx.ShapeType.rect, { x: 0.7 + ii * 1.85, y: ly + 0.35, w: 1.65, h: 0.55,
      fill: { color: C.WHITE }, line: { color: C.BORDER, width: 1 } });
    slide.addText(item, { x: 0.7 + ii * 1.85, y: ly + 0.35, w: 1.65, h: 0.55,
      fontSize: 10, color: C.CHARCOAL, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  });
});

// Retrain loop arrow on left side
slide.addShape(pptx.ShapeType.rect, { x: 0.15, y: 1.5, w: 0.25, h: 4.5,
  fill: { color: 'FEE2E2' }, line: { color: C.RED, width: 1 } });
slide.addText('↻\nAuto\nRetrain\nLoop', { x: 0.15, y: 2.5, w: 0.25, h: 2.5,
  fontSize: 8, bold: true, color: C.RED, fontFace: 'Calibri', align: 'center', valign: 'middle' });

// Right 35%: 7-step flow
slide.addText('7-Step Lifecycle', { x: 8.6, y: 1.5, w: 4.2, h: 0.4,
  fontSize: 20, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const steps = [
  '1. Collect — sensors, logs, feedback',
  '2. Label — active learning + human QA',
  '3. Train — GPU cluster + MLflow',
  '4. Evaluate — A/B vs champion + SHAP',
  '5. Optimize — TensorRT for edge',
  '6. Deploy — canary → OTA rollout',
  '7. Monitor — drift detect → auto-retrain'
];
steps.forEach((s, i) => {
  slide.addShape(pptx.ShapeType.rect, { x: 8.6, y: 2.0 + i * 0.72, w: 4.2, h: 0.58,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addShape(pptx.ShapeType.rect, { x: 8.6, y: 2.0 + i * 0.72, w: 0.06, h: 0.58,
    fill: { color: i === 6 ? C.RED : C.NAVY_DEEP }, line: { color: i === 6 ? C.RED : C.NAVY_DEEP, width: 0 } });
  slide.addText(s, { x: 8.8, y: 2.0 + i * 0.72, w: 3.9, h: 0.58,
    fontSize: 11, color: i === 6 ? C.RED : C.CHARCOAL, fontFace: 'Calibri',
    bold: i === 6, valign: 'middle', wrap: true });
});

// ============================================================================
// SLIDE 5 — COMPONENTS DEEP DIVE
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Components Deep Dive', 'What each pipeline stage does');

addCard(slide, 0.5, 1.4, 5.9, 2.5, 'Data Collection & Labeling',
  ['Plant floor sensors, cameras, RFID generate raw data streams',
   'Edge inference logs capture every prediction with score + confidence',
   'Human feedback: rework confirmations, quality inspector labels',
   'Active learning selects highest-value samples for annotation',
   'DVC / S3-versioned datasets with reproducible train/val/test splits']);
addCard(slide, 6.8, 1.4, 5.9, 2.5, 'Feature Engineering & Training',
  ['SageMaker Feature Store: offline (batch) + online (real-time) serving',
   'Great Expectations data validation gates training pipeline entry',
   'GPU training (P4d/A100) with Bayesian hyperparameter tuning',
   'MLflow experiment tracking: metrics, params, artifacts, comparisons',
   'Model evaluation: A/B vs champion, SHAP explainability, bias checks']);
addCard(slide, 0.5, 4.2, 5.9, 2.5, 'Packaging & Deployment',
  ['TensorRT / ONNX / OpenVINO optimization for <200ms edge latency',
   'Docker container with model + runtime → ECR/ACR registry',
   'CI/CD: automated test → build → deploy with approval gates',
   'Canary: 5% traffic to challenger, auto-rollback on regression',
   'Edge OTA via IoT Greengrass / IoT Edge: rolling, zero-downtime']);
addCard(slide, 6.8, 4.2, 5.9, 2.5, 'Monitoring & Governance',
  ['Performance tracked per model, per plant, per shift',
   'Drift detection: KL divergence (data) + accuracy decay (concept)',
   'Threshold breach → auto-retrain trigger (no human required)',
   'Full audit trail: training data → experiment → deployment → rollback',
   'Business value tracking: ROI per model, weekly digest to leadership']);

// ============================================================================
// SLIDE 6 — COMPARISON: OUR PIPELINE VS. AD-HOC
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Automated Pipeline vs. Ad-Hoc ML', 'Why the investment in MLOps pays off');

addTableRow(slide, 0.5, 1.5, 12.33, 0.5,
  ['Dimension', 'Ad-Hoc / Manual ML', 'Our MLOps Pipeline'], 2);
const rows = [
  ['Model refresh cycle', 'Months (manual retrain on request)', 'Weekly auto-retrain + emergency on drift'],
  ['Deployment method', 'USB drives / manual SSH to edge', 'OTA rolling update, zero downtime'],
  ['Drift detection', 'None — discovered via quality escapes', 'KL divergence + accuracy monitoring, auto-alert'],
  ['Rollback capability', 'None — pray the new model works', 'Instant auto-rollback during canary phase'],
  ['Audit trail', 'Excel spreadsheets, if lucky', 'Full lineage: data → training → deployment → monitoring'],
  ['Time to fix a bad model', '2–6 weeks', '< 24 hours (auto-retrain + expedited deploy)'],
  ['Compliance readiness', 'Scramble before audits', 'Continuous audit log, IATF/ISO-ready'],
];
rows.forEach((r, i) => {
  addTableRow(slide, 0.5, 2.05 + i * 0.6, 12.33, 0.55, r, 2);
});

// ============================================================================
// SLIDE 7 — IMPLEMENTATION / CODE VIEW
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Implementation View', 'Training pipeline + edge OTA deployment');

slide.addText('Weekly Retraining Pipeline', { x: 0.5, y: 1.4, w: 5.5, h: 0.4,
  fontSize: 20, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const trainBullets = [
  { text: 'Inference logs + rework confirmations accumulate all week', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Active learning selects high-value samples for labeling', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Great Expectations validates data schema + distributions', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'SageMaker training job with MLflow tracking', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Challenger compared vs champion on all key metrics', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
];
slide.addText(trainBullets, { x: 0.5, y: 1.9, w: 5.5, h: 2.2, valign: 'top' });

slide.addText('Edge Deployment Flow', { x: 0.5, y: 4.2, w: 5.5, h: 0.4,
  fontSize: 20, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const deployBullets = [
  { text: 'TensorRT INT8 quantization → Docker container → ECR', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'CI/CD pipeline with approval gate for safety-critical models', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: '5% canary → 24h monitor → full OTA rollout', options: { bullet: true, fontSize: 12, color: C.CHARCOAL, fontFace: 'Calibri' } },
];
slide.addText(deployBullets, { x: 0.5, y: 4.7, w: 5.5, h: 1.3, valign: 'top' });

addCodeBlock(slide, 6.5, 1.4, 6.3, 5.2,
`# Weekly Retraining Pipeline (simplified)
# ─────────────────────────────────────

# 1. Collect new training data
new_data = feature_store.get_recent(days=7)
labels = labeling_pipeline.get_completed()
dataset = merge(new_data, labels)
dvc.commit(dataset, version="v3.3")

# 2. Validate data quality
ge.validate(dataset, expectation_suite="prod")

# 3. Train challenger model
with mlflow.start_run(experiment="uc01-visual"):
  model = train(
    arch="resnet50",
    dataset=dataset,
    epochs=50,
    gpus=4  # P4d cluster
  )
  mlflow.log_metrics(evaluate(model, test_set))

# 4. Compare vs champion
champion = mlflow.registry.get("Production")
if model.accuracy > champion.accuracy:
  mlflow.registry.promote(model, stage="Staging")

# 5. Optimize for edge + deploy
optimized = tensorrt.optimize(model, precision="INT8")
container = docker.build(optimized, runtime="triton")
ecr.push(container, tag="v3.3")

# 6. Canary → full rollout
iot_greengrass.deploy(
  container="v3.3",
  strategy="canary",    # 5% traffic first
  monitor_hours=24,
  auto_rollback=True    # rollback if regression
)`);

// ============================================================================
// SLIDE 8 — KEY METRICS
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Pipeline Performance', 'What the MLOps pipeline delivers');

// Left: impact areas
slide.addShape(pptx.ShapeType.rect, { x: 0.5, y: 1.5, w: 5.5, h: 5.0,
  fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
slide.addText('Pipeline Impact Areas', { x: 0.7, y: 1.6, w: 5.1, h: 0.4,
  fontSize: 16, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });

const impacts = [
  { label: 'Model Freshness', detail: 'Weekly auto-retrain vs months of manual cycles', color: '0369A1' },
  { label: 'Deployment Speed', detail: 'Training → edge in hours, not weeks', color: '15803D' },
  { label: 'Drift Response', detail: 'Auto-detect and retrain in <24 hours', color: 'C2410C' },
  { label: 'Governance', detail: 'Full audit trail, IATF/ISO-ready, no gaps', color: 'BE185D' },
];
impacts.forEach((area, i) => {
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
addMetric(slide, 6.8, 1.5, 5.5, '<24h', 'Drift-to-fix time — from detection to retrained model in production');
addMetric(slide, 6.8, 3.2, 5.5, '0', 'Manual deployment steps — fully automated from registry to edge');
addMetric(slide, 6.8, 4.9, 5.5, '100%', 'Audit coverage — every model change tracked end-to-end');

// ============================================================================
// SLIDE 9 — KEY DATA FLOW (timeline)
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Model Update Lifecycle', 'Weekly retraining cycle — 9 automated steps');

const flowSteps = [
  { n: '1', label: 'Collect\nData', detail: 'Logs +\nfeedback' },
  { n: '2', label: 'Active\nLabeling', detail: 'High-value\nsamples' },
  { n: '3', label: 'Feature\nStore', detail: 'Compute +\nvalidate' },
  { n: '4', label: 'GPU\nTraining', detail: 'SageMaker\n+ MLflow' },
  { n: '5', label: 'Evaluate\nvs Champ', detail: 'A/B + SHAP\nbias check' },
  { n: '6', label: 'Optimize\nfor Edge', detail: 'TensorRT\nINT8' },
  { n: '7', label: 'Canary\nDeploy', detail: '5% traffic\n24h watch' },
  { n: '8', label: 'Full OTA\nRollout', detail: 'Zero\ndowntime' },
  { n: '9', label: 'Monitor\n+ Drift', detail: 'Auto-retrain\non breach' },
];
const stepW = 1.2;
const startX = 0.3;
const stepY = 1.8;

flowSteps.forEach((s, i) => {
  const sx = startX + i * (stepW + 0.17);
  slide.addShape(pptx.ShapeType.ellipse, { x: sx + 0.35, y: stepY, w: 0.4, h: 0.4,
    fill: { color: i === 8 ? C.RED : C.NAVY_DEEP }, line: { color: i === 8 ? C.RED : C.NAVY_DEEP, width: 0 } });
  slide.addText(s.n, { x: sx + 0.35, y: stepY, w: 0.4, h: 0.4,
    fontSize: 14, bold: true, color: C.WHITE, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  slide.addShape(pptx.ShapeType.rect, { x: sx, y: stepY + 0.55, w: stepW, h: 1.3,
    fill: { color: C.LIGHT_BG }, line: { color: C.BORDER, width: 1 } });
  slide.addText(s.label, { x: sx + 0.05, y: stepY + 0.58, w: stepW - 0.1, h: 0.55,
    fontSize: 11, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  slide.addText(s.detail, { x: sx + 0.05, y: stepY + 1.1, w: stepW - 0.1, h: 0.6,
    fontSize: 9, color: C.MUTED, fontFace: 'Calibri', align: 'center', valign: 'top' });
  if (i < flowSteps.length - 1) {
    slide.addText('→', { x: sx + stepW, y: stepY + 0.85, w: 0.17, h: 0.4,
      fontSize: 14, color: C.RED, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  }
});

// Emergency retrain flow below
slide.addText('Emergency Retrain Flow (drift-triggered)', { x: 0.5, y: 4.2, w: 12.33, h: 0.4,
  fontSize: 18, bold: true, color: C.RED, fontFace: 'Calibri' });

const emergSteps = [
  { n: '1', label: 'Drift\nDetected', detail: 'Accuracy\n>5% drop' },
  { n: '2', label: 'Auto\nAlert', detail: 'Slack +\nauto-trigger' },
  { n: '3', label: 'Fast\nRetrain', detail: 'Fine-tune\n~2 hours' },
  { n: '4', label: 'Expedited\nEval', detail: 'SHAP drift\nanalysis' },
  { n: '5', label: 'Emergency\nDeploy', detail: '1h canary\n→ full OTA' },
];
const eStepW = 2.15;
const eStartX = 0.5;
const eStepY = 4.7;

emergSteps.forEach((s, i) => {
  const sx = eStartX + i * (eStepW + 0.25);
  slide.addShape(pptx.ShapeType.ellipse, { x: sx + 0.85, y: eStepY, w: 0.38, h: 0.38,
    fill: { color: C.RED }, line: { color: C.RED, width: 0 } });
  slide.addText(s.n, { x: sx + 0.85, y: eStepY, w: 0.38, h: 0.38,
    fontSize: 13, bold: true, color: C.WHITE, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  slide.addShape(pptx.ShapeType.rect, { x: sx, y: eStepY + 0.48, w: eStepW, h: 1.05,
    fill: { color: 'FEE2E2' }, line: { color: C.RED, width: 1 } });
  slide.addText(s.label, { x: sx + 0.05, y: eStepY + 0.5, w: eStepW - 0.1, h: 0.42,
    fontSize: 11, bold: true, color: C.RED, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  slide.addText(s.detail, { x: sx + 0.05, y: eStepY + 0.9, w: eStepW - 0.1, h: 0.5,
    fontSize: 10, color: C.CHARCOAL, fontFace: 'Calibri', align: 'center', valign: 'top' });
  if (i < emergSteps.length - 1) {
    slide.addText('→', { x: sx + eStepW, y: eStepY + 0.75, w: 0.25, h: 0.4,
      fontSize: 14, color: C.RED, fontFace: 'Calibri', align: 'center', valign: 'middle' });
  }
});

// ============================================================================
// SLIDE 10 — SUMMARY / CTA
// ============================================================================
slide = pptx.addSlide();
slide.background = { color: C.WHITE };
addTitle(slide, 'Summary & Next Steps');

addCard(slide, 0.5, 1.5, 3.9, 2.8, 'Automated Lifecycle',
  'No more train-once-deploy-forever. Weekly auto-retrain with drift detection ensures models stay accurate as plant conditions change. Emergency retrain path for sudden degradation — fix in <24 hours, not weeks.');
addCard(slide, 4.7, 1.5, 3.9, 2.8, 'Edge-First Deployment',
  'Every model optimized for edge hardware (TensorRT INT8). Canary deployment with auto-rollback protects the line. OTA rollout with zero downtime — no USB drives, no SSH, no manual intervention. Supports all 8 use case model types.');
addCard(slide, 8.9, 1.5, 3.9, 2.8, 'Governance Built In',
  'Full audit trail from training data to deployed version. Approval gates for safety-critical models (PPE, SOP). IATF 16949 and ISO 9001 audit-ready. Business value tracking with weekly ROI digest per model per plant.');

slide.addText('Key Design Decisions', { x: 0.5, y: 4.6, w: 12.33, h: 0.4,
  fontSize: 18, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri' });
const decisions = [
  { text: 'MLflow as single backbone — one lineage from data to deployment', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Edge optimization as first-class stage — not an afterthought', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Canary before full rollout — catch regressions offline eval misses', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
  { text: 'Closed-loop auto-retrain — no waiting for humans to notice drift', options: { bullet: true, fontSize: 13, color: C.CHARCOAL, fontFace: 'Calibri' } },
];
slide.addText(decisions, { x: 0.5, y: 5.1, w: 12.33, h: 1.5, valign: 'top' });

addBanner(slide, 'The pipeline ships with the platform — not a separate workstream.');

// ============================================================================
// SAVE
// ============================================================================
pptx.writeFile({ fileName: 'mlops-pipeline-architecture.pptx' })
  .then(() => console.log('Saved: mlops-pipeline-architecture.pptx'))
  .catch(err => console.error(err));
