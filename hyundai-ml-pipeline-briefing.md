# Account Briefing: Hyundai Motor Group — ML Pipeline Use Cases

**Prepared for:** PeopleTech pre-sales team
**Date:** 2026-05-22
**Focus:** 8 AI/ML use cases + MLOps pipeline positioning
**Previous briefing:** See `hyundai-account-briefing.md` for general account context

---

## What's Changed Since Last Briefing

### 1. MakinaRocks Partnership (CRITICAL — Competitive Intelligence)
- **Strategic partner since 2018** via ZER01NE open innovation platform
- Hyundai made an **equity investment** in MakinaRocks
- Deployed **Robot Prognostics and Maintenance System (RPMS)** at Asan plant
- Expanding to **Ulsan, India, Jeonju, EV plants** (Ulsan EV, Kia Hwaseong EV)
- **1,400 robots** covered by end of 2026
- Predicts equipment failures **5 days in advance** with **90%+ accuracy**
- Diagnoses actuator condition, setup anomalies, real-time status alerts
- **Impact on PeopleTech:** They already have a partner for UC06 (predictive maintenance on robots). We must NOT pitch robot predictive maintenance as our wedge — position around it or above it.

### 2. Hyundai AutoEver — In-House IT Capabilities
Hyundai's IT subsidiary already provides:
- **MES** — real-time production management, integrated with SDF
- **Factory BI** — data visualization and operational insights
- **Virtual Factory Platform** — cloud-native digital twin solution
- **CMS/PHM** — AI-based edge computing for equipment anomaly prediction (overlaps UC06)
- **IoT Platform** — data collection from industrial equipment
- **SD Brain** — AI agent platform for autonomous factory decision-making
- **Impact on PeopleTech:** AutoEver covers infrastructure. PeopleTech must position at the **AI application layer above their infrastructure**, not as a replacement.

### 3. E-FOREST Center — The Org to Sell Into
- **E-FOREST** is Hyundai's smart factory brand (not just a marketing term — it's an organizational unit)
- Manufacturing Solution Division was restructured under E-FOREST Center (May 2026)
- New team: **Robot Manufacturing Solution Strategy Team**
- Key people at E-FOREST Center:
  - **Alpesh Patel** — EVP, Software Defined Factory division (presented at GTC 2026)
  - **Jongho Shin** — Managing Director, Manufacturing Solution Division at E-FOREST Center
  - **Bansuk Kim** — Managing Director, Electrification Production Technology Center

### 4. Dark Factory Strategy (GTC 2026)
- Goal: fully unmanned factories where AI and robotics lead production
- Digital twin pre-validation of all robotic processes
- **ROAI / XELO platform** — spinoff from HMG Manufacturing Solution HQ
  - Automates robot placement and path design
  - Reduces process design from 3 months → 1 week
  - 15% productivity improvement
  - Deployed at Genesis line, HMGICS Singapore

### 5. Metaplant America (Georgia)
- First US-based EV mass-production plant
- **Spot robots** already doing quality-control inspections on finished vehicles
- Atlas humanoid deployment planned for 2028 (parts sequencing first, assembly by 2030)
- Every single vehicle goes through human-driven test drive (95% pass rate)
- Building Ioniq 9, Kia model joining later

### 6. HMGICS Singapore Tech Stack (from Exa)
PyTorch, TensorFlow, OpenCV, CUDA, Apache Kafka, Kubernetes, Docker, PostgreSQL, Oracle, Tableau, Git, GitLab, Helm, Terraform, Ansible, Red Hat, Spring Boot, React, Angular, SCADA, Siemens, Harness, Playwright, OWASP

---

## The 8 Use Cases — Where PeopleTech Fits vs. What's Already Covered

| UC | Name | Hyundai's Current State | PeopleTech Opportunity |
|----|------|------------------------|----------------------|
| **01** | Visual Inspection | Spot robots doing QC; HMGICS has AI vision. **Partially covered.** | **HIGH** — Multi-model SDF lines need variant-aware defect classification. Their current vision is single-model. |
| **02** | Variant Confirmation | SDF enables 10-model switching. BOM validation is MES-level. | **HIGH** — Real-time model matching at station level during rapid changeover is unsolved at scale. |
| **03** | Seating Validation | Traditional torque/force verification in place. | **MEDIUM** — AI-enhanced validation adds predictive catch for borderline cases. Incremental improvement. |
| **04** | SOP Compliance | No evidence of pose estimation AI deployed. | **HIGH** — Human-robot collaboration safety is top priority (Atlas deployment). AI-driven SOP monitoring fills a gap. |
| **05** | Predictive Quality | SPC exists. AI-driven quality prediction not deployed at scale. | **HIGHEST** — Multi-model SDF lines create exponential quality failure modes. This is the #1 wedge. |
| **06** | Predictive Maintenance | **MakinaRocks RPMS on 1,400 robots. Hyundai AutoEver CMS/PHM.** | **LOW** — Already covered by strategic partner + in-house. Do NOT lead with this. |
| **07** | Safety Monitoring | Spot robots can patrol. No evidence of AI-driven zone/PPE detection. | **HIGH** — Atlas deployment in 2028 requires human-robot safety monitoring AI. Regulatory requirement. |
| **08** | Digital Traceability | MES handles basic tracking. No evidence of end-to-end part genealogy. | **HIGH** — Recent Creta/Verna recall (7,698 units). Supply chain traceability is a pain point. |

### Positioning Summary

**Lead with:** UC05 (Predictive Quality) — the only use case that directly addresses their #1 strategic challenge (maintaining quality while scaling SDF to 15+ plants with 10-model flexibility).

**Strong second:** UC04 (SOP Compliance) + UC07 (Safety Monitoring) — positioned as enablers for Atlas robot deployment. Human-robot collaboration safety is a board-level concern.

**Support with:** UC01 (Visual Inspection) + UC02 (Variant Confirmation) + UC08 (Traceability) — demonstrate platform breadth.

**Avoid leading with:** UC06 (Predictive Maintenance) — MakinaRocks owns this. Mention only as "we integrate with your existing predictive maintenance data" to show we're complementary, not competitive.

**Avoid entirely:** UC03 (Seating Validation) — too narrow, incremental value, not strategic.

---

## MLOps Pipeline — The Platform Play

The 8 use cases are the entry points, but the **MLOps pipeline is the platform sale**. Position it as:

> "You have MakinaRocks for robot health, AutoEver for MES and IoT, NVIDIA for compute. What you don't have is a **unified ML lifecycle** that manages the models powering ALL your use cases — training, deployment, monitoring, retraining — across ALL your plants."

### MLOps Components Mapped to Hyundai's Stack

| MLOps Component | Hyundai Has | PeopleTech Adds |
|-----------------|-------------|-----------------|
| Data Collection | AVEVA PI, IoT Platform, Edge sensors | Unified data pipeline across use cases + labeling automation |
| Feature Engineering | Nothing cross-use-case | Centralized feature store serving all 8 use cases |
| Model Training | NVIDIA Blackwell GPUs (50,000!) | MLflow-based experiment tracking + registry across use cases |
| Model Optimization | Unknown | TensorRT/ONNX edge optimization for <200ms on Jetson/Hailo |
| Deployment | IoT Greengrass/Edge (exists) | Canary deployment + auto-rollback across plant fleet |
| Monitoring | AutoEver CMS/PHM (equipment only) | Cross-model drift detection + auto-retrain for AI models |
| Governance | IATF 16949 compliance manual | Automated audit trail mapping to ISO/IATF requirements |

### Key Argument
MakinaRocks solves ONE use case (robot health). AutoEver solves infrastructure. PeopleTech provides the **AI model lifecycle platform** that scales from 1 use case to 8, from 1 plant to 15+, with closed-loop retraining and governance baked in.

---

## Key People (Updated for ML Pipeline Pitch)

| Name | Title | Why They Matter for This Pitch |
|------|-------|-------------------------------|
| **Alpesh Patel** | EVP, Software Defined Factory | Decision maker for SDF AI integration. Presented at GTC 2026 on AI + digital twins. Understands the gap between infrastructure and AI outcomes. |
| **Jongho Shin** | MD, Manufacturing Solution Division (E-FOREST) | Owns factory automation strategy. Just restructured org to put robotics at center. Needs AI layer for the robots. |
| **Bansuk Kim** | MD, Electrification Production Technology | Owns EV manufacturing. Metaplant and EV-specific quality challenges. |
| **Juncheul Jung** | President, Head of Manufacturing | Top-level sponsor. Promoted Jan 2026. Will want to show AI ROI in first year. |
| **Eunsook Jin** | President, Head of ICT/Digital | Budget holder. Her team manages NVIDIA relationship and AutoEver. Key gatekeeper. |

---

## Risks & Landmines

1. **MakinaRocks relationship is deep** — 8 years, equity investment, ZER01NE incubation. Don't position against them. Position as complementary: "MakinaRocks for robot health, PeopleTech for production quality AI."

2. **Hyundai AutoEver is the internal IT arm** — they will resist external AI platforms that threaten their mandate. Frame PeopleTech as running ON TOP of AutoEver infrastructure (MES, IoT Platform), not replacing it.

3. **ROAI/XELO exists for robotic process optimization** — another internal spinoff. Avoid overlapping with their robot path optimization. Our lane is production quality and safety AI.

4. **"Build vs. buy" pressure** — with 50,000 GPUs and a Physical AI Application Center, they may believe they can build everything. Counter: "The compute is the easy part. Manufacturing domain expertise across 8 use cases is 15 years of engineering. That's what you're buying."

5. **Atlas deployment timeline** — robots arrive 2028. If we sell SOP/safety AI now, we're selling into a need that materializes in 2 years. Frame it as "deploy and tune the AI before the robots arrive, not after."
