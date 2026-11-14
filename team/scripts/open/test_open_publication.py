import copy
import unittest

from open_publication import reconcile_public


class PublicationBoundaryTests(unittest.TestCase):
    def setUp(self):
        # Synthetic shape-only fixture. No customer, bank, wallet or receipt data.
        self.data = {
            'month': '2026-11', 'reconciliation_complete': True,
            'kpis': [{'key': 'revm', 'usd': 31.8}, {'key': 'cost', 'usd': 293.7}],
            'wallets': [{'private': 'synthetic'}],
            'balances': [{'private': 'synthetic'}],
            'costs_month': [{'item': 'Google Cloud', 'jpy': 44298}],
            'monthly': [{'revenue_usd': 31.8, 'gross_profit_usd': -261.9}],
            'summary': {
                'bank': {'private': 'synthetic'},
                'platforms': [
                    {'platform': 'Coconala', 'this_month': 31.8},
                    {'platform': 'Capafy', 'this_month': 0, 'pending': 26.97},
                ],
                'products': [],
            },
        }
        self.metrics = {'totals': {'revenue_mtd_usd': 31.8}, 'monthly': []}
        self.ledger = {'history_coverage': {'complete': False}, 'expense_coverage': {'complete': False}}

    def result(self):
        return reconcile_public(self.data, self.metrics, self.ledger)

    def test_unreconciled_month_keeps_observed_revenue_but_not_company_profit(self):
        data, metrics = self.result()
        self.assertFalse(data['reconciliation_complete'])
        self.assertEqual(next(x for x in data['kpis'] if x['key'] == 'revm')['usd'], 31.8)
        self.assertIsNone(metrics['totals']['gross_profit_mtd_usd'])

    def test_asset_totals_are_sanitized_when_source_is_unknown(self):
        data, _ = self.result()
        self.assertEqual(data.get('balances', []), [])
        self.assertEqual(data.get('wallets', []), [])
        self.assertEqual(data['summary']['bank'], {'usd': None, 'jpy': None, 'status': 'unknown (source error)'})
        self.assertIsNone(data['summary']['net_worth']['usd'])
        self.assertIsNone(data['summary']['net_worth']['jpy'])

    def test_capafy_notice_is_not_zero_sales_or_payable(self):
        data, _ = self.result()
        row = next(x for x in data['summary']['platforms'] if x['platform'] == 'Capafy')
        self.assertIsNone(row['this_month'])
        self.assertIsNone(row['pending'])

    def test_accepted_gross_is_separate_from_net_sales(self):
        data, _ = self.result()
        row = next(x for x in data['summary']['platforms'] if x['platform'] == 'Coconala')
        self.assertIsNone(row['this_month'])
        self.assertEqual(row['observed_accepted_gross_usd'], 31.8)
        self.assertIsNone(row['net_sales_usd'])

    def test_usage_period_does_not_change_observed_amount(self):
        data, _ = self.result()
        row = data['costs_month'][0]
        self.assertIn('October 2026 usage', row['period_note'])
        self.assertEqual(row['jpy'], 44298)

    def test_missing_coverage_fails_closed(self):
        self.ledger = {}
        data, _ = self.result()
        self.assertFalse(data['reconciliation_complete'])

    def test_source_inputs_are_unchanged(self):
        before = copy.deepcopy((self.data, self.metrics, self.ledger))
        self.result()
        self.assertEqual((self.data, self.metrics, self.ledger), before)


if __name__ == '__main__':
    unittest.main()
