# Conversation Prep: Hyundai ML Pipeline Use Cases Pitch

**With:** Hyundai E-FOREST Center / SDF leadership
**About:** PeopleTech's 8 AI use cases + MLOps platform for SDF manufacturing
**Your Goal:** Secure a 90-day pilot for predictive quality (UC05) at Ulsan Plant 5 + Atlas readiness scoping at Metaplant America
**Their Likely Goal:** Understand if PeopleTech adds value on top of MakinaRocks, AutoEver, and their NVIDIA investment — or if it's redundant

---

## Before You Start

**Mindset:** This is NOT a cold pitch about AI in manufacturing. Hyundai already has AI partners (MakinaRocks), internal AI teams (AutoEver, ROAI), and massive compute (50K NVIDIA GPUs). You're selling into a sophisticated buyer who will immediately spot generic AI claims.

**The angle:** You know their specific architecture (SDF, E-FOREST, MakinaRocks RPMS), and you're filling a gap they haven't solved yet — **multi-model quality AI + ML lifecycle management across use cases and plants.**

**Critical: What NOT to say:**
- Don't pitch predictive maintenance for robots. MakinaRocks has been doing this for 8 years with Hyundai's own investment. You will instantly lose credibility.
- Don't position against AutoEver. They're internal. You run on top of AutoEver infrastructure.
- Don't claim to replace Omniverse or NVIDIA compute. You complement their stack.
- Don't use the phrase "AI platform" without specifics. They've heard it from Siemens, Rockwell, C3.ai, PTC, and every startup at CES.

---

## The Opening

**Option 1 (Direct — Use with Alpesh Patel):**
"Your SDF can switch between 10 models on one line — that's a manufacturing breakthrough no one else has. But it also means your quality system needs to be 10x smarter. Traditional SPC can't adapt fast enough when the model changes every few hours. We've built an AI quality layer specifically for multi-model flexible lines — and we'd like to prove it on one SDF line at Ulsan."

**Option 2 (Complementary — Use with Eunsook Jin):**
"You've made smart investments — NVIDIA for compute, MakinaRocks for robot health, AutoEver for MES and IoT. Where we see a gap is the ML lifecycle: who manages the models powering visual inspection, quality prediction, and safety monitoring across 15 plants? Who handles drift detection, retraining, and IATF audit trails? That's what we do."

**Option 3 (Forward-Looking — Use with Jongho Shin):**
"Atlas arrives in 2028. Human-robot collaboration is going to require AI safety monitoring — pose estimation, zone detection, SOP compliance — that doesn't exist in your stack today. The smart play is to deploy and tune that AI layer now on human workflows, so it's ready when the robots arrive. We're proposing to start that at Metaplant America."

---

## Key Points to Make

### 1. "We're not competing with MakinaRocks — we're the other 7 use cases."
"MakinaRocks does robot health brilliantly — 90% accuracy, 5-day prediction window, 1,400 robots. That's one use case solved. We cover the other seven: visual inspection, variant confirmation, SOP compliance, predictive quality, safety monitoring, and digital traceability. And we provide the unified MLOps pipeline that manages models across ALL use cases, including integrating MakinaRocks data as an input."

### 2. "SDF creates a quality problem that traditional tools can't solve."
"When you switch between 10 models on one line, quality inspection parameters change with every switch. A weld that's acceptable on Model A might be a defect on Model B. Traditional SPC was designed for single-model lines running thousands of identical units. Our predictive quality AI recalibrates per variant in real-time — it knows which model is on the line and adjusts detection thresholds automatically."

### 3. "Your NVIDIA GPUs train the models. We manage their entire lifecycle."
"50,000 Blackwell GPUs give you incredible training capacity. But training a model is 10% of the work. The other 90% is: optimizing it for edge hardware, deploying it safely with canary rollouts, monitoring for drift when a new paint formulation changes the input distribution, auto-retraining when accuracy drops, and maintaining a full audit trail for IATF 16949. That's the MLOps pipeline."

### 4. "Atlas readiness = AI readiness. Start now."
"You're planning to deploy 25,000 Atlas robots across your plants by 2030. Every one of those deployments will require AI-driven safety monitoring — zone detection, PPE compliance, human-robot proximity alerts. ISO 10218 and ISO/TS 15066 require it. If you start training that AI layer today on human workflows, you'll have 2 years of production data to ensure safety compliance from day one of Atlas deployment."

### 5. "We run on your infrastructure — not beside it."
"We integrate via OPC-UA from your PLCs, REST APIs to Omniverse for twin data, MQTT for real-time streaming. We deploy on your NVIDIA infrastructure or in containers on AutoEver's IoT Platform. We feed our predictions back into AutoEver MES for quality gate decisions. Zero rip-and-replace."

---

## Use Case Deep Dives (If They Ask)

### UC05: Predictive Quality (Lead Use Case)
**Problem they have:** SDF 10-model switching creates exponential quality failure modes. Current SPC can't adapt in real-time.
**What we do:** ML model per production station that recalibrates quality thresholds per model variant. Trained on historical defect data + real-time sensor streams. Predicts quality deviations before they become defects.
**Edge deployment:** <200ms inference on Jetson/Hailo at each station. Models optimized with TensorRT.
**MLOps angle:** Weekly auto-retrain cycle. Drift detection when new model variant is introduced. Closed-loop with MES quality gates.

### UC04: SOP Compliance
**Problem they have:** Human workers follow standard operating procedures manually. With Atlas co-working in 2028, SOP compliance becomes safety-critical.
**What we do:** Computer vision (pose estimation + action sequence matching) verifies workers follow SOP steps in order. Alerts for skipped steps, wrong sequence, or unsafe posture.
**Atlas angle:** Same AI layer monitors human-robot handoff zones. Detects when a human enters a robot work envelope. Compliant with ISO 10218 / ISO/TS 15066.

### UC07: Safety Monitoring
**Problem they have:** Spot robots patrol but don't do real-time AI safety analysis. Atlas deployment requires continuous safety monitoring.
**What we do:** Camera-based zone detection, PPE compliance verification, human-robot proximity tracking. Real-time alerts to EHS system.
**Regulatory angle:** OSHA, ISO 10218, ISO/TS 15066. One safety incident during Atlas deployment = $10M+ liability + production halt + regulatory scrutiny.

### UC01: Visual Inspection
**Problem they have:** Spot does QC patrols. HMGICS has some AI vision. But multi-model visual inspection across SDF lines at scale is unsolved.
**What we do:** CNN-based defect classification per model variant. Camera array at inspection stations. Adapts to each model's specific defect patterns.
**Differentiation:** We don't replace Spot — we complement it. Spot patrols and flags areas. Our station-level inspection catches defects in-line before the vehicle reaches Spot.

### UC08: Digital Traceability
**Problem they have:** Recent 7,698-unit recall (Creta/Verna). MES tracks high-level production data but lacks part-level genealogy.
**What we do:** End-to-end part tracking from supplier through assembly to finished vehicle. Part genealogy graph enables surgical recall (affected VINs only, not entire production runs).
**ROI:** A recall of 7,698 units at ~$500/unit = $3.8M. Surgical recall on 500 affected units = $250K. Traceability saves $3.5M per incident.

---

## Likely Pushback & How to Respond

### "We already have MakinaRocks for AI in manufacturing."
**Response:** "Yes — and they're excellent at robot health. What they don't cover is production quality AI for SDF lines, visual inspection across model variants, SOP compliance for human-robot collaboration, or the unified MLOps platform that manages models across all these use cases. We're complementary. In fact, we'd want to integrate MakinaRocks RPMS data as an input to our cross-plant monitoring dashboard."

### "AutoEver can build this internally."
**Response:** "AutoEver is strong on infrastructure — MES, IoT Platform, Factory BI. Building production-grade ML models for 8 different manufacturing use cases is a different discipline. It requires 15 years of domain expertise in computer vision for defect detection, pose estimation for SOP compliance, and anomaly detection for quality prediction. AutoEver should own the infrastructure layer. We provide the AI application layer on top."

### "We have 50,000 GPUs — we can train our own models."
**Response:** "Absolutely — and we'd use those GPUs for training. The hard part isn't compute. It's knowing what to train, how to validate it against automotive quality standards, how to optimize it for edge inference in <200ms, how to detect when it's drifting, and how to retrain automatically without disrupting the line. That's the MLOps pipeline. You don't build MLflow expertise — you buy it and focus your GPU budget on the models that matter."

### "What about ROAI and XELO?"
**Response:** "XELO is brilliant for robotic process design and path optimization — 3 months to 1 week for process design, 15% productivity gain. Totally different domain from ours. They optimize how robots move. We optimize what robots — and humans — produce in terms of quality, safety, and compliance. No overlap."

### "We need to see this at another automaker first."
**Response:** "Fair enough. What we can offer is a 90-day proof of value at Ulsan Plant 5 with hard success metrics agreed upfront. If we don't hit the targets, you walk away with the data and learnings for free. The risk is $500K for 90 days — the risk of NOT deploying quality AI before scaling SDF to 15 plants is measured in J.D. Power rankings and warranty costs."

### "The budget for 2026 is already committed."
**Response:** "The Ulsan pilot is under $1M — within discretionary range for E-FOREST Center. And the Atlas readiness work at Metaplant America could be structured under the robotics capex budget rather than the AI line item. We're flexible on how this gets classified."

---

## Non-Negotiables

- **Must have:** Technical discovery session with E-FOREST Center engineers (not just procurement)
- **Must have:** Access to SDF line data for at least one model switch cycle
- **Ideal outcome:** 90-day pilot at Ulsan Plant 5 (UC05) + Atlas readiness scoping at Metaplant America (UC04/UC07)
- **Walk-away point:** If they only want a generic RFP process running through AutoEver procurement with 12+ month timelines — offer a technical white paper and revisit when Atlas deployment pressure increases (mid-2027)

---

## How to Close

**If it goes well:**
"Let's schedule a half-day technical workshop at E-FOREST Center with Alpesh-san's SDF team. We'll bring our manufacturing AI architect, walk through the SDF data flows together, and design the Ulsan pilot scope. What does the calendar look like in the next 3 weeks?"

**If it's unresolved:**
"I'll send over two things: (1) a technical integration brief showing exactly how our MLOps pipeline works on top of AutoEver IoT and NVIDIA compute, and (2) the UC05 predictive quality specification tailored to your SDF 10-model configuration. Can we reconnect in two weeks?"

**If it goes badly:**
"I understand the timing may not be right. Here's what I'd suggest: when Atlas deployment prep begins in earnest — probably mid-2027 — the need for AI safety monitoring becomes urgent. We'll keep our Atlas readiness architecture current and share it when the time is right."

---

## Contract Review

**Status:** No contract or terms document provided for this session. When Hyundai shares procurement terms, MSA, or NDA — run `/contract-reviewer` to flag risks and generate negotiation scripts before signing.

---

## One-Page Cheat Sheet

### 3 Key Facts About Hyundai
1. **SDF = 10 models on one line** — manufacturing breakthrough, but creates 10x quality complexity
2. **MakinaRocks owns robot predictive maintenance** (1,400 robots, 8-year relationship, equity investment) — don't compete here
3. **Atlas robots arrive 2028** — 25,000 planned across plants — AI safety monitoring gap is real

### Your Positioning Angle
"PeopleTech is the AI application layer that sits between Hyundai's infrastructure (NVIDIA, AutoEver, Omniverse) and production outcomes. We deploy, monitor, and continuously improve ML models across 8 manufacturing use cases — the gap nobody else fills."

### Top 3 Objections with Responses
1. **"MakinaRocks already does this"** → "They do robot health. We do the other 7 use cases + the unified MLOps platform."
2. **"AutoEver can build internally"** → "Infrastructure ≠ AI applications. 15 years of manufacturing domain expertise in 8 use cases."
3. **"Budget is committed"** → "Pilot is <$1M, fits E-FOREST discretionary. Atlas readiness fits robotics capex."

### Your Opening Line
"Your SDF can switch between 10 models on one line. That's a manufacturing breakthrough. But it also means your quality AI needs to be 10x smarter than traditional SPC. We've built exactly that."

---

*Want to practice? I'll play Alpesh Patel (EVP, SDF) and push back with technical questions about how PeopleTech integrates with E-FOREST and AutoEver. Just say "role-play."*
