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


if __name__ == "__main__":
    unittest.main()
