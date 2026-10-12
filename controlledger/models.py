from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UseCase:
    system_id: str
    name: str
    purpose: str
    users: tuple[str, ...]
    data_categories: tuple[str, ...]
    autonomy: str
    decision_impact: str
    domain: str
    version: int = 1


@dataclass(frozen=True)
class Classification:
    tier: str
    rule_version: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Control:
    control_id: str
    title: str
    required_tiers: tuple[str, ...]
    evidence_days: int


@dataclass(frozen=True)
class Evidence:
    system_id: str
    control_id: str
    artifact: str
    issued_on: str
    expires_on: str
    reviewer: str
