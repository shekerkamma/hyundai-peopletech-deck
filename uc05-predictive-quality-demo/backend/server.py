#!/usr/bin/env python3
"""UC05 Predictive Quality demo backend.

Runs with Python standard library only:

    python3 backend/server.py

The server exposes JSON APIs, persists events/incidents/model versions in
SQLite, and mirrors the browser-side scoring model so the demo has a real data
layer behind it.
"""

from __future__ import annotations

import json
import math
import random
import sqlite3
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "quality_demo.sqlite3"


VARIANTS: dict[str, dict[str, Any]] = {
    "ioniq5": {
        "code": "NE",
        "name": "IONIQ 5 · EV crossover",
        "stations": [
            {"id": "body-weld", "name": "Body weld", "metric": "gap_variance_mm", "mean": 0.18, "sigma": 0.035, "limit": 0.34, "drift": 0.045, "speed": 0.036},
            {"id": "battery-seal", "name": "Battery seal", "metric": "thermal_leak_index", "mean": 0.11, "sigma": 0.032, "limit": 0.27, "drift": 0.06, "speed": 0.022},
            {"id": "paint-booth", "name": "Paint booth", "metric": "film_drift_index", "mean": 0.21, "sigma": 0.044, "limit": 0.41, "drift": 0.052, "speed": 0.034},
            {"id": "final-torque", "name": "Final torque", "metric": "torque_residual_nm", "mean": 0.16, "sigma": 0.038, "limit": 0.32, "drift": 0.038, "speed": 0.05},
        ],
    },
    "santafe": {
        "code": "MX5",
        "name": "Santa Fe · SUV",
        "stations": [
            {"id": "body-weld", "name": "Body weld", "metric": "gap_variance_mm", "mean": 0.2, "sigma": 0.042, "limit": 0.4, "drift": 0.052, "speed": 0.038},
            {"id": "door-fitment", "name": "Door fitment", "metric": "flushness_delta_mm", "mean": 0.15, "sigma": 0.036, "limit": 0.31, "drift": 0.044, "speed": 0.032},
            {"id": "paint-booth", "name": "Paint booth", "metric": "orange_peel_index", "mean": 0.18, "sigma": 0.04, "limit": 0.38, "drift": 0.058, "speed": 0.03},
            {"id": "final-torque", "name": "Final torque", "metric": "torque_residual_nm", "mean": 0.18, "sigma": 0.04, "limit": 0.35, "drift": 0.04, "speed": 0.052},
        ],
    },
    "palisade": {
        "code": "LX3",
        "name": "Palisade · large SUV",
        "stations": [
            {"id": "body-weld", "name": "Body weld", "metric": "gap_variance_mm", "mean": 0.24, "sigma": 0.046, "limit": 0.46, "drift": 0.054, "speed": 0.042},
            {"id": "seat-install", "name": "Seat install", "metric": "mounting_offset_mm", "mean": 0.17, "sigma": 0.034, "limit": 0.33, "drift": 0.042, "speed": 0.028},
            {"id": "paint-booth", "name": "Paint booth", "metric": "film_drift_index", "mean": 0.2, "sigma": 0.042, "limit": 0.4, "drift": 0.06, "speed": 0.032},
            {"id": "final-torque", "name": "Final torque", "metric": "torque_residual_nm", "mean": 0.2, "sigma": 0.044, "limit": 0.38, "drift": 0.044, "speed": 0.056},
        ],
    },
}


@dataclass
class StationResult:
    station_id: str
    station_name: str
    metric: str
    value: float
    limit: float
    score: int
    z_score: float
    status: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
              id TEXT PRIMARY KEY,
              created_at TEXT NOT NULL,
              variant_id TEXT NOT NULL,
              variant_name TEXT NOT NULL,
              line_speed INTEGER NOT NULL,
              drift REAL NOT NULL,
              escape_risk INTEGER NOT NULL,
              status TEXT NOT NULL,
              action TEXT NOT NULL,
              payload TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS incidents (
              id TEXT PRIMARY KEY,
              created_at TEXT NOT NULL,
              event_id TEXT NOT NULL,
              severity TEXT NOT NULL,
              title TEXT NOT NULL,
              recommendation TEXT NOT NULL,
              payload TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS model_versions (
              id TEXT PRIMARY KEY,
              created_at TEXT NOT NULL,
              status TEXT NOT NULL,
              variant_id TEXT,
              notes TEXT NOT NULL,
              metrics TEXT NOT NULL
            );
            """
        )
        existing = conn.execute("SELECT COUNT(*) FROM model_versions").fetchone()[0]
        if existing == 0:
            conn.execute(
                "INSERT INTO model_versions VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "body-weld-risk-v1.0",
                    now_iso(),
                    "production",
                    None,
                    "Baseline model from historical SDF quality records.",
                    json.dumps({"precision": 0.94, "recall": 0.91, "latency_ms_p95": 126}),
                ),
            )


def score_station(station: dict[str, Any], value: float) -> StationResult:
    z_score = (value - station["mean"]) / station["sigma"]
    threshold_ratio = value / station["limit"]
    score = max(0, min(99, 22 + z_score * 17 + threshold_ratio * 28))
    status = "clear"
    if score >= 82 or value >= station["limit"] * 1.04:
      status = "hold"
    elif score >= 62 or value >= station["limit"] * 0.92:
      status = "inspect"

    return StationResult(
        station_id=station["id"],
        station_name=station["name"],
        metric=station["metric"],
        value=round(value, 4),
        limit=station["limit"],
        score=round(score),
        z_score=round(z_score, 3),
        status=status,
    )


def generate_event(variant_id: str, line_speed: int, drift: float) -> dict[str, Any]:
    variant = VARIANTS.get(variant_id, VARIANTS["ioniq5"])
    speed_pressure = max(0, min(1, (line_speed - 42) / 26))
    sequence = int(time.time() * 1000) % 100000
    station_results: list[StationResult] = []

    for index, station in enumerate(variant["stations"]):
        wave = math.sin(sequence * 0.019 + index * 0.9) * station["sigma"] * 0.45
        value = random.gauss(
            station["mean"] + drift * station["drift"] + speed_pressure * station["speed"] + wave,
            station["sigma"],
        )
        station_results.append(score_station(station, value))

    max_score = max(result.score for result in station_results)
    avg_score = round(sum(result.score for result in station_results) / len(station_results))
    escape_risk = round(max_score * 0.65 + avg_score * 0.35)
    status_rank = {"clear": 0, "inspect": 1, "hold": 2}
    status = max((result.status for result in station_results), key=lambda value: status_rank[value])
    action = {"clear": "CONTINUE", "inspect": "INSPECT_NEXT_UNIT", "hold": "HOLD_AND_REWORK"}[status]

    event_id = f"{variant['code']}-{sequence}-{uuid.uuid4().hex[:6]}"
    payload = {
        "event_id": event_id,
        "timestamp": now_iso(),
        "plant": "Ulsan Plant 5",
        "line_id": "SDF-LINE-03",
        "vin": f"KM8{uuid.uuid4().hex[:14].upper()}",
        "model_variant": variant["name"],
        "work_order": f"WO-{random.randint(880000, 889999)}",
        "shift": random.choice(["A", "B", "C"]),
        "line_speed": line_speed,
        "drift_level": drift,
        "station_results": [result.__dict__ for result in station_results],
        "prediction": {
            "escape_risk": escape_risk,
            "status": status,
            "model_version": "body-weld-risk-v1.0",
            "reason_codes": reason_codes(station_results),
        },
        "mes_action": {
            "action": action,
            "quality_gate": "QG-SDF-03",
            "ticket_id": f"RWK-{random.randint(900000, 909999)}" if status == "hold" else None,
        },
    }

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event_id,
                payload["timestamp"],
                variant_id,
                variant["name"],
                line_speed,
                drift,
                escape_risk,
                status,
                action,
                json.dumps(payload),
            ),
        )

    if status == "hold":
        create_incident(payload)

    return payload


def reason_codes(station_results: list[StationResult]) -> list[str]:
    codes: list[str] = []
    for result in station_results:
        if result.value >= result.limit:
            codes.append(f"{result.metric}_above_limit")
        elif result.status != "clear":
            codes.append(f"{result.metric}_drift_warning")
    return codes or ["within_variant_thresholds"]


def create_incident(event: dict[str, Any]) -> dict[str, Any]:
    incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
    worst = max(event["station_results"], key=lambda result: result["score"])
    payload = {
        "id": incident_id,
        "created_at": now_iso(),
        "event_id": event["event_id"],
        "severity": "high",
        "title": f"Quality hold triggered at {worst['station_name']}",
        "recommendation": "Hold unit, inspect station telemetry, and require quality engineer sign-off before release.",
        "evidence": {
            "vin": event["vin"],
            "variant": event["model_variant"],
            "escape_risk": event["prediction"]["escape_risk"],
            "worst_station": worst,
            "mes_action": event["mes_action"],
        },
    }
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                payload["id"],
                payload["created_at"],
                payload["event_id"],
                payload["severity"],
                payload["title"],
                payload["recommendation"],
                json.dumps(payload),
            ),
        )
    return payload


def rows_to_payloads(rows: list[tuple[Any, ...]]) -> list[dict[str, Any]]:
    return [json.loads(row[-1]) for row in rows]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_common_headers()
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path == "/api/health":
            self.write_json({"ok": True, "db": str(DB_PATH), "variants": list(VARIANTS)})
        elif parsed.path == "/api/variants":
            self.write_json({"variants": VARIANTS})
        elif parsed.path == "/api/events":
            limit = int(query.get("limit", ["25"])[0])
            with sqlite3.connect(DB_PATH) as conn:
                rows = conn.execute(
                    "SELECT * FROM events ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            self.write_json({"events": rows_to_payloads(rows)})
        elif parsed.path == "/api/incidents":
            with sqlite3.connect(DB_PATH) as conn:
                rows = conn.execute(
                    "SELECT * FROM incidents ORDER BY created_at DESC LIMIT 25"
                ).fetchall()
            self.write_json({"incidents": rows_to_payloads(rows)})
        elif parsed.path == "/api/model-versions":
            with sqlite3.connect(DB_PATH) as conn:
                rows = conn.execute(
                    "SELECT id, created_at, status, variant_id, notes, metrics FROM model_versions ORDER BY created_at DESC"
                ).fetchall()
            self.write_json({
                "model_versions": [
                    {
                        "id": row[0],
                        "created_at": row[1],
                        "status": row[2],
                        "variant_id": row[3],
                        "notes": row[4],
                        "metrics": json.loads(row[5]),
                    }
                    for row in rows
                ]
            })
        elif parsed.path == "/api/events/stream":
            self.stream_events(query)
        else:
            self.write_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        body = self.read_json()
        if parsed.path == "/api/events/generate":
            event = generate_event(
                body.get("variant_id", "ioniq5"),
                int(body.get("line_speed", 54)),
                float(body.get("drift", 0)),
            )
            self.write_json({"event": event})
        elif parsed.path == "/api/model-versions/retrain":
            version = f"body-weld-risk-v1.{int(time.time()) % 1000}"
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    "INSERT INTO model_versions VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        version,
                        now_iso(),
                        "shadow",
                        body.get("variant_id"),
                        "Candidate generated from latest event and incident telemetry.",
                        json.dumps({"precision": 0.945, "recall": 0.925, "latency_ms_p95": 132}),
                    ),
                )
            self.write_json({"model_version": version, "status": "shadow"})
        else:
            self.write_json({"error": "not found"}, status=404)

    def stream_events(self, query: dict[str, list[str]]) -> None:
        variant_id = query.get("variant_id", ["ioniq5"])[0]
        line_speed = int(query.get("line_speed", ["54"])[0])
        drift = float(query.get("drift", ["0"])[0])
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_common_headers()
        self.end_headers()
        for _ in range(20):
            event = generate_event(variant_id, line_speed, drift)
            self.wfile.write(f"data: {json.dumps(event)}\n\n".encode("utf-8"))
            self.wfile.flush()
            time.sleep(1)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def write_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_common_headers()
        self.end_headers()
        self.wfile.write(body)

    def send_common_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format: str, *args: Any) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8025), Handler)
    print("UC05 backend running on http://127.0.0.1:8025")
    server.serve_forever()


if __name__ == "__main__":
    main()
