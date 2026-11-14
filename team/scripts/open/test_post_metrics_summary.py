import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from post_metrics_summary import summarize_post_metrics


class PostMetricsSummaryTest(unittest.TestCase):
    def test_preserves_sample_scope_periods_and_unknowns_without_private_post_data(self):
        feed = {
            "built_at": "2026-11-06T09:00:00+09:00",
            "window_start": "2026-10-27T00:00:00Z",
            "window_end": "2026-11-05T00:00:00Z",
            "selection": "up to 5 most recent published posts per connected account",
            "posts": {
                "post-1": {
                    "platform": "TikTok",
                    "account": "private account name",
                    "url": "https://private.example/post-1",
                    "t": "2026-11-04T10:00:00Z",
                    "fetched_at": "2026-11-06T08:59:00+09:00",
                    "views": 10,
                    "likes": 2,
                    "replies": None,
                    "reposts": 0,
                    "metric_periods": {
                        "views": "2026-11-04",
                        "likes": "2026-11-04",
                        "reposts": "2026-11-04",
                    },
                    "metric_series": {"views": [
                        {"date": "2026-11-04", "value": 11},
                        {"date": "2026-11-05", "value": 10},
                    ]},
                },
                "post-2": {
                    "platform": "TikTok",
                    "account": "private account name",
                    "url": "https://private.example/post-2",
                    "t": "2026-11-03T10:00:00Z",
                    "fetched_at": "2026-11-06T08:58:00+09:00",
                    "views": 0,
                    "likes": None,
                    "replies": None,
                    "reposts": None,
                    "metric_periods": {"views": "2026-11-03"},
                    "metric_series": {"views": [
                        {"date": "2026-11-03", "value": 8},
                        {"date": "2026-11-04", "value": 9},
                    ]},
                },
                "post-3": {
                    "platform": "Instagram",
                    "account": "another private account",
                    "url": "https://private.example/post-3",
                    "t": "2026-11-02T10:00:00Z",
                    "fetched_at": "2026-11-06T08:57:00+09:00",
                    "views": None,
                    "likes": 1,
                    "replies": 0,
                    "reposts": None,
                    "metric_periods": {"likes": "2026-11-02", "replies": "2026-11-02"},
                },
            },
        }

        summary = summarize_post_metrics(feed)
        serialized = json.dumps(summary)

        self.assertEqual(summary["observed_at"], feed["built_at"])
        self.assertEqual(summary["query_window"], {
            "from": feed["window_start"],
            "to": feed["window_end"],
        })
        self.assertEqual(summary["coverage"]["sampled_posts"], 3)
        self.assertEqual(summary["coverage"]["sampled_accounts"], 2)
        tiktok = next(p for p in summary["platforms"] if p["platform"] == "TikTok")
        self.assertEqual(tiktok["sampled_posts"], 2)
        self.assertEqual(tiktok["metrics"]["views"], {
            "sample_sum": 10,
            "posts_with_value": 2,
            "posts_missing_value": 0,
            "period_from": "2026-11-03",
            "period_to": "2026-11-04",
        })
        self.assertEqual(tiktok["metrics"]["likes"]["posts_missing_value"], 1)
        self.assertEqual(tiktok["metrics"]["likes"]["sample_sum"], 2)
        self.assertEqual(tiktok["metrics"]["replies"]["sample_sum"], None)
        self.assertEqual(tiktok["daily"], [
            {"date": "2026-11-03", "eligible_posts": 1, "metrics": {
                "views": {"sample_sum": 8, "posts_with_value": 1, "posts_missing_value": 0},
                "likes": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 1},
                "replies": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 1},
                "reposts": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 1},
            }},
            {"date": "2026-11-04", "eligible_posts": 2, "metrics": {
                "views": {"sample_sum": 20, "posts_with_value": 2, "posts_missing_value": 0},
                "likes": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 2},
                "replies": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 2},
                "reposts": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 2},
            }},
            {"date": "2026-11-05", "eligible_posts": 2, "metrics": {
                "views": {"sample_sum": 10, "posts_with_value": 1, "posts_missing_value": 1},
                "likes": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 2},
                "replies": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 2},
                "reposts": {"sample_sum": None, "posts_with_value": 0, "posts_missing_value": 2},
            }},
        ])
        instagram = next(p for p in summary["platforms"] if p["platform"] == "Instagram")
        self.assertEqual(instagram["metrics"]["views"]["sample_sum"], None)
        self.assertNotIn("private account name", serialized)
        self.assertNotIn("private.example", serialized)

    def test_distinguishes_successful_empty_collection_from_missing_feed(self):
        empty = summarize_post_metrics({"built_at": "2026-11-06T09:00:00+09:00", "posts": {}})
        missing = summarize_post_metrics(None)

        self.assertEqual(empty["status"], "observed_empty")
        self.assertEqual(empty["coverage"]["sampled_posts"], 0)
        self.assertEqual(missing["status"], "unavailable")


if __name__ == "__main__":
    unittest.main()
