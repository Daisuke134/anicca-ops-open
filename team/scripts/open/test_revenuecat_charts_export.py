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


class RevenueCatChartExportTests(unittest.TestCase):
    def test_builder_preserves_observed_and_unavailable_projects(self):
        charts = {
            "source": "RevenueCat Charts API v2",
            "observed_at": "2026-11-06T00:00:00Z",
            "window": {"start_date": "2026-10-07", "end_date": "2026-11-05", "resolution": "day"},
            "projects": [
                {
                    "name": "Anicca",
                    "project_id": "projbb7b9d1b",
                    "status": "observed",
                    "charts": {"mrr": {"id": "mrr", "incomplete": True, "values": [{"value": 20.34, "incomplete": True}]}},
                },
                {
                    "name": "Honne",
                    "project_id": "projcfa60dd8",
                    "status": "credential_missing",
                    "reason": "project_scoped_key_unavailable",
                    "charts": {},
                },
            ],
        }
        env = {
            **os.environ,
            "OPEN_TEAM_DIR": str(TEAM),
            "OPEN_MARKETING_DIR": str(REPO / "marketing"),
        }

        with tempfile.TemporaryDirectory() as tmp:
            source_path = Path(tmp) / "revenuecat-charts.json"
            output_path = Path(tmp) / "metrics.json"
            source_path.write_text(json.dumps(charts))
            env["OPEN_REVENUECAT_CHARTS"] = str(source_path)
            subprocess.run(
                [sys.executable, str(BUILDER), str(output_path)],
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            output = json.loads(output_path.read_text())

        feed = output.get("revenuecat_charts")
        self.assertIsNotNone(feed, "Open feed must include the live RevenueCat chart source")
        projects = {project["name"]: project for project in feed["projects"]}
        self.assertTrue(projects["Anicca"]["charts"]["mrr"]["values"][0]["incomplete"])
        self.assertEqual(projects["Honne"]["status"], "credential_missing")
        self.assertEqual(projects["Honne"]["charts"], {})


if __name__ == "__main__":
    unittest.main()
