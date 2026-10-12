from __future__ import annotations

from .models import UseCase


def systems() -> list[UseCase]:
    return [
        UseCase("faq", "FAQ assistant", "Answer public product questions", ("customers",), ("public",), "informational", "none", "general"),
        UseCase("claims", "Claims triage", "Recommend claim review priority", ("adjusters",), ("financial",), "decision-support", "none", "insurance-operations"),
        UseCase("hiring", "Applicant ranker", "Rank employment candidates", ("recruiters",), ("identity",), "fully-automated", "eligibility", "employment"),
        UseCase("notes", "Internal summarizer", "Summarize internal project notes", ("employees",), ("internal",), "informational", "none", "general"),
        UseCase("care", "Care navigator", "Recommend care routing", ("patients", "clinicians"), ("health",), "decision-support", "safety", "healthcare"),
    ]
