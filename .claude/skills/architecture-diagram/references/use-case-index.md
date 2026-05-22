# Use Case Architecture Index

| UC | Name | Key components | Edge integration |
|----|------|---------------|-----------------|
| 01 | Visual Inspection | Camera array, CNN inference, defect classification | MES quality gate |
| 02 | Variant Confirmation | Barcode/RFID scan, model matching, BOM validation | MES work order |
| 03 | Seating Validation | Force sensors, torque verification, position check | GQMS record |
| 04 | SOP Compliance | Pose estimation, action sequence matching, alert | Safety system |
| 05 | Predictive Quality | SPC data, ML anomaly detection, trend analysis | GQMS early warning |
| 06 | Predictive Maintenance | Vibration/temp sensors, degradation model, scheduling | CMMS work order |
| 07 | Safety Monitoring | Camera feeds, zone detection, PPE compliance | EHS alert system |
| 08 | Digital Traceability | End-to-end part tracking, genealogy graph, recall support | Blockchain ledger |

## Common architecture pattern

All use cases follow: `Edge Sensor -> Data Ingestion -> AI Pipeline -> Business Logic -> Integration Layer -> Hyundai System`
