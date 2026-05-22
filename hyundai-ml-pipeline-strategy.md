# AI Strategy Brief: Hyundai Motor Group x PeopleTech — ML Pipeline Use Cases

**One-page executive brief for positioning 8 AI use cases + MLOps platform**

---

## The Opportunity

Hyundai Motor Group has invested in AI infrastructure (50,000 NVIDIA Blackwell GPUs), digital twins (Omniverse), robotics (Boston Dynamics Atlas), and internal IT (AutoEver MES/IoT). They have strategic partners for specific point solutions (MakinaRocks for robot health).

**What they don't have:** A unified AI application layer that deploys, monitors, and continuously improves ML models across multiple production use cases, across multiple plants, with automotive-grade governance.

**PeopleTech fills the gap between individual AI experiments and enterprise-scale AI operations.**

---

## Strategic Positioning: The MLOps Platform Play

### What Already Exists at Hyundai

| Layer | Who Owns It | Status |
|-------|------------|--------|
| **Compute** | NVIDIA (50K Blackwell GPUs) | Building now — operational 2027-2029 |
| **Digital Twin** | NVIDIA Omniverse + AutoEver | Deployed at HMGICS, expanding |
| **MES / IoT** | Hyundai AutoEver | Mature, deployed globally |
| **Robot Health AI** | MakinaRocks | 1,400 robots by end 2026 |
| **Robot Process Optimization** | ROAI (XELO platform) | Genesis line, HMGICS |
| **ML Model Lifecycle** | **Nobody** | Gap |
| **Production Quality AI** | **Nobody** | Gap |
| **Safety/SOP AI** | **Nobody** | Gap |
| **Cross-Plant AI Governance** | **Nobody** | Gap |

### Where PeopleTech Sits

```
  NVIDIA Compute (GPUs)     Omniverse (Twin)     AutoEver (MES/IoT)
         |                       |                       |
         +-----------------------------------------------+
                                 |
                    +---------------------------+
                    |   PeopleTech AI Layer     |
                    |                           |
                    |  MLOps Pipeline:           |
                    |  - Model training          |
                    |  - Edge deployment         |
                    |  - Drift monitoring        |
                    |  - Auto-retrain            |
                    |  - Governance/audit        |
                    |                           |
                    |  8 AI Use Cases:           |
                    |  - Quality prediction      |
                    |  - Visual inspection       |
                    |  - SOP compliance          |
                    |  - Safety monitoring       |
                    |  - Variant confirmation    |
                    |  - Digital traceability    |
                    +---------------------------+
                                 |
                    Production Decisions & Outcomes
```

---

## The Use Case Portfolio: Phased Deployment

### Phase 1: Quick Win — 90 Days (UC05 Predictive Quality)

**The pitch:** "Your SDF can switch between 10 models on one line. Traditional SPC breaks when the model changes every few hours. Our AI adapts quality prediction per variant in real-time."

- Deploy at **Ulsan Plant 5** (already top J.D. Power quality — they'll want to defend the position)
- 3 model variants on one SDF line
- Success metrics: defect detection rate, false positive rate, time-to-detection
- **ROI:** 1% defect reduction = ~$13M/year in reduced warranty costs
- **Budget:** $500K-$1M pilot

### Phase 2: Atlas Readiness — 6 Months (UC04 + UC07)

**The pitch:** "Atlas robots arrive in 2028. The AI safety layer needs to be deployed and tuned BEFORE the robots, not after. Deploy now, train on current human workflows, and be ready when Atlas joins the line."

- **UC04 (SOP Compliance):** Pose estimation + action sequence monitoring for human workers NOW, extends to human-robot collaboration zones in 2028
- **UC07 (Safety Monitoring):** Zone detection + PPE compliance + human-robot proximity alerts
- Deploy at **Metaplant America** (greenfield, Atlas deployment site, clean integration)
- **ROI:** Regulatory compliance for human-robot collaboration (OSHA, ISO 10218, ISO/TS 15066). One safety incident = $10M+ liability + production halt.
- **Budget:** $1-2M for both use cases

### Phase 3: Platform Scale — 12 Months (UC01 + UC02 + UC08 + MLOps)

**The pitch:** "You've validated AI-driven quality and safety at two sites. Now scale to 15+ plants with a unified MLOps platform that manages every model across every use case."

- **UC01 (Visual Inspection):** CNN-based defect classification adapted per model variant, complementing Spot robot QC patrols
- **UC02 (Variant Confirmation):** Real-time BOM validation during SDF model switches
- **UC08 (Digital Traceability):** End-to-end part genealogy for recall reduction (recent 7,698-unit recall proves the need)
- **MLOps Pipeline:** Centralized model registry, edge deployment automation, drift detection, auto-retrain, compliance audit trail
- **ROI:** Cross-plant AI consistency + IATF 16949 automated compliance + 30-50% reduction in model deployment time
- **Budget:** $5-15M/year platform license

---

## Competitive Differentiation

| Dimension | MakinaRocks | Hyundai AutoEver | Siemens MindSphere | PeopleTech |
|-----------|-------------|-----------------|-------------------|------------|
| **Scope** | Robot health only | Infrastructure (MES, IoT) | Full stack, horizontal | 8 production AI use cases |
| **ML Lifecycle** | Single model | None | Basic | Full MLOps (train → deploy → monitor → retrain) |
| **Multi-Model SDF** | N/A | N/A | Generic | Built for multi-variant quality |
| **Edge Optimization** | Unknown | No | Cloud-first | TensorRT/ONNX, <200ms on Jetson |
| **Governance** | Per-robot | Per-system | Per-platform | Per-model, IATF-mapped |
| **Cross-Plant Scale** | Expanding (4 sites) | Global MES | Global | Designed for 15+ plant fleet |

**PeopleTech's wedge:** Only vendor purpose-built for multi-model flexible manufacturing (SDF) with a full ML lifecycle across multiple production AI use cases. MakinaRocks does one thing well (robot health). AutoEver does infrastructure. Siemens is horizontal. PeopleTech is the vertical AI application layer.

---

## Three Meetings Worth Requesting

### Meeting 1: Alpesh Patel (EVP, SDF)
**Agenda:** "How PeopleTech's predictive quality AI integrates with your SDF architecture to solve the multi-model quality challenge."
**Goal:** Technical validation + discovery of SDF data flows

### Meeting 2: Jongho Shin (MD, Manufacturing Solutions / E-FOREST)
**Agenda:** "AI safety monitoring for human-robot collaboration — getting the AI layer ready before Atlas deployment."
**Goal:** Align PeopleTech UC04/UC07 with Atlas readiness roadmap

### Meeting 3: Eunsook Jin (President, ICT/Digital)
**Agenda:** "Unified MLOps platform running on your NVIDIA infrastructure and AutoEver IoT — no rip-and-replace."
**Goal:** Budget holder buy-in + AutoEver integration commitment

---

## Key Numbers for the Pitch

| Metric | Value | Source |
|--------|-------|--------|
| HMG annual revenue | $132B | Public filings |
| Warranty cost estimate (1% of revenue) | $1.3B/year | Industry benchmark |
| Value of 1% defect reduction | ~$13M/year | Derived |
| MakinaRocks robot coverage | 1,400 by end 2026 | MakinaRocks press release, Apr 2026 |
| Atlas robots planned | 25,000+ across HMG plants | CES 2026 announcement |
| NVIDIA GPUs committed | 50,000 Blackwell | Oct 2025 announcement |
| SDF model variants per line | Up to 10 | HMG SDF specification |
| Global plants | 16 production facilities | HMG corporate |
| Recent recall size | 7,698 units (Creta/Verna) | Previous briefing |
| Saudi plant launch | Q4 2026, 50K unit capacity | Public announcement |

---

## Ask

1. **Phase 1 pilot agreement** — Predictive quality on one SDF line at Ulsan Plant 5, 90-day proof of value
2. **Atlas readiness scoping session** — Map UC04/UC07 requirements for Metaplant America before 2028
3. **MLOps architecture review** — Joint workshop with AutoEver and PeopleTech to define integration points
