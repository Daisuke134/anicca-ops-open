import contextlib
import datetime as dt
import io
import json
import os
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/fill_post_metrics.py"


class Response(io.BytesIO):
    pass


class FillPostMetricsConfigTest(unittest.TestCase):
    def run_collector(self, postiz_key, secret_file_key=None, existing_metrics=None):
        temp = tempfile.TemporaryDirectory(prefix="post-metrics-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        team = root / "team"
        marketing = root / "marketing"
        secrets = root / ".secrets"
        (team / "metrics").mkdir(parents=True)
        if existing_metrics:
            (team / "metrics/post-metrics.json").write_text(json.dumps(existing_metrics))
        marketing.mkdir()
        secrets.mkdir()
        if secret_file_key:
            (secrets / "postiz").write_text(secret_file_key)
        post_log = marketing / "POST-LOG.csv"
        post_log.write_text(
            "date_jst,platform,post_url,impr_24h,likes,replies,reposts\n"
            "2026-11-05 09:00,tiktok,postiz:post-1,0,,,\n"
        )
        requests = []

        def urlopen(request, timeout=0):
            requests.append((request.full_url, request.get_header("Authorization")))
            if "/posts?" in request.full_url:
                body = {"posts": [{
                    "id": "post-1",
                    "state": "PUBLISHED",
                    "publishDate": "2026-11-05T00:00:00Z",
                    "integration": {"id": "int-1", "name": "public account"},
                }]}
            elif request.full_url.endswith("/integrations"):
                body = [{"id": "int-1", "identifier": "tiktok", "profile": "public account"}]
            elif request.full_url.endswith("/analytics/post/post-1"):
                body = [{
                    "label": "Views",
                    "data": [
                        {"date": "2026-11-04", "total": "11"},
                        {"date": "2026-11-05", "total": "15"},
                    ],
                }]
            else:
                raise AssertionError(f"unexpected request path: {request.full_url}")
            return Response(json.dumps(body).encode())

        env = {
            "OPEN_TEAM_DIR": str(team),
            "OPEN_MARKETING_DIR": str(marketing),
            "OPEN_SECRETS_DIR": str(secrets),
            "POSTIZ_API_KEY": postiz_key or "",
        }
        stdout = io.StringIO()
        with (
            patch.dict(os.environ, env),
            patch.object(sys, "argv", [str(SCRIPT)]),
            patch("urllib.request.urlopen", side_effect=urlopen),
            contextlib.redirect_stdout(stdout),
        ):
            runpy.run_path(str(SCRIPT), run_name="__main__")

        metrics = json.loads((team / "metrics/post-metrics.json").read_text())
        return requests, stdout.getvalue(), metrics, post_log

    def test_env_key_and_configured_paths_are_used_without_logging_the_key(self):
        requests, stdout, metrics, post_log = self.run_collector(
            "environment-secret", secret_file_key="fallback-secret"
        )

        self.assertTrue(requests)
        self.assertTrue(all(key == "environment-secret" for _, key in requests))
        self.assertNotIn("environment-secret", stdout)
        self.assertNotIn("fallback-secret", stdout)
        self.assertTrue(metrics["built_at"])
        self.assertTrue(metrics["window_start"])
        self.assertTrue(metrics["window_end"])
        self.assertIn("up to 5", metrics["selection"])
        post = metrics["posts"]["post-1"]
        self.assertEqual(post["views"], 15)
        self.assertEqual(post["metric_periods"]["views"], "2026-11-05")
        self.assertEqual(post["metric_series"]["views"], [
            {"date": "2026-11-04", "value": 11},
            {"date": "2026-11-05", "value": 15},
        ])
        self.assertTrue(post["fetched_at"])
        self.assertTrue(post_log.exists())

    def test_configured_secret_file_is_used_when_env_key_is_empty(self):
        requests, stdout, metrics, _ = self.run_collector(
            "", secret_file_key="fallback-secret"
        )

        self.assertTrue(requests)
        self.assertTrue(all(key == "fallback-secret" for _, key in requests))
        self.assertNotIn("fallback-secret", stdout)
        self.assertTrue(metrics["built_at"])

    def test_cached_post_analytics_are_refreshed_within_one_day(self):
        old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=30)).isoformat()
        requests, _, _, _ = self.run_collector(
            "environment-secret",
            existing_metrics={"posts": {"post-1": {
                "views": 15,
                "metric_periods": {"views": "2026-11-05"},
                "metric_series": {"views": [{"date": "2026-11-05", "value": 15}]},
                "fetched_at": old,
            }}},
        )

        self.assertTrue(any(url.endswith("/analytics/post/post-1") for url, _ in requests))

    def test_recent_cache_without_daily_series_is_refetched_for_upgrade(self):
        recent = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)).isoformat()
        requests, _, _, _ = self.run_collector(
            "environment-secret",
            existing_metrics={"posts": {"post-1": {
                "views": 15,
                "metric_periods": {"views": "2026-11-05"},
                "fetched_at": recent,
            }}},
        )

        self.assertTrue(any(url.endswith("/analytics/post/post-1") for url, _ in requests))


class ScriptNsTest(unittest.TestCase):
    def load_script_ns(self):
        temp = tempfile.TemporaryDirectory(prefix="opener-effect-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        team = root / "team"
        marketing = root / "marketing"
        secrets = root / ".secrets"
        (team / "metrics").mkdir(parents=True)
        marketing.mkdir()
        secrets.mkdir()
        (marketing / "POST-LOG.csv").write_text(
            "date_jst,platform,post_url,impr_24h,likes,replies,reposts\n"
            "2026-11-05 09:00,tiktok,postiz:post-1,0,,,\n"
        )

        def urlopen(request, timeout=0):
            url = request.full_url
            if "/posts?" in url:
                body = {"posts": [{
                    "id": "post-1",
                    "state": "PUBLISHED",
                    "publishDate": "2026-11-05T00:00:00Z",
                    "integration": {"id": "int-1", "name": "public account"},
                }]}
            elif url.endswith("/integrations"):
                body = [{"id": "int-1", "identifier": "tiktok", "profile": "public account"}]
            elif url.endswith("/analytics/post/post-1"):
                body = [{"label": "Views", "data": [{"date": "2026-11-05", "total": "15"}]}]
            else:
                raise AssertionError(f"unexpected request path: {url}")
            return Response(json.dumps(body).encode())

        env = {
            "OPEN_TEAM_DIR": str(team),
            "OPEN_MARKETING_DIR": str(marketing),
            "OPEN_SECRETS_DIR": str(secrets),
            "POSTIZ_API_KEY": "test-key",
        }
        with (
            patch.dict(os.environ, env),
            patch.object(sys, "argv", [str(SCRIPT)]),
            patch("urllib.request.urlopen", side_effect=urlopen),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            ns = runpy.run_path(str(SCRIPT), run_name="__main__")
        return ns

    @staticmethod
    def sample_rows():
        rows = []
        for i in range(40):
            opener = "request" if i % 2 == 0 else "number"
            base = 200 if opener == "request" else 100
            step = 10 if opener == "request" else 5
            rows.append({"opener": opener, "impressions": base + (i % 5) * step})
        return rows

class OpenerEffectTest(ScriptNsTest):
    def test_opener_effect_is_deterministic_with_seed(self):
        opener_effect = self.load_script_ns()["opener_effect"]
        rows = self.sample_rows()

        first = opener_effect(rows, n_boot=500, seed=7)
        second = opener_effect(rows, n_boot=500, seed=7)
        other = opener_effect(rows, n_boot=500, seed=8)

        self.assertEqual(first, second)
        self.assertNotEqual(first["ci"], other["ci"])

    def test_opener_effect_ci_contains_point_estimate(self):
        opener_effect = self.load_script_ns()["opener_effect"]
        rows = self.sample_rows()

        result = opener_effect(rows, n_boot=2000, seed=0)
        lo, hi = result["ci"]

        self.assertAlmostEqual(result["ratio"], 2.0, places=6)
        self.assertLessEqual(lo, result["ratio"])
        self.assertLessEqual(result["ratio"], hi)
        self.assertLess(lo, hi)


class OpenerOfTest(ScriptNsTest):
    def opener_of(self):
        return self.load_script_ns()["opener_of"]

    def test_digit_opener_is_number(self):
        self.assertEqual(self.opener_of()("42 builders shipped this week"), "number")

    def test_dollar_opener_is_number(self):
        self.assertEqual(self.opener_of()("$99 MRR in 30 days"), "number")

    def test_day_opener_is_number(self):
        self.assertEqual(self.opener_of()("Day 3 of building in public"), "number")

    def test_request_keyword_on_first_line_is_request(self):
        opener_of = self.opener_of()
        self.assertEqual(opener_of("Looking for founders to swap notes"), "request")
        self.assertEqual(opener_of("connect with builders\nrest of post"), "request")

    def test_keyword_on_later_line_or_no_keyword_is_none(self):
        opener_of = self.opener_of()
        self.assertIsNone(opener_of("A quiet update\nconnect with me later"))
        self.assertIsNone(opener_of("Just a regular post with no hook"))


if __name__ == "__main__":
    unittest.main()
