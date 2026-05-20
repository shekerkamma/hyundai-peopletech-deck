# MLOps Pipeline — Architecture Guide

## What is the MLOps Pipeline?

The MLOps Pipeline is the closed-loop model lifecycle that powers all eight AI use cases in Hyundai's plant operations platform. It automates the entire journey from raw plant-floor data through model training, optimization, edge deployment, monitoring, and automatic retraining — ensuring that every AI model deployed across Hyundai's global plants continuously improves without manual intervention. The pipeline runs on AWS SageMaker or Azure ML, with edge deployment via IoT Greengrass / IoT Edge, and uses MLflow as the central experiment tracking and model registry backbone.

---

## Architecture Overview

The pipeline is organized into four stages, flowing left to right with a feedback loop from monitoring back to data collection:

1. **Data Collection** — plant floor sensors, inference logs, human feedback, labeling, dataset versioning
2. **Feature Engineering & Training** — feature store, data validation, GPU training, experiment tracking, model evaluation, model registry
3. **Packaging & Deployment** — model optimization (TensorRT/ONNX), containerization, CI/CD, canary deployment, edge OTA rollout
4. **Monitoring & Feedback** — performance monitoring, drift detection, auto-retrain alerts, governance, business value tracking

The closed loop (stage 4 → stage 1) is the key differentiator: when drift is detected, the pipeline automatically triggers retraining with fresh labeled data — no human-in-the-loop required for routine model refresh.

---

## Component: Data Collection

What it does: Gathers and prepares the raw material for model training from multiple sources across the plant floor.

- **Plant Floor Sensors** — cameras, IoT sensors, RFID scanners, OPC-UA buses, and torque tools generate raw data streams
- **Edge Inference Logs** — every prediction made by edge models is logged with score, confidence, latency, and metadata for downstream analysis
- **Human Feedback** — rework confirmations from quality inspectors, maintenance outcome records, and operator-flagged corrections provide ground truth labels
- **Quality & Defect DB** (PostgreSQL) — historical defect records used for training data enrichment and baseline comparison
- **AVEVA PI Historian** — time-series sensor data and machine parameters for predictive quality and maintenance models
- **Labeling Pipeline** — active learning selects the highest-value samples for human annotation; includes annotation queue and label QA review
- **Dataset Versioning** — DVC or S3-versioned buckets maintain reproducible train/val/test splits with full lineage

---

## Component: Feature Engineering & Training

What it does: Transforms raw data into features, trains models on cloud GPU, evaluates against the current champion, and promotes winners to the model registry.

- **Feature Store** (SageMaker Feature Store / Azure ML Feature Tables) — centralized feature computation with both offline (batch training) and online (real-time inference) serving modes
- **Data Validation** (Great Expectations) — automated schema checks, distribution monitoring, and drift flags that gate training pipeline entry
- **Training Jobs** — GPU-accelerated training on SageMaker (P4d instances) or Azure ML Compute (A100 clusters); includes hyperparameter tuning with Bayesian optimization
- **Experiment Tracking** (MLflow) — logs metrics, parameters, artifacts, and model comparisons across every training run; enables reproducibility
- **Model Evaluation** — A/B comparison against the current production champion; SHAP explainability reports; fairness and bias checks for safety-critical models (PPE detection, SOP compliance)
- **Model Registry** (MLflow Model Registry) — versioned model storage with staging → production promotion workflow; tracks version lineage, tags, and approval status

---

## Component: Packaging & Deployment

What it does: Optimizes trained models for edge hardware, packages them into deployable containers, and safely rolls them out to plant-floor edge devices.

- **Model Optimization** — TensorRT (NVIDIA), ONNX Runtime, and OpenVINO conversions; INT8/FP16 quantization and pruning to meet the <200ms edge latency budget on Jetson/Hailo hardware
- **Container Build** — Docker images bundling the optimized model with its inference runtime; pushed to ECR (AWS) or ACR (Azure) container registries
- **CI/CD Pipeline** (GitHub Actions / CodePipeline) — automated test → build → deploy pipeline with approval gates; includes integration tests against synthetic data and smoke tests against edge hardware profiles
- **Canary / Shadow Deployment** — new model receives 5% of traffic alongside the champion; automated comparison on accuracy, latency, and false positive rate; auto-rollback if the challenger regresses
- **Edge OTA Deployment** (AWS IoT Greengrass / Azure IoT Edge) — rolling update to edge device fleet with zero line downtime; staged rollout by plant → line → station; instant rollback capability
- **Cloud Endpoint** (SageMaker Endpoint / Azure ML Managed) — for batch inference jobs (predictive quality weekly analysis, traceability graph scoring) that don't require edge latency

---

## Component: Monitoring & Feedback

What it does: Watches every deployed model in production, detects when performance degrades, and automatically triggers the retraining loop.

- **Performance Monitor** — tracks accuracy, precision, recall, latency, and throughput per model, per plant, per shift; compares against deployment-time baselines
- **Drift Detection** — monitors data drift (KL divergence on input distributions), concept drift (accuracy decay over time), and feature drift; configurable sensitivity thresholds
- **Alert Engine** — threshold-based triggers that can auto-initiate retraining when drift exceeds limits; integrates with Slack, PagerDuty, and the MLOps dashboard for human notification
- **MLOps Dashboard** — unified model health overview showing training history, deployment status, drift trends, and model version comparisons across all 8 use cases
- **Model Governance** — full audit log of every model change; approval workflows for safety-critical models; lineage tracking from training data to deployed version; compliance reporting for ISO/IATF audits
- **Business Value Tracking** — ROI per model per plant; defects caught, downtime hours saved, safety incidents prevented; weekly value digest sent to plant directors and PeopleTech delivery leads

---

## Key Data Flows

### A typical model update (weekly retraining cycle)

1. **Data accumulation** — Edge inference logs and human feedback (rework confirmations) accumulate over the week in the quality DB and inference log store
2. **Active learning selection** — Labeling pipeline identifies the highest-value unlabeled samples (e.g., low-confidence predictions, edge cases) and queues them for human annotation
3. **Feature engineering** — New labeled data flows into the feature store; data validation checks confirm schema compliance and flags distribution shifts
4. **Training** — SageMaker launches a training job on the versioned dataset; MLflow logs metrics, parameters, and the resulting model artifact
5. **Evaluation** — New model is compared against the production champion on held-out test data; SHAP reports generated for explainability review
6. **Registry promotion** — If the challenger beats the champion on all key metrics, it's promoted to "staging" in the model registry; approval gate for safety-critical models
7. **Optimization & packaging** — Model is optimized for edge (TensorRT quantization), containerized, and pushed to the container registry
8. **CI/CD & canary** — Automated pipeline deploys the new model to 5% of edge devices; monitors for 24 hours; if no regression, full rollout via OTA
9. **Monitoring resumes** — Performance monitor tracks the new model in production; drift detection resets baselines; the cycle continues

### A drift-triggered emergency retrain

1. **Drift detected** — Performance monitor observes accuracy drop >5% on the Ulsan paint inspection model over 48 hours
2. **Alert fired** — Alert engine sends Slack notification to ML lead and auto-triggers a retraining job with the last 7 days of production data
3. **Fast retrain** — Training job runs on the same architecture with fine-tuning (not full training); completes in ~2 hours
4. **Expedited eval** — Challenger compared against the degraded champion; SHAP analysis confirms the drift source (e.g., new paint formulation)
5. **Emergency deploy** — Approved model pushed directly to edge fleet via OTA with a 1-hour canary window
6. **Resolution** — Performance monitor confirms accuracy recovery; incident logged in governance system with root cause

---

## Design Decisions

- **MLflow as the single backbone**: Rather than separate tools for experiment tracking, model registry, and artifact storage, we use MLflow end-to-end. This gives every model a single lineage from training data → experiment → registry → deployment. Reduces integration complexity and audit burden.

- **Edge-optimized packaging as a first-class stage**: Most MLOps pipelines stop at "deploy to cloud endpoint." We add a dedicated optimization stage (TensorRT/ONNX/OpenVINO) because all real-time use cases (visual inspection, safety, SOP) require <200ms on edge GPU. This optimization is automated, not manual.

- **Canary before full rollout**: Every model update goes through shadow/canary deployment before hitting the full edge fleet. This catches regressions that offline evaluation misses (e.g., lighting changes on a specific line, sensor calibration drift). Auto-rollback protects the line.

- **Closed-loop auto-retrain**: The pipeline doesn't wait for humans to notice model degradation. Drift detection triggers retraining automatically, using the most recent production data. This is critical for automotive manufacturing where conditions change with new model year launches, paint formulation changes, and seasonal variations.

- **Governance by default**: Every model change — training, promotion, deployment, rollback — is logged with full audit trail. Safety-critical models (PPE detection, SOP compliance) require human approval gates. This maps directly to IATF 16949 and ISO 9001 audit requirements in automotive manufacturing.
