import unittest
from dataclasses import replace
from datetime import date

from controlledger.audit import csv_export, portfolio
from controlledger.changes import reclassification_trigger, scope_diff
from controlledger.controls import required_controls
from controlledger.demo import run_demo
from controlledger.evidence import evidence_status
from controlledger.fixtures import systems
from controlledger.models import Evidence
from controlledger.rules import RULE_VERSION, classify
from controlledger.store import Registry
from controlledger.shared import (
    EvidenceDependency,
    SharedEvidence,
    dependency_statuses,
    shared_evidence_experiment,
)


class ControlLedgerTests(unittest.TestCase):
    def setUp(self):
        self.items = systems()

    def test_fixture_spans_tiers(self):
        self.assertEqual({"limited", "elevated", "high"}, {classify(item).tier for item in self.items})

    def test_rule_version_recorded(self):
        self.assertTrue(all(classify(item).rule_version == RULE_VERSION for item in self.items))

    def test_hiring_is_high(self):
        self.assertEqual("high", classify(self.items[2]).tier)

    def test_sensitive_data_elevates(self):
        changed = replace(self.items[0], data_categories=("public", "biometric"))
        self.assertEqual("elevated", classify(changed).tier)

    def test_high_tier_has_more_controls(self):
        self.assertGreater(len(required_controls(classify(self.items[2]))), len(required_controls(classify(self.items[0]))))

    def test_missing_evidence(self):
        control = required_controls(classify(self.items[0]))[0]
        self.assertEqual("missing", evidence_status(control, None, date(2026, 10, 12)))

    def test_expired_evidence(self):
        control = required_controls(classify(self.items[0]))[0]
        item = Evidence("faq", control.control_id, "x", "2025-01-01", "2025-12-31", "r")
        self.assertEqual("expired", evidence_status(control, item, date(2026, 10, 12)))

    def test_current_evidence(self):
        control = required_controls(classify(self.items[0]))[0]
        item = Evidence("faq", control.control_id, "x", "2026-01-01", "2026-12-31", "r")
        self.assertEqual("current", evidence_status(control, item, date(2026, 10, 12)))

    def test_store_roundtrip(self):
        store = Registry()
        store.save_system(self.items[0])
        self.assertEqual(self.items[0], store.systems()[0])

    def test_scope_diff_detects_only_changes(self):
        updated = replace(self.items[0], version=2, autonomy="fully-automated")
        self.assertEqual({"autonomy"}, set(scope_diff(self.items[0], updated)))

    def test_system_id_cannot_change(self):
        with self.assertRaises(ValueError):
            scope_diff(self.items[0], replace(self.items[0], system_id="new"))

    def test_non_material_version_bump_does_not_reopen(self):
        result = reclassification_trigger(self.items[0], replace(self.items[0], version=2))
        self.assertFalse(result["material"])

    def test_autonomy_change_reopens_oversight(self):
        result = reclassification_trigger(self.items[0], replace(self.items[0], version=2, autonomy="fully-automated"))
        self.assertIn("human-oversight", result["reopen_controls"])

    def test_data_change_reopens_bias_control(self):
        result = reclassification_trigger(self.items[0], replace(self.items[0], version=2, data_categories=("biometric",)))
        self.assertIn("bias-evaluation", result["reopen_controls"])

    def test_portfolio_has_denominators(self):
        rows = portfolio(self.items, [], date(2026, 10, 12))
        self.assertTrue(all("controls_required" in row for row in rows))

    def test_csv_has_header(self):
        rows = portfolio(self.items, [], date(2026, 10, 12))
        self.assertIn("system_id", csv_export(rows).splitlines()[0])

    def test_scope_experiment_has_no_misses(self):
        result = run_demo()["scope_change_experiment"]
        self.assertEqual(result["seeded"], result["reopened"])
        self.assertEqual(0, result["false_negatives"])

    def test_shared_evidence_avoids_duplicate_submissions(self):
        result = shared_evidence_experiment()
        self.assertEqual(3, result["duplicate_submissions_avoided"])

    def test_shared_evidence_finds_all_seeded_stale_links(self):
        result = shared_evidence_experiment()
        self.assertEqual(5, result["stale_dependencies_found"])
        self.assertEqual(0, result["false_negatives"])
        self.assertTrue(result["acceptance_passed"])

    def test_new_evidence_version_invalidates_pinned_dependencies(self):
        result = shared_evidence_experiment()
        self.assertEqual(3, sum(row["status"] == "superseded" for row in result["after"]))

    def test_expiry_invalidates_every_dependent_claim(self):
        result = shared_evidence_experiment()
        self.assertEqual(2, sum(row["status"] == "expired" for row in result["after"]))

    def test_applicability_is_separate_from_evidence_freshness(self):
        result = shared_evidence_experiment()
        self.assertEqual(1, result["applicability_exclusions"])
        self.assertEqual(1, sum(row["status"] == "not_applicable" for row in result["after"]))

    def test_missing_shared_evidence_is_visible(self):
        link = EvidenceDependency("claims", "usage-logging", "missing", 1, "applicable", "Expected platform control")
        self.assertEqual("missing", dependency_statuses([], [link], date(2026, 10, 28))[0]["status"])

    def test_control_mismatch_is_rejected_as_current(self):
        item = SharedEvidence("platform", "model-card", 1, "x.md", "2026-01-01", "2026-12-31", "reviewer")
        link = EvidenceDependency("claims", "usage-logging", "platform", 1, "applicable", "Incorrectly linked")
        self.assertEqual("control_mismatch", dependency_statuses([item], [link], date(2026, 10, 28))[0]["status"])

    def test_duplicate_shared_evidence_version_is_rejected(self):
        item = SharedEvidence("platform", "usage-logging", 1, "x.md", "2026-01-01", "2026-12-31", "reviewer")
        with self.assertRaisesRegex(ValueError, "duplicate evidence version"):
            dependency_statuses([item, item], [], date(2026, 10, 28))

    def test_applicability_requires_rationale(self):
        link = EvidenceDependency("claims", "usage-logging", "platform", 1, "pending", "")
        with self.assertRaisesRegex(ValueError, "rationale"):
            dependency_statuses([], [link], date(2026, 10, 28))


if __name__ == "__main__":
    unittest.main()

