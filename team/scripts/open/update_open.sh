#!/usr/bin/env bash
# Daily /open v2 refresh (spec team/OPEN-PAGE-V2.md). Build fails (exit 1, nothing published) if any displayed row has no source
# or if snapshot JSON contains a forbidden label. The products repository owns the public HTML template.
# Public metrics.json is the rich build_open_metrics.py snapshot (same schema as aniccaai.com/open),
# published by publish_open_repo.sh over HTTPS from this box. Thin v2 JSON is kept locally and is
# not allowed to overwrite the rich public files.
set -euo pipefail
D=/workspace/team/scripts/open; S=$D/site; mkdir -p $S
python3 /workspace/team/metrics/collect_all.py >/tmp/collect_all.log 2>&1 || { rc=$?; echo "collect_all.py failed (exit=$rc); refusing to publish stale metrics; log=/tmp/collect_all.log" >&2; exit "$rc"; }  # refreshes metrics/snapshots/latest.json (MRR)
python3 /workspace/team/finance/build_revenue_ledger.py >/tmp/build_revenue_ledger.log 2>&1 || { rc=$?; echo "build_revenue_ledger.py failed (exit=$rc); refusing to publish stale revenue; log=/tmp/build_revenue_ledger.log" >&2; exit "$rc"; }  # refreshes finance/REVENUE-BY-SOURCE.*
python3 $D/build_open_v2.py $S
if [ -f "$S/store_funnel.json" ]; then
  python3 $D/validate_funnel_monotonic.py "$S/store_funnel.json"
  python3 $D/validate_funnel_integrity.py "$S/store_funnel.json"
fi
# Rich public metrics (loops/charts/businesses). Reuse the live RevenueCat/Stripe
# sidecars when a fresh collector export is not present, so a box publish can
# proceed without GitHub Actions or Postiz.
RC_CHARTS=${OPEN_REVENUECAT_CHARTS:-$S/revenuecat-charts.json}
if [ -z "${OPEN_REVENUECAT_CHARTS:-}" ] && [ ! -f "$RC_CHARTS" ] && [ -f /tmp/revenuecat-charts-live.json ]; then
  RC_CHARTS=/tmp/revenuecat-charts-live.json
fi
ST_METRICS=${OPEN_STRIPE_METRICS:-}
if [ -z "${ST_METRICS}" ] && [ -f /tmp/stripe-metrics-live.json ]; then
  ST_METRICS=/tmp/stripe-metrics-live.json
fi
export OPEN_REVENUECAT_CHARTS=$RC_CHARTS
[ -n "$ST_METRICS" ] && export OPEN_STRIPE_METRICS=$ST_METRICS
python3 $D/build_open_metrics.py $S/metrics.public.json
# Stage a publish dir with rich metrics only (do not ship thin v2 data.json).
PUB=$S/public; mkdir -p "$PUB"
cp -f $S/metrics.public.json $PUB/metrics.json
bash $D/publish_open_repo.sh $PUB/metrics.json   # publishes snapshot JSON; products repo owns the public UI (Netlify deploy action)
