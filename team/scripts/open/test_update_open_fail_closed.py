import os
from pathlib import Path
import subprocess
import tempfile
import unittest


UPDATE_OPEN = Path(__file__).with_name("update_open.sh")


class UpdateOpenFailureTest(unittest.TestCase):
    def run_refresh(self, collector_exit, finance_exit):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            open_dir = workspace / "team/scripts/open"
            metrics_dir = workspace / "team/metrics"
            finance_dir = workspace / "team/finance"
            marker_dir = root / "markers"
            for directory in (open_dir, metrics_dir, finance_dir, marker_dir):
                directory.mkdir(parents=True, exist_ok=True)

            def mark_script(path, marker, exit_env):
                path.write_text(
                    "from pathlib import Path\n"
                    "import os\n"
                    f"Path(os.environ['TEST_MARKER_DIR'], '{marker}').touch()\n"
                    f"raise SystemExit(int(os.environ['{exit_env}']))\n"
                )

            (metrics_dir / "collect_all.py").write_text(
                "import os\nraise SystemExit(int(os.environ['COLLECTOR_EXIT']))\n"
            )
            mark_script(finance_dir / "build_revenue_ledger.py", "finance", "FINANCE_EXIT")
            mark_script(open_dir / "build_open_v2.py", "build", "BUILD_EXIT")
            (open_dir / "publish_open_repo.sh").write_text(
                "#!/usr/bin/env bash\n"
                "touch \"$TEST_MARKER_DIR/publish\"\n"
            )

            isolated_script = root / "update_open.sh"
            isolated_script.write_text(
                UPDATE_OPEN.read_text().replace("/workspace", str(workspace))
            )
            env = dict(
                os.environ,
                TEST_MARKER_DIR=str(marker_dir),
                COLLECTOR_EXIT=str(collector_exit),
                FINANCE_EXIT=str(finance_exit),
                BUILD_EXIT="0",
            )
            result = subprocess.run(
                ["bash", str(isolated_script)],
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            return result, sorted(path.name for path in marker_dir.iterdir())

    def test_collector_failure_stops_before_finance_build_and_publish(self):
        result, markers = self.run_refresh(collector_exit=23, finance_exit=0)
        self.assertEqual(result.returncode, 23, result.stderr)
        self.assertEqual(markers, [])

    def test_finance_failure_stops_before_open_build_and_publish(self):
        result, markers = self.run_refresh(collector_exit=0, finance_exit=24)
        self.assertEqual(result.returncode, 24, result.stderr)
        self.assertEqual(markers, ["finance"])


if __name__ == "__main__":
    unittest.main()
