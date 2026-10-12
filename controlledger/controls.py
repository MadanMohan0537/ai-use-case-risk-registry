from __future__ import annotations

from .models import Classification, Control

CONTROL_LIBRARY = (
    Control("inventory-owner", "Named accountable owner", ("limited", "elevated", "high"), 365),
    Control("usage-logging", "Usage and decision logging", ("elevated", "high"), 180),
    Control("human-oversight", "Documented human oversight", ("elevated", "high"), 180),
    Control("model-card", "System and model documentation", ("elevated", "high"), 365),
    Control("bias-evaluation", "Impact and bias evaluation", ("high",), 180),
    Control("incident-plan", "AI incident response plan", ("high",), 365),
)


def required_controls(classification: Classification) -> list[Control]:
    return [control for control in CONTROL_LIBRARY if classification.tier in control.required_tiers]
