import unittest
import json
import tempfile
import pathlib
from validate_funnel_monotonic import validate_app_funnel, validate_store_funnel_file, FunnelInconsistencyError

class TestFunnelMonotonic(unittest.TestCase):
    def test_valid_monotonic_app(self):
        app = {
            "app": "Anicca",
            "asc": {
                "impressions": 1000,
                "page_views": 100,
                "first_time_downloads": 10
            },
            "in_app_starts": 10,
            "paywall_views": 8
        }
        self.assertTrue(validate_app_funnel(app))

    def test_page_views_exceeds_impressions(self):
        app = {
            "app": "Honne",
            "asc": {
                "impressions": 50,
                "page_views": 100,
                "first_time_downloads": 5
            }
        }
        with self.assertRaises(FunnelInconsistencyError) as ctx:
            validate_app_funnel(app)
        self.assertIn("page_views (100) > impressions (50)", str(ctx.exception))

    def test_downloads_exceeds_page_views(self):
        app = {
            "app": "Dhamma Quotes",
            "asc": {
                "impressions": 200,
                "page_views": 10,
                "first_time_downloads": 25
            }
        }
        with self.assertRaises(FunnelInconsistencyError) as ctx:
            validate_app_funnel(app)
        self.assertIn("first_time_downloads (25) > page_views (10)", str(ctx.exception))

    def test_dl14_inapp23_contradiction(self):
        app = {
            "app": "Anicca",
            "asc": {
                "impressions": 1045,
                "page_views": 81,
                "first_time_downloads": 14
            },
            "in_app_starts": 23
        }
        with self.assertRaises(FunnelInconsistencyError) as ctx:
            validate_app_funnel(app)
        self.assertIn("in_app_starts (23) > first_time_downloads (14)", str(ctx.exception))

    def test_full_file_validation_success(self):
        data = {
            "apps": [
                {
                    "app": "App1",
                    "asc": {"impressions": 100, "page_views": 20, "first_time_downloads": 5}
                },
                {
                    "app": "App2",
                    "asc": {"impressions": 50, "page_views": 10, "first_time_downloads": 2}
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(data, f)
            path = f.name
        self.assertTrue(validate_store_funnel_file(path))
        pathlib.Path(path).unlink()

if __name__ == "__main__":
    unittest.main()
