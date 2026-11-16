#!/usr/bin/env python3
"""x_presim.py — synthetic-persona pre-score for a post BEFORE it ships, then predicted-vs-actual at +24h.

Lightweight stand-in for MiroFish (github.com/666ghj/MiroFish, AGPL-3.0; needs an LLM key + Zep Cloud key + many
simulation rounds — not runnable on the box today). Same idea, small: a panel of audience personas reacts to the
post; reactions are aggregated into predicted impressions/likes/replies/follows, scaled by the account's own
baseline; every prediction is logged and later scored against the real 24h numbers.

Backends
  heuristic  deterministic, free, instant (feature x persona affinity). Default; always available.
  codex      the same persona panel judged by an LLM via Codex CLI on the ChatGPT plan (no per-token cost).
             Uses CODEX_HOME=/home/box/.codex-chatgpt. Never uses any pay-per-token key. Falls back to heuristic.

Usage
  x_presim.py score --account diceai0 --text "post text" [--id 123] [--backend heuristic|codex] [--surface x]
  x_presim.py score --account diceai0 --file posts.json            # [{"id":..,"text":..}, ...]
  x_presim.py actual                                               # fill actual_* from team/marketing/X-METRICS.csv (age>=24h)
  x_presim.py report                                               # calibration: median |log error| per metric, per backend
Log: team/metrics/presim-log.csv (one row per prediction; append-only)
"""
import argparse, csv, datetime, hashlib, json, math, os, re, statistics, subprocess, sys

import presim_calib

ROOT = os.environ.get('ANICCA_OPS', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
METRICS = os.path.join(ROOT, 'team/marketing/X-METRICS.csv')
LOG = os.path.join(ROOT, 'team/metrics/presim-log.csv')
JST = datetime.timezone(datetime.timedelta(hours=9))
FIELDS = ['ts_jst', 'surface', 'account', 'post_id', 'text_sha', 'backend', 'baseline_impr', 'stop_rate',
          'pred_impr', 'pred_likes', 'pred_replies', 'pred_follows', 'top_persona', 'weak_persona', 'fix_hint',
          'actual_impr', 'actual_likes', 'actual_replies', 'actual_follows', 'abs_log_err_impr', 'abs_log_err_likes',
          'text_preview']

# Persona panel: share of the account's reachable audience + what makes each stop scrolling.
PERSONAS = [
    dict(name='indie_hacker_en', share=.22, lang='en', likes=['revenue', '$', 'mrr', 'users', 'paid', 'shipped', 'app store', 'downloads', 'build in public'], hates=['hackathon', 'announce']),
    dict(name='ai_agent_builder_en', share=.20, lang='en', likes=['agent', 'agents', 'github', 'repo', 'open-source', 'open source', 'skill', 'llm', 'eval', 'prompt', 'claude', 'codex'], hates=['affirmation']),
    dict(name='vc_yc_scout_en', share=.06, lang='en', likes=['yc', 'zero-human', 'autonomous', 'revenue', 'growth', 'company', 'traction'], hates=['lol']),
    dict(name='ios_dev_en', share=.10, lang='en', likes=['apple', 'ios', 'iphone', 'app store', 'rejected', 'paywall', 'revenuecat', 'testflight'], hates=[]),
    dict(name='wellness_user_en', share=.07, lang='en', likes=['sleep', 'anxiety', 'meditation', 'habit', 'suffering', 'mind', 'affirmation'], hates=['api', 'repo']),
    dict(name='jp_startup', share=.17, lang='ja', likes=['yc', 'エージェント', '起業', '売上', 'ハッカソン', 'スタートアップ', '自律', 'ai', '会社'], hates=[]),
    dict(name='jp_dev', share=.10, lang='ja', likes=['github', 'コード', 'プラグイン', 'エージェント', 'claude', 'cursor', 'oss', '公開'], hates=[]),
    dict(name='lurker_generalist', share=.08, lang='*', likes=['?', 'how', 'why', 'なぜ', 'どう'], hates=[]),
]

def feats(t):
    tl = t.lower(); first = t.strip().split('\n')[0]
    return dict(
        lang='ja' if re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', t) else 'en',
        nums=len(re.findall(r'\d[\d,.]*', t)),
        link=bool(re.search(r'https?://', t)),
        length=len(t),
        lines=t.count('\n') + 1,
        hook_num=bool(re.search(r'\d', first)),
        hook_short=len(first) <= 90,
        story=bool(re.search(r'\b(we|i|our)\b|私たち|自分', tl)),
        failure=bool(re.search(r'rejected|failed|0 paid|broke|mistake|lost|入賞なし|失敗|落ち', tl)),
        question=t.strip().endswith('?') or '？' in t,
        mention=bool(re.search(r'@\w+', t)),
        tl=tl)

def heuristic_panel(text):
    f = feats(text); out = []
    for p in PERSONAS:
        if p['lang'] not in ('*', f['lang']):
            stop = 0.02  # wrong language: almost nobody stops
        else:
            hits = sum(1 for k in p['likes'] if k in f['tl']); miss = sum(1 for k in p['hates'] if k in f['tl'])
            stop = 0.05 + 0.06 * min(hits, 4) - 0.04 * miss
            stop += 0.05 * f['hook_num'] + 0.03 * f['hook_short'] + 0.04 * f['failure'] + 0.02 * f['story']
            stop += 0.02 * min(f['nums'], 4) / 4 - 0.03 * (f['length'] > 600) - 0.02 * f['mention']
        stop = max(0.01, min(0.6, stop))
        like = stop * (0.10 + 0.05 * f['failure'] + 0.03 * f['story'])
        reply = stop * (0.02 + 0.04 * f['question'] + 0.02 * f['failure'])
        follow = stop * 0.006 * (1 + (p['name'] in ('ai_agent_builder_en', 'jp_startup', 'indie_hacker_en')))
        out.append(dict(persona=p['name'], stop=round(stop, 3), like=round(like, 4), reply=round(reply, 4), follow=round(follow, 4),
                        why=f"hits={sum(1 for k in p['likes'] if k in f['tl'])}"))
    return out

CODEX_PROMPT = """You are simulating an X (Twitter) audience panel. Do not run any commands or edit files. Reply with JSON only.
For each persona below, estimate for ONE impression of this post: stop = probability they stop scrolling and read,
like/reply/follow = probability of that action per impression. Be realistic (typical like rate per impression is 0.5-3%).
Personas: {personas}
Post:
<<<
{text}
>>>
Output exactly: {{"panel":[{{"persona":"<name>","stop":0.0,"like":0.0,"reply":0.0,"follow":0.0,"why":"<8 words>"}}...],"fix_hint":"<one concrete rewrite tip, 15 words>"}}"""

def codex_panel(text):
    env = dict(os.environ, CODEX_HOME='/home/box/.codex-chatgpt')
    desc = '; '.join(f"{p['name']} ({p['lang']}, cares about {', '.join(p['likes'][:5])})" for p in PERSONAS)
    try:
        r = subprocess.run(['codex', 'exec', '--skip-git-repo-check', '--sandbox', 'read-only',
                            CODEX_PROMPT.format(personas=desc, text=text)], capture_output=True, text=True, timeout=300, env=env, cwd='/tmp')
        m = re.findall(r'\{.*"panel".*\}', r.stdout, re.S)
        d = json.loads(m[-1][m[-1].find('{"panel"'):] if '{"panel"' in m[-1] else m[-1])
        panel = [x for x in d['panel'] if x.get('persona') in {p['name'] for p in PERSONAS}]
        if len(panel) < len(PERSONAS) // 2: raise ValueError('short panel')
        return panel, d.get('fix_hint', '')
    except Exception as e:
        print(f'[x_presim] codex backend failed ({type(e).__name__}); using heuristic', file=sys.stderr)
        return None, ''

def baseline(account):
    """Median 24h+ impressions of the account's original posts (not replies/self-reply links/retweets)."""
    vals = []
    try:
        for r in csv.DictReader(open(METRICS, encoding='utf-8')):
            if r['account'] == account and r['format'] not in ('reply', 'profile', 'retweet', 'self_reply_link') and r['impressions'] and float(r['age_h'] or 0) >= 24:
                vals.append(float(r['impressions']))
    except FileNotFoundError:
        pass
    return statistics.median(vals) if vals else 50.0

def connect_baseline(log_path):
    """Median actual_impr of past connect-format predictions (fmt_row == 'connect', actual > 0)."""
    vals = []
    try:
        for r in csv.DictReader(open(log_path, encoding='utf-8')):
            try:
                a = float(r.get('actual_impr') or 0)
            except ValueError:
                continue
            if a > 0 and presim_calib.fmt_row(r) == 'connect':
                vals.append(a)
    except FileNotFoundError:
        pass
    return statistics.median(vals) if len(vals) >= 2 else None

def aggregate(panel, base, lang='en'):
    # X mostly shows a post to readers of its language: other-language personas count at 20% of their share.
    share = {p['name']: p['share'] * (1 if p['lang'] in ('*', lang) else 0.2) for p in PERSONAS}
    w = sum(share[x['persona']] for x in panel)
    S = lambda k: sum(share[x['persona']] * float(x[k]) for x in panel) / w
    stop = S('stop')
    # X distributes more when early viewers dwell: scale baseline by stop rate vs a 0.15 "typical" stop rate.
    impr = base * max(0.25, min(4.0, (stop / 0.15) ** 1.5))
    best = max(panel, key=lambda x: float(x['stop'])); worst = min(panel, key=lambda x: float(x['stop']))
    return dict(stop_rate=round(stop, 3), pred_impr=round(impr), pred_likes=round(impr * S('like'), 1),
                pred_replies=round(impr * S('reply'), 1), pred_follows=round(impr * S('follow'), 2),
                top_persona=best['persona'], weak_persona=worst['persona'])

def ensure_log():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    if not os.path.exists(LOG):
        with open(LOG, 'w', newline='', encoding='utf-8') as fh: csv.writer(fh).writerow(FIELDS)

def score(posts, account, backend, surface, write=True):
    ensure_log(); acct_base = baseline(account); rows = []
    for p in posts:
        text = p['text']; hint = ''
        base = acct_base
        if presim_calib.fmt(text) == 'connect':
            cb = connect_baseline(LOG)
            if cb is not None: base = cb
        panel = None
        if backend == 'codex': panel, hint = codex_panel(text)
        used = 'codex' if panel else 'heuristic'
        if not panel: panel = heuristic_panel(text)
        if not hint:
            f = feats(text)
            hint = ('put a number in line 1' if not f['hook_num'] else 'cut line 1 under 90 chars' if not f['hook_short']
                    else 'end with a concrete question' if not f['question'] else 'name the failure plainly')
        a = aggregate(panel, base, feats(text)['lang'])
        row = dict(ts_jst=datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M'), surface=surface, account=account,
                   post_id=p.get('id', ''), text_sha=hashlib.sha1(text.encode()).hexdigest()[:10], backend=used,
                   baseline_impr=base, fix_hint=hint, text_preview=text[:80].replace('\n', ' '), **a)
        rows.append((row, panel))
        if write:
            with open(LOG, 'a', newline='', encoding='utf-8') as fh:
                csv.DictWriter(fh, FIELDS).writerow({k: row.get(k, '') for k in FIELDS})
    return rows

def le(pred, act):
    return round(abs(math.log((float(act) + 1) / (float(pred) + 1))), 3)

def fill_actual():
    ensure_log()
    m = {}
    for r in csv.DictReader(open(METRICS, encoding='utf-8')):
        if r['post_id'] and r['impressions'] and float(r['age_h'] or 0) >= 24: m[r['post_id']] = r  # later rows win
    rows = list(csv.DictReader(open(LOG, encoding='utf-8'))); n = 0
    for r in rows:
        a = m.get(r['post_id'])
        if a and not r['actual_impr']:
            r.update(actual_impr=a['impressions'], actual_likes=a['likes'], actual_replies=a['replies'], actual_follows='',
                     abs_log_err_impr=le(r['pred_impr'], a['impressions']), abs_log_err_likes=le(r['pred_likes'], a['likes'])); n += 1
    with open(LOG, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, FIELDS); w.writeheader(); w.writerows(rows)
    print(f'filled {n} rows')

def report(by='backend'):
    rows = [r for r in csv.DictReader(open(LOG, encoding='utf-8')) if r['abs_log_err_impr']]
    if by == 'lang':
        key = lambda r: feats(r.get('text_preview', ''))['lang']
    elif by == 'surface':
        key = lambda r: r['surface']
    else:
        key = lambda r: r['backend']
    for g in sorted({key(r) for r in rows}):
        rs = [r for r in rows if key(r) == g]
        print(f"{g}: n={len(rs)} median|logerr| impr={statistics.median(float(r['abs_log_err_impr']) for r in rs):.2f} "
              f"likes={statistics.median(float(r['abs_log_err_likes']) for r in rs):.2f}  (0.69 = off by 2x)")
    if not rows: print('no scored rows yet')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('score'); s.add_argument('--account', default='diceai0'); s.add_argument('--text'); s.add_argument('--id', default='')
    s.add_argument('--file'); s.add_argument('--backend', default='heuristic', choices=['heuristic', 'codex'])
    s.add_argument('--surface', default='x'); s.add_argument('--dry', action='store_true'); s.add_argument('--panel', action='store_true')
    sp.add_parser('actual'); rp = sp.add_parser('report'); rp.add_argument('--by', default='backend', choices=['backend', 'surface', 'lang'])
    a = ap.parse_args()
    if a.cmd == 'score':
        posts = json.load(open(a.file, encoding='utf-8')) if a.file else [dict(id=a.id, text=a.text)]
        for row, panel in score(posts, a.account, a.backend, a.surface, write=not a.dry):
            print(json.dumps({k: row[k] for k in ('post_id', 'backend', 'baseline_impr', 'stop_rate', 'pred_impr', 'pred_likes', 'pred_replies', 'pred_follows', 'top_persona', 'weak_persona', 'fix_hint')}, ensure_ascii=False))
            if a.panel: print(json.dumps(panel, ensure_ascii=False))
    elif a.cmd == 'actual': fill_actual()
    else: report(a.by)
