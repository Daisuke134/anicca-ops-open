import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
TEAM = HERE.parents[1]
REPO = TEAM.parent
BUILDER = HERE / "build_open_metrics.py"


class StripeMetricsExportTests(unittest.TestCase):
    def build(self, tmp, feed=None):
        env = {
            **os.environ,
            "OPEN_TEAM_DIR": str(TEAM),
            "OPEN_MARKETING_DIR": str(REPO / "marketing"),
        }
        output_path = Path(tmp) / "metrics.json"
        if feed is not None:
            source_path = Path(tmp) / "stripe-metrics.json"
            source_path.write_text(json.dumps(feed))
            env["OPEN_STRIPE_METRICS"] = str(source_path)
        else:
            env.pop("OPEN_STRIPE_METRICS", None)
        subprocess.run(
            [sys.executable, str(BUILDER), str(output_path)],
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(output_path.read_text())

    def test_builder_preserves_observed_feed_and_does_not_collapse_unknown_to_zero(self):
        observed = {
            "source": "Stripe API", "status": "partial", "observed_at": "2026-11-06T03:00:00Z",
            "window": {"start": "2026-08-08T03:00:00Z", "end": "2026-11-06T03:00:00Z"},
            "balance": {"status": "observed", "currencies": [{"currency": "USD", "available_minor": 12000, "pending_minor": 500}]},
            "subscriptions": {"status": "observed", "currencies": [{"currency": "USD", "active": 1, "trialing": 0}]},
            "balance_transactions": {"status": "observed", "currencies": [], "daily": []},
            "refunds": {"status": "unavailable", "currencies": []},
            "payouts": {"status": "observed_empty", "currencies": []},
            "coverage": {"refunds": {"status": "unavailable"}},
        }
        with tempfile.TemporaryDirectory() as tmp:
            output = self.build(tmp, observed)
        self.assertEqual(output["stripe_metrics"], observed)
        self.assertEqual(output["stripe_metrics"]["refunds"]["status"], "unavailable")
        self.assertIn("Stripe metrics partial", output["missing"])

    def test_missing_collector_file_exports_explicit_unknown_not_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = self.build(tmp)
        feed = output["stripe_metrics"]
        self.assertEqual(feed["status"], "unavailable")
        self.assertEqual(feed["reason"], "restricted_read_key_missing")
        self.assertIsNone(feed["observed_at"])
        self.assertEqual(feed["balance"]["currencies"], [])
        self.assertIn("Stripe metrics unavailable", output["missing"])


if __name__ == "__main__":
    unittest.main()
