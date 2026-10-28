from __future__ import annotations

from dataclasses import dataclass
from datetime import date


APPLICABILITY = {"applicable", "not_applicable", "pending"}


@dataclass(frozen=True)
class SharedEvidence:
    artifact_id: str
    control_id: str
    version: int
    artifact: str
    issued_on: str
    expires_on: str
    reviewer: str


@dataclass(frozen=True)
class EvidenceDependency:
    system_id: str
    control_id: str
    artifact_id: str
    evidence_version: int
    applicability: str
    rationale: str


def _index_evidence(
    evidence: list[SharedEvidence],
) -> tuple[dict[tuple[str, int], SharedEvidence], dict[str, int]]:
    versions: dict[tuple[str, int], SharedEvidence] = {}
    latest: dict[str, int] = {}
    for item in evidence:
        if item.version < 1:
            raise ValueError("evidence version must be positive")
        key = (item.artifact_id, item.version)
        if key in versions:
            raise ValueError(f"duplicate evidence version: {item.artifact_id} v{item.version}")
        if date.fromisoformat(item.issued_on) > date.fromisoformat(item.expires_on):
            raise ValueError("evidence cannot expire before it is issued")
        versions[key] = item
        latest[item.artifact_id] = max(latest.get(item.artifact_id, 0), item.version)
    return versions, latest


def dependency_statuses(
    evidence: list[SharedEvidence],
    dependencies: list[EvidenceDependency],
    on: date,
) -> list[dict]:
    versions, latest = _index_evidence(evidence)
    seen: set[tuple[str, str]] = set()
    rows: list[dict] = []
    for link in dependencies:
        link_key = (link.system_id, link.control_id)
        if link_key in seen:
            raise ValueError(f"duplicate control dependency: {link.system_id}/{link.control_id}")
        seen.add(link_key)
        if link.applicability not in APPLICABILITY:
            raise ValueError(f"invalid applicability: {link.applicability}")
        if not link.rationale.strip():
            raise ValueError("applicability rationale is required")
        item = versions.get((link.artifact_id, link.evidence_version))
        if link.applicability == "not_applicable":
            status = "not_applicable"
        elif link.applicability == "pending":
            status = "pending_applicability"
        elif item is None:
            status = "missing"
        elif item.control_id != link.control_id:
            status = "control_mismatch"
        elif link.evidence_version < latest[link.artifact_id]:
            status = "superseded"
        elif date.fromisoformat(item.expires_on) < on:
            status = "expired"
        else:
            status = "current"
        rows.append(
            {
                "system_id": link.system_id,
                "control_id": link.control_id,
                "artifact_id": link.artifact_id,
                "evidence_version": link.evidence_version,
                "applicability": link.applicability,
                "status": status,
            }
        )
    return rows


def shared_evidence_experiment() -> dict:
    initial = [
        SharedEvidence(
            "platform-logging",
            "usage-logging",
            1,
            "logging-assurance-v1.md",
            "2026-01-01",
            "2026-12-31",
            "platform-governance",
        ),
        SharedEvidence(
            "platform-incident",
            "incident-plan",
            1,
            "incident-plan-v1.md",
            "2025-01-01",
            "2026-06-30",
            "security",
        ),
    ]
    links = [
        EvidenceDependency(system_id, "usage-logging", "platform-logging", 1, "applicable", "Uses the governed platform logger")
        for system_id in ("claims", "hiring", "care")
    ] + [
        EvidenceDependency(system_id, "incident-plan", "platform-incident", 1, "applicable", "Uses the shared incident process")
        for system_id in ("hiring", "care")
    ] + [
        EvidenceDependency("faq", "usage-logging", "platform-logging", 1, "not_applicable", "Informational system has no decision log requirement")
    ]
    before = dependency_statuses(initial, links, date(2026, 3, 1))
    changed = initial + [
        SharedEvidence(
            "platform-logging",
            "usage-logging",
            2,
            "logging-assurance-v2.md",
            "2026-07-01",
            "2027-06-30",
            "platform-governance",
        )
    ]
    after = dependency_statuses(changed, links, date(2026, 10, 28))
    applicable_links = [row for row in before if row["applicability"] == "applicable"]
    referenced_artifacts = {
        (row["artifact_id"], row["evidence_version"]) for row in applicable_links
    }
    seeded_stale = 5
    stale_statuses = {"superseded", "expired", "missing", "control_mismatch"}
    found = sum(row["status"] in stale_statuses for row in after)
    return {
        "applicable_dependencies": len(applicable_links),
        "shared_submissions": len(referenced_artifacts),
        "duplicate_submissions_avoided": len(applicable_links) - len(referenced_artifacts),
        "seeded_stale_dependencies": seeded_stale,
        "stale_dependencies_found": found,
        "false_negatives": seeded_stale - found,
        "applicability_exclusions": sum(
            row["status"] == "not_applicable" for row in after
        ),
        "acceptance_passed": found == seeded_stale,
        "before": before,
        "after": after,
    }
