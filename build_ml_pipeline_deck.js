const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

// ── Theme: Enterprise Consulting (from hyundai-deal-prep.pptx template) ──
const C = {
  WHITE:'FFFFFF',CHARCOAL:'1A1A1A',NAVY_DEEP:'1F3B6E',NAVY_CARD:'0D3B5E',
  RED:'E31837',LIGHT_BG:'F5F7FA',BORDER:'D0D5DD',MUTED:'6B7280',CODE_BG:'F0F2F5',
  GREEN:'10B981',AMBER:'F59E0B',RED_ALERT:'B91C1C',GOLD:'B45309'
};
pptx.layout='LAYOUT_WIDE'; pptx.title='Hyundai ML Pipeline Use Cases — PeopleTech';

// ── Helpers (identical to hyundai-deal-prep.pptx template) ──
function addTitle(s,t,sub){
  s.addText(t,{x:0.5,y:0.25,w:12.5,h:0.7,fontSize:36,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
  if(sub)s.addText(sub,{x:0.5,y:0.9,w:12.5,h:0.4,fontSize:14,color:C.MUTED,fontFace:'Calibri'});
}
function addCard(s,x,y,w,h,hdr,body,opts={}){
  s.addShape(pptx.ShapeType.rect,{x,y,w,h,line:{color:C.BORDER,width:1},fill:{color:opts.fill||C.WHITE},rectRadius:0.08});
  if(hdr){
    s.addShape(pptx.ShapeType.rect,{x,y,w,h:0.38,fill:{color:opts.hc||C.NAVY_CARD},rectRadius:0.08});
    s.addText(hdr,{x:x+0.12,y:y+0.06,w:w-0.24,h:0.28,fontSize:12,bold:true,color:C.WHITE,fontFace:'Calibri'});
  }
  s.addText(body,{x:x+0.12,y:y+(hdr?0.44:0.12),w:w-0.24,h:h-(hdr?0.56:0.24),fontSize:opts.fs||11,color:C.CHARCOAL,fontFace:'Calibri',valign:'top',wrap:true});
}
function addBanner(s,t){
  s.addShape(pptx.ShapeType.rect,{x:0,y:6.85,w:13.33,h:0.65,fill:{color:C.NAVY_CARD}});
  s.addText(t,{x:0.4,y:6.88,w:12.5,h:0.58,fontSize:14,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
}
function addMetric(s,x,y,num,label,color){
  s.addText(num,{x,y,w:2.8,h:0.55,fontSize:30,bold:true,color:color||C.NAVY_DEEP,fontFace:'Calibri',align:'center'});
  s.addText(label,{x,y:y+0.5,w:2.8,h:0.3,fontSize:9,color:C.MUTED,fontFace:'Calibri',align:'center'});
}
// Use case detail slide builder
function addUcSlide(uc){
  let s=pptx.addSlide(); s.background={fill:C.WHITE};
  // UC badge
  s.addShape(pptx.ShapeType.roundRect,{x:0.5,y:0.25,w:0.9,h:0.4,fill:{color:C.NAVY_DEEP},rectRadius:0.1});
  s.addText(uc.id,{x:0.5,y:0.25,w:0.9,h:0.4,fontSize:14,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
  // Phase badge
  s.addShape(pptx.ShapeType.roundRect,{x:1.55,y:0.25,w:1.4,h:0.4,fill:{color:uc.phaseColor},rectRadius:0.1});
  s.addText(uc.phase,{x:1.55,y:0.25,w:1.4,h:0.4,fontSize:10,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
  // Title
  s.addText(uc.name,{x:3.2,y:0.22,w:9,h:0.5,fontSize:32,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
  s.addText(uc.subtitle,{x:3.2,y:0.65,w:9,h:0.3,fontSize:13,color:C.MUTED,fontFace:'Calibri'});

  // Left: Problem + Solution
  addCard(s,0.3,1.2,6.2,2.0,'Problem',uc.problem,{hc:C.RED_ALERT,fs:10});
  addCard(s,0.3,3.4,6.2,2.0,'PeopleTech Solution',uc.solution,{hc:C.GREEN,fs:10});

  // Right: OpenHands Realization + Tech Stack
  addCard(s,6.8,1.2,6.2,2.5,'OpenHands Realization',uc.openhands,{hc:'7C3AED',fs:10});
  addCard(s,6.8,3.9,6.2,1.5,'Technical Stack',uc.techStack,{hc:C.NAVY_CARD,fs:10});

  // Bottom: Metrics
  uc.metrics.forEach((m,i)=>{
    addMetric(s, 0.3+i*3.2, 5.7, m.num, m.label, m.color);
  });
  addBanner(s,uc.banner);
  return s;
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 1: Title
// ═══════════════════════════════════════════════════════════════
let s1=pptx.addSlide(); s1.background={fill:C.WHITE};
s1.addText('Hyundai Motor Group',{x:0.5,y:1.8,w:8,h:0.9,fontSize:44,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
s1.addText('ML Pipeline Use Cases',{x:0.5,y:2.7,w:8,h:0.6,fontSize:26,color:C.CHARCOAL,fontFace:'Calibri'});
s1.addText('8 AI Use Cases + MLOps Platform for Software-Defined Factory',{x:0.5,y:3.4,w:8,h:0.4,fontSize:14,color:C.MUTED,fontFace:'Calibri'});
s1.addShape(pptx.ShapeType.roundRect,{x:0.5,y:4.1,w:5.5,h:0.36,fill:{color:C.RED},rectRadius:0.1});
s1.addText('Realized with OpenHands AI-Driven Development  |  github.com/OpenHands/OpenHands',{x:0.5,y:4.1,w:5.5,h:0.36,fontSize:9,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
addBanner(s1,'PeopleTech AI Plant Operations — May 2026');

// ═══════════════════════════════════════════════════════════════
// SLIDE 2: Company Snapshot (from deal-prep template)
// ═══════════════════════════════════════════════════════════════
let s2=pptx.addSlide(); s2.background={fill:C.WHITE};
addTitle(s2,'Company Snapshot','Hyundai Motor Group at a glance');
const facts=[
  {h:'Revenue & Scale',b:'$132B trailing twelve months\n3 brands: Hyundai, Kia, Genesis\n250,000 employees, 16 global plants'},
  {h:'2026 Investments',b:'$6.7B Saemangeum AI/robotics hub\n50,000 NVIDIA Blackwell GPUs\nSaudi Arabia plant Q4 2026\n$26B US investment by 2028'},
  {h:'AI Partnerships',b:'MakinaRocks — robot predictive maintenance\n  (1,400 robots, 90% accuracy, since 2018)\nROAI/XELO — robotic process optimization\nHyundai AutoEver — MES, IoT, PHM'},
  {h:'Key Decision Makers',b:'Alpesh Patel — EVP, Software-Defined Factory\nJongho Shin — MD, E-FOREST Center\nJuncheul Jung — President, Manufacturing\nEunsook Jin — President, ICT/Digital'}
];
facts.forEach((f,i)=>{
  const col=i%2, row=Math.floor(i/2);
  addCard(s2, 0.5+col*6.2, 1.5+row*2.4, 5.8, 2.1, f.h, f.b);
});

// ═══════════════════════════════════════════════════════════════
// SLIDE 3: The Gap — What's Missing
// ═══════════════════════════════════════════════════════════════
let s3=pptx.addSlide(); s3.background={fill:C.WHITE};
addTitle(s3,'The Gap','Hyundai has infrastructure — not AI applications');
// Existing stack
const existStack=[
  {h:'NVIDIA Compute',b:'50K Blackwell GPUs\nModel training capacity',x:0.3},
  {h:'Omniverse Twin',b:'Virtual factory replicas\nSimulation & validation',x:2.7},
  {h:'AutoEver IT',b:'MES, IoT Platform\nCMS/PHM, Factory BI',x:5.1},
  {h:'MakinaRocks',b:'Robot health AI\n1,400 robots covered',x:7.5},
  {h:'ROAI / XELO',b:'Robot path optimization\nProcess design AI',x:9.9},
];
existStack.forEach(f=>{
  addCard(s3,f.x,1.5,2.2,1.6,f.h,f.b,{fs:9});
});
// Gap highlight
s3.addShape(pptx.ShapeType.rect,{x:0.3,y:3.4,w:12,h:0.5,line:{color:C.RED,width:2,dashType:'dash'},fill:{color:'FEF2F2'},rectRadius:0.06});
s3.addText('GAP:  No multi-model quality AI  |  No ML lifecycle management  |  No AI safety for Atlas  |  No cross-plant governance',
  {x:0.5,y:3.42,w:11.5,h:0.45,fontSize:11,bold:true,color:C.RED_ALERT,fontFace:'Calibri',align:'center',valign:'middle'});
// PeopleTech layer
addCard(s3,0.3,4.2,3.8,2.3,'PeopleTech AI Layer',
  '8 production AI use cases\nMLOps lifecycle platform\nEdge-optimized (<200ms)\nCross-plant governance\nIATF 16949 audit trail',{hc:C.NAVY_DEEP});
addCard(s3,4.4,4.2,3.8,2.3,'Realized with OpenHands',
  'AI Agent SDK for ML model development\nDocker-sandboxed training environments\nMulti-agent delegation per use case\nGitHub Actions CI/CD automation\nKubernetes enterprise deployment',{hc:'7C3AED'});
addCard(s3,8.5,4.2,3.8,2.3,'Why This Matters',
  'MakinaRocks = 1 use case (robot health)\nAutoEver = infrastructure only\nSiemens = horizontal, retrofitted AI\nPeopleTech = 8 vertical AI use cases\n  + unified MLOps + OpenHands velocity',{hc:C.RED_ALERT});

// ═══════════════════════════════════════════════════════════════
// SLIDE 4: 8 Use Cases Overview
// ═══════════════════════════════════════════════════════════════
let s4=pptx.addSlide(); s4.background={fill:C.WHITE};
addTitle(s4,'8 AI Use Cases for SDF','Phased deployment across quality, safety, compliance, and traceability');
const ucs=[
  {id:'UC05',n:'Predictive Quality',p:'Phase 1',pc:C.GREEN,d:'Multi-model SPC replacement\nAdapts per variant in real-time\nROI: $13M/year per 1% improvement'},
  {id:'UC04',n:'SOP Compliance',p:'Phase 2',pc:C.AMBER,d:'Pose estimation + action matching\nAtlas robot readiness (2028)\nISO 10218 / ISO/TS 15066'},
  {id:'UC07',n:'Safety Monitoring',p:'Phase 2',pc:C.AMBER,d:'Zone detection + PPE compliance\nHuman-robot proximity alerts\nCritical for Atlas deployment'},
  {id:'UC01',n:'Visual Inspection',p:'Phase 3',pc:C.NAVY_DEEP,d:'CNN defect classification\nPer-model-variant detection\nComplements Spot robot QC'},
  {id:'UC02',n:'Variant Confirmation',p:'Phase 3',pc:C.NAVY_DEEP,d:'Real-time BOM validation\nDuring SDF model switches\nStation-level verification'},
  {id:'UC08',n:'Digital Traceability',p:'Phase 3',pc:C.NAVY_DEEP,d:'Part-level genealogy graph\nSurgical recall capability\nSaves $3.5M per incident'},
  {id:'UC03',n:'Seating Validation',p:'Phase 3',pc:C.NAVY_DEEP,d:'AI-enhanced torque/force check\nBorderline case prediction\nIncremental quality lift'},
  {id:'UC06',n:'Predictive Maint.',p:'Covered',pc:C.MUTED,d:'MakinaRocks RPMS deployed\nWe integrate, not compete\nData feed into our platform'},
];
ucs.forEach((u,i)=>{
  const col=i%4, row=Math.floor(i/4);
  const x=0.3+col*3.2, y=1.5+row*2.6;
  s4.addShape(pptx.ShapeType.rect,{x,y,w:3,h:2.3,line:{color:C.BORDER,width:1},fill:{color:C.WHITE},rectRadius:0.08});
  s4.addShape(pptx.ShapeType.roundRect,{x:x+0.1,y:y+0.1,w:0.7,h:0.28,fill:{color:C.NAVY_DEEP},rectRadius:0.06});
  s4.addText(u.id,{x:x+0.1,y:y+0.1,w:0.7,h:0.28,fontSize:9,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
  s4.addShape(pptx.ShapeType.roundRect,{x:x+1.9,y:y+0.1,w:1,h:0.28,fill:{color:u.pc},rectRadius:0.06});
  s4.addText(u.p,{x:x+1.9,y:y+0.1,w:1,h:0.28,fontSize:8,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
  s4.addText(u.n,{x:x+0.12,y:y+0.5,w:2.76,h:0.35,fontSize:13,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
  s4.addText(u.d,{x:x+0.12,y:y+0.85,w:2.76,h:1.3,fontSize:10,color:C.CHARCOAL,fontFace:'Calibri',valign:'top',wrap:true});
});
addBanner(s4,'Each use case realized with OpenHands Agent SDK — see detailed slides →');

// ═══════════════════════════════════════════════════════════════
// SLIDES 5-10: Detailed Use Case Slides
// ═══════════════════════════════════════════════════════════════

// UC05: Predictive Quality
addUcSlide({
  id:'UC05', phase:'Phase 1', phaseColor:C.GREEN,
  name:'Predictive Quality', subtitle:'Multi-model SPC replacement for SDF lines',
  problem:
    'SDF switches between 10 model variants on one line. Traditional SPC was designed for single-model runs.\n\n'+
    'When Model A switches to Model B, quality thresholds change — weld specs, gap tolerances, torque values, paint thickness. SPC can\'t recalibrate in real-time.\n\n'+
    'Result: quality escapes during model transitions. 10x more failure modes threaten J.D. Power #1 ranking.',
  solution:
    'ML model per production station recalibrates quality thresholds per model variant in real-time.\n\n'+
    'Trained on historical defect data (Quality & Defect DB) + real-time sensor streams (AVEVA PI Historian). Edge inference <200ms on Jetson/Hailo via TensorRT.\n\n'+
    'Closed-loop: predictions feed back into AutoEver MES quality gates. Weekly auto-retrain via MLOps pipeline.',
  openhands:
    'OpenHands Agent SDK builds the ML pipeline:\n\n'+
    '• CodeAct Agent writes PyTorch training code from defect data schema\n'+
    '• Docker Workspace provides sandboxed training environment\n'+
    '• Multi-agent delegation: one agent per model variant\n'+
    '• GitHub Actions workflow for CI/CD: train → validate → optimize → deploy\n'+
    '• Skills system injects SDF domain knowledge (variant specs, tolerance tables)\n\n'+
    'github.com/OpenHands/OpenHands → SDK + Agent Server',
  techStack:
    'PyTorch / TensorFlow  |  MLflow (registry)  |  TensorRT / ONNX (edge)  |  SageMaker / Azure ML (training)\n'+
    'AVEVA PI Historian (data)  |  PostgreSQL (defect DB)  |  Jetson / Hailo (edge GPU)  |  OPC-UA (PLC integration)',
  metrics:[
    {num:'$13M',label:'Value of 1% defect reduction / year',color:C.RED},
    {num:'90',label:'Days to proof of value',color:C.NAVY_DEEP},
    {num:'<$1M',label:'Pilot investment',color:C.NAVY_DEEP},
    {num:'<200ms',label:'Edge inference latency',color:C.GREEN},
  ],
  banner:'Phase 1: Ulsan Plant 5 — 3+ SDF model variants — 90-day proof of value'
});

// UC04: SOP Compliance
addUcSlide({
  id:'UC04', phase:'Phase 2', phaseColor:C.AMBER,
  name:'SOP Compliance', subtitle:'Pose estimation for Atlas robot readiness (2028)',
  problem:
    'Human workers follow standard operating procedures manually. No automated verification that steps are completed correctly and in order.\n\n'+
    'With Atlas robots co-working from 2028, SOP compliance becomes safety-critical — incorrect human actions in robot work zones cause injuries.\n\n'+
    'Current state: compliance is audited post-shift via paper checklists. Zero real-time enforcement.',
  solution:
    'Computer vision AI monitors worker compliance in real-time:\n\n'+
    '• Pose estimation tracks body position and movement patterns\n'+
    '• Action sequence matching verifies steps completed in correct order\n'+
    '• Real-time alerts for skipped steps, wrong sequence, unsafe posture\n\n'+
    'ATLAS ANGLE: Same AI extends to human-robot handoff zones. Train on human workflows NOW — 2 years of data before Atlas arrives.',
  openhands:
    'OpenHands builds the computer vision pipeline:\n\n'+
    '• CodeAct Agent develops pose estimation model (MediaPipe / OpenPose)\n'+
    '• Browsing Agent researches ISO 10218 compliance requirements\n'+
    '• Docker Workspace: isolated CV training with GPU passthrough\n'+
    '• Micro Agents specialize per station type (assembly, welding, paint)\n'+
    '• Agent Server (Kubernetes) scales inference across camera fleet\n\n'+
    'github.com/OpenHands/OpenHands → Multi-agent delegation',
  techStack:
    'MediaPipe / OpenPose (pose)  |  YOLOv8 (object detection)  |  OpenCV (video)  |  PyTorch (training)\n'+
    'NVIDIA DeepStream (edge video)  |  MQTT (alerts)  |  Kubernetes (inference scaling)  |  EHS system (integration)',
  metrics:[
    {num:'25K+',label:'Atlas robots planned by 2030',color:C.NAVY_DEEP},
    {num:'2028',label:'First Atlas deployment',color:C.GOLD},
    {num:'$10M+',label:'Liability per safety incident',color:C.RED},
    {num:'ISO',label:'10218 / TS 15066 compliance',color:C.NAVY_DEEP},
  ],
  banner:'Phase 2: Metaplant America (Georgia) — Deploy AI safety layer before Atlas arrives'
});

// UC07: Safety Monitoring
addUcSlide({
  id:'UC07', phase:'Phase 2', phaseColor:C.AMBER,
  name:'Safety Monitoring', subtitle:'Zone detection, PPE compliance, human-robot proximity',
  problem:
    'Spot robots patrol but don\'t perform real-time AI safety analysis. No continuous zone monitoring.\n\n'+
    'Atlas deployment (2028) requires 24/7 human-robot proximity tracking — OSHA, ISO 10218, ISO/TS 15066 mandate it.\n\n'+
    'One safety incident during Atlas rollout = $10M+ liability, production halt, regulatory scrutiny, and media attention that threatens the "Partnering Human Progress" narrative.',
  solution:
    'Camera-based AI safety monitoring across the production floor:\n\n'+
    '• Zone detection: track who/what occupies each work area in real-time\n'+
    '• PPE compliance: hard hat, safety vest, eye protection, glove verification\n'+
    '• Human-robot proximity tracking: alert when humans enter robot work envelope\n'+
    '• Real-time EHS system integration: instant alerts to safety officers\n'+
    '• Incident video capture: 30-second pre/post clips for investigation',
  openhands:
    'OpenHands accelerates safety AI development:\n\n'+
    '• CodeAct Agent builds YOLOv8 object detection for PPE items\n'+
    '• Multi-agent: zone segmentation agent + PPE agent + proximity agent\n'+
    '• Docker Workspace: training on synthetic data (Omniverse-generated)\n'+
    '• GitHub Actions: automated model validation against safety test suite\n'+
    '• Enterprise deployment: self-hosted in Hyundai VPC via Kubernetes\n\n'+
    'github.com/OpenHands/OpenHands → Enterprise self-hosting',
  techStack:
    'YOLOv8 / RT-DETR (detection)  |  DeepSORT (tracking)  |  NVIDIA DeepStream (video pipeline)\n'+
    'Omniverse (synthetic data)  |  PagerDuty / Slack (alerts)  |  EHS system (compliance)  |  S3 (incident video)',
  metrics:[
    {num:'24/7',label:'Continuous monitoring coverage',color:C.GREEN},
    {num:'<100ms',label:'Alert latency requirement',color:C.NAVY_DEEP},
    {num:'99.5%',label:'Target PPE detection accuracy',color:C.NAVY_DEEP},
    {num:'OSHA',label:'Regulatory compliance',color:C.RED},
  ],
  banner:'Phase 2: Paired with UC04 for complete Atlas readiness package — $1-2M combined'
});

// UC01: Visual Inspection
addUcSlide({
  id:'UC01', phase:'Phase 3', phaseColor:C.NAVY_DEEP,
  name:'Visual Inspection', subtitle:'CNN defect classification per SDF model variant',
  problem:
    'Spot robots perform post-line QC patrols. HMGICS has some AI vision. But neither handles in-line, station-level defect detection across 10 SDF model variants.\n\n'+
    'Each model variant has different defect patterns — a scratch on a Genesis ≠ a scratch on an Ioniq. Current inspection doesn\'t adapt classification thresholds per model.\n\n'+
    'Metaplant tests every vehicle (human test drive, 95% pass rate) but catches defects too late in the process.',
  solution:
    'CNN-based defect classification at inspection stations, adapted per model variant:\n\n'+
    '• Camera array captures high-res images at critical stations (paint, body, trim)\n'+
    '• Model-aware classification: switches detection profile when SDF variant changes\n'+
    '• Defect taxonomy: surface (scratch, dent, orange peel), assembly (gap, flush), paint (runs, sags, contamination)\n'+
    '• Complements Spot patrols: station-level catches defects BEFORE Spot finds them post-line',
  openhands:
    'OpenHands builds variant-aware defect classifiers:\n\n'+
    '• CodeAct Agent creates per-variant CNN architectures (EfficientNet / ResNet)\n'+
    '• Skills: inject defect taxonomy knowledge per model line\n'+
    '• Multi-agent: one training agent per defect type (surface, assembly, paint)\n'+
    '• Agent Server: orchestrates parallel training across variant datasets\n'+
    '• GitHub Actions: retrain trigger when new variant introduced to SDF line\n\n'+
    'github.com/OpenHands/OpenHands → Skills + custom tools',
  techStack:
    'EfficientNet / ResNet (classification)  |  OpenCV (image pre-processing)  |  Albumentations (augmentation)\n'+
    'ONNX Runtime (edge inference)  |  GStreamer (camera pipeline)  |  MLflow (experiment tracking)  |  AutoEver MES (quality gate)',
  metrics:[
    {num:'10',label:'SDF model variants per line',color:C.NAVY_DEEP},
    {num:'<50ms',label:'Per-image inference target',color:C.GREEN},
    {num:'99%+',label:'Target defect detection rate',color:C.NAVY_DEEP},
    {num:'95%',label:'Current human test pass rate',color:C.MUTED},
  ],
  banner:'Phase 3: In-line detection complements Spot post-line patrols — catches defects earlier'
});

// UC08: Digital Traceability
addUcSlide({
  id:'UC08', phase:'Phase 3', phaseColor:C.NAVY_DEEP,
  name:'Digital Traceability', subtitle:'Part-level genealogy for surgical recall',
  problem:
    'Recent recall: 7,698 Creta/Verna units. MES tracks high-level production data but lacks part-level genealogy.\n\n'+
    'Without part traceability, a defect in one supplier batch forces recall of the entire production run — not just affected vehicles. Costs $500+/unit.\n\n'+
    'IATF 16949 requires traceability. Hyundai\'s current system relies on batch-level tracking, not individual part lineage.',
  solution:
    'End-to-end part tracking from supplier receipt to finished vehicle:\n\n'+
    '• Part genealogy graph: every component linked to its supplier lot, station, operator, timestamp\n'+
    '• Surgical recall: query "which VINs have parts from Supplier X, Lot Y?" — returns 500 VINs, not 7,698\n'+
    '• Supplier quality scoring: track defect rates per supplier per part per lot\n'+
    '• Blockchain-ready: hash-anchored traceability records for tamper-proof audit',
  openhands:
    'OpenHands builds the traceability data pipeline:\n\n'+
    '• CodeAct Agent develops graph database schema (Neo4j / Neptune)\n'+
    '• Multi-agent: ingestion agent (MES → graph) + query agent (recall search)\n'+
    '• Docker Workspace: isolated testing with synthetic production data\n'+
    '• GitHub Actions: automated IATF compliance validation suite\n'+
    '• Enterprise: Kubernetes deployment with per-plant graph shards\n\n'+
    'github.com/OpenHands/OpenHands → Docker sandboxed execution',
  techStack:
    'Neo4j / Amazon Neptune (graph DB)  |  Apache Kafka (event streaming)  |  RFID / barcode (part identity)\n'+
    'AutoEver MES (data source)  |  GraphQL (query API)  |  IPFS / blockchain (audit anchoring)  |  Grafana (dashboard)',
  metrics:[
    {num:'$3.5M',label:'Saved per surgical vs. mass recall',color:C.RED},
    {num:'7,698',label:'Recent recall size (could be 500)',color:C.GOLD},
    {num:'IATF',label:'16949 compliance automated',color:C.NAVY_DEEP},
    {num:'<5s',label:'Recall query response time',color:C.GREEN},
  ],
  banner:'Phase 3: Surgical recall saves millions and protects brand reputation'
});

// UC02: Variant Confirmation
addUcSlide({
  id:'UC02', phase:'Phase 3', phaseColor:C.NAVY_DEEP,
  name:'Variant Confirmation', subtitle:'Real-time BOM validation during SDF model switches',
  problem:
    'SDF lines switch between 10 models. Each switch changes the Bill of Materials — different parts, different assembly sequence, different configurations.\n\n'+
    'Mis-builds during model transitions are the #1 quality risk in flexible manufacturing. Wrong part installed = rework ($2,000+/vehicle) or warranty claim.\n\n'+
    'Current validation is MES work-order based — no real-time station-level confirmation that the physical part matches the digital BOM.',
  solution:
    'Real-time confirmation at each station during model switches:\n\n'+
    '• RFID/barcode scan validates part number against current BOM variant\n'+
    '• Vision verification confirms physical part matches expected geometry\n'+
    '• Station-level alerts: "wrong part for Model B — expecting P/N 12345"\n'+
    '• Transition monitoring: tracks error rate during first 10 units after each switch\n'+
    '• Integration: feeds validation status back to AutoEver MES',
  openhands:
    'OpenHands develops the validation logic layer:\n\n'+
    '• CodeAct Agent builds BOM matching algorithms from MES data schema\n'+
    '• Skills: inject BOM structure per model variant (part hierarchies)\n'+
    '• Multi-agent: scan validation agent + vision matching agent\n'+
    '• Agent Server: handles real-time validation requests per station\n'+
    '• GitHub Actions: regression tests against known mis-build scenarios\n\n'+
    'github.com/OpenHands/OpenHands → Custom tools + MCP integration',
  techStack:
    'RFID readers / barcode scanners (identity)  |  YOLOv8 (part geometry)  |  FastAPI (validation API)\n'+
    'Redis (real-time state)  |  AutoEver MES (BOM source)  |  OPC-UA (station PLC)  |  MQTT (alerts)',
  metrics:[
    {num:'$2K+',label:'Rework cost per mis-build',color:C.RED},
    {num:'10',label:'Model variants per SDF line',color:C.NAVY_DEEP},
    {num:'<1s',label:'Validation response time',color:C.GREEN},
    {num:'0',label:'Target mis-builds per shift',color:C.NAVY_DEEP},
  ],
  banner:'Phase 3: Station-level validation prevents mis-builds during SDF model transitions'
});

// ═══════════════════════════════════════════════════════════════
// SLIDE 11: OpenHands Platform Overview
// ═══════════════════════════════════════════════════════════════
let s11=pptx.addSlide(); s11.background={fill:C.WHITE};
addTitle(s11,'OpenHands: AI-Driven Development','How PeopleTech realizes use cases 10x faster');
s11.addText('github.com/OpenHands/OpenHands  |  72K+ stars  |  MIT license  |  470+ contributors',
  {x:0.5,y:0.95,w:12,h:0.3,fontSize:11,color:'7C3AED',fontFace:'Calibri'});

addCard(s11,0.3,1.5,4,2.2,'Software Agent SDK',
  '• Composable Python library for building AI coding agents\n'+
  '• CodeAct Agent: writes, tests, and deploys ML code\n'+
  '• Custom tools: integrate with OPC-UA, MES, IoT\n'+
  '• Skills system: inject manufacturing domain knowledge\n'+
  '• Multi-agent delegation: parallel development',{hc:'7C3AED',fs:10});

addCard(s11,4.6,1.5,4,2.2,'Agent Server (Production)',
  '• Docker-sandboxed execution environments\n'+
  '• Kubernetes deployment for enterprise scale\n'+
  '• Multi-user isolation per plant / team\n'+
  '• WebSocket streaming for real-time monitoring\n'+
  '• Self-hosted in Hyundai VPC (Enterprise tier)',{hc:'7C3AED',fs:10});

addCard(s11,8.9,1.5,3.8,2.2,'CI/CD Automation',
  '• GitHub Actions workflows for ML pipeline\n'+
  '• Auto-retrain on drift detection trigger\n'+
  '• Automated code review (quality gates)\n'+
  '• Model validation test suites\n'+
  '• Continuous deployment to edge fleet',{hc:'7C3AED',fs:10});

// Use case mapping table
const ucMap=[
  ['Use Case','OpenHands Component','How It Accelerates'],
  ['UC05 Predictive Quality','CodeAct + Skills + GitHub Actions','Agent writes training code from data schema, auto-deploys via CI/CD'],
  ['UC04 SOP Compliance','Multi-Agent + Docker Workspace','Parallel agents develop per-station pose models in sandboxed GPU envs'],
  ['UC07 Safety Monitoring','Agent Server + Enterprise K8s','Production inference scaling across camera fleet, per-plant isolation'],
  ['UC01 Visual Inspection','Skills + Custom Tools','Domain knowledge injection: defect taxonomy per model variant'],
  ['UC02 Variant Confirmation','CodeAct + MCP Integration','Agent builds BOM validation logic, integrates with MES via MCP tools'],
  ['UC08 Digital Traceability','Docker Workspace + GitHub Actions','Isolated graph DB development + automated IATF compliance tests'],
];
const ucCw=[2.8,3.5,6];
ucMap.forEach((row,ri)=>{
  const ry=4.0+ri*0.55;
  row.forEach((cell,ci)=>{
    const cx=0.5+ucCw.slice(0,ci).reduce((a,b)=>a+b,0);
    const isH=ri===0;
    const fill=isH?'7C3AED':(ri%2===0?C.LIGHT_BG:C.WHITE);
    const tc=isH?C.WHITE:C.CHARCOAL;
    s11.addShape(pptx.ShapeType.rect,{x:cx,y:ry,w:ucCw[ci],h:0.5,fill:{color:fill},line:{color:C.BORDER,width:0.5}});
    s11.addText(cell,{x:cx+0.08,y:ry+0.02,w:ucCw[ci]-0.16,h:0.46,fontSize:isH?10:9,bold:isH||ci===0,color:tc,fontFace:'Calibri',valign:'middle',wrap:true});
  });
});

// ═══════════════════════════════════════════════════════════════
// SLIDE 12: MLOps Pipeline
// ═══════════════════════════════════════════════════════════════
let s12=pptx.addSlide(); s12.background={fill:C.WHITE};
addTitle(s12,'MLOps Pipeline','Closed-loop model lifecycle powering all use cases');
const stages=[
  {h:'1. Data Collection',b:'Plant sensors, inference logs\nHuman feedback, labeling\nDataset versioning (DVC)\nAVEVA PI + AutoEver IoT',x:0.3,hc:C.NAVY_CARD},
  {h:'2. Feature & Training',b:'Feature store (SageMaker)\nData validation (Gt. Expect.)\nGPU training (Blackwell)\nMLflow experiment tracking',x:3.4,hc:C.NAVY_CARD},
  {h:'3. Package & Deploy',b:'TensorRT / ONNX optimization\nContainer build (ECR/ACR)\nCanary deployment (5%)\nEdge OTA (IoT Greengrass)',x:6.5,hc:C.NAVY_CARD},
  {h:'4. Monitor & Retrain',b:'Drift detection (KL div.)\nAuto-retrain alerts\nIATF 16949 audit trail\nBusiness value tracking',x:9.6,hc:C.RED_ALERT},
];
stages.forEach(f=>{
  addCard(s12,f.x,1.5,2.9,2.5,f.h,f.b,{hc:f.hc,fs:10});
});
[3.2,6.3,9.4].forEach(x=>{
  s12.addText('→',{x,y:2.4,w:0.3,h:0.5,fontSize:24,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri',align:'center'});
});
s12.addShape(pptx.ShapeType.rect,{x:0.3,y:4.3,w:12.3,h:0.4,line:{color:C.RED,width:2,dashType:'dash'},fill:{color:'FEF2F2'},rectRadius:0.06});
s12.addText('← CLOSED LOOP: Drift detected → auto-retrain → canary deploy → performance validated →',
  {x:0.5,y:4.32,w:11.9,h:0.35,fontSize:10,bold:true,color:C.RED,fontFace:'Calibri',align:'center',valign:'middle'});
addCard(s12,0.3,5.0,4,1.5,'Hyundai Integration',
  '• AVEVA PI Historian (time-series)\n• AutoEver MES (quality gates)\n• AutoEver IoT Platform (sensors)\n• Omniverse (twin validation)\n• MakinaRocks RPMS (robot data)',{fs:10});
addCard(s12,4.6,5.0,4,1.5,'Edge Deployment',
  '• NVIDIA Jetson / Hailo accelerators\n• <200ms inference budget\n• Rolling OTA: plant → line → station\n• Instant rollback capability\n• Zero line downtime',{fs:10});
addCard(s12,8.9,5.0,3.8,1.5,'Governance',
  '• Full audit: data → model → deploy\n• Safety-critical approval gates\n• IATF 16949 / ISO 9001 mapping\n• MLflow Model Registry\n• ROI digest per plant',{fs:10});

// ═══════════════════════════════════════════════════════════════
// SLIDE 13: Competitive Landscape
// ═══════════════════════════════════════════════════════════════
let s13=pptx.addSlide(); s13.background={fill:C.WHITE};
addTitle(s13,'Competitive Landscape','Why PeopleTech + OpenHands, not alternatives');
const tbl=[
  [{text:'Dimension',options:{bold:true,fill:{color:C.NAVY_DEEP},color:C.WHITE}},
   {text:'MakinaRocks',options:{bold:true,fill:{color:C.NAVY_DEEP},color:C.WHITE}},
   {text:'AutoEver',options:{bold:true,fill:{color:C.NAVY_DEEP},color:C.WHITE}},
   {text:'Siemens',options:{bold:true,fill:{color:C.NAVY_DEEP},color:C.WHITE}},
   {text:'PeopleTech',options:{bold:true,fill:{color:C.RED},color:C.WHITE}}],
  ['Scope','Robot health only','Infrastructure (MES, IoT)','Full stack, horizontal','8 production AI use cases'],
  ['ML Lifecycle','Single model','None','Basic','Full MLOps (train→deploy→monitor→retrain)'],
  ['Multi-Model SDF','N/A','N/A','Generic','Built for 10-variant quality'],
  ['Dev Velocity','Traditional ML','In-house teams','Consulting-heavy','OpenHands AI agents (10x faster)'],
  ['Edge Optimization','Unknown','No','Cloud-first','TensorRT/ONNX, <200ms Jetson'],
  ['Governance','Per-robot','Per-system','Per-platform','Per-model, IATF-mapped'],
  ['Cross-Plant','4 sites','Global MES','Global','Designed for 15+ plant fleet'],
];
s13.addTable(tbl,{x:0.3,y:1.4,w:12.7,colW:[2.2,2.4,2.4,2.4,3.3],
  border:{pt:0.5,color:C.BORDER},rowH:0.55,fontSize:10,fontFace:'Calibri',color:C.CHARCOAL,autoPage:false});
addCard(s13,0.3,5.7,12.7,0.9,'PeopleTech Wedge',
  'Only vendor with (1) purpose-built multi-model SDF quality AI, (2) full MLOps lifecycle across 8 use cases, (3) OpenHands-accelerated development velocity, and (4) cross-plant IATF governance. MakinaRocks does robot health. AutoEver does infrastructure. Siemens is horizontal. PeopleTech is the vertical AI application layer.',{hc:C.RED,fs:10});

// ═══════════════════════════════════════════════════════════════
// SLIDE 14: Next Steps (from deal-prep template)
// ═══════════════════════════════════════════════════════════════
let s14=pptx.addSlide(); s14.background={fill:C.WHITE};
addTitle(s14,'Next Steps','Three actions to move forward');
addCard(s14,0.5,1.5,3.8,3.0,'Step 1: Ulsan Pilot\n(Phase 1 — 90 days)',
  'Predictive quality (UC05) on one SDF line with 3+ model variants at Ulsan Plant 5.\n\nHard success metrics upfront.\nRisk-free: miss targets → you keep the data.\n\nInvestment: $500K-$1M',{hc:C.GREEN});
addCard(s14,4.6,1.5,3.8,3.0,'Step 2: Atlas Scoping\n(Phase 2 — 6 months)',
  'SOP compliance (UC04) + safety monitoring (UC07) at Metaplant America.\n\nAlign with 2028 Atlas deployment timeline.\nJoint session with robotics team.\n\nInvestment: $1-2M',{hc:C.AMBER});
addCard(s14,8.7,1.5,3.8,3.0,'Step 3: MLOps Workshop\n(Phase 3 — 12 months)',
  'Joint architecture review with AutoEver + E-FOREST Center.\n\nDesign cross-plant governance model.\nScale to 15+ plants, all 8 use cases.\n\nInvestment: $5-15M/year platform',{hc:C.NAVY_DEEP});

// Key people
s14.addText('Key Meetings to Request',{x:0.5,y:4.8,w:12,h:0.3,fontSize:16,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
const people=[
  ['Alpesh Patel','EVP, SDF','Technical validation: predictive quality AI for SDF data flows'],
  ['Jongho Shin','MD, E-FOREST Center','Atlas readiness: AI safety layer for human-robot collaboration'],
  ['Eunsook Jin','President, ICT/Digital','Budget holder: MLOps platform on NVIDIA + AutoEver infrastructure'],
  ['Juncheul Jung','President, Manufacturing','Executive sponsor: AI ROI impact in year one'],
];
const pCw=[2.2,2.5,7.6];
people.forEach((row,ri)=>{
  const ry=5.2+ri*0.42;
  row.forEach((cell,ci)=>{
    const cx=0.5+pCw.slice(0,ci).reduce((a,b)=>a+b,0);
    const fill=ri%2===0?C.LIGHT_BG:C.WHITE;
    s14.addShape(pptx.ShapeType.rect,{x:cx,y:ry,w:pCw[ci],h:0.38,fill:{color:fill},line:{color:C.BORDER,width:0.5}});
    s14.addText(cell,{x:cx+0.08,y:ry+0.02,w:pCw[ci]-0.16,h:0.34,fontSize:10,bold:ci===0,color:C.CHARCOAL,fontFace:'Calibri',valign:'middle',wrap:true});
  });
});
addBanner(s14,'PeopleTech + OpenHands — The AI Application Layer for Software-Defined Factories');

// ═══════════════════════════════════════════════════════════════
// Generate
// ═══════════════════════════════════════════════════════════════
pptx.writeFile({fileName:'hyundai-ml-pipeline-deck.pptx'})
  .then(()=>console.log('✓ hyundai-ml-pipeline-deck.pptx generated (14 slides)'))
  .catch(e=>console.error('✗ Error:',e));
