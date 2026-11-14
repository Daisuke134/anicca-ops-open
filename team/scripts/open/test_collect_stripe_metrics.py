import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from collect_stripe_metrics import collect  # noqa: E402


NOW = datetime.fromisoformat("2026-11-06T12:00:00+09:00")


def list_response(data, has_more=False):
    return {"object": "list", "data": data, "has_more": has_more}


class StripeMetricsCollectorTests(unittest.TestCase):
    def fixture_get(self, fail_path=None):
        calls = []

        def request_get(path, params):
            params = dict(params)
            calls.append((path, params))
            if path == fail_path:
                raise TimeoutError("private provider response body")
            if path == "/v1/balance":
                return {
                    "available": [
                        {"currency": "usd", "amount": 12000},
                        {"currency": "jpy", "amount": 900},
                    ],
                    "pending": [{"currency": "usd", "amount": 500}],
                }
            if path == "/v1/subscriptions":
                status = params.get("status")
                values = {
                    "active": [
                        {"id": "sub_private_1", "customer": "cus_private_1", "currency": "usd", "status": "active", "metadata": {"private": "do not publish"}},
                        {"id": "sub_private_2", "currency": "jpy", "status": "active"},
                    ],
                    "trialing": [{"id": "sub_private_3", "currency": "usd", "status": "trialing", "description": "private description"}],
                }
                return list_response(values.get(status, []))
            if path == "/v1/balance_transactions":
                first = [
                    {"id": "txn_private_1", "created": 1793836800, "amount": 1000, "fee": 59, "net": 941, "currency": "usd", "reporting_category": "charge", "type": "charge", "description": "private memo"}
                ]
                second = [
                    {"id": "txn_private_2", "created": 1793750400, "amount": -200, "fee": 0, "net": -200, "currency": "usd", "reporting_category": "refund", "type": "refund"}
                ]
                return list_response(second) if params.get("starting_after") == "txn_private_1" else list_response(first, True)
            if path == "/v1/refunds":
                return list_response([
                    {"id": "re_private_1", "created": 1793836800, "amount": 200, "currency": "usd", "status": "succeeded", "reason": "private reason"},
                    {"id": "re_private_2", "created": 1793836800, "amount": 300, "currency": "jpy", "status": "pending"},
                ])
            if path == "/v1/payouts":
                return list_response([
                    {"id": "po_private_1", "created": 1793836800, "amount": 941, "currency": "usd", "status": "paid", "description": "private payout memo"},
                    {"id": "po_private_2", "created": 1793836800, "amount": 900, "currency": "jpy", "status": "pending"},
                ])
            raise AssertionError(f"unexpected endpoint {path}")

        return request_get, calls

    def test_missing_or_unrestricted_key_returns_unknown_without_requests(self):
        request_get, calls = self.fixture_get()
        missing = collect(None, request_get, NOW)
        unrestricted = collect("sk_live_do_not_use", request_get, NOW)

        self.assertEqual(missing["status"], "unavailable")
        self.assertEqual(unrestricted["status"], "unavailable")
        self.assertEqual(missing["balance"]["currencies"], [])
        self.assertEqual(calls, [])

    def test_aggregates_currency_counts_balances_transactions_refunds_and_payouts(self):
        request_get, calls = self.fixture_get()
        feed = collect("rk_live_test_only", request_get, NOW)

        self.assertEqual(feed["status"], "observed")
        self.assertEqual(feed["window"]["end"], "2026-11-06T03:00:00Z")
        self.assertEqual(feed["subscriptions"]["currencies"], [
            {"currency": "JPY", "active": 1, "trialing": 0},
            {"currency": "USD", "active": 1, "trialing": 1},
        ])
        self.assertEqual(feed["balance"]["currencies"], [
            {"currency": "JPY", "available_minor": 900, "pending_minor": 0},
            {"currency": "USD", "available_minor": 12000, "pending_minor": 500},
        ])
        usd = next(row for row in feed["balance_transactions"]["currencies"] if row["currency"] == "USD")
        self.assertEqual((usd["amount_minor"], usd["fee_minor"], usd["net_minor"], usd["count"]), (800, 59, 741, 2))
        self.assertEqual(len(feed["balance_transactions"]["daily"]), 2)
        self.assertEqual(feed["refunds"]["currencies"], [
            {"currency": "JPY", "statuses": [{"status": "pending", "count": 1, "amount_minor": 300}]},
            {"currency": "USD", "statuses": [{"status": "succeeded", "count": 1, "amount_minor": 200}]},
        ])
        self.assertEqual(feed["payouts"]["currencies"][1]["currency"], "USD")
        self.assertEqual(feed["payouts"]["currencies"][1]["statuses"], [{"status": "paid", "count": 1, "amount_minor": 941}])
        self.assertTrue(any(path == "/v1/balance_transactions" and "starting_after" in params for path, params in calls))
        self.assertTrue(all(params.get("created[gte]") and params.get("created[lte]") for path, params in calls if path in {"/v1/balance_transactions", "/v1/refunds", "/v1/payouts"}))

    def test_output_contains_no_provider_ids_descriptions_metadata_or_error_body(self):
        request_get, _ = self.fixture_get(fail_path="/v1/refunds")
        feed = collect("rk_live_test_only", request_get, NOW)
        serialized = json.dumps(feed)

        for secret in ["sub_private", "cus_private", "txn_private", "re_private", "po_private", "private memo", "private description", "private reason", "provider response body"]:
            self.assertNotIn(secret, serialized)
        self.assertEqual(feed["status"], "partial")
        self.assertEqual(feed["refunds"]["status"], "unavailable")
        self.assertEqual(feed["coverage"]["refunds"]["error_type"], "TimeoutError")
        self.assertEqual(feed["payouts"]["status"], "observed")

    def test_missing_pagination_cursor_marks_endpoint_partial(self):
        request_get, _ = self.fixture_get()

        def broken_get(path, params):
            if path == "/v1/balance_transactions":
                return list_response([{"created": 1793836800, "amount": 100, "fee": 1, "net": 99, "currency": "usd"}], True)
            return request_get(path, params)

        feed = collect("rk_live_test_only", broken_get, NOW)
        self.assertEqual(feed["status"], "partial")
        self.assertEqual(feed["balance_transactions"]["status"], "partial")
        self.assertEqual(feed["coverage"]["balance_transactions"]["error_type"], "PaginationCursorInvalid")

    def test_incomplete_subscription_page_keeps_count_unknown(self):
        request_get, _ = self.fixture_get()

        def broken_get(path, params):
            if path == "/v1/subscriptions" and dict(params).get("status") == "active":
                return list_response([{"id": "sub_private_1", "currency": "usd", "status": "active"}], True)
            return request_get(path, params)

        feed = collect("rk_live_test_only", broken_get, NOW)
        usd = next(row for row in feed["subscriptions"]["currencies"] if row["currency"] == "USD")
        self.assertIsNone(usd["active"])
        self.assertEqual(usd["trialing"], 1)
        self.assertEqual(feed["coverage"]["subscriptions_active"]["status"], "partial")

    def test_missing_balance_bucket_stays_unknown_instead_of_becoming_zero(self):
        request_get, _ = self.fixture_get()

        def broken_get(path, params):
            if path == "/v1/balance":
                return {"available": [{"currency": "usd", "amount": 300}], "pending": None}
            return request_get(path, params)

        feed = collect("rk_live_test_only", broken_get, NOW)
        self.assertEqual(feed["balance"]["status"], "partial")
        self.assertEqual(feed["balance"]["currencies"], [{"currency": "USD", "available_minor": 300, "pending_minor": None}])


if __name__ == "__main__":
    unittest.main()
