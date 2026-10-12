from __future__ import annotations

from .models import Classification, UseCase

RULE_VERSION = "illustrative-2026.10"


def classify(system: UseCase) -> Classification:
    reasons: list[str] = []
    tier = "limited"
    sensitive_domains = {"employment", "credit", "healthcare", "education", "public-benefits"}
    if system.domain in sensitive_domains and system.decision_impact in {"eligibility", "access", "rights", "safety"}:
        tier = "high"
        reasons.append("consequential decision in a sensitive domain")
    if system.autonomy == "fully-automated":
        tier = "high"
        reasons.append("fully automated action without mandatory human confirmation")
    if {"biometric", "health", "financial", "children"} & set(system.data_categories):
        if tier == "limited":
            tier = "elevated"
        reasons.append("sensitive data category")
    if system.autonomy == "decision-support" and tier == "limited":
        tier = "elevated"
        reasons.append("influences a human decision")
    if not reasons:
        reasons.append("informational use with low autonomy and no declared sensitive data")
    return Classification(tier, RULE_VERSION, tuple(reasons))
