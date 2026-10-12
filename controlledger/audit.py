from __future__ import annotations

import csv
import io
from datetime import date

from .controls import required_controls
from .evidence import checklist
from .models import Evidence, UseCase
from .rules import classify


def portfolio(systems: list[UseCase], all_evidence: list[Evidence], on: date) -> list[dict]:
    rows = []
    for system in systems:
        result = classify(system)
        checks = checklist(system.system_id, required_controls(result), all_evidence, on)
        current = sum(row["status"] == "current" for row in checks)
        rows.append({"system_id": system.system_id, "name": system.name, "version": system.version, "tier": result.tier, "rule_version": result.rule_version, "controls_current": current, "controls_required": len(checks), "evidence_complete": current == len(checks)})
    return rows


def csv_export(rows: list[dict]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]) if rows else [])
    if rows:
        writer.writeheader()
        writer.writerows(rows)
    return output.getvalue()
