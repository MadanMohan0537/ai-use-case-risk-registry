from __future__ import annotations

from .models import UseCase

MATERIAL_FIELDS = ("purpose", "users", "data_categories", "autonomy", "decision_impact", "domain")


def scope_diff(before: UseCase, after: UseCase) -> dict:
    if before.system_id != after.system_id:
        raise ValueError("system_id cannot change")
    changes = {}
    for field in MATERIAL_FIELDS:
        old, new = getattr(before, field), getattr(after, field)
        if old != new:
            changes[field] = {"before": old, "after": new}
    return changes


def reclassification_trigger(before: UseCase, after: UseCase) -> dict:
    changes = scope_diff(before, after)
    material = bool(changes)
    affected = []
    if material:
        affected.extend(["inventory-owner", "model-card"])
    if {"users", "autonomy", "decision_impact", "domain"} & changes.keys():
        affected.extend(["human-oversight", "usage-logging"])
    if "data_categories" in changes:
        affected.extend(["bias-evaluation", "model-card"])
    return {"material": material, "changed_fields": changes, "reopen_controls": sorted(set(affected))}
