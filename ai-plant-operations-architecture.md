# AI Plant Operations Platform — Architecture Guide

## What is the AI Plant Operations Platform?

The AI Plant Operations Platform is Hyundai's end-to-end architecture for deploying AI across automotive manufacturing plants. Built jointly by Hyundai and PeopleTech, the platform connects plant-floor sensors, cameras, and scanners through edge compute and event streaming to cloud AI models, enterprise systems (SAP MES/ERP, SAP PM), and operator-facing dashboards. It supports eight AI use cases — from visual inspection and predictive maintenance to safety monitoring and digital traceability — all running on a shared infrastructure with sub-200ms line-side latency. The architecture is designed to pilot on one line and scale across Hyundai's global plant network (Ulsan, Asan, HMGMA, HMMA, HMMC, HMI).

---

## Architecture Overview

The platform is organized into four layers, flowing left to right:

1. **Plant Floor / Edge Capture** — sensors, cameras, RFID, edge compute
2. **Streaming & Integration** — event bus, enterprise connectors, databases
3. **AI / ML Compute (Cloud)** — model training, 8 use case models, MLOps
4. **Application & UX** — dashboards, operator UIs, alerts, reporting

A closed-loop MLOps pipeline connects cloud-trained models back to edge devices via OTA updates.

---

## Component: Plant Floor / Edge Capture

What it does: Captures raw data from the production line and runs first-pass inference at the edge for sub-200ms latency.

- **Vision Cameras** (Cognex, Basler, Keyence) — high-resolution multi-angle capture for defect detection, variant verification, seating validation
- **IoT Sensors** — vibration accelerometers, acoustic emission sensors, thermal cameras, pressure and temperature probes for predictive maintenance and quality
- **RFID & Barcode Scanners** (UHF RFID, Datalogic, DataMan) — component tracking, VIN scanning, genealogy data capture
- **Safety / SOP Cameras** — wide-FOV IP cameras with on-device privacy blurring for SOP compliance and safety zone monitoring
- **Smart Torque Tools** — IIoT-connected torque wrenches providing fastening verification telemetry
- **Edge Compute** (NVIDIA Jetson, Hailo, Intel) — runs inference models locally; managed by AWS IoT Greengrass or Azure IoT Edge; latency budget <200ms
- **OPC-UA Bus** — industrial protocol layer carrying machine signals and PLC data
- **Edge Gateway** — aggregates sensor data, protocol translation, local cache for connectivity resilience

---

## Component: Streaming & Integration

What it does: Moves data between edge, cloud, and enterprise systems in real time. This layer ensures no rip-and-replace — AI plugs into Hyundai's existing SAP and historian landscape.

- **Kafka / Event Stream** — real-time event bus carrying quality, maintenance, and safety events with standardized schemas
- **MES / SAP Connector Library** — PeopleTech accelerator with pre-built connectors for line-hold triggers, work-order generation, and quality event publishing
- **SAP MES / ERP** — production orders, bill of materials, quality records (Hyundai enterprise system)
- **SAP PM / CMMS (Maximo)** — maintenance work orders, asset registry, scheduling (auto-generated from predictive maintenance)
- **AVEVA PI / Aspen IP21 Historian** — time-series storage for sensor data, used by predictive quality and maintenance models
- **Quality & Defect DB** (PostgreSQL) — defect records, rework tracking, defect-to-station traceability
- **Neo4j Genealogy Graph** — component-to-vehicle traceability, recall scope calculation, supplier quality chain
- **EHS Compliance System** — incident management, audit trail, safety event records

---

## Component: AI / ML Compute (Cloud)

What it does: Trains, serves, and manages AI models across all eight use cases. Runs on AWS SageMaker or Azure ML with a unified MLOps pipeline.

### Use Case Models

| Use Case | Models | Purpose |
|----------|--------|---------|
| UC-01 Visual Inspection | ResNet50, EfficientNet, PatchCore | CNN anomaly scoring against quality standards |
| UC-02 Variant Confirmation | YOLOv8, PaddleOCR | Object detection + OCR for BOM-match verification |
| UC-03 Seating Validation | YOLOv8 + keypoint head | Pose-based fitment classification |
| UC-04 SOP Compliance | MoveNet, SlowFast | Pose estimation + action recognition vs. SOP graph |
| UC-05 Predictive Quality | XGBoost, LSTM, SHAP | Sensor fusion defect prediction with explainability |
| UC-06 Predictive Maintenance | Autoencoder, DeepSurv, Audio CNN | Multi-sensor anomaly detection + survival analysis |
| UC-07 Safety Monitoring | YOLOv8 (PPE heads) | PPE detection, zone-violation, proximity tracking |
| UC-08 Traceability | Genealogy graph, Flink, Supplier risk ML | Stream processing + graph-based tracking |

### MLOps Pipeline

- **MLflow** — experiment tracking, model registry, versioning
- **CI/CD** — automated training → validation → deployment pipelines
- **Drift detection** — monitors model performance decay, triggers auto-retraining
- **Model optimization** — TensorRT, ONNX, OpenVINO compression for edge deployment
- **OTA updates** — pushes retrained models to edge fleet without line downtime

### Data Lake / Feature Store

- S3 / Azure Data Lake Storage with Parquet / Delta Lake format
- Stores training datasets, inference logs, and feature store tables
- Feeds both batch retraining and real-time feature serving

### IoT Platform

- AWS IoT / Azure IoT Hub for device management, telemetry ingestion, and rules engine
- Manages edge device fleet across all plants

---

## Component: Application & UX Layer

What it does: Presents AI outputs to the right person at the right time — from line operators to plant directors.

- **Quality Dashboard** — real-time defect monitoring with drill-down by station, shift, and operator
- **Operator Station UI** — pass/fail visual cues, hold-station controls, mismatch alerts at the assembly station
- **Asset Health Dashboard** — risk-prioritized maintenance work queue, failure-cause analytics, asset lifespan tracking
- **EHS Live Wall** — PPE compliance monitoring, zone violation alerts, auto-generated incident reports with video clips
- **SOP Compliance Scorecard** — live deviation feed, operator coaching overlay, per-shift compliance scoring
- **Vehicle Genealogy Viewer** — root-cause drill-down, recall scope calculator, auditor export portal
- **Mobile Technician App** — push-notification work orders, photo capture, maintenance confirmation in the field
- **Alerting & Notifications** — Slack, Teams, SMS, Andon integration with severity-based escalation rules
- **Executive BI / ROI Reporting** — Power BI / Tableau dashboards, weekly value digest, ROI tracking against pilot baselines

---

## Key Data Flows

### A typical defect detection (UC-01 Visual Inspection)

1. **Capture** — High-res cameras photograph vehicle surface as it passes through the LED light tunnel
2. **Edge inference** — Jetson runs CNN anomaly model, scores defect probability in <2 seconds
3. **Event publish** — Edge publishes scored event to Kafka with image, score, station ID, and timestamp
4. **MES integration** — If score exceeds threshold, MES connector triggers automatic line-hold via SAP MES API
5. **Quality DB write** — Defect record persisted to PostgreSQL with full traceability metadata
6. **Dashboard update** — Quality dashboard updates in real time; operator station UI shows pass/fail
7. **Retraining loop** — Rework-confirmed defects feed back to SageMaker for weekly model retraining
8. **OTA deploy** — Retrained model optimized (TensorRT) and pushed to edge fleet via IoT Greengrass OTA

### A typical failure prediction (UC-06 Predictive Maintenance)

1. **Sensor capture** — Vibration, acoustic, and thermal sensors continuously stream data from stamping press
2. **Edge aggregation** — Edge gateway aggregates multi-sensor readings, applies windowed features
3. **Anomaly detection** — Autoencoder flags deviation from normal operating envelope; survival model estimates remaining useful life
4. **Work order generation** — If RUL drops below threshold, SAP PM work order is auto-generated with recommended action
5. **Technician notification** — Mobile app pushes work order; asset health dashboard updates risk queue
6. **Validation** — Maintenance team confirms predicted failure during planned downtime window
7. **Model feedback** — Confirmed/missed predictions feed back into model retraining for improved accuracy

---

## Design Decisions

- **Edge-first inference with cloud retraining**: Real-time use cases (visual inspection, safety, SOP) require <200ms latency, so inference runs on edge GPU. Cloud handles training, retraining, and batch analytics. This hybrid approach balances latency with model improvement velocity.

- **Integration-first, no rip-and-replace**: The platform connects to Hyundai's existing SAP MES/ERP, SAP PM, and AVEVA PI historian rather than replacing them. Pre-built connector library reduces integration risk and ensures AI outputs flow into the systems operators already trust.

- **Shared infrastructure across all 8 use cases**: One edge compute fleet, one event bus, one MLOps pipeline, one data lake — rather than 8 siloed stacks. This amortizes infrastructure cost and enables cross-use-case data fusion (e.g., combining sensor data from UC-05 Predictive Quality with UC-06 Predictive Maintenance).

- **Pilot-first architecture**: Designed to run on a single line with 3–5 edge nodes and scale to plant-wide (50+ nodes) without re-architecture. The modular component design means adding a new use case is a model deployment, not an infrastructure project.
