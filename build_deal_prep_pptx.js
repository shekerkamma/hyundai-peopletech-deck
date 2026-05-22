const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
const C = {
  WHITE:'FFFFFF',CHARCOAL:'1A1A1A',NAVY_DEEP:'1F3B6E',NAVY_CARD:'0D3B5E',
  RED:'E31837',LIGHT_BG:'F5F7FA',BORDER:'D0D5DD',MUTED:'6B7280',CODE_BG:'F0F2F5'
};
pptx.layout='LAYOUT_WIDE'; pptx.title='Hyundai Deal Prep';

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
  s.addText(body,{x:x+0.12,y:y+(hdr?0.44:0.12),w:w-0.24,h:h-(hdr?0.56:0.24),fontSize:11,color:C.CHARCOAL,fontFace:'Calibri',valign:'top',wrap:true});
}
function addBanner(s,t){
  s.addShape(pptx.ShapeType.rect,{x:0,y:6.85,w:13.33,h:0.65,fill:{color:C.NAVY_CARD}});
  s.addText(t,{x:0.4,y:6.88,w:12.5,h:0.58,fontSize:14,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
}

// S1: Title
let s1=pptx.addSlide(); s1.background={fill:C.WHITE};
s1.addText('Hyundai Motor Group',{x:0.5,y:1.8,w:8,h:0.9,fontSize:44,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
s1.addText('Pre-Sales Deal Prep',{x:0.5,y:2.7,w:8,h:0.6,fontSize:26,color:C.CHARCOAL,fontFace:'Calibri'});
s1.addText('PeopleTech AI Plant Operations',{x:0.5,y:3.5,w:8,h:0.4,fontSize:14,color:C.MUTED,fontFace:'Calibri'});
s1.addShape(pptx.ShapeType.roundRect,{x:0.5,y:4.2,w:2.4,h:0.36,fill:{color:C.RED},rectRadius:0.1});
s1.addText('$132B Revenue  |  250K Employees',{x:0.5,y:4.2,w:2.4,h:0.36,fontSize:9,bold:true,color:C.WHITE,fontFace:'Calibri',align:'center',valign:'middle'});
addBanner(s1,'Prepared by PeopleTech AI Engineering — May 2026');

// S2: Company snapshot
let s2=pptx.addSlide(); s2.background={fill:C.WHITE};
addTitle(s2,'Company Snapshot','Hyundai Motor Group at a glance');
const facts=[
  {h:'Revenue',b:'$132B trailing twelve months\n3 brands: Hyundai, Kia, Genesis'},
  {h:'Employees',b:'250,000 worldwide\n15+ manufacturing plants globally'},
  {h:'2026 Investments',b:'KRW 9T ($6.7B) new industrial complex\nNVIDIA AI Factory (Blackwell)\nSaudi Arabia plant Q4 2026'},
  {h:'Key Decision Makers',b:'Juncheul Jung — President, Manufacturing\nEunsook Jin — President, ICT/Digital\nManfred Harrer — President, R&D'}
];
facts.forEach((f,i)=>{
  const col=i%2, row=Math.floor(i/2);
  addCard(s2, 0.5+col*6.2, 1.5+row*2.4, 5.8, 2.1, f.h, f.b);
});

// S3: What they're doing
let s3=pptx.addSlide(); s3.background={fill:C.WHITE};
addTitle(s3,'Strategic Initiatives','What Hyundai is investing in right now');
const inits=[
  {h:'Software-Defined Factory',b:'Single line switches between 10 model variants (hybrid, BEV, extended-range). Data and software drive production. Their manufacturing moat.'},
  {h:'NVIDIA AI Factory',b:'Blackwell-based AI supercomputer for in-vehicle AI, autonomous driving, smart factories, and robotics. Foundation infrastructure.'},
  {h:'AI Robotics (CES 2026)',b:'Next-gen Atlas robots for human-robot collaboration. Theme: "Partnering Human Progress." Commercializing robotic co-workers.'},
  {h:'Digital Twin (Omniverse)',b:'Factory digital twins for precision control, simulation, and virtual commissioning. Gap: no closed-loop to live production.'}
];
inits.forEach((f,i)=>{
  const col=i%2, row=Math.floor(i/2);
  addCard(s3, 0.5+col*6.2, 1.5+row*2.4, 5.8, 2.1, f.h, f.b);
});

// S4: Pain points
let s4=pptx.addSlide(); s4.background={fill:C.WHITE};
addTitle(s4,'Pain Points','Where Hyundai needs help — and where PeopleTech fits');
const pains=[
  {h:'Scaling SDF Globally',b:'SDF works at pilot scale. Scaling to 15+ plants with consistent quality across 10 model variants requires AI orchestration.'},
  {h:'Quality Across Variants',b:'#1 in J.D. Power today, but 10 models on one line = 10x failure modes. Traditional SPC can\'t adapt fast enough.'},
  {h:'Twin-to-Production Gap',b:'Digital twins exist (Omniverse) but the bridge to real-time production decisions is manual. No automated feedback loop.'},
  {h:'Saudi Plant Ramp-Up',b:'Greenfield plant launching Q4 2026. Getting to full quality in months instead of 12-18 months is critical.'}
];
pains.forEach((f,i)=>{
  const col=i%2, row=Math.floor(i/2);
  addCard(s4, 0.5+col*6.2, 1.5+row*2.4, 5.8, 2.1, f.h, f.b, {hc:'B91C1C'});
});

// S5: Positioning
let s5=pptx.addSlide(); s5.background={fill:C.WHITE};
addTitle(s5,'PeopleTech Positioning','The AI decision layer between infrastructure and outcomes');
s5.addText('Sensors/IoT  →  NVIDIA Omniverse Twin  →  PeopleTech AI Layer  →  Production Decisions',{x:0.5,y:1.6,w:12.3,h:0.5,fontSize:14,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri',align:'center'});
addCard(s5,0.5,2.3,3.8,2.8,'What We Are NOT',
  '• Not another IoT platform\n  (they have NVIDIA Omniverse)\n\n• Not a robotics company\n  (they have Boston Dynamics)\n\n• Not an ERP overlay\n  (they have SAP/Oracle)');
addCard(s5,4.6,2.3,3.8,2.8,'What We ARE',
  '• AI decision layer between\n  infrastructure and outcomes\n\n• Purpose-built for multi-model\n  flexible manufacturing (SDF)\n\n• Real-time anomaly detection\n  that adapts per model variant');
addCard(s5,8.7,2.3,3.8,2.8,'Why Us, Not Them',
  '• AI-native (not retrofitted)\n• SDF-specific (no competitor has this)\n• Faster to deploy: 90 days to value\n• Complements NVIDIA/Omniverse\n  (doesn\'t compete)');
addBanner(s5,'We fill the gap between Hyundai\'s infrastructure investments and operational AI outcomes');

// S6: Three proposals
let s6=pptx.addSlide(); s6.background={fill:C.WHITE};
addTitle(s6,'Three Proposals','Tiered approach: quick win → timely → strategic');
addCard(s6,0.5,1.5,3.8,3.8,'Proposal 1: Predictive Quality\n(Quick Win — 90 days)',
  'Deploy AI quality prediction on one SDF line with 3+ model variants at Ulsan Plant 5.\n\nTarget: 3-5% defect detection improvement.\n\nROI: 1% defect reduction = ~$13M/year saved.\n\nInvestment: $500K-$1M pilot.',{hc:'10B981'});
addCard(s6,4.6,1.5,3.8,3.8,'Proposal 2: Greenfield Accelerator\n(Timely — Saudi Q4 2026)',
  'AI-driven ramp-up for Saudi Arabia plant. Compress time-to-full-quality from 12-18 months to 4-6 months.\n\nROI: Every month faster = 50K units × margin.\n\nClean deployment: no legacy systems.\n\nInvestment: included in plant capex.',{hc:'F59E0B'});
addCard(s6,8.7,1.5,3.8,3.8,'Proposal 3: Closed-Loop Twin\n(Strategic — 12 months)',
  'Bridge Omniverse twins to live production. Automated: sensor → twin → adjust → measure.\n\nROI: Closes the "last mile" of their biggest investment.\n\nEntry: Eunsook Jin\'s ICT team.\n\nInvestment: $5-15M annually across 5 plants.',{hc:C.NAVY_DEEP});

// S7: Objections
let s7=pptx.addSlide(); s7.background={fill:C.WHITE};
addTitle(s7,'Anticipated Objections','What they\'ll say and how to respond');
const objs=[
  ['Objection','Response'],
  ['"We\'re working with Siemens"','Their AI is retrofitted. Ours is AI-native. Head-to-head on one line.'],
  ['"We\'ll build in-house with NVIDIA"','NVIDIA = compute foundation. Manufacturing domain expertise = 15 years of ours. Saves 2-3 years.'],
  ['"Budget is allocated for 2026"','Pilot is <$1M, discretionary for manufacturing org. Saudi plant falls under capex.'],
  ['"How does it work at our scale?"','90-day proof at Ulsan, hard metrics. If we miss, you keep the data for free.'],
  ['"How does it integrate?"','OPC-UA from PLCs, REST to Omniverse, MQTT streaming. Containerized. No rip-and-replace.']
];
const cw=[3.5,8.5];
objs.forEach((row,ri)=>{
  const ry=1.5+ri*0.78;
  row.forEach((cell,ci)=>{
    const cx=0.5+cw.slice(0,ci).reduce((a,b)=>a+b,0);
    const isH=ri===0;
    const fill=isH?C.NAVY_DEEP:(ri%2===0?C.LIGHT_BG:C.WHITE);
    const tc=isH?C.WHITE:C.CHARCOAL;
    s7.addShape(pptx.ShapeType.rect,{x:cx,y:ry,w:cw[ci],h:0.72,fill:{color:fill},line:{color:C.BORDER,width:0.5}});
    s7.addText(cell,{x:cx+0.1,y:ry+0.05,w:cw[ci]-0.2,h:0.62,fontSize:isH?12:11,bold:isH||ci===0,color:tc,fontFace:'Calibri',valign:'middle',wrap:true});
  });
});

// S8: Opening & close
let s8=pptx.addSlide(); s8.background={fill:C.WHITE};
addTitle(s8,'Opening Line & Ask','Walk in with this');
s8.addText('Opening Line',{x:0.5,y:1.5,w:12,h:0.3,fontSize:16,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
s8.addShape(pptx.ShapeType.rect,{x:0.5,y:1.9,w:12.3,h:1.2,fill:{color:C.LIGHT_BG},line:{color:C.NAVY_DEEP,width:2},rectRadius:0.1});
s8.addText('"Your Software-Defined Factory can switch between 10 models on a single line. That\'s a manufacturing breakthrough — but it also creates 10x the quality failure modes. We\'ve built the AI layer that keeps quality at J.D. Power #1 while you scale SDF globally."',
  {x:0.7,y:2.0,w:11.9,h:1.0,fontSize:14,italic:true,color:C.CHARCOAL,fontFace:'Calibri',valign:'middle',wrap:true});

s8.addText('The Ask',{x:0.5,y:3.5,w:12,h:0.3,fontSize:16,bold:true,color:C.NAVY_DEEP,fontFace:'Calibri'});
addCard(s8,0.5,3.9,3.8,2.2,'Step 1: Discovery Workshop',
  '2-hour workshop with SDF line team at Ulsan. We bring our manufacturing AI architect with a draft integration map.');
addCard(s8,4.6,3.9,3.8,2.2,'Step 2: 90-Day Pilot',
  'Predictive quality on 3 model variants at Ulsan Plant 5. Hard success metrics agreed upfront. Risk-free.');
addCard(s8,8.7,3.9,3.8,2.2,'Step 3: Saudi Scoping',
  'Pre-deployment AI architecture review for Saudi plant before Q4 2026 launch. Included in plant capex budget.');
addBanner(s8,'Target: Discovery workshop within 3 weeks with Juncheul Jung\'s manufacturing team');

pptx.writeFile({fileName:'hyundai-deal-prep.pptx'})
  .then(()=>console.log('Created: hyundai-deal-prep.pptx'))
  .catch(err=>console.error(err));
