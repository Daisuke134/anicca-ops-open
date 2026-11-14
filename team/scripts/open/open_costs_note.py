"""Decided /open cost facts (参謀 2026-10-31). Imported by build_open_metrics.py and build_open_data.py so both JSONs agree.
Display is USD; yen kept as a secondary note. FX = team finance rate fx_jpy_per_usd in finance/REVENUE-BY-SOURCE.json."""
GROK_ULTRA_PAID_JPY = 20445      # paid 2026-10-31, invoice 766D3D820C (this month's actual spend)
GROK_ULTRA_MONTHLY_JPY = 34800   # recurring from 2026-11-30; replaces X Super ¥17,800/month (not added to it)
OLD_SUPER_NAME = 'Grok Bot + Cursor (X Super)'
def grok_ultra(fx):
    u = lambda j: round(j / fx, 2)
    return [dict(item='Grok Bot Ultra — this month (actual spend)', label_ja='Grok Bot Ultra 今月の実支出', date='2026-10-31', invoice='766D3D820C',
                 amount_usd=u(GROK_ULTRA_PAID_JPY), amount_jpy=GROK_ULTRA_PAID_JPY, kind='paid'),
            dict(item='Grok Bot Ultra — recurring from 2026-11-30', label_ja='Grok Bot Ultra 11/30からの固定費', starts='2026-11-30',
                 monthly_usd=u(GROK_ULTRA_MONTHLY_JPY), monthly_jpy=GROK_ULTRA_MONTHLY_JPY, kind='recurring',
                 replaces='X Super ¥17,800/month (not double-counted)')]
def fx_note(fx): return f'USD/JPY {fx} (team finance rate, finance/REVENUE-BY-SOURCE.json fx_jpy_per_usd, 2026-10-31)'
EXPENSES_STATUS = 'partial'
GROSS_PROFIT_STATUS = dict(en='partial', ja='partial')
ULTRA_PAID_LINE = 'Grok Bot Ultra (paid 2026-10-31, invoice 766D3D820C)'
ULTRA_PAID_DATE = '2026-10-31'
def expenses(led, fx, month=None, observed=None):
    """Expense lines for the reported month (default: current JST month).
    Ledger MTD lines count only if the ledger is from that month; the Grok Ultra payment only if its
    transaction date falls in that month (2026-11-01 fix: no carry-over into other months)."""
    import datetime as _dt
    month = month or _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=9))).strftime('%Y-%m')
    items = dict(led.get('expense_by_vendor_mtd') or {}) if str(led.get('date', ''))[:7] == month else {}
    if ULTRA_PAID_DATE[:7] == month and not any('Ultra' in k for k in items): items[ULTRA_PAID_LINE] = round(GROK_ULTRA_PAID_JPY / fx, 2)
    coverage = expense_coverage(led, month, observed)
    unknown = coverage['unknown_vendor_count'] or coverage['unknown_amount_row_count']
    total = None if unknown or not items or not coverage['ledger_month_available'] else round(sum(items.values()), 2)
    return items, total

def expense_coverage(led, month=None, observed=None):
    """Public-safe scope only: never export receipt IDs, raw rows or account metadata.
    Native JPY is a separately labelled observed-payment subset, not an FX conversion,
    usage expense, complete company total, or final settlement total.
    """
    import datetime as _dt
    import math
    month = month or _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=9))).strftime('%Y-%m')
    available = str(led.get('date', ''))[:7] == month and isinstance(led.get('expense_by_vendor_mtd'), dict)
    items = led['expense_by_vendor_mtd'] if available else {}
    numeric = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    known = [v for v in items.values() if numeric(v)]
    obs = observed or {}
    scope = (obs.get('observed_payment_subsets_by_month') or {}).get(month) or {}
    if not scope:
        old = obs.get('observed_payment_subset') or {}
        if str(old.get('period_start', ''))[:7] == month: scope = old
    rows = [r for r in obs.get('charges', []) if str(r.get('date', ''))[:7] == month]
    native = scope.get('canonical_amount_jpy')
    return dict(month=month, status='partial', ledger_month_available=available,
                unknown_vendor_count=sum(not numeric(v) for v in items.values()),
                unknown_amount_row_count=sum(not numeric(r.get('amount_usd')) for r in rows),
                known_partial_usd=round(sum(known), 2) if known else None,
                observed_payment_subset_jpy=native if numeric(native) else None,
                observed_payment_row_count=scope.get('row_count'),
                observed_payment_as_of=scope.get('verified_at'), coverage_complete=False,
                company_total_usd=None,
                note='Observed payment subset only; missing USD values remain unknown. Native JPY is not a complete company expense total.')

