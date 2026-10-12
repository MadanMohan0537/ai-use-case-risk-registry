from __future__ import annotations

from dataclasses import replace
from datetime import date

from .audit import csv_export, portfolio
from .changes import reclassification_trigger
from .controls import required_controls
from .fixtures import systems
from .models import Evidence
from .rules import classify


def run_demo() -> dict:
    baseline = systems()
    evidence = [Evidence("faq", "inventory-owner", "owner-signoff.md", "2026-01-01", "2026-12-31", "governance")]
    rows = portfolio(baseline, evidence, date(2026, 10, 12))
    low = baseline[0]
    seeded = [
        replace(low, version=2, autonomy="fully-automated"),
        replace(low, version=2, data_categories=("public", "biometric")),
        replace(low, version=2, users=("customers", "children")),
        replace(low, version=2, purpose="Decide eligibility", decision_impact="eligibility", domain="public-benefits"),
    ]
    triggers = [reclassification_trigger(low, item) for item in seeded]
    return {
        "systems": len(baseline),
        "tiers": {row["tier"]: sum(item["tier"] == row["tier"] for item in rows) for row in rows},
        "portfolio": rows,
        "evidence_completion_rate": sum(row["evidence_complete"] for row in rows) / len(rows),
        "scope_change_experiment": {"seeded": len(seeded), "reopened": sum(item["material"] and bool(item["reopen_controls"]) for item in triggers), "false_negatives": sum(not item["material"] for item in triggers), "results": triggers},
        "control_counts": {system.system_id: len(required_controls(classify(system))) for system in baseline},
        "csv": csv_export(rows),
    }
