"""Build a native PowerPoint version of the Hyundai x PeopleTech deck.

Produces 15 slides matching the HTML deck structure. Editable native shapes,
text boxes, and tables — designed to be the .pptx that gets emailed around
and tweaked by the pre-sales team before the meeting.

Run:  python3 build_pptx.py
Out:  Hyundai_PeopleTech_AI_Plant_Operations.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ============================================================================
# DESIGN TOKENS
# ============================================================================
NAVY_900 = RGBColor(0x0F, 0x17, 0x29)
NAVY_800 = RGBColor(0x1A, 0x27, 0x54)
NAVY_700 = RGBColor(0x24, 0x38, 0x70)
TEAL     = RGBColor(0x14, 0xA0, 0x85)
TEAL_2   = RGBColor(0x0E, 0x7B, 0x6A)
ORANGE   = RGBColor(0xD9, 0x77, 0x06)
PURPLE   = RGBColor(0x7C, 0x3A, 0xED)
RED      = RGBColor(0xDC, 0x26, 0x26)
INK      = RGBColor(0x1E, 0x29, 0x3B)
INK_SOFT = RGBColor(0x47, 0x55, 0x69)
INK_MUTE = RGBColor(0x64, 0x74, 0x8B)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
SLATE_50 = RGBColor(0xF8, 0xFA, 0xFC)
SLATE_200 = RGBColor(0xE2, 0xE8, 0xF0)
SLATE_300 = RGBColor(0xCB, 0xD5, 0xE1)
SLATE_400 = RGBColor(0x94, 0xA3, 0xB8)

FONT = "Calibri"

# 16:9 slide @ 13.333 x 7.5 inches (standard widescreen)
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# ============================================================================
# HELPERS
# ============================================================================
def add_rect(slide, x, y, w, h, fill_color, line_color=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill_color
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
    shp.shadow.inherit = False
    return shp

def add_text(slide, x, y, w, h, text, *,
             font_size=14, color=INK, bold=False, italic=False,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             font_name=FONT, line_spacing=1.2):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    return tb

def add_bullets(slide, x, y, w, h, bullets, *,
                font_size=11, color=INK, font_name=FONT, bullet_char="•",
                line_spacing=1.35):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.margin_left = Emu(0); tf.margin_right = Emu(0)
    tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        run = p.add_run()
        run.text = f"{bullet_char}  {bullet}"
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
    return tb

def slide_footer(slide, slide_num, total=17, brand="PeopleTech · AI Manufacturing Practice"):
    add_rect(slide, 0, Inches(7.0), SLIDE_W, Inches(0.5), NAVY_900)
    add_text(slide, Inches(0.5), Inches(7.05), Inches(8), Inches(0.4),
             brand, font_size=9, color=SLATE_300, anchor=MSO_ANCHOR.MIDDLE, bold=True)
    add_text(slide, Inches(8.5), Inches(7.05), Inches(4.3), Inches(0.4),
             f"{slide_num:02d} / {total} · CONFIDENTIAL", font_size=9,
             color=SLATE_400, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)

def uc_band(slide, color, tag, title, subtitle):
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.9), color)
    add_text(slide, Inches(0.5), 0, Inches(2.5), Inches(0.9),
             tag, font_size=11, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(3), 0, Inches(7), Inches(0.9),
             title, font_size=22, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(10), 0, Inches(2.8), Inches(0.9),
             subtitle, font_size=11, color=WHITE, italic=True,
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def std_header(slide, eyebrow, title, right_text):
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.9), NAVY_800)
    add_text(slide, Inches(0.5), 0, Inches(2.5), Inches(0.9),
             eyebrow, font_size=10, color=SLATE_300, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(3), 0, Inches(7), Inches(0.9),
             title, font_size=22, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, Inches(10), 0, Inches(2.8), Inches(0.9),
             right_text, font_size=10, color=SLATE_300,
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def card(slide, x, y, w, h, label, body_text=None, body_bullets=None,
         accent=NAVY_700, label_color=None):
    """A card with left accent bar, label, and body content."""
    # Background
    bg = add_rect(slide, x, y, w, h, WHITE)
    # Left accent stripe
    add_rect(slide, x, y, Inches(0.06), h, accent)
    label_color = label_color or accent
    # Label
    add_text(slide, x + Inches(0.18), y + Inches(0.1), w - Inches(0.25), Inches(0.25),
             label, font_size=9, color=label_color, bold=True)
    # Body
    body_x = x + Inches(0.18)
    body_y = y + Inches(0.4)
    body_w = w - Inches(0.25)
    body_h = h - Inches(0.45)
    if body_bullets:
        add_bullets(slide, body_x, body_y, body_w, body_h, body_bullets, font_size=10)
    elif body_text:
        add_text(slide, body_x, body_y, body_w, body_h, body_text,
                 font_size=11, color=INK, line_spacing=1.35)

def meta_card(slide, x, y, w, h, label, text, accent=NAVY_800):
    add_rect(slide, x, y, w, h, WHITE)
    add_rect(slide, x, y, Inches(0.06), h, accent)
    add_text(slide, x + Inches(0.18), y + Inches(0.08), w - Inches(0.25), Inches(0.22),
             label, font_size=8, color=INK_MUTE, bold=True)
    add_text(slide, x + Inches(0.18), y + Inches(0.32), w - Inches(0.25), h - Inches(0.35),
             text, font_size=10, color=INK, line_spacing=1.3)

def metric_tile(slide, x, y, w, h, value, label, color):
    add_rect(slide, x, y, w, h, color)
    add_text(slide, x, y + Inches(0.1), w, Inches(0.55),
             value, font_size=24, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, x, y + Inches(0.65), w, Inches(0.35),
             label, font_size=9, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, line_spacing=1.2)

def stack_strip(slide, x, y, w, h, layers):
    """4-column solution stack strip. layers = [(title, body), ...]"""
    add_rect(slide, x, y, w, h, WHITE)
    add_rect(slide, x, y, w, Inches(0.04), NAVY_700)  # top border
    add_text(slide, x + Inches(0.2), y + Inches(0.08), w - Inches(0.4), Inches(0.22),
             "SOLUTION STACK & ARCHITECTURE", font_size=9, color=NAVY_700, bold=True)
    col_w = (w - Inches(0.4)) / 4
    for i, (title, body) in enumerate(layers):
        cx = x + Inches(0.2) + col_w * i
        add_text(slide, cx, y + Inches(0.35), col_w - Inches(0.1), Inches(0.22),
                 title, font_size=9, color=NAVY_800, bold=True)
        add_text(slide, cx, y + Inches(0.6), col_w - Inches(0.1), h - Inches(0.65),
                 body, font_size=8, color=INK_SOFT, line_spacing=1.3)

# ============================================================================
# USE CASE DATA
# ============================================================================
USE_CASES = [
    {
        "n": "01",
        "title": "AI-based Visual Inspection",
        "sub": "Computer Vision + Deep Learning",
        "color": TEAL,
        "challenge": "Paint defects, scratches, dents, welding inconsistencies, and panel misalignments escape manual inspection and reach downstream stages, driving rework costs and warranty claims.",
        "solution": "High-resolution AI cameras inspect vehicle surfaces in real time. CNN models compare images against quality standards, score anomalies, and automatically flag vehicles before they advance.",
        "capabilities": [
            "Real-time surface defect detection across paint, welds, and panel gaps",
            "CNN-based anomaly scoring against golden-sample quality standards",
            "Auto-triggered downstream hold for flagged vehicles",
            "Defect traceability linked to production station, shift, and operator",
        ],
        "metrics": [("−45%", "Rework Costs"), ("−60%", "Escape Defects"),
                    ("<2s", "Detection Latency"), ("+35%", "Line Throughput")],
        "systems": "Edge AI cameras · AWS Rekognition / Azure Custom Vision · MES · Defect DB · Quality Dashboard",
        "users": "Quality Engineers · Line Supervisors · Plant Managers",
        "stack": [
            ("EDGE / CAPTURE", "Industrial high-res cameras (Cognex / Basler) · LED light tunnels · NVIDIA Jetson edge inference"),
            ("COMPUTE / AI MODELS", "CNN anomaly models (ResNet50, EfficientNet) · AWS Rekognition Custom Labels / Azure Custom Vision · SageMaker training pipeline"),
            ("INTEGRATION", "MES connector · OPC-UA bus · Defect database (PostgreSQL) · Kafka event stream"),
            ("UX / DECISION", "Real-time quality dashboard · Operator hold-station UI · Defect drill-down portal · Slack/Teams alerts"),
        ],
        "hyundai_start": "Paint shop · IONIQ 5 / IONIQ 9 line at Metaplant America (HMGMA) — newest line, highest variant complexity, premium-segment defect sensitivity. Fast-follow on Tucson / Santa Fe paint at HMMA.",
    },
    {
        "n": "02",
        "title": "Model & Variant Confirmation",
        "sub": "AI Variant Verification",
        "color": ORANGE,
        "challenge": "Wrong variant assembly — mismatched trim, components, or accessories — costs millions in rework and creates downstream warranty exposure across the entire production run.",
        "solution": "Computer vision and VIN/barcode recognition validate vehicle model, trim level, and installed components during assembly. Detected parts are checked against BOM and MES data in real time.",
        "capabilities": [
            "VIN + barcode scanning for model and variant identification",
            "Vision-based BOM comparison against installed components",
            "Real-time mismatch alerts before vehicle advances to next stage",
            "MES integration to block line progression on confirmation failure",
        ],
        "metrics": [("−90%", "Wrong Variants"), ("−70%", "Rework Events"),
                    ("99.8%", "Verification Accuracy"), ("<1s", "Check Latency")],
        "systems": "Vision cameras · VIN/barcode scanners · SAP MES · BOM database · Line controllers",
        "users": "Assembly Operators · Quality Control · Production Supervisors",
        "stack": [
            ("EDGE / CAPTURE", "Vision cameras · VIN/barcode scanners (Datalogic, Cognex DataMan) · Edge gateway with local cache"),
            ("COMPUTE / AI MODELS", "OCR + object detection (YOLOv8, PaddleOCR) · BOM-match rules engine · Hybrid edge inference / cloud retraining"),
            ("INTEGRATION", "SAP MES API · BOM database · PLC / line-controller signal-out · Variant configuration service"),
            ("UX / DECISION", "Station mismatch console · Auto-line-hold trigger · Supervisor mobile alert · Variant audit report"),
        ],
    },
    {
        "n": "03",
        "title": "Seating & Component Validation",
        "sub": "Vision AI Fitment Checks",
        "color": PURPLE,
        "challenge": "Incorrect seat type, orientation, or mounting errors pass undetected during assembly and cause safety issues, costly post-delivery recalls, and customer satisfaction failures.",
        "solution": "AI cameras verify seat type, orientation, mounting alignment, fastening completion, and fitment accuracy for every vehicle variant. Mismatches are caught before the vehicle leaves the station.",
        "capabilities": [
            "Seat type and orientation verification via vision AI",
            "Torque and fastening completion detection",
            "Variant-matched fitment checks against vehicle configuration",
            "Alert generation before vehicle moves to next assembly station",
        ],
        "metrics": [("−85%", "Fitment Errors"), ("Zero", "Seat Recalls"),
                    ("+30%", "Inspection Speed"), ("100%", "Vehicle Coverage")],
        "systems": "Vision cameras · Torque tool integration · MES · Variant configuration DB",
        "users": "Assembly Operators · Quality Inspectors · Plant Engineers",
        "stack": [
            ("EDGE / CAPTURE", "Multi-angle station cameras · Smart torque wrenches with IIoT telemetry · Edge inference (Jetson Orin)"),
            ("COMPUTE / AI MODELS", "Object detection & pose estimation (YOLOv8 + keypoint head) · Fitment classifier · Variant rule engine"),
            ("INTEGRATION", "MES · Variant configuration DB · Torque tool gateway · Quality event bus"),
            ("UX / DECISION", "Operator station tablet · Pass/fail visual cue · Engineer review queue · Post-shift fitment report"),
        ],
    },
    {
        "n": "04",
        "title": "SOP Compliance Monitoring",
        "sub": "Vision + Pose Estimation",
        "color": TEAL_2,
        "challenge": "Operators skipping steps or deviating from defined procedures introduce assembly defects that only surface during final inspection — or worse, in the field after delivery.",
        "solution": "AI monitors operator activities against SOP workflows using video analytics and pose estimation. Skipped steps, wrong tool usage, and process deviations are flagged with real-time alerts.",
        "capabilities": [
            "Pose estimation to detect operator step sequences and ergonomics",
            "SOP workflow comparison with real-time deviation alerts",
            "Incorrect tool usage detection via object recognition",
            "Compliance reporting by operator, station, and shift",
        ],
        "metrics": [("−65%", "SOP Deviations"), ("−40%", "Final Defects"),
                    ("+90%", "Compliance Rate"), ("Real-time", "Deviation Alerts")],
        "systems": "Video analytics platform · Pose estimation models · MES · EHS compliance system",
        "users": "Shift Supervisors · Quality Managers · EHS Officers · Process Engineers",
        "stack": [
            ("EDGE / CAPTURE", "Station-mounted IP cameras (fisheye + standard) · Privacy-aware on-device blurring · Edge GPU"),
            ("COMPUTE / AI MODELS", "Pose estimation (MoveNet, MMPose) · Action recognition (SlowFast) · Sequence matcher against SOP graph"),
            ("INTEGRATION", "SOP digital library · MES work-order context · EHS compliance system · LDAP for operator ID"),
            ("UX / DECISION", "Supervisor live deviation feed · Operator coaching overlay · Compliance scorecard per shift"),
        ],
    },
    {
        "n": "05",
        "title": "Predictive Quality Analytics",
        "sub": "ML Quality Prediction Engine",
        "color": RED,
        "challenge": "Defects found at end-of-line or post-delivery cost 10–100× more than defects caught in process. Current reactive models miss early warning signals buried in sensor and process data.",
        "solution": "ML models analyze production line sensor data, machine parameters, environmental conditions, and historical defect trends to predict quality failures before they materialize.",
        "capabilities": [
            "Real-time sensor data fusion across temperature, pressure, and vibration",
            "Predictive defect scoring with explainability for root-cause guidance",
            "Early-warning alerts pushed to line supervisors before quality escapes",
            "Historical trend analysis to identify chronic defect contributors",
        ],
        "metrics": [("−35%", "Scrap & Rework"), ("−25%", "Warranty Claims"),
                    ("+20%", "Overall OEE"), ("3–5×", "Measured ROI")],
        "systems": "IoT sensors · AWS SageMaker / Azure ML · MES · Historian DB · Quality database",
        "users": "Quality Engineers · Plant Managers · Process Improvement Teams",
        "stack": [
            ("EDGE / CAPTURE", "IoT sensors (temp, pressure, vibration) · OPC-UA gateways · AVEVA PI historian connectors"),
            ("COMPUTE / AI MODELS", "XGBoost / LightGBM defect classifiers · LSTM time-series models · SHAP for explainability · SageMaker / Azure ML"),
            ("INTEGRATION", "MES · Quality DB · Historian (PI / Aspen IP21) · Kafka for streaming inference"),
            ("UX / DECISION", "Early-warning dashboard · Root-cause drill-down · Auto-tuning parameter recommendations · Weekly trend digest"),
        ],
    },
    {
        "n": "06",
        "title": "Predictive Maintenance",
        "sub": "Industrial AI Maintenance Platform",
        "color": NAVY_800,
        "challenge": "Unplanned downtime costs automotive plants an average of $22,000 per minute. Reactive maintenance schedules miss early failure signals and create dangerous, expensive surprises.",
        "solution": "AI models continuously monitor machine vibration, temperature, pressure, acoustics, and operational patterns to predict equipment failures and schedule maintenance before breakdown.",
        "capabilities": [
            "Continuous multi-sensor anomaly monitoring across vibration, temperature, and acoustics",
            "Failure prediction with configurable lead-time windows",
            "Automated maintenance work order generation in EAM and SAP PM",
            "Asset health dashboards with risk prioritization by criticality",
        ],
        "metrics": [("−40%", "Unplanned Downtime"), ("−30%", "Maintenance Cost"),
                    ("+25%", "Asset Lifespan"), ("5:1", "Measured ROI")],
        "systems": "IoT sensors · AWS IoT / Azure IoT Hub · SAP PM · CMMS · Asset historian",
        "users": "Maintenance Teams · Plant Engineers · Operations Managers",
        "stack": [
            ("EDGE / CAPTURE", "Vibration accelerometers · Acoustic emission sensors · Thermal cameras · Edge concentrators (AWS IoT Greengrass / Azure IoT Edge)"),
            ("COMPUTE / AI MODELS", "Autoencoder anomaly detection · Survival analysis (Weibull, DeepSurv) · Acoustic ML (audio CNN) · MLflow tracking"),
            ("INTEGRATION", "SAP PM · CMMS (Maximo) · Asset historian · Work-order auto-generation API"),
            ("UX / DECISION", "Asset health dashboard · Risk-prioritized work queue · Mobile technician app · Failure-cause analytics"),
        ],
        "hyundai_start": "Ulsan stamping presses + Asan welding cells — high-criticality assets where one unplanned hour ripples across the world's largest auto plant. 3–5 assets in pilot, scale to all critical lines on validation.",
    },
    {
        "n": "07",
        "title": "AI Safety Monitoring",
        "sub": "Vision AI Safety Surveillance",
        "color": TEAL,
        "challenge": "PPE non-compliance, restricted zone violations, and unsafe movements cause workplace injuries and EHS compliance failures that expose the plant to regulatory risk and production shutdowns.",
        "solution": "Vision AI monitors PPE compliance, restricted zone access, forklift interactions, and unsafe operator behavior. Real-time alerts are generated for violations, with audit-ready EHS reporting.",
        "capabilities": [
            "PPE detection — helmets, vests, goggles, gloves — per zone and shift",
            "Restricted area intrusion detection with instant alert escalation",
            "Unsafe movement and forklift proximity monitoring",
            "EHS compliance dashboards and audit-ready incident reporting",
        ],
        "metrics": [("−55%", "Safety Incidents"), ("98%", "PPE Compliance"),
                    ("<500ms", "Alert Latency"), ("Audit-Ready", "EHS Reports")],
        "systems": "Safety cameras · Edge AI processors · EHS platform · Incident management system",
        "users": "EHS Officers · Safety Teams · Plant Managers · Compliance Auditors",
        "stack": [
            ("EDGE / CAPTURE", "Wide-FOV safety cameras · Forklift onboard cams · Edge AI processors (Hailo / Jetson) · On-device person anonymization"),
            ("COMPUTE / AI MODELS", "PPE detector (YOLOv8 + custom heads) · Person-vehicle proximity tracker · Zone-violation rule engine"),
            ("INTEGRATION", "EHS platform · Incident management system · Andon/PA siren API · Access-control system"),
            ("UX / DECISION", "EHS live wall · Auto-incident report with video clip · Compliance scorecard · Audit export"),
        ],
    },
    {
        "n": "08",
        "title": "Digital Traceability & Tracking",
        "sub": "AI Traceability Platform",
        "color": TEAL_2,
        "challenge": "Lack of end-to-end component traceability makes defect root-cause analysis, recall management, and audit compliance slow, costly, and prone to gaps across the supply chain.",
        "solution": "AI integrates with MES, ERP, RFID, barcode, IoT, and vision systems to provide end-to-end traceability of every component, assembly, and production event across the manufacturing lifecycle.",
        "capabilities": [
            "End-to-end genealogy tracking from component to finished vehicle",
            "Real-time RFID and barcode scan integration with MES and ERP",
            "Defect root-cause traceability with drill-down to station and supplier",
            "Recall management and supplier quality chain tracking",
        ],
        "metrics": [("100%", "Part Traceability"), ("−70%", "Recall Investigation"),
                    ("Full", "Audit Trail"), ("QA", "Chain Coverage")],
        "systems": "RFID · Barcode scanners · SAP MES/ERP · IoT platform · Quality DB · Vision systems",
        "users": "Quality Directors · Supply Chain · Plant Managers · Compliance Teams",
        "stack": [
            ("EDGE / CAPTURE", "RFID readers (UHF) · Barcode / DataMatrix scanners · IoT sensors · Vision OCR stations"),
            ("COMPUTE / AI MODELS", "Genealogy graph DB (Neo4j) · Defect propagation ML model · Supplier risk scoring · Stream processing (Flink)"),
            ("INTEGRATION", "SAP MES/ERP · Supplier portals · Quality DB · IoT platform · Recall management system"),
            ("UX / DECISION", "Vehicle genealogy viewer · Root-cause drill-down · Recall scope calculator · Auditor export portal"),
        ],
    },
]

# ============================================================================
# BUILD
# ============================================================================
prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
blank_layout = prs.slide_layouts[6]

def new_slide():
    s = prs.slides.add_slide(blank_layout)
    add_rect(s, 0, 0, SLIDE_W, SLIDE_H, SLATE_50)  # bg
    return s

# ---------- SLIDE 1: COVER ----------
s = prs.slides.add_slide(blank_layout)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY_800)
add_rect(s, 0, 0, Inches(0.08), SLIDE_H, TEAL)
add_text(s, Inches(0.8), Inches(0.9), Inches(8), Inches(0.3),
         "AI-DRIVEN MANUFACTURING", font_size=12, color=SLATE_300, bold=True)
add_text(s, Inches(0.8), Inches(1.3), Inches(12), Inches(1.4),
         "AI for Plant Operations", font_size=54, color=WHITE, bold=True)
add_text(s, Inches(0.8), Inches(2.7), Inches(12), Inches(0.7),
         "Hyundai  ·  PeopleTech", font_size=30, color=SLATE_400)
add_rect(s, Inches(0.8), Inches(3.55), Inches(3.5), Inches(0.04), TEAL)
# 4 outcome chips in 2x2
chips = [
    "✓ Reduce defects & warranty claims",
    "✓ Cut unplanned downtime & rework",
    "✓ Enforce safety & SOP compliance",
    "✓ End-to-end traceability & quality data",
]
chip_w = Inches(5.2); chip_h = Inches(0.5)
for i, chip in enumerate(chips):
    cx = Inches(0.8 + (i % 2) * 5.4)
    cy = Inches(4.0 + (i // 2) * 0.65)
    add_rect(s, cx, cy, chip_w, chip_h, RGBColor(0x29, 0x36, 0x5F))
    add_rect(s, cx, cy, Inches(0.04), chip_h, TEAL)
    add_text(s, cx + Inches(0.2), cy, chip_w - Inches(0.25), chip_h,
             chip, font_size=12, color=SLATE_200, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.8), Inches(5.7), Inches(12), Inches(0.35),
         "Plant Directors · Operations Leaders · Quality Management",
         font_size=12, italic=True, color=SLATE_400)
add_text(s, Inches(0.8), Inches(6.1), Inches(12), Inches(0.3),
         "8 AI Use Cases · Visual Inspection · Predictive Maintenance · Safety · Quality & Traceability",
         font_size=10, color=SLATE_400)
add_text(s, Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.4),
         "01 / 17", font_size=9, color=SLATE_400,
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

# ---------- SLIDE 2: WHY PEOPLETECH ----------
s = new_slide()
std_header(s, "PRE-SALES POSITIONING", "Why PeopleTech for Hyundai",
           "Pre-Sales · AI Manufacturing Practice")
# Left: heading + lead + 3 strength cards
add_text(s, Inches(0.5), Inches(1.2), Inches(7.5), Inches(0.9),
         "A delivery partner built for industrial AI at plant scale.",
         font_size=24, color=NAVY_800, bold=True, line_spacing=1.15)
add_text(s, Inches(0.5), Inches(2.2), Inches(7.5), Inches(0.9),
         "PeopleTech is a global services company with deep practices across data engineering, computer vision, MLOps, and enterprise integration. We bring proven accelerators and a delivery model tuned for the realities of automotive manufacturing — uptime pressure, line-side latency, and zero-tolerance for defects reaching customers.",
         font_size=10.5, color=INK_SOFT, line_spacing=1.4)
# Hyundai-specific callout
add_rect(s, Inches(0.5), Inches(3.15), Inches(7.5), Inches(0.5), RGBColor(0xEC, 0xFD, 0xF5))
add_rect(s, Inches(0.5), Inches(3.15), Inches(0.06), Inches(0.5), TEAL)
add_text(s, Inches(0.68), Inches(3.15), Inches(7.2), Inches(0.5),
         "Hyundai already operates HMGICS Singapore as a smart-factory hub and has invested in AI via AIRS Company and Boston Dynamics. PeopleTech brings these innovations to production scale at Ulsan, Asan, HMGMA, HMMA, HMMC, HMI.",
         font_size=9.5, color=RGBColor(0x0D, 0x8A, 0x72), italic=True,
         line_spacing=1.35, anchor=MSO_ANCHOR.MIDDLE)
strengths = [
    ("End-to-end AI delivery, not just models",
     "Data pipelines, model training, edge deployment, integration with MES/ERP, dashboards, and Day-2 operations — under one accountable team."),
    ("Manufacturing & automotive domain depth",
     "Engineers who have shipped vision QA, predictive maintenance, and traceability stacks for Tier-1 OEMs and suppliers across Asia, Europe, and North America."),
    ("Hyperscaler & ISV partnerships",
     "AWS & Azure advanced partners. Pre-built integrations with SAP MES/ERP, OPC-UA, AVEVA PI, RFID, and major vision-camera ecosystems."),
]
for i, (h, p) in enumerate(strengths):
    y = Inches(3.85 + i * 0.95)
    add_rect(s, Inches(0.5), y, Inches(7.5), Inches(0.85), WHITE)
    add_rect(s, Inches(0.5), y, Inches(0.06), Inches(0.85), TEAL)
    add_text(s, Inches(0.68), y + Inches(0.08), Inches(7.2), Inches(0.3),
             h, font_size=11, color=NAVY_800, bold=True)
    add_text(s, Inches(0.68), y + Inches(0.35), Inches(7.2), Inches(0.5),
             p, font_size=9, color=INK_SOFT, line_spacing=1.4)
# Right: pillars card
add_rect(s, Inches(8.4), Inches(1.2), Inches(4.5), Inches(5.5), NAVY_800)
add_text(s, Inches(8.7), Inches(1.45), Inches(4), Inches(0.4),
         "WHAT WE BRING ON DAY 1", font_size=11, color=SLATE_300, bold=True)
pillars = [
    ("Reusable Accelerators", "Vision-AI Starter Kit, Industrial IoT reference architecture, MES connector library — cuts time-to-pilot by 40–60%."),
    ("Senior Delivery Pods", "Solution architect + ML lead + vision engineer + DevOps + plant-floor integration specialist. Embedded with Hyundai teams from week one."),
    ("Outcome Contracts", "Fixed-scope pilots with measurable KPIs. ROI proven in 8–12 weeks before any commitment to scale."),
    ("Run & Sustain Model", "Managed services for model retraining, drift monitoring, and 24×7 support once solutions are in production."),
]
for i, (h, p) in enumerate(pillars):
    y = Inches(2.0 + i * 1.15)
    add_text(s, Inches(8.7), y, Inches(4), Inches(0.35),
             h, font_size=13, color=WHITE, bold=True)
    add_text(s, Inches(8.7), y + Inches(0.4), Inches(4), Inches(0.7),
             p, font_size=9, color=SLATE_400, line_spacing=1.4)
slide_footer(s, 2)

# ---------- SLIDE 3: APPROACH ----------
s = new_slide()
std_header(s, "ENGAGEMENT MODEL", "Four-Phase Delivery Approach",
           "Discovery → Pilot → Scale → Run")
add_text(s, Inches(0.5), Inches(1.2), Inches(12), Inches(0.55),
         "De-risked path from first use case to plant-wide rollout",
         font_size=22, color=NAVY_800, bold=True)
add_text(s, Inches(0.5), Inches(1.85), Inches(12), Inches(0.85),
         "We never start with a multi-quarter program. We start by proving one use case end-to-end on a real line, then we scale what works. Each phase has fixed scope, fixed KPIs, and a go/no-go gate before the next. Designed for the scale of Ulsan (~1.6M vehicles/year, world's largest auto plant) and the production cadence of Metaplant America (IONIQ 5 / IONIQ 9 line).",
         font_size=11, color=INK_SOFT, line_spacing=1.4)
phase_colors = [TEAL, ORANGE, PURPLE, NAVY_700]
phases = [
    ("PHASE 01", "Discovery", "2–3 weeks", [
        "Plant-floor workshop & line walk-through",
        "Use case prioritization scorecard",
        "Data & systems landscape audit",
        "Pilot scope, KPIs, success criteria",
    ]),
    ("PHASE 02", "Pilot", "8–12 weeks", [
        "1–2 high-impact use cases on one line",
        "Data collection, model training, edge deploy",
        "MES & dashboard integration",
        "Measured ROI vs. baseline",
    ]),
    ("PHASE 03", "Scale", "3–6 months", [
        "Rollout across lines, shifts, and plants",
        "Hardening, retraining, A/B variants",
        "Operator & engineer enablement",
        "Cross-use-case data platform",
    ]),
    ("PHASE 04", "Run", "Ongoing", [
        "Managed services, 24×7 monitoring",
        "Drift detection & auto-retraining",
        "Quarterly value reviews",
        "Roadmap of next use cases",
    ]),
]
pw = Inches(2.95); ph = Inches(3.7); px = Inches(0.5); py = Inches(2.9)
for i, (num, name, meta, items) in enumerate(phases):
    x = px + (pw + Inches(0.18)) * i
    add_rect(s, x, py, pw, ph, WHITE)
    add_rect(s, x, py, pw, Inches(0.06), phase_colors[i])
    add_text(s, x + Inches(0.2), py + Inches(0.18), pw - Inches(0.3), Inches(0.25),
             num, font_size=9, color=INK_MUTE, bold=True)
    add_text(s, x + Inches(0.2), py + Inches(0.45), pw - Inches(0.3), Inches(0.5),
             name, font_size=20, color=NAVY_800, bold=True)
    add_text(s, x + Inches(0.2), py + Inches(0.95), pw - Inches(0.3), Inches(0.3),
             meta, font_size=9, color=INK_MUTE, italic=True)
    add_bullets(s, x + Inches(0.2), py + Inches(1.3), pw - Inches(0.3), ph - Inches(1.4),
                items, font_size=10, bullet_char="→", line_spacing=1.4)
slide_footer(s, 3)

# ---------- SLIDES 4-11: USE CASES ----------
for idx, uc in enumerate(USE_CASES):
    n = 4 + idx
    s = new_slide()
    uc_band(s, uc["color"], f"USE CASE {uc['n']}", uc["title"], uc["sub"])
    # LEFT COLUMN: Challenge, Solution, Capabilities cards
    lx = Inches(0.5); lw = Inches(7.0)
    card(s, lx, Inches(1.1), lw, Inches(1.2),
         "CHALLENGE", body_text=uc["challenge"], accent=RED, label_color=RED)
    card(s, lx, Inches(2.45), lw, Inches(1.2),
         "SOLUTION", body_text=uc["solution"], accent=uc["color"])
    card(s, lx, Inches(3.8), lw, Inches(1.8),
         "CAPABILITIES", body_bullets=uc["capabilities"], accent=uc["color"])
    # RIGHT COLUMN: Business Value 2x2, Systems, Users
    rx = Inches(7.7); rw = Inches(5.1)
    add_text(s, rx, Inches(1.1), rw, Inches(0.25),
             "BUSINESS VALUE", font_size=9, color=INK_MUTE, bold=True)
    tile_w = Inches(2.5); tile_h = Inches(0.95)
    for mi, (val, lbl) in enumerate(uc["metrics"]):
        tx = rx + (tile_w + Inches(0.1)) * (mi % 2)
        ty = Inches(1.4) + (tile_h + Inches(0.1)) * (mi // 2)
        metric_tile(s, tx, ty, tile_w, tile_h, val, lbl, uc["color"])
    meta_card(s, rx, Inches(3.55), rw, Inches(0.85),
              "SYSTEMS INTEGRATED", uc["systems"])
    meta_card(s, rx, Inches(4.5), rw, Inches(0.65),
              "TARGET USERS", uc["users"])
    # Optional Hyundai start card (UC-01 and UC-06 only)
    if uc.get("hyundai_start"):
        add_rect(s, rx, Inches(5.25), rw, Inches(0.45), RGBColor(0xEC, 0xFD, 0xF5))
        add_rect(s, rx, Inches(5.25), Inches(0.06), Inches(0.45), TEAL)
        add_text(s, rx + Inches(0.15), Inches(5.27), rw - Inches(0.2), Inches(0.18),
                 "RECOMMENDED HYUNDAI START", font_size=8,
                 color=RGBColor(0x0D, 0x8A, 0x72), bold=True)
        add_text(s, rx + Inches(0.15), Inches(5.43), rw - Inches(0.2), Inches(0.27),
                 uc["hyundai_start"], font_size=8.5, color=INK, line_spacing=1.3)
    # BOTTOM STRIP: solution stack
    stack_strip(s, Inches(0.5), Inches(5.75), Inches(12.3), Inches(1.15), uc["stack"])
    slide_footer(s, n)

# ---------- SLIDE 12: CASE STUDIES ----------
s = new_slide()
std_header(s, "PROOF OF DELIVERY", "Reference Case Studies",
           "Manufacturing & Automotive Portfolio")
cases = [
    {"color": TEAL, "industry": "TIER-1 AUTOMOTIVE OEM",
     "title": "Paint defect CV pilot scaled to 4 lines in 18 weeks",
     "challenge": "Manual paint inspection missed ~12% of surface defects; rework rate above 8% on premium SUV line.",
     "solution": "Edge AI cameras + CNN anomaly model integrated with MES line-hold; closed-loop retraining from rework data.",
     "stack": "Cognex cameras · Jetson edge · AWS SageMaker · MES connector · React quality dashboard",
     "outcome": "−58% escape defects, −42% rework cost, 14-month payback"},
    {"color": NAVY_700, "industry": "GLOBAL EV MANUFACTURER",
     "title": "Predictive maintenance across stamping & weld shops",
     "challenge": "Unplanned downtime on press lines averaging 6.4 hrs/week; reactive maintenance dominated budget.",
     "solution": "Vibration + acoustic sensor mesh feeding autoencoder + survival models; auto-generated work orders in SAP PM.",
     "stack": "Azure IoT Hub · Azure ML · MLflow · SAP PM · Power BI asset health",
     "outcome": "−38% unplanned downtime, 5.2:1 ROI in year one"},
    {"color": ORANGE, "industry": "AEROSPACE TIER-1 SUPPLIER",
     "title": "SOP compliance with pose estimation on assembly cells",
     "challenge": "Complex multi-step assembly with high audit burden; manual SOP checks slowed cycle time and missed deviations.",
     "solution": "Multi-camera pose-estimation pipeline matched to SOP graph; live deviation alerts; auto-generated compliance audit pack.",
     "stack": "MoveNet + custom action classifier · NVIDIA Triton · MES · EHS compliance system",
     "outcome": "96% SOP compliance, audit prep time cut by 70%"},
    {"color": PURPLE, "industry": "HEAVY EQUIPMENT MANUFACTURER",
     "title": "RFID + vision traceability across 11 plants",
     "challenge": "Field recall investigations took 4–6 weeks; component genealogy fragmented across regional systems.",
     "solution": "Unified traceability platform with RFID, barcode, and vision OCR feeding a Neo4j genealogy graph integrated with SAP.",
     "stack": "UHF RFID · Datalogic scanners · Neo4j · Apache Flink · SAP MES/ERP",
     "outcome": "Recall investigation time cut from weeks to days; full audit trail"},
]
cw = Inches(6.15); ch = Inches(2.85)
for i, c in enumerate(cases):
    x = Inches(0.5) + (cw + Inches(0.2)) * (i % 2)
    y = Inches(1.15) + (ch + Inches(0.2)) * (i // 2)
    add_rect(s, x, y, cw, ch, WHITE)
    add_rect(s, x, y, cw, Inches(0.06), c["color"])
    add_text(s, x + Inches(0.25), y + Inches(0.18), cw - Inches(0.4), Inches(0.25),
             c["industry"], font_size=9, color=INK_MUTE, bold=True)
    add_text(s, x + Inches(0.25), y + Inches(0.45), cw - Inches(0.4), Inches(0.5),
             c["title"], font_size=14, color=NAVY_800, bold=True, line_spacing=1.2)
    for ri, (k, v) in enumerate([("Challenge", c["challenge"]),
                                  ("Solution", c["solution"]),
                                  ("Stack", c["stack"])]):
        ry = y + Inches(1.05) + Inches(0.45) * ri
        add_text(s, x + Inches(0.25), ry, Inches(0.9), Inches(0.4),
                 k.upper(), font_size=8, color=INK_MUTE, bold=True)
        add_text(s, x + Inches(1.2), ry, cw - Inches(1.5), Inches(0.45),
                 v, font_size=9, color=INK, line_spacing=1.35)
    # Outcome strip
    oy = y + ch - Inches(0.5)
    add_rect(s, x + Inches(0.2), oy, cw - Inches(0.4), Inches(0.4), NAVY_800)
    add_text(s, x + Inches(0.35), oy, cw - Inches(0.5), Inches(0.4),
             f"Outcome:  {c['outcome']}", font_size=10, color=WHITE, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
slide_footer(s, 12)

# ---------- SLIDE 13: ACCELERATORS ----------
s = new_slide()
std_header(s, "REUSABLE IP", "Accelerators & Frameworks",
           "Cut time-to-pilot by 40–60%")
add_text(s, Inches(0.5), Inches(1.1), Inches(12.3), Inches(0.6),
         "PeopleTech invests in productized assets so every engagement starts from a higher baseline. Below are the six accelerators most relevant to Hyundai's stated use case set — each is field-proven, customer-tested, and licensed under the engagement.",
         font_size=11, color=INK_SOFT, line_spacing=1.4)
accels = [
    (TEAL, "VK", "Vision-AI Starter Kit",
     "Pre-trained CNN backbones (ResNet, EfficientNet, YOLOv8), labeling templates, dataset versioning, and inference scaffolds for defect, OCR, and pose tasks. Ships with reference training pipelines on SageMaker and Azure ML."),
    (NAVY_700, "IRA", "Industrial IoT Reference Architecture",
     "OPC-UA gateway templates, edge compute patterns (AWS IoT Greengrass / Azure IoT Edge), time-series ingestion to historian + lake, and proven sensor onboarding playbooks."),
    (ORANGE, "MES", "MES / SAP Integration Connector Library",
     "Production-grade connectors for SAP MES/ERP, SAP PM, AVEVA PI, Maximo CMMS, and major MES vendors. Standardized event schemas for line-hold, work-order generation, and quality events."),
    (PURPLE, "MLO", "MLOps Blueprint (AWS & Azure)",
     "End-to-end pattern for model training, registry, deployment, drift monitoring, and auto-retraining. Includes CI/CD pipelines, feature store templates, and explainability hooks."),
    (RED, "EDT", "Edge Deployment Toolkit",
     "Model optimization (TensorRT, ONNX, OpenVINO), OTA update framework, edge fleet management, and observability across Jetson, Hailo, and Intel edge platforms. <200ms latency."),
    (TEAL, "TGP", "Traceability Graph Platform",
     "Neo4j-based genealogy schema, RFID/barcode/vision ingestion adapters, recall scope calculator, and supplier quality chain tracking. Cuts recall investigation from weeks to days."),
]
aw = Inches(6.15); ah = Inches(1.45)
for i, (col, ic, h, p) in enumerate(accels):
    x = Inches(0.5) + (aw + Inches(0.2)) * (i % 2)
    y = Inches(2.0) + (ah + Inches(0.15)) * (i // 2)
    add_rect(s, x, y, aw, ah, WHITE)
    add_rect(s, x, y, Inches(0.06), ah, col)
    add_rect(s, x + Inches(0.2), y + Inches(0.2), Inches(0.6), Inches(0.6), NAVY_800)
    add_text(s, x + Inches(0.2), y + Inches(0.2), Inches(0.6), Inches(0.6),
             ic, font_size=12, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, x + Inches(0.95), y + Inches(0.2), aw - Inches(1.1), Inches(0.35),
             h, font_size=12, color=NAVY_800, bold=True)
    add_text(s, x + Inches(0.95), y + Inches(0.55), aw - Inches(1.1), ah - Inches(0.6),
             p, font_size=9, color=INK_SOFT, line_spacing=1.4)
slide_footer(s, 13)

# ---------- SLIDE 14: CV CAPABILITIES MATRIX ----------
s = new_slide()
std_header(s, "CAPABILITY MATRIX", "AI Computer Vision Capabilities",
           "Models · Maturity · Hyundai Use Case Mapping")
add_text(s, Inches(0.5), Inches(1.1), Inches(12.3), Inches(0.6),
         "Our vision-AI practice covers the full spectrum of plant-floor tasks Hyundai needs. The matrix below maps each capability to the model families we deploy, our delivery maturity, and the specific Hyundai use case it powers.",
         font_size=11, color=INK_SOFT, line_spacing=1.4)
rows = [
    ("Defect & anomaly detection", "ResNet50 · EfficientNet · PatchCore · custom CNN anomaly heads", "Production", "UC-01 Visual Inspection · UC-05 Predictive Quality"),
    ("Object detection", "YOLOv8 / YOLOv9 · DETR · RT-DETR", "Production", "UC-02 Variant · UC-03 Seating · UC-07 Safety (PPE)"),
    ("OCR & VIN / barcode reading", "PaddleOCR · TrOCR · DataMan SDK · custom OCR + barcode decoders", "Production", "UC-02 Variant Confirmation · UC-08 Traceability"),
    ("Pose estimation", "MoveNet · MMPose · OpenPose · BlazePose", "Production", "UC-04 SOP Compliance · UC-07 Safety (unsafe movement)"),
    ("Action / activity recognition", "SlowFast · MViT · TimeSformer · custom temporal heads", "Pilot", "UC-04 SOP Compliance · UC-07 Safety (forklift)"),
    ("Semantic / instance segmentation", "SAM / SAM 2 · Mask R-CNN · Segformer · Mask2Former", "Production", "UC-01 Visual Inspection · UC-03 Seating Validation"),
    ("Vision-language models (zero-shot)", "CLIP · ViT · LLaVA · GPT-4o vision · Claude Vision", "Pilot", "Cross-cutting: rapid prototyping, audit Q&A"),
    ("Multi-modal anomaly (vision+sensor)", "Cross-modal transformers · gated fusion · time-aligned ViT", "PoC", "UC-05 Predictive Quality · UC-06 Predictive Maintenance"),
]
tx = Inches(0.5); ty = Inches(1.95)
tw = Inches(12.3); th = Inches(4.85)
table = s.shapes.add_table(len(rows) + 1, 4, tx, ty, tw, th).table
table.columns[0].width = Inches(2.7)
table.columns[1].width = Inches(4.0)
table.columns[2].width = Inches(1.5)
table.columns[3].width = Inches(4.1)
headers = ["CAPABILITY", "MODELS WE DEPLOY", "MATURITY", "HYUNDAI USE CASE MAPPING"]
for ci, htxt in enumerate(headers):
    cell = table.cell(0, ci)
    cell.fill.solid(); cell.fill.fore_color.rgb = NAVY_800
    cell.margin_left = Emu(60000); cell.margin_right = Emu(60000)
    cell.margin_top = Emu(40000); cell.margin_bottom = Emu(40000)
    tf = cell.text_frame; tf.clear()
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = htxt
    r.font.name = FONT; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = WHITE
maturity_colors = {"Production": (RGBColor(0xD1, 0xFA, 0xE5), RGBColor(0x06, 0x5F, 0x46)),
                   "Pilot": (RGBColor(0xFE, 0xF3, 0xC7), RGBColor(0x92, 0x40, 0x0E)),
                   "PoC": (RGBColor(0xED, 0xE9, 0xFE), RGBColor(0x5B, 0x21, 0xB6))}
for ri, row in enumerate(rows):
    for ci, val in enumerate(row):
        cell = table.cell(ri + 1, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SLATE_50 if ri % 2 == 0 else WHITE
        cell.margin_left = Emu(60000); cell.margin_right = Emu(60000)
        cell.margin_top = Emu(50000); cell.margin_bottom = Emu(50000)
        tf = cell.text_frame; tf.clear()
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = val
        r.font.name = FONT; r.font.size = Pt(10)
        if ci == 0:
            r.font.color.rgb = NAVY_800; r.font.bold = True
        elif ci == 2:
            bg, fg = maturity_colors[val]
            cell.fill.solid(); cell.fill.fore_color.rgb = bg
            r.font.color.rgb = fg; r.font.bold = True; r.font.size = Pt(9)
        else:
            r.font.color.rgb = INK
slide_footer(s, 14)

# ---------- SLIDE 15: SUMMARY ----------
s = prs.slides.add_slide(blank_layout)
add_rect(s, 0, 0, SLIDE_W, SLIDE_H, NAVY_800)
add_rect(s, 0, 0, Inches(0.08), SLIDE_H, TEAL)
add_text(s, Inches(0.8), Inches(0.7), Inches(8), Inches(0.3),
         "STRATEGIC SUMMARY", font_size=11, color=SLATE_300, bold=True)
add_text(s, Inches(0.8), Inches(1.1), Inches(12), Inches(1.0),
         "AI-Driven Manufacturing", font_size=44, color=WHITE, bold=True)
add_text(s, Inches(0.8), Inches(2.05), Inches(12), Inches(0.7),
         "8 use cases · Built for Hyundai plant ops",
         font_size=22, color=SLATE_400)
add_rect(s, Inches(0.8), Inches(2.95), Inches(3.3), Inches(0.04), TEAL)
bullets = [
    "8 use cases mapped to Hyundai's stated key areas — visual inspection, predictive quality, maintenance, safety, traceability.",
    "Edge AI + cloud architecture on AWS / Azure — production-ready, line-side latency <200ms, scalable from one line to enterprise.",
    "Integration-first: MES, ERP, RFID, IoT, and vision stacks — no rip-and-replace, no parallel systems of record.",
    "Start with 2 pilots — Visual Inspection at HMGMA (IONIQ paint) + Predictive Maintenance at Ulsan stamping / Asan welding. ROI proven in 12 weeks, then scale across the global Hyundai plant network.",
]
for i, b in enumerate(bullets):
    y = Inches(3.4 + i * 0.6)
    add_text(s, Inches(0.8), y, Inches(0.4), Inches(0.5),
             "→", font_size=18, color=TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.2), y, Inches(11.5), Inches(0.55),
             b, font_size=14, color=SLATE_200, line_spacing=1.4, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.8), Inches(6.0), Inches(12), Inches(0.4),
         "Ready to build? Let's pick the first use case and move fast.",
         font_size=16, color=TEAL, italic=True, bold=True)
add_text(s, Inches(0.8), Inches(6.5), Inches(12), Inches(0.35),
         "Next step: Pilot scoping workshop with PeopleTech's AI Manufacturing practice.",
         font_size=12, color=SLATE_300)
add_text(s, Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.4),
         "15 / 17", font_size=9, color=SLATE_400,
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

# ---------- SLIDE 16: VISUAL INSPECTION ARCHITECTURE (APPENDIX) ----------
s = new_slide()
add_rect(s, 0, 0, SLIDE_W, Inches(0.7), NAVY_800)
add_text(s, Inches(0.5), 0, Inches(2.5), Inches(0.7),
         "APPENDIX · PILOT 1", font_size=10, color=SLATE_300, bold=True,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(3), 0, Inches(7), Inches(0.7),
         "Visual Inspection — Reference Architecture", font_size=18, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(10), 0, Inches(2.8), Inches(0.7),
         "HMGMA · IONIQ paint shop", font_size=10, color=SLATE_300,
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, italic=True)
# Architecture diagram image
s.shapes.add_picture("architecture_visual_inspection.png",
                     Inches(0.4), Inches(0.85),
                     width=Inches(12.5), height=Inches(6.1))
slide_footer(s, 16)

# ---------- SLIDE 17: PREDICTIVE MAINTENANCE ARCHITECTURE (APPENDIX) ----------
s = new_slide()
add_rect(s, 0, 0, SLIDE_W, Inches(0.7), NAVY_800)
add_text(s, Inches(0.5), 0, Inches(2.5), Inches(0.7),
         "APPENDIX · PILOT 2", font_size=10, color=SLATE_300, bold=True,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(3), 0, Inches(7), Inches(0.7),
         "Predictive Maintenance — Reference Architecture", font_size=18, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(10), 0, Inches(2.8), Inches(0.7),
         "Ulsan stamping · Asan welding", font_size=10, color=SLATE_300,
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, italic=True)
s.shapes.add_picture("architecture_predictive_maintenance.png",
                     Inches(0.4), Inches(0.85),
                     width=Inches(12.5), height=Inches(6.1))
slide_footer(s, 17)

# ============================================================================
# SAVE
# ============================================================================
out = "Hyundai_PeopleTech_AI_Plant_Operations.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
