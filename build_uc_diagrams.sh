#!/usr/bin/env bash
# Build architecture diagrams for all 8 Hyundai AI Plant Operations use cases
set -e
CLI="cli-anything-drawio"
DIR="/home/shekerk/projects/hyundai-peopletech-deck"

NAVY="#1F3B6E"
NAVY_CARD="#0D3B5E"
TEAL="#14A085"
ORANGE="#D97706"
PURPLE="#7C3AED"
RED="#DC2626"
TEAL2="#0E7B6A"
WHITE="#FFFFFF"
BORDER="#D0D5DD"

# Helper: all commands use --project flag for statefulness
D() { $CLI --project "$F" "$@"; }

# ============================================================================
# UC-01: AI-based Visual Inspection
# ============================================================================
echo "=== UC-01: AI-based Visual Inspection ==="
F="$DIR/uc01-visual-inspection-architecture.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-01: AI-based Visual Inspection" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18
D shape style title fontStyle 1
D shape style title fontColor "$NAVY"

# Edge
D shape add rounded -l "High-Res Cameras (Cognex/Basler) + LED Light Tunnel" --x 50 --y 60 -w 140 -h 65 --id cam
D shape style cam fillColor "$WHITE"
D shape style cam strokeColor "$BORDER"

D shape add rounded -l "Edge GPU (Jetson) TensorRT CNN <2s" --x 50 --y 150 -w 140 -h 65 --id edge
D shape style edge fillColor "$NAVY"
D shape style edge fontColor "$WHITE"

# AI
D shape add rounded -l "CNN Anomaly (ResNet50, EfficientNet)" --x 240 --y 60 -w 150 -h 60 --id cnn
D shape style cnn fillColor "$WHITE"
D shape style cnn strokeColor "$TEAL"
D shape style cnn strokeWidth 2

D shape add rounded -l "SageMaker Training Pipeline" --x 240 --y 145 -w 150 -h 55 --id sage
D shape style sage fillColor "$NAVY"
D shape style sage fontColor "$WHITE"

D shape add rounded -l "MLOps + OTA Deploy" --x 240 --y 225 -w 150 -h 50 --id mlops
D shape style mlops fillColor "#E0E7FF"
D shape style mlops strokeColor "#818CF8"

# Integration
D shape add rounded -l "Kafka Event Stream" --x 440 --y 60 -w 130 -h 50 --id kafka
D shape style kafka fillColor "$WHITE"
D shape style kafka strokeColor "$BORDER"

D shape add rounded -l "MES Connector → SAP Line-Hold" --x 440 --y 130 -w 130 -h 55 --id mes
D shape style mes fillColor "$NAVY"
D shape style mes fontColor "$WHITE"

D shape add rounded -l "Defect DB (PostgreSQL)" --x 440 --y 210 -w 130 -h 50 --id db
D shape style db fillColor "$WHITE"
D shape style db strokeColor "$BORDER"

# App
D shape add rounded -l "Quality Dashboard" --x 620 --y 60 -w 120 -h 45 --id dash
D shape style dash fillColor "$WHITE"
D shape style dash strokeColor "$BORDER"

D shape add rounded -l "Operator Station Pass/Fail" --x 620 --y 125 -w 120 -h 45 --id opui
D shape style opui fillColor "$WHITE"
D shape style opui strokeColor "$BORDER"

D shape add rounded -l "Alerts (Slack/Teams)" --x 620 --y 190 -w 120 -h 45 --id alerts
D shape style alerts fillColor "$RED"
D shape style alerts fontColor "$WHITE"

# Connect
D connect add cam edge --style orthogonal -l "1 Capture"
D connect add edge cnn --style orthogonal -l "2 Infer"
D connect add cnn kafka --style orthogonal -l "3 Score"
D connect add kafka mes --style orthogonal -l "4 Line-Hold"
D connect add kafka db --style orthogonal -l "Persist"
D connect add cnn sage --style orthogonal -l "Retrain"
D connect add sage mlops --style orthogonal
D connect add mlops edge --style curved -l "5 OTA"
D connect add cnn dash --style orthogonal -l "6 Display"
D connect add edge opui --style curved
D connect add kafka alerts --style curved

D project save
echo "  Done: uc01"

# ============================================================================
# UC-02: Model & Variant Confirmation
# ============================================================================
echo "=== UC-02: Model & Variant Confirmation ==="
F="$DIR/uc02-variant-confirmation-architecture.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-02: Model & Variant Confirmation" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18 && D shape style title fontStyle 1 && D shape style title fontColor "$NAVY"

D shape add rounded -l "Vision Cameras + VIN Scanner" --x 50 --y 60 -w 140 -h 55 --id cam
D shape style cam fillColor "$WHITE" && D shape style cam strokeColor "$BORDER"
D shape add rounded -l "Barcode / DataMatrix" --x 50 --y 135 -w 140 -h 50 --id barcode
D shape style barcode fillColor "$WHITE" && D shape style barcode strokeColor "$BORDER"
D shape add rounded -l "Edge Gateway" --x 50 --y 205 -w 140 -h 50 --id gw
D shape style gw fillColor "#E0E7FF" && D shape style gw strokeColor "#818CF8"

D shape add rounded -l "YOLOv8 Object Detection" --x 240 --y 60 -w 150 -h 55 --id yolo
D shape style yolo fillColor "$WHITE" && D shape style yolo strokeColor "$ORANGE" && D shape style yolo strokeWidth 2
D shape add rounded -l "PaddleOCR VIN Reader" --x 240 --y 135 -w 150 -h 50 --id ocr
D shape style ocr fillColor "$WHITE" && D shape style ocr strokeColor "$ORANGE" && D shape style ocr strokeWidth 2
D shape add rounded -l "BOM-Match Rules Engine" --x 240 --y 205 -w 150 -h 50 --id bom
D shape style bom fillColor "$WHITE" && D shape style bom strokeColor "$ORANGE" && D shape style bom strokeWidth 2

D shape add rounded -l "SAP MES + BOM Database" --x 440 --y 60 -w 130 -h 55 --id sap
D shape style sap fillColor "$NAVY" && D shape style sap fontColor "$WHITE"
D shape add rounded -l "PLC / Line Controller" --x 440 --y 135 -w 130 -h 50 --id plc
D shape style plc fillColor "#FEF3C7" && D shape style plc strokeColor "#F59E0B"
D shape add rounded -l "Variant Config Service" --x 440 --y 205 -w 130 -h 50 --id variant
D shape style variant fillColor "$WHITE" && D shape style variant strokeColor "$BORDER"

D shape add rounded -l "Mismatch Console" --x 620 --y 60 -w 120 -h 45 --id console
D shape style console fillColor "$WHITE" && D shape style console strokeColor "$BORDER"
D shape add rounded -l "Auto Line-Hold" --x 620 --y 125 -w 120 -h 45 --id hold
D shape style hold fillColor "$RED" && D shape style hold fontColor "$WHITE"
D shape add rounded -l "Variant Audit Report" --x 620 --y 190 -w 120 -h 45 --id audit
D shape style audit fillColor "$WHITE" && D shape style audit strokeColor "$BORDER"

D connect add cam yolo --style orthogonal -l "1 Scan"
D connect add barcode ocr --style orthogonal -l "2 Read"
D connect add yolo bom --style orthogonal -l "3 Match"
D connect add ocr bom --style orthogonal
D connect add bom sap --style orthogonal -l "4 Verify BOM"
D connect add bom plc --style orthogonal -l "5 Signal"
D connect add plc hold --style orthogonal -l "Block"
D connect add bom console --style orthogonal -l "6 Alert"
D connect add console audit --style orthogonal

D project save
echo "  Done: uc02"

# ============================================================================
# UC-03: Seating & Component Validation
# ============================================================================
echo "=== UC-03: Seating & Component Validation ==="
F="$DIR/uc03-seating-validation-architecture.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-03: Seating & Component Validation" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18 && D shape style title fontStyle 1 && D shape style title fontColor "$NAVY"

D shape add rounded -l "Multi-Angle Station Cameras" --x 50 --y 60 -w 140 -h 50 --id cam
D shape style cam fillColor "$WHITE" && D shape style cam strokeColor "$BORDER"
D shape add rounded -l "Smart Torque Wrenches (IIoT)" --x 50 --y 130 -w 140 -h 50 --id torque
D shape style torque fillColor "$WHITE" && D shape style torque strokeColor "$BORDER"
D shape add rounded -l "Edge Inference (Jetson Orin)" --x 50 --y 200 -w 140 -h 50 --id edge
D shape style edge fillColor "$NAVY" && D shape style edge fontColor "$WHITE"

D shape add rounded -l "YOLOv8 + Keypoint Head" --x 240 --y 60 -w 150 -h 50 --id yolo
D shape style yolo fillColor "$WHITE" && D shape style yolo strokeColor "$PURPLE" && D shape style yolo strokeWidth 2
D shape add rounded -l "Fitment Classifier" --x 240 --y 130 -w 150 -h 50 --id fitment
D shape style fitment fillColor "$WHITE" && D shape style fitment strokeColor "$PURPLE" && D shape style fitment strokeWidth 2
D shape add rounded -l "Variant Rule Engine" --x 240 --y 200 -w 150 -h 50 --id rules
D shape style rules fillColor "$WHITE" && D shape style rules strokeColor "$PURPLE" && D shape style rules strokeWidth 2

D shape add rounded -l "MES / Variant Config DB" --x 440 --y 60 -w 130 -h 50 --id mes
D shape style mes fillColor "$NAVY" && D shape style mes fontColor "$WHITE"
D shape add rounded -l "Torque Tool Gateway" --x 440 --y 130 -w 130 -h 50 --id tgw
D shape style tgw fillColor "$WHITE" && D shape style tgw strokeColor "$BORDER"
D shape add rounded -l "Quality Event Bus" --x 440 --y 200 -w 130 -h 50 --id bus
D shape style bus fillColor "$WHITE" && D shape style bus strokeColor "$BORDER"

D shape add rounded -l "Operator Tablet Pass/Fail" --x 620 --y 60 -w 120 -h 45 --id tablet
D shape style tablet fillColor "$WHITE" && D shape style tablet strokeColor "$BORDER"
D shape add rounded -l "Engineer Review Queue" --x 620 --y 125 -w 120 -h 45 --id review
D shape style review fillColor "$WHITE" && D shape style review strokeColor "$BORDER"
D shape add rounded -l "Fitment Report" --x 620 --y 190 -w 120 -h 45 --id report
D shape style report fillColor "$WHITE" && D shape style report strokeColor "$BORDER"

D connect add cam yolo --style orthogonal -l "1 Image"
D connect add torque fitment --style orthogonal -l "2 Torque"
D connect add yolo fitment --style orthogonal -l "3 Pose"
D connect add fitment rules --style orthogonal -l "4 Check"
D connect add rules mes --style orthogonal -l "5 Verify"
D connect add torque tgw --style orthogonal
D connect add rules bus --style orthogonal -l "6 Event"
D connect add fitment tablet --style orthogonal -l "7 Result"
D connect add bus review --style orthogonal
D connect add review report --style orthogonal

D project save
echo "  Done: uc03"

# ============================================================================
# UC-04: SOP Compliance Monitoring
# ============================================================================
echo "=== UC-04: SOP Compliance Monitoring ==="
F="$DIR/uc04-sop-compliance-architecture.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-04: SOP Compliance Monitoring" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18 && D shape style title fontStyle 1 && D shape style title fontColor "$NAVY"

D shape add rounded -l "Station IP Cameras (Fisheye)" --x 50 --y 60 -w 140 -h 50 --id cam
D shape style cam fillColor "$WHITE" && D shape style cam strokeColor "$BORDER"
D shape add rounded -l "Privacy-Aware On-Device Blur" --x 50 --y 130 -w 140 -h 45 --id blur
D shape style blur fillColor "$WHITE" && D shape style blur strokeColor "$BORDER"
D shape add rounded -l "Edge GPU" --x 50 --y 195 -w 140 -h 45 --id edge
D shape style edge fillColor "$NAVY" && D shape style edge fontColor "$WHITE"

D shape add rounded -l "MoveNet/MMPose (Pose)" --x 240 --y 60 -w 150 -h 50 --id pose
D shape style pose fillColor "$WHITE" && D shape style pose strokeColor "$TEAL2" && D shape style pose strokeWidth 2
D shape add rounded -l "SlowFast (Action Recog.)" --x 240 --y 130 -w 150 -h 50 --id action
D shape style action fillColor "$WHITE" && D shape style action strokeColor "$TEAL2" && D shape style action strokeWidth 2
D shape add rounded -l "SOP Graph Sequence Matcher" --x 240 --y 200 -w 150 -h 50 --id sop
D shape style sop fillColor "$WHITE" && D shape style sop strokeColor "$TEAL2" && D shape style sop strokeWidth 2

D shape add rounded -l "SOP Digital Library" --x 440 --y 60 -w 130 -h 50 --id lib
D shape style lib fillColor "$WHITE" && D shape style lib strokeColor "$BORDER"
D shape add rounded -l "MES Work-Order Context" --x 440 --y 130 -w 130 -h 45 --id mes
D shape style mes fillColor "$NAVY" && D shape style mes fontColor "$WHITE"
D shape add rounded -l "EHS Compliance System" --x 440 --y 195 -w 130 -h 50 --id ehs
D shape style ehs fillColor "$WHITE" && D shape style ehs strokeColor "$BORDER"

D shape add rounded -l "Live Deviation Feed" --x 620 --y 60 -w 120 -h 42 --id feed
D shape style feed fillColor "$WHITE" && D shape style feed strokeColor "$BORDER"
D shape add rounded -l "Coaching Overlay" --x 620 --y 122 -w 120 -h 42 --id coach
D shape style coach fillColor "$WHITE" && D shape style coach strokeColor "$BORDER"
D shape add rounded -l "Compliance Scorecard" --x 620 --y 184 -w 120 -h 45 --id score
D shape style score fillColor "$WHITE" && D shape style score strokeColor "$BORDER"

D connect add cam blur --style orthogonal -l "1 Video"
D connect add blur edge --style orthogonal -l "2 Anonymize"
D connect add edge pose --style orthogonal -l "3 Infer"
D connect add pose action --style orthogonal
D connect add action sop --style orthogonal -l "4 Match SOP"
D connect add sop lib --style orthogonal -l "5 Lookup"
D connect add sop ehs --style orthogonal -l "6 Log"
D connect add sop feed --style orthogonal -l "7 Alert"
D connect add feed coach --style orthogonal
D connect add ehs score --style orthogonal

D project save
echo "  Done: uc04"

# ============================================================================
# UC-05: Predictive Quality Analytics
# ============================================================================
echo "=== UC-05: Predictive Quality Analytics ==="
F="$DIR/uc05-predictive-quality-architecture.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-05: Predictive Quality Analytics" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18 && D shape style title fontStyle 1 && D shape style title fontColor "$NAVY"

D shape add rounded -l "IoT Sensors (Temp, Pressure, Vibration)" --x 50 --y 60 -w 140 -h 55 --id sensors
D shape style sensors fillColor "$WHITE" && D shape style sensors strokeColor "$BORDER"
D shape add rounded -l "OPC-UA Gateways" --x 50 --y 135 -w 140 -h 45 --id opcua
D shape style opcua fillColor "#FEF3C7" && D shape style opcua strokeColor "#F59E0B"
D shape add rounded -l "AVEVA PI Historian" --x 50 --y 200 -w 140 -h 50 --id historian
D shape style historian fillColor "$WHITE" && D shape style historian strokeColor "$BORDER"

D shape add rounded -l "XGBoost/LightGBM Defect Classifier" --x 240 --y 60 -w 155 -h 55 --id xgb
D shape style xgb fillColor "$WHITE" && D shape style xgb strokeColor "$RED" && D shape style xgb strokeWidth 2
D shape add rounded -l "LSTM Time-Series Model" --x 240 --y 135 -w 155 -h 50 --id lstm
D shape style lstm fillColor "$WHITE" && D shape style lstm strokeColor "$RED" && D shape style lstm strokeWidth 2
D shape add rounded -l "SHAP Explainability" --x 240 --y 205 -w 155 -h 50 --id shap
D shape style shap fillColor "$WHITE" && D shape style shap strokeColor "$RED" && D shape style shap strokeWidth 2

D shape add rounded -l "SageMaker / Azure ML" --x 445 --y 60 -w 130 -h 50 --id cloud
D shape style cloud fillColor "$NAVY" && D shape style cloud fontColor "$WHITE"
D shape add rounded -l "Kafka Streaming Inference" --x 445 --y 130 -w 130 -h 50 --id kafka
D shape style kafka fillColor "$WHITE" && D shape style kafka strokeColor "$BORDER"
D shape add rounded -l "Quality DB + MES" --x 445 --y 200 -w 130 -h 50 --id qdb
D shape style qdb fillColor "$NAVY" && D shape style qdb fontColor "$WHITE"

D shape add rounded -l "Early-Warning Dashboard" --x 625 --y 60 -w 120 -h 42 --id warn
D shape style warn fillColor "$WHITE" && D shape style warn strokeColor "$BORDER"
D shape add rounded -l "Root-Cause Drill-Down" --x 625 --y 122 -w 120 -h 42 --id root
D shape style root fillColor "$WHITE" && D shape style root strokeColor "$BORDER"
D shape add rounded -l "Auto-Tuning Recommendations" --x 625 --y 184 -w 120 -h 48 --id tune
D shape style tune fillColor "$WHITE" && D shape style tune strokeColor "$BORDER"

D connect add sensors opcua --style orthogonal -l "1 Stream"
D connect add opcua historian --style orthogonal -l "2 Store"
D connect add opcua xgb --style orthogonal -l "3 Feed"
D connect add xgb lstm --style orthogonal
D connect add lstm shap --style orthogonal -l "4 Explain"
D connect add xgb cloud --style orthogonal -l "5 Train"
D connect add xgb kafka --style orthogonal -l "6 Score"
D connect add kafka qdb --style orthogonal
D connect add xgb warn --style orthogonal -l "7 Alert"
D connect add shap root --style orthogonal
D connect add root tune --style orthogonal

D project save
echo "  Done: uc05"

# ============================================================================
# UC-06: Predictive Maintenance
# ============================================================================
echo "=== UC-06: Predictive Maintenance ==="
F="$DIR/uc06-predictive-maintenance-architecture.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-06: Predictive Maintenance" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18 && D shape style title fontStyle 1 && D shape style title fontColor "$NAVY"

D shape add rounded -l "Vibration Accelerometers" --x 50 --y 60 -w 140 -h 45 --id vib
D shape style vib fillColor "$WHITE" && D shape style vib strokeColor "$BORDER"
D shape add rounded -l "Acoustic Emission Sensors" --x 50 --y 125 -w 140 -h 45 --id acoustic
D shape style acoustic fillColor "$WHITE" && D shape style acoustic strokeColor "$BORDER"
D shape add rounded -l "Thermal Cameras" --x 50 --y 190 -w 140 -h 45 --id thermal
D shape style thermal fillColor "$WHITE" && D shape style thermal strokeColor "$BORDER"
D shape add rounded -l "Edge Concentrator (IoT Greengrass)" --x 50 --y 255 -w 140 -h 50 --id edge
D shape style edge fillColor "$NAVY" && D shape style edge fontColor "$WHITE"

D shape add rounded -l "Autoencoder Anomaly Detection" --x 240 --y 60 -w 155 -h 50 --id ae
D shape style ae fillColor "$WHITE" && D shape style ae strokeColor "$NAVY_CARD" && D shape style ae strokeWidth 2
D shape add rounded -l "DeepSurv Survival Analysis" --x 240 --y 130 -w 155 -h 50 --id surv
D shape style surv fillColor "$WHITE" && D shape style surv strokeColor "$NAVY_CARD" && D shape style surv strokeWidth 2
D shape add rounded -l "Audio CNN Acoustic ML" --x 240 --y 200 -w 155 -h 50 --id audio
D shape style audio fillColor "$WHITE" && D shape style audio strokeColor "$NAVY_CARD" && D shape style audio strokeWidth 2
D shape add rounded -l "MLflow Model Registry" --x 240 --y 270 -w 155 -h 45 --id mlflow
D shape style mlflow fillColor "#E0E7FF" && D shape style mlflow strokeColor "#818CF8"

D shape add rounded -l "SAP PM" --x 445 --y 60 -w 130 -h 45 --id sappm
D shape style sappm fillColor "$NAVY" && D shape style sappm fontColor "$WHITE"
D shape add rounded -l "CMMS (Maximo)" --x 445 --y 125 -w 130 -h 45 --id cmms
D shape style cmms fillColor "$NAVY" && D shape style cmms fontColor "$WHITE"
D shape add rounded -l "Asset Historian" --x 445 --y 190 -w 130 -h 45 --id hist
D shape style hist fillColor "$WHITE" && D shape style hist strokeColor "$BORDER"
D shape add rounded -l "Work-Order Auto-Gen API" --x 445 --y 255 -w 130 -h 45 --id woapi
D shape style woapi fillColor "$WHITE" && D shape style woapi strokeColor "$BORDER"

D shape add rounded -l "Asset Health Dashboard" --x 625 --y 60 -w 120 -h 42 --id health
D shape style health fillColor "$WHITE" && D shape style health strokeColor "$BORDER"
D shape add rounded -l "Risk-Prioritized Work Queue" --x 625 --y 122 -w 120 -h 42 --id queue
D shape style queue fillColor "$WHITE" && D shape style queue strokeColor "$BORDER"
D shape add rounded -l "Mobile Technician App" --x 625 --y 184 -w 120 -h 45 --id mobile
D shape style mobile fillColor "$WHITE" && D shape style mobile strokeColor "$BORDER"
D shape add rounded -l "Failure-Cause Analytics" --x 625 --y 249 -w 120 -h 42 --id analytics
D shape style analytics fillColor "$WHITE" && D shape style analytics strokeColor "$BORDER"

D connect add vib edge --style orthogonal -l "1 Sense"
D connect add acoustic edge --style orthogonal
D connect add thermal edge --style orthogonal
D connect add edge ae --style orthogonal -l "2 Analyze"
D connect add ae surv --style orthogonal -l "3 RUL"
D connect add acoustic audio --style orthogonal
D connect add surv sappm --style orthogonal -l "4 Work Order"
D connect add surv woapi --style orthogonal
D connect add woapi cmms --style orthogonal
D connect add ae health --style orthogonal -l "5 Display"
D connect add surv queue --style orthogonal
D connect add woapi mobile --style orthogonal -l "6 Push"
D connect add audio analytics --style orthogonal

D project save
echo "  Done: uc06"

# ============================================================================
# UC-07: AI Safety Monitoring
# ============================================================================
echo "=== UC-07: AI Safety Monitoring ==="
F="$DIR/uc07-safety-monitoring-architecture.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-07: AI Safety Monitoring" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18 && D shape style title fontStyle 1 && D shape style title fontColor "$NAVY"

D shape add rounded -l "Wide-FOV Safety Cameras" --x 50 --y 60 -w 140 -h 50 --id safecam
D shape style safecam fillColor "$WHITE" && D shape style safecam strokeColor "$BORDER"
D shape add rounded -l "Forklift Onboard Cams" --x 50 --y 130 -w 140 -h 45 --id forklift
D shape style forklift fillColor "$WHITE" && D shape style forklift strokeColor "$BORDER"
D shape add rounded -l "Edge AI (Hailo/Jetson)" --x 50 --y 195 -w 140 -h 50 --id edge2
D shape style edge2 fillColor "$NAVY" && D shape style edge2 fontColor "$WHITE"
D shape add rounded -l "Person Anonymization" --x 50 --y 265 -w 140 -h 45 --id anon
D shape style anon fillColor "$WHITE" && D shape style anon strokeColor "$BORDER"

D shape add rounded -l "YOLOv8 PPE Detector" --x 240 --y 60 -w 150 -h 50 --id ppe
D shape style ppe fillColor "$WHITE" && D shape style ppe strokeColor "$TEAL" && D shape style ppe strokeWidth 2
D shape add rounded -l "Person-Vehicle Proximity Tracker" --x 240 --y 130 -w 150 -h 50 --id prox
D shape style prox fillColor "$WHITE" && D shape style prox strokeColor "$TEAL" && D shape style prox strokeWidth 2
D shape add rounded -l "Zone-Violation Rule Engine" --x 240 --y 200 -w 150 -h 50 --id zone
D shape style zone fillColor "$WHITE" && D shape style zone strokeColor "$TEAL" && D shape style zone strokeWidth 2

D shape add rounded -l "EHS Platform" --x 440 --y 60 -w 130 -h 50 --id ehs2
D shape style ehs2 fillColor "$WHITE" && D shape style ehs2 strokeColor "$BORDER"
D shape add rounded -l "Incident Mgmt System" --x 440 --y 130 -w 130 -h 45 --id incident
D shape style incident fillColor "$WHITE" && D shape style incident strokeColor "$BORDER"
D shape add rounded -l "Andon / PA Siren" --x 440 --y 195 -w 130 -h 50 --id andon
D shape style andon fillColor "$RED" && D shape style andon fontColor "$WHITE"
D shape add rounded -l "Access Control System" --x 440 --y 265 -w 130 -h 45 --id access
D shape style access fillColor "$WHITE" && D shape style access strokeColor "$BORDER"

D shape add rounded -l "EHS Live Wall" --x 620 --y 60 -w 120 -h 42 --id wall
D shape style wall fillColor "$WHITE" && D shape style wall strokeColor "$BORDER"
D shape add rounded -l "Auto-Incident Report + Video" --x 620 --y 122 -w 120 -h 48 --id report2
D shape style report2 fillColor "$WHITE" && D shape style report2 strokeColor "$BORDER"
D shape add rounded -l "Compliance Scorecard" --x 620 --y 190 -w 120 -h 42 --id scorecard
D shape style scorecard fillColor "$WHITE" && D shape style scorecard strokeColor "$BORDER"
D shape add rounded -l "Audit Export" --x 620 --y 252 -w 120 -h 42 --id auditexp
D shape style auditexp fillColor "$WHITE" && D shape style auditexp strokeColor "$BORDER"

D connect add safecam edge2 --style orthogonal -l "1 Video"
D connect add forklift edge2 --style orthogonal
D connect add edge2 ppe --style orthogonal -l "2 Detect"
D connect add edge2 prox --style orthogonal
D connect add ppe zone --style orthogonal -l "3 Rules"
D connect add zone andon --style orthogonal -l "4 Siren"
D connect add zone ehs2 --style orthogonal -l "5 Log"
D connect add ehs2 incident --style orthogonal
D connect add ppe wall --style orthogonal -l "6 Display"
D connect add incident report2 --style orthogonal
D connect add ehs2 scorecard --style orthogonal
D connect add scorecard auditexp --style orthogonal

D project save
echo "  Done: uc07"

# ============================================================================
# UC-08: Digital Traceability & Tracking
# ============================================================================
echo "=== UC-08: Digital Traceability & Tracking ==="
F="$DIR/uc08-digital-traceability-architecture-v2.drawio"
$CLI project new -o "$F"

D shape add text -l "UC-08: Digital Traceability & Tracking" --x 40 --y 10 -w 500 -h 30 --id title
D shape style title fontSize 18 && D shape style title fontStyle 1 && D shape style title fontColor "$NAVY"

D shape add rounded -l "RFID Readers (UHF)" --x 50 --y 60 -w 140 -h 45 --id rfid
D shape style rfid fillColor "$WHITE" && D shape style rfid strokeColor "$BORDER"
D shape add rounded -l "Barcode / DataMatrix" --x 50 --y 125 -w 140 -h 45 --id barcode2
D shape style barcode2 fillColor "$WHITE" && D shape style barcode2 strokeColor "$BORDER"
D shape add rounded -l "IoT Sensors" --x 50 --y 190 -w 140 -h 40 --id iot
D shape style iot fillColor "$WHITE" && D shape style iot strokeColor "$BORDER"
D shape add rounded -l "Vision OCR Stations" --x 50 --y 250 -w 140 -h 45 --id vocr
D shape style vocr fillColor "$WHITE" && D shape style vocr strokeColor "$BORDER"

D shape add rounded -l "Neo4j Genealogy Graph" --x 240 --y 60 -w 155 -h 55 --id neo4j
D shape style neo4j fillColor "$WHITE" && D shape style neo4j strokeColor "$TEAL2" && D shape style neo4j strokeWidth 2
D shape add rounded -l "Apache Flink Stream Processing" --x 240 --y 135 -w 155 -h 50 --id flink
D shape style flink fillColor "$WHITE" && D shape style flink strokeColor "$TEAL2" && D shape style flink strokeWidth 2
D shape add rounded -l "Defect Propagation ML" --x 240 --y 205 -w 155 -h 45 --id defml
D shape style defml fillColor "$WHITE" && D shape style defml strokeColor "$TEAL2" && D shape style defml strokeWidth 2
D shape add rounded -l "Supplier Risk Scoring" --x 240 --y 270 -w 155 -h 45 --id supplier
D shape style supplier fillColor "$WHITE" && D shape style supplier strokeColor "$TEAL2" && D shape style supplier strokeWidth 2

D shape add rounded -l "SAP MES / ERP" --x 445 --y 60 -w 130 -h 50 --id sap2
D shape style sap2 fillColor "$NAVY" && D shape style sap2 fontColor "$WHITE"
D shape add rounded -l "Supplier Portals" --x 445 --y 130 -w 130 -h 45 --id portals
D shape style portals fillColor "$WHITE" && D shape style portals strokeColor "$BORDER"
D shape add rounded -l "Quality DB" --x 445 --y 195 -w 130 -h 42 --id qdb2
D shape style qdb2 fillColor "$WHITE" && D shape style qdb2 strokeColor "$BORDER"
D shape add rounded -l "Recall Mgmt System" --x 445 --y 257 -w 130 -h 48 --id recall
D shape style recall fillColor "$RED" && D shape style recall fontColor "$WHITE"

D shape add rounded -l "Vehicle Genealogy Viewer" --x 625 --y 60 -w 120 -h 48 --id viewer
D shape style viewer fillColor "$WHITE" && D shape style viewer strokeColor "$BORDER"
D shape add rounded -l "Root-Cause Drill-Down" --x 625 --y 128 -w 120 -h 42 --id rootcause
D shape style rootcause fillColor "$WHITE" && D shape style rootcause strokeColor "$BORDER"
D shape add rounded -l "Recall Scope Calculator" --x 625 --y 190 -w 120 -h 45 --id scope
D shape style scope fillColor "$WHITE" && D shape style scope strokeColor "$BORDER"
D shape add rounded -l "Auditor Export Portal" --x 625 --y 255 -w 120 -h 42 --id auditor
D shape style auditor fillColor "$WHITE" && D shape style auditor strokeColor "$BORDER"

D connect add rfid flink --style orthogonal -l "1 Scan"
D connect add barcode2 flink --style orthogonal
D connect add iot flink --style orthogonal
D connect add vocr flink --style orthogonal
D connect add flink neo4j --style orthogonal -l "2 Build Graph"
D connect add neo4j defml --style orthogonal -l "3 Analyze"
D connect add defml supplier --style orthogonal -l "4 Score"
D connect add neo4j sap2 --style orthogonal -l "5 Sync"
D connect add supplier portals --style orthogonal
D connect add defml qdb2 --style orthogonal
D connect add neo4j viewer --style orthogonal -l "6 Display"
D connect add defml rootcause --style orthogonal
D connect add recall scope --style orthogonal
D connect add qdb2 auditor --style orthogonal

D project save
echo "  Done: uc08"

echo ""
echo "=== ALL 8 USE CASE DIAGRAMS COMPLETE ==="
ls -la "$DIR"/uc0*.drawio
