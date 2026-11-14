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


class OpenMetricsProvenanceTests(unittest.TestCase):
    def test_export_preserves_the_source_snapshot_time(self):
        snapshot = json.loads((TEAM / "metrics/snapshots/latest.json").read_text())
        env = {
            **os.environ,
            "OPEN_TEAM_DIR": str(TEAM),
            "OPEN_MARKETING_DIR": str(REPO / "marketing"),
        }

        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "metrics.json"
            subprocess.run(
                [sys.executable, str(BUILDER), str(output_path)],
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            output = json.loads(output_path.read_text())

        self.assertEqual(output.get("source_updated_at"), snapshot.get("updated_at"))


if __name__ == "__main__":
    unittest.main()
