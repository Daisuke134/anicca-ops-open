"""Public accounting boundary; no I/O or source-ledger mutation."""
from copy import deepcopy

def reconcile_public(data, metrics, ledger):
    d, m = deepcopy(data), deepcopy(metrics)
    note = 'Coverage incomplete; company revenue and profit are not established.'
    # An old coverage boolean is not a same-period gross/net reconciliation.
    # Re-enable totals only after stage-specific accounting has been reviewed.
    d['reconciliation_complete'] = False
    d['coverage_note'] = note
    for key in ('balances', 'wallets', 'active_costs', 'by_agent'):
        d[key] = []
    d.pop('cost_reconciliation', None)
    d.pop('company', None)  # mixed private/raw snapshots; do not republish wholesale
    d.pop('active_costs_total', None)
    d['gross_profit_detail'] = {'usd': None, 'jpy': None, 'status': note}
    for k in d.get('kpis', []):
        if k.get('key') in ('rev7','rev30','gp','gpl','margin','run'):
            k.update(usd=None, jpy=None, pct=None, pending=note)
        if k.get('key') in ('cost','costl'):
            k['label'] = 'Observed payment notices (' + ('current month' if k['key']=='cost' else 'prior month') + ')'
            k['source'] = 'Provider/payment notices; coverage incomplete; not accrual expenses or final bank settlement'
    for row in d.get('costs_month', []):
        row['period_note'] = 'Payment-notice month ' + d.get('month','unknown') + '; service period varies'
        if d.get('month') == '2026-11' and row.get('item') == 'Google Cloud' and row.get('jpy') == 44298:
            row['period_note'] = 'October 2026 usage; November payment notice; JPY 40,271 + tax 4,027; final settlement not established'
    for row in d.get('monthly', []):
        row.update(revenue_usd=None, gross_profit_usd=None, coverage_note=note)
    d['streams'] = []
    d['streams_total'] = {'earned_usd':None,'source':note}
    d['notices_unpaid'] = []  # notification gross is not a payable balance
    summary = d.setdefault('summary', {})
    # 成田さん 11/01 rule (参謀 11/03 02:00): bank total, net worth, all-time and MTD revenue stay public, totals only.
    b = summary.get('bank') or {}
    if b.get('usd') is None:
        summary['bank'] = {'usd': None, 'jpy': None, 'status': 'unknown (source error)'}
    else:
        summary['bank'] = {k: b.get(k) for k in ('usd', 'jpy', 'fx', 'as_of', 'source')}
    summary['net_worth'] = dict(summary['bank'], basis='Bank total; no debt on record')
    summary['all_time_source'] = 'cfo/revenue_facts.py booked revenue (paid + accepted) + RevenueCat App Store lifetime gross; as of ' + str(d.get('updated_at'))
    _at = [x.get('all_time') for x in summary.get('platforms', [])]
    summary['all_time_usd'] = None if summary.get('all_time_confirmed') is None else round(sum(v or 0 for v in _at), 2)
    if summary.get('all_time_confirmed') is None:
        summary['all_time_status'] = 'unknown (source error)'
    summary['trend'] = []  # historical mixed recognition cannot establish a company total
    for p in summary.get('platforms', []):
        platform = p.get('platform')
        if platform == 'Coconala':
            p['observed_accepted_gross_usd'] = p.get('this_month')
            p.update(this_month=None, last_month=None, all_time=None, pending=None,
                     net_sales_usd=None, paid_out_usd=None, status='stage reconciliation',
                     note='Accepted order gross shown separately; fees, net sales and payout require matched platform statements')
        elif platform == 'Capafy':
            p.update(this_month=None, last_month=None, all_time=None, pending=None,
                     net_sales_usd=None, paid_out_usd=None, status='stage reconciliation',
                     note='Order notices, publisher settlement credits and bank payouts are distinct; current complete period not established')
        elif platform == 'Stripe' and not (ledger.get('history_coverage') or {}).get('complete'):
            p.update(this_month=None, note='Current coverage incomplete')
    for p in summary.get('products', []):
        if p.get('platform') in ('Coconala','Capafy','Stripe'):
            p.update(this_month=None, all_time=None, note='See platform stage reconciliation; unknown is not zero')
    for k in ('revenue_7d_usd','revenue_30d_usd','revenue_mtd_usd','gross_profit_mtd_usd','margin_pct','active_costs_monthly_usd'):
        m.setdefault('totals', {})[k] = None
    m['totals']['reconciliation_complete'] = False
    m['monthly'] = deepcopy(d.get('monthly', []))
    m['coverage_note'] = note
    return d, m
