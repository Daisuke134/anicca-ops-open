#!/usr/bin/env bash
# Day-over-day check: yesterday (Y) vs day before (B). Free; reads local files only.
# Sources: finance/REVENUE-BY-SOURCE.csv (dated rows with amount_jpy, excluding all-time cumulative rows),
#          metrics/x-followers.csv (diceai0, last reading per day), metrics/capafy-daily.csv (kind=day orders).
# Gap: no dated per-day X impressions file exists, so impressions are not compared.
set -euo pipefail
T=/workspace/team; Y=$(date -d yesterday +%F); B=$(date -d '2 days ago' +%F)
rev(){ python3 - "$1" <<'P'
import csv,sys
d=sys.argv[1];s=0
for r in csv.DictReader(open('/workspace/team/finance/REVENUE-BY-SOURCE.csv')):
    if r['date']==d and r['amount_jpy'] and 'all-time' not in r['status']: s+=float(r['amount_jpy'])
print(round(s,2))
P
}
fol(){ awk -F, -v d="$1" '$2=="diceai0" && substr($1,1,10)<=d {v=$3} END{print v+0}' $T/metrics/x-followers.csv; }
# Apify: metrics/apify-latest.json from scripts/tracking/apify_daily.py (run first)
cap(){ awk -F, -v d="$1" '$1==d && $2=="day"{v=$3} END{print v+0}' $T/metrics/capafy-daily.csv; }
RY=$(rev $Y); RB=$(rev $B); FY=$(fol $Y); FB=$(fol $B); CY=$(cap $Y); CB=$(cap $B)
pct(){ python3 -c "a,b=float('$1'),float('$2');print('n/a' if b==0 else round((a-b)/b*100,1))"; }
pass(){ python3 -c "a,b=float('$1'),float('$2');print('PASS' if (b==0 and a>0) or (b>0 and a>=b*1.1) else 'FAIL')"; }
AP=$(python3 -c "import json;d=json.load(open('$T/metrics/apify-latest.json'));print(d['users_total'],d['runs_total'],d['revenue_usd'],sep='|')" 2>/dev/null || echo "unknown (source error)|unknown (source error)|unknown (source error)")
IFS='|' read AU AR AV <<<"$AP"
# RapidAPI: metrics/rapidapi-latest.json from scripts/tracking/rapidapi_daily.py (run first)
RA=$(python3 -c "import json;d=json.load(open('$T/metrics/rapidapi-latest.json'));print(d['subscribers'],d['calls_total'],d['revenue_usd'],sep='|')" 2>/dev/null || echo "unknown (source error)|unknown (source error)|unknown (source error)")
IFS='|' read RS RC RV <<<"$RA"
PR=$(pct $RY $RB); PF=$(pct $FY $FB); PC=$(pct $CY $CB)
SR=$(pass $RY $RB); SF=$(pass $FY $FB); SC=$(pass $CY $CB)
OUT=$T/metrics/DOD.csv
[ -f $OUT ] || echo "run_at,day,prev_day,revenue_jpy,revenue_prev,rev_pct,rev_result,diceai0_followers,followers_prev,fol_pct,fol_result,capafy_orders,capafy_prev,cap_pct,cap_result,overall,apify_users,apify_runs,apify_revenue_usd,rapidapi_subscribers,rapidapi_calls,rapidapi_revenue_usd" > $OUT
ALL=PASS; [ "$SR" = PASS ] && [ "$SF" = PASS ] || ALL=FAIL
echo "$(date '+%F %H:%M'),$Y,$B,$RY,$RB,$PR,$SR,$FY,$FB,$PF,$SF,$CY,$CB,$PC,$SC,$ALL,$AU,$AR,$AV,$RS,$RC,$RV" >> $OUT
echo "DOD $Y vs $B | revenue ¥$RY vs ¥$RB ($PR%) $SR | @diceai0 followers $FY vs $FB ($PF%) $SF | Capafy orders $CY vs $CB ($PC%) $SC | overall $ALL | Apify users $AU runs $AR revenue $AV | RapidAPI subscribers $RS calls $RC revenue $RV"
echo "gap: X impressions not compared (no dated daily impressions file)"
