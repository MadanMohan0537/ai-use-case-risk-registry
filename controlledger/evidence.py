from __future__ import annotations

from datetime import date

from .models import Control, Evidence


def evidence_status(control: Control, evidence: Evidence | None, on: date) -> str:
    if evidence is None:
        return "missing"
    if date.fromisoformat(evidence.expires_on) < on:
        return "expired"
    return "current"


def checklist(system_id: str, controls: list[Control], evidence: list[Evidence], on: date) -> list[dict]:
    by_control = {item.control_id: item for item in evidence if item.system_id == system_id}
    return [{"control_id": c.control_id, "title": c.title, "status": evidence_status(c, by_control.get(c.control_id), on)} for c in controls]
