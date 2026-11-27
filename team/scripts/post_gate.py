#!/usr/bin/env python3
"""Hard pre-post gate for every create / schedule / delete / cancel on a social account.

Why: on 2026-11-11 a 参謀 batch posted to Muse-owned TikTok/IG/YouTube (@aniccaaffirmation ...)
with no winner original and no coordination, and cancelled Muse's scheduled posts. This gate makes
that impossible for any script that calls it. It FAILS CLOSED: if anything cannot be verified, exit 2.

A post / delete / cancel is allowed only when ALL hold:
  (a) owner   : the poster is the owner of the account in team/ACCOUNT-OWNERS.md (```post-gate-owners``` block)
  (b) source  : a non-placeholder http(s) source URL is passed (create/schedule: the cited winner original;
                delete/cancel: the file/decision URL that authorises it)
  (c) claim   : team/CLAIMS.md on main has, from this poster, a POST-CLAIM that is still open
                (open = claimed and not released; a claim stays open until a later POST-RELEASE):
                  - POST-CLAIM | YYYY-MM-DD HH:MM JST | <poster> | <platform>:<@handle> | <action> | <source URL>
                and no OTHER poster holds an open claim on that account (open = claimed, no later POST-RELEASE)
                  - POST-RELEASE | YYYY-MM-DD HH:MM JST | <poster> | <platform>:<@handle>
  (d) hold    : no hold for that account / integration / lane in any marketing-destinations.json
                (a hold may exempt posters via "allowed_posters": [...]; holds whose reason starts with
                 "muse_only" exempt only muse, because they exist to keep everyone else off Muse's accounts)

  (e) x-dedup : X create/schedule only. The candidate text (--text-file) is compared with the account's own posts
                from a FRESH read-back (--recent-json, the raw x get_users_posts output, file <= 10 min old). Refused
                when the same/near-same text (same first line, or similarity >= 0.85, URLs ignored) is already live in
                the last 24h. Also refused when this text was already ATTEMPTED (intent ledger
                team/state/x-post-intents.jsonl, written by --record-intent) unless the read-back was taken >= 3 min
                after that attempt and does not contain it. This is the "uncertain submit" rule: after a Post click
                that seems to hang, read the timeline back; never click Post again blind.

  (f) intent lock: every allowed create/schedule with text is appended to the intent ledger
                (team/state/x-post-intents.jsonl, override with $POST_GATE_INTENTS). A second
                create/schedule whose text has the same sha256 within INTENT_LOCK_MIN (30) minutes
                is refused, so an allowed attempt cannot be silently repeated.

Data is read from GitHub main (Daisuke134/anicca-ops) so a claim only counts once it is committed and visible
to everyone. Token: $GITHUB_TOKEN or $GH_TOKEN, else `gh api`. Tests / offline: POST_GATE_LOCAL_ROOT=<repo root>.

CLI:
  post-gate.py --poster muse --platform tiktok --account @aniccaaffirmation --action create --source-url URL
  post-gate.py --poster muse --postiz-payload payload.json --action schedule --source-url URL
Library (inside a posting script, right before the provider call):
  import post_gate; post_gate.guard_postiz(method, url, body)   # poster/source from env
Env for scripts: ANICCA_POSTER (required), ANICCA_SOURCE_URL (required), POST_GATE_ACCOUNT=platform:@handle (deletes).
Exit codes: 0 allowed, 2 refused.
"""
from __future__ import annotations
import argparse, base64, datetime as dt, glob, json, os, re, subprocess, sys, urllib.request

REPO = os.environ.get("POST_GATE_REPO", "Daisuke134/anicca-ops")
REF = os.environ.get("POST_GATE_REF", "main")
JST = dt.timezone(dt.timedelta(hours=9))
FUTURE_CLAIM_TOLERANCE_MIN = 5
DEST_FILES = ["team/distribution/shortform/marketing-destinations.json",
              "team/lm-compat/lm/config/marketing-destinations.json"]
ALIASES = {
    "muse": "muse", "ミューズ": "muse",
    "dots": "dots", "codex": "codex",
    "grok-sanbo": "grok-sanbo", "sanbo": "grok-sanbo", "参謀": "grok-sanbo", "grok": "grok-sanbo",
    "grok-bot": "grok-sanbo",
    # X Operator is its own poster since 2026-11-13 23:5x JST (sole @diceai0/@selawmqt publisher after the 11/13
    # duplicates). It used to alias to grok-sanbo, which let 参謀 routines pass the owner check on X.
    "x-operator": "x-operator", "xoperator": "x-operator", "x operator": "x-operator",
    "marketer": "marketer", "anicca-marketer": "marketer",
    "dr-eggbot": "dr-eggbot", "eggbot": "dr-eggbot", "fucker": "fucker",
}
PLATFORM_ALIASES = {"tt": "tiktok", "tiktok": "tiktok", "ig": "instagram", "instagram": "instagram",
                    "instagram-standalone": "instagram", "youtube": "youtube", "yt": "youtube",
                    "x": "x", "twitter": "x", "threads": "threads", "bluesky": "bluesky", "mastodon": "mastodon",
                    "linkedin": "linkedin", "linkedin-page": "linkedin", "tumblr": "tumblr", "pinterest": "pinterest"}
MUTATING = {"create", "schedule", "delete", "cancel", "update"}
PLACEHOLDER = re.compile(r"(example\.com|<|>|TODO|TBD|placeholder|^https?://?$)", re.I)


class Refused(Exception):
    pass


# ---------------------------------------------------------------- (e) X duplicate gate
DEDUP_WINDOW_H = 24
RECENT_MAX_AGE_MIN = 10
UNCERTAIN_WAIT_MIN = 3
SIMILAR = 0.85
INTENT_LOCK_MIN = 30
URL_RE = re.compile(r"https?://\S+")
HERE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def norm_text(t: str) -> str:
    t = URL_RE.sub(" ", t or "").lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def first_line(t: str) -> str:
    for line in (t or "").splitlines():
        n = norm_text(line)
        if n:
            return n
    return ""


def text_key(t: str, in_reply_to: str = "") -> str:
    import hashlib
    return hashlib.sha256(f"{in_reply_to}|{norm_text(t)}".encode()).hexdigest()[:16]


def load_recent(path: str, now=None):
    """Parse the raw output of the x get_users_posts / get_posts_by_ids tool (or a JSON list). Fail closed."""
    now = now or dt.datetime.now(JST)
    if not path or not os.path.exists(path):
        raise Refused("(e) --recent-json is required for X posts: save a FRESH x get_users_posts read of the account "
                      "(last 24h, replies included) to a file and pass it")
    import time as _t  # file mtimes are wall-clock, so freshness uses the wall clock even when --now is simulated
    age_min = (_t.time() - os.path.getmtime(path)) / 60
    if age_min > RECENT_MAX_AGE_MIN and not os.environ.get("POST_GATE_IGNORE_MTIME"):
        raise Refused(f"(e) {path} is {age_min:.0f} min old; read the account's timeline again (max {RECENT_MAX_AGE_MIN} min)")
    raw = open(path, encoding="utf-8").read()
    data = None
    for start in [m.start() for m in re.finditer(r"[\[{]", raw)][:50]:
        try:
            data, _ = json.JSONDecoder().raw_decode(raw[start:])
            break
        except ValueError:
            continue
    if data is None:
        raise Refused(f"(e) cannot parse posts JSON in {path}")
    posts = data.get("data", []) if isinstance(data, dict) else data
    if isinstance(posts, dict):
        posts = [posts]
    out = []
    for p in posts or []:
        if isinstance(p, dict) and "text" in p and "created_at" in p:
            out.append(p)
    if posts and not out:
        raise Refused("(e) read-back has posts without text/created_at; request post.fields created_at,text")
    return out, dt.datetime.fromtimestamp(os.path.getmtime(path), JST)


def _intents_path():
    return os.environ.get("POST_GATE_INTENTS", os.path.join(HERE_ROOT, "team/state/x-post-intents.jsonl"))


def load_intents():
    p = _intents_path()
    if not os.path.exists(p):
        return []
    out = []
    for line in open(p, encoding="utf-8"):
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def record_intent(account, poster, text, in_reply_to="", now=None):
    now = dt.datetime.now(JST)  # wall clock: compared with read-back file mtimes
    p = _intents_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    import hashlib
    rec = {"at": now.strftime("%Y-%m-%d %H:%M:%S JST"), "ts": now.timestamp(), "account": account, "poster": poster,
           "key": text_key(text, in_reply_to), "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
           "first_line": first_line(text)[:80], "in_reply_to": in_reply_to}
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def intent_lock(account, poster, text, in_reply_to="", now=None):
    """(f) Refuse a second create/schedule of the same text sha256 within INTENT_LOCK_MIN minutes.

    On success the attempt is appended to the intent ledger (same file as --record-intent) and the
    record's `at` timestamp is returned, so callers can surface it like res["intent"]."""
    import hashlib
    now = now or dt.datetime.now(JST)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    key = text_key(text, in_reply_to)
    lo = now - dt.timedelta(minutes=INTENT_LOCK_MIN)
    for it in load_intents():
        if it.get("account") != account:
            continue
        same = it.get("sha256") == sha or (it.get("sha256") is None and it.get("key") == key)
        if not same:
            continue
        try:
            t = dt.datetime.fromtimestamp(it["ts"], JST)
        except (KeyError, TypeError, ValueError):
            continue
        if lo <= t <= now + dt.timedelta(minutes=5):
            raise Refused(f"(f) intent lock: identical text was already submitted for {account} at "
                          f"{it.get('at')} by {it.get('poster')}; a second create/schedule of the same text is "
                          f"refused for {INTENT_LOCK_MIN} min. Change the text or wait.")
    p = _intents_path()
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    rec = {"at": now.strftime("%Y-%m-%d %H:%M:%S JST"), "ts": now.timestamp(), "account": account,
           "poster": poster, "key": key, "sha256": sha, "first_line": first_line(text)[:80],
           "in_reply_to": in_reply_to, "lock": True}
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec["at"]


def x_dedup_check(account, text, recent_posts, readback_at, in_reply_to="", now=None, intents=None):
    """Raise Refused if `text` is already live (24h) or was already attempted without a later clean read-back."""
    import difflib
    now = now or dt.datetime.now(JST)
    if not (text or "").strip():
        raise Refused("(e) --text-file is empty; the exact text to be posted is required")
    cand, cand_fl = norm_text(text), first_line(text)
    lo = now - dt.timedelta(hours=DEDUP_WINDOW_H)
    for p in recent_posts:
        try:
            when = dt.datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
        except ValueError:
            continue
        if when < lo:
            continue
        live = norm_text(p["text"])
        same_fl = len(cand_fl) >= 20 and first_line(p["text"]) == cand_fl
        ratio = difflib.SequenceMatcher(None, cand, live).ratio() if len(cand) >= 30 else (1.0 if cand == live and cand else 0.0)
        if same_fl or ratio >= SIMILAR:
            raise Refused(f"(e) duplicate: same/near-same text is already live on {account} as "
                          f"https://x.com/i/status/{p.get('id')} ({when.astimezone(JST):%m-%d %H:%M} JST, "
                          f"{'same first line' if same_fl else f'similarity {ratio:.2f}'}). Do not post it again.")
    key = text_key(text, in_reply_to)
    for it in (intents if intents is not None else load_intents()):
        if it.get("key") != key or it.get("account") != account:
            continue
        t = dt.datetime.fromtimestamp(it["ts"], JST)
        if dt.datetime.now(JST) - t > dt.timedelta(hours=DEDUP_WINDOW_H):
            continue
        if readback_at < t + dt.timedelta(minutes=UNCERTAIN_WAIT_MIN):
            raise Refused(f"(e) this text was already submitted at {it['at']} by {it.get('poster')}. Uncertain submit: "
                          f"wait, then read {account}'s timeline again (read-back must be >= {UNCERTAIN_WAIT_MIN} min after the "
                          "attempt). If it is live, you are done. Never click Post twice.")
    return {"dedup": "ok", "checked_posts": len(recent_posts), "key": key}


def norm_poster(p: str) -> str:
    k = (p or "").strip().lower().replace(" ", "-").replace("_", "-")
    return ALIASES.get(k, ALIASES.get((p or "").strip(), k))


def norm_platform(p: str) -> str:
    return PLATFORM_ALIASES.get((p or "").strip().lower(), (p or "").strip().lower())


def ct_link_check(platform, action, text):
    """X create/schedule only: self-reply / app links must go through aniccaai.com/go/anicca?ct=<ct>.
    Fails closed if the linter cannot be imported."""
    if norm_platform(platform) != "x" or (action or "").lower() not in ("create", "schedule") \
            or not (text or "").strip():
        return
    try:
        scripts_dir = os.path.dirname(os.path.abspath(__file__))
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from ct_link_lint import lint
    except Exception as e:
        raise Refused(f"ct-link: cannot load link linter: {e}")
    problems = lint(text)
    if problems:
        raise Refused(f"ct-link: {', '.join(problems)} — self-reply/app links must be aniccaai.com/go/anicca?ct=<ct>")


def norm_handle(h: str) -> str:
    h = (h or "").strip().lower()
    if h and h != "*" and not h.startswith("@") and re.fullmatch(r"[\w.\-]+", h):
        h = "@" + h
    return h


# ---------------------------------------------------------------- data source (GitHub main by default)
def _gh_token():
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def read_repo_file(path: str) -> str:
    local = os.environ.get("POST_GATE_LOCAL_ROOT")
    if local:
        with open(os.path.join(local, path), encoding="utf-8") as f:
            return f.read()
    api = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={REF}"
    tok = _gh_token()
    if tok:
        req = urllib.request.Request(api, headers={"Authorization": f"Bearer {tok}",
                                                   "Accept": "application/vnd.github.raw"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    try:
        out = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw",
                              f"repos/{REPO}/contents/{path}?ref={REF}"],
                             capture_output=True, text=True, timeout=30)
        if out.returncode == 0:
            return out.stdout
    except FileNotFoundError:
        pass
    # Fallback 3: a git checkout of the same repo (this script's own repo, or POST_GATE_GIT_DIR).
    # Fetch origin/<REF> fresh, then read the committed file, so the check is still against main.
    gdir = os.environ.get("POST_GATE_GIT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        url = subprocess.run(["git", "-C", gdir, "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=10).stdout
        if REPO.lower() in url.lower():
            global _FETCHED
            if not globals().get("_FETCHED"):
                f = subprocess.run(["git", "-C", gdir, "fetch", "-q", "origin", REF],
                                   capture_output=True, text=True, timeout=60)
                _FETCHED = f.returncode == 0
            if globals().get("_FETCHED"):
                out = subprocess.run(["git", "-C", gdir, "show", f"origin/{REF}:{path}"],
                                     capture_output=True, text=True, timeout=30)
                if out.returncode == 0:
                    return out.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    raise Refused(f"cannot read {path} from GitHub {REPO}@{REF} (set GITHUB_TOKEN/GH_TOKEN or log in gh). "
                  "Refusing: claims must be checked against main.")


# ---------------------------------------------------------------- owners + integration map
def load_owners():
    """Parse the ```post-gate-owners``` block in team/ACCOUNT-OWNERS.md.
    Row: platform | account | owner | integration_ids (comma separated, optional)."""
    text = read_repo_file("team/ACCOUNT-OWNERS.md")
    m = re.search(r"```post-gate-owners\n(.*?)```", text, re.S)
    if not m:
        raise Refused("team/ACCOUNT-OWNERS.md has no ```post-gate-owners``` block")
    rows, integ = [], {}
    for line in m.group(1).splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        plat, acct, owner = norm_platform(parts[0]), norm_handle(parts[1]), norm_poster(parts[2])
        rows.append((plat, acct, owner))
        for iid in (parts[3].split(",") if len(parts) > 3 else []):
            if iid.strip():
                integ[iid.strip()] = (plat, acct)
    return rows, integ


def load_destinations():
    targets, holds = [], []
    for p in DEST_FILES:
        try:
            d = json.loads(read_repo_file(p))
        except Refused:
            raise
        except Exception as e:  # missing file is fine only if the other exists
            continue
        targets += d.get("targets") or []
        holds += d.get("holds") or []
    if not targets and not holds:
        raise Refused("no marketing-destinations.json could be read; cannot check holds")
    return targets, holds


def integration_map(owner_integ, targets, holds):
    m = dict(owner_integ)
    for t in list(targets) + list(holds):
        iid = t.get("integration_id")
        if iid and iid not in m:
            h = t.get("native_handle") or t.get("postiz_profile")
            m[iid] = (norm_platform(t.get("platform", "")), norm_handle(h))
    return m


def owner_of(rows, platform, account):
    exact = [o for (p, a, o) in rows if p == platform and a == account]
    if exact:
        return exact[0]
    wild = [o for (p, a, o) in rows if p == platform and a == "*"]
    return wild[0] if wild else None


# ---------------------------------------------------------------- claims
CLAIM_RE = re.compile(r"POST-(CLAIM|RELEASE)\s*\|\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*JST\s*\|\s*([^|]+?)\s*\|\s*([^|\s]+)")


def parse_claims(text):
    out = []
    for line in text.splitlines():
        m = CLAIM_RE.search(line)
        if not m:
            continue
        kind, ts, who, acct = m.groups()
        when = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M").replace(tzinfo=JST)
        plat, _, handle = acct.partition(":")
        out.append((kind, when, norm_poster(who), norm_platform(plat), norm_handle(handle)))
    return out


def open_claims(claims, platform, account, now):
    """Return {poster: latest claim time} for claims on this account that are still open."""
    state = {}
    for kind, when, who, plat, acct in sorted(claims, key=lambda c: c[1]):
        if plat != platform or acct != account:
            continue
        if kind == "CLAIM":
            state[who] = when
        elif kind == "RELEASE" and who in state and when >= state[who]:
            del state[who]
    # A claim stays open until a POST-RELEASE; only claims dated too far in the future are ignored.
    return {w: t for w, t in state.items()
            if t <= now + dt.timedelta(minutes=FUTURE_CLAIM_TOLERANCE_MIN)}


# ---------------------------------------------------------------- the gate
def check(poster, platform, account, action, source_url, integration_id=None, now=None, _cache=None,
          text=None, recent_json=None, in_reply_to="", lang=None, kind=None):
    now = now or dt.datetime.now(JST)
    poster, platform, account, action = norm_poster(poster), norm_platform(platform), norm_handle(account), (action or "").lower()
    if not poster:
        raise Refused("no poster given (ANICCA_POSTER / --poster)")
    if action not in MUTATING:
        raise Refused(f"unknown action {action!r}; use one of {sorted(MUTATING)}")
    c = _cache if _cache is not None else {}
    if "owners" not in c:
        c["owners"] = load_owners()
        c["dest"] = load_destinations()
        c["claims"] = parse_claims(read_repo_file("team/CLAIMS.md"))
    rows, owner_integ = c["owners"]
    targets, holds = c["dest"]
    imap = integration_map(owner_integ, targets, holds)
    if integration_id and (not platform or not account):
        if integration_id not in imap:
            raise Refused(f"integration {integration_id} is not mapped to an account in ACCOUNT-OWNERS.md post-gate-owners "
                          "or marketing-destinations.json; add it before posting")
        platform, account = imap[integration_id]
    if not platform or not account:
        raise Refused("platform and account are required")
    acct_key = f"{platform}:{account}"
    # (a) owner
    owner = owner_of(rows, platform, account)
    if owner is None:
        raise Refused(f"(a) {acct_key} has no owner in ACCOUNT-OWNERS.md post-gate-owners")
    if owner != poster:
        raise Refused(f"(a) {acct_key} is owned by {owner}; {poster} may not {action} on it. "
                      f"Write a draft to team-outbox/{poster}/to-{owner}-*.md instead.")
    # (b) source URL
    if not source_url or not re.match(r"^https?://\S+\.\S+", source_url) or PLACEHOLDER.search(source_url):
        raise Refused("(b) a real winner/source URL is required (--source-url / ANICCA_SOURCE_URL)")
    # (g) EN connect opener: first line must lead with the request (checked before claims so the
    # advice is reported even when the claim itself would refuse)
    if lang == "en" and kind == "connect" and action in ("create", "schedule") and (text or "").strip():
        check_en_connect_opener(text)
    # (c) claim on main
    oc = open_claims(c["claims"], platform, account, now)
    if poster not in oc:
        raise Refused(f"(c) no POST-CLAIM by {poster} for {acct_key} in team/CLAIMS.md on main "
                      f"(a claim stays open until a POST-RELEASE). Append: '- POST-CLAIM | {now:%Y-%m-%d %H:%M} JST | "
                      f"{poster} | {acct_key} | {action} | <source URL>' and commit it to main first.")
    others = sorted(w for w in oc if w != poster)
    if others:
        raise Refused(f"(c) conflicting open claim on {acct_key} by {', '.join(others)}")
    # (d) holds
    for h in holds:
        hp = norm_platform(h.get("platform", ""))
        handles = {norm_handle(h.get("postiz_profile")), norm_handle(h.get("native_handle"))} - {""}
        lanes = {h.get("lane_id"), h.get("former_lane_id")} - {None}
        hit = (hp == platform and account in handles) or (integration_id and h.get("integration_id") == integration_id)
        if not hit:
            for t in targets:
                if t.get("lane_id") in lanes and norm_platform(t.get("platform", "")) == platform and \
                        account in {norm_handle(t.get("native_handle")), norm_handle(t.get("postiz_profile"))}:
                    hit = True
        allowed = set(norm_poster(x) for x in (h.get("allowed_posters") or []))
        if str(h.get("reason", "")).startswith("muse_only"):
            allowed.add("muse")  # "muse_only_*" holds stop everyone else's loops; Muse is the owner they protect
        if hit and poster not in allowed:
            raise Refused(f"(d) hold on {acct_key}: reason={h.get('reason')} target_daily_limit={h.get('target_daily_limit')}")
    res = {"allowed": True, "poster": poster, "account": acct_key, "action": action, "owner": owner,
           "claim_at": oc[poster].strftime("%Y-%m-%d %H:%M JST"), "source_url": source_url}
    # (e) X duplicate gate (create/schedule only)
    if platform == "x" and action in ("create", "schedule"):
        ct_link_check(platform, action, text)
        posts, readback_at = load_recent(recent_json, now)
        res.update(x_dedup_check(acct_key, text or "", posts, readback_at, in_reply_to=in_reply_to, now=now))
    # (f) intent lock: record every allowed create/schedule; refuse an identical-text repeat within 30 min
    if action in ("create", "schedule") and (text or "").strip():
        res["intent"] = intent_lock(acct_key, poster, text, in_reply_to=in_reply_to, now=now)
    return res


def _postiz_type_to_platform(t):
    t = (t or "").lower()
    for k in ("tiktok", "instagram", "youtube", "threads", "bluesky", "mastodon", "linkedin", "pinterest", "tumblr"):
        if k in t:
            return k
    return "x" if t in ("x", "twitter") else ""


def check_postiz_payload(payload, poster, action, source_url, now=None, lang=None, kind=None):
    """Gate every integration in a Postiz /posts payload. Unknown integration -> refused."""
    if isinstance(payload, (bytes, str)):
        payload = json.loads(payload)
    posts = payload.get("posts") or []
    if not posts:
        raise Refused("Postiz payload has no posts[]; cannot verify the account")
    cache, results = {}, []
    for p in posts:
        iid = ((p.get("integration") or {}).get("id")) or ""
        if not iid:
            raise Refused("Postiz post without integration id")
        if "owners" not in cache:
            cache["owners"] = load_owners(); cache["dest"] = load_destinations()
            cache["claims"] = parse_claims(read_repo_file("team/CLAIMS.md"))
        imap = integration_map(cache["owners"][1], *cache["dest"])
        if iid not in imap:
            raise Refused(f"integration {iid} (settings.__type={(p.get('settings') or {}).get('__type')}) is not mapped; "
                          "add it to the post-gate-owners block in team/ACCOUNT-OWNERS.md")
        plat, acct = imap[iid]
        stype = _postiz_type_to_platform((p.get("settings") or {}).get("__type"))
        if stype and stype != plat:
            raise Refused(f"integration {iid} mapped to {plat} but payload says {stype}")
        vals = p.get("value") or [{}]
        text = (vals[0] or {}).get("content", "") if vals else ""
        results.append(check(poster, plat, acct, action, source_url, integration_id=iid, now=now, _cache=cache,
                             text=text, recent_json=os.environ.get("POST_GATE_X_RECENT", ""),
                             lang=lang, kind=kind))
    return results


def guard_postiz(method, url, body=None, poster=None, source_url=None):
    """Call right before any Postiz HTTP call. No-op for reads and uploads; gates create/schedule/delete."""
    method = (method or ("POST" if body is not None else "GET")).upper()
    path = re.sub(r"^https?://[^/]+", "", url or "").split("?")[0]
    if method == "GET" or "/upload" in path or "/posts" not in path:
        return None
    poster = poster or os.environ.get("ANICCA_POSTER", "")
    source_url = source_url or os.environ.get("ANICCA_SOURCE_URL", "")
    try:
        if method == "DELETE" or (method in ("PUT", "PATCH") and re.search(r"/posts/[^/]+", path)):
            acct = os.environ.get("POST_GATE_ACCOUNT", "")
            if ":" not in acct:
                raise Refused("delete/cancel needs POST_GATE_ACCOUNT=platform:@handle of the post being removed")
            plat, _, handle = acct.partition(":")
            res = [check(poster, plat, handle, "delete" if method == "DELETE" else "update", source_url)]
        else:
            if isinstance(body, (bytes, bytearray)):
                body = body.decode("utf-8")
            payload = json.loads(body) if isinstance(body, str) else (body or {})
            action = "schedule" if payload.get("type") == "schedule" else "create"
            res = check_postiz_payload(payload, poster, action, source_url)
    except Refused as e:
        sys.stderr.write(f"POST-GATE REFUSED: {e}\n")
        raise SystemExit(2)
    sys.stderr.write("POST-GATE OK: " + json.dumps(res, ensure_ascii=False) + "\n")
    return res



# X-ADVICE-LOG A-denominator (@10JAQK https://x.com/10JAQK/status/2121714613683392687):
# "I now write the denominator next to every percentage before I let myself believe it."
# Advisory only (never refuses): printed after POST-GATE OK so the writer adds "14 of 334" next to "4%".
_PCT = re.compile(r"\d+(?:\.\d+)?\s*[%％]")
_DENOM = re.compile(r"\d[\d,]*\s*(?:/|of|out of|中|分の)\s*\d|\d[\d,]*\D{0,8}?(?:→|->)\s*\d", re.I)
_CONNECT_REQ = re.compile(r"つながりたい|love to connect", re.I)
EN_CONNECT_ADVICE = "lead with the request (I'd love to connect with ...), numbers on line 2"
_EN_DAY_OPENER = re.compile(r"day\s+\d", re.I)


def check_en_connect_opener(text):
    """EN connect posts: the first non-empty line must be the request, not a number/"$"/"Day <n>" lead."""
    first = _first_nonempty_line(text).strip()
    if first[:1].isdigit() or first.startswith("$") or _EN_DAY_OPENER.match(first):
        raise Refused(f"en-connect: first line must be the connect request, not a number/day lead: {EN_CONNECT_ADVICE}")
    return None


def _first_nonempty_line(text):
    for line in (text or "").splitlines():
        if line.strip():
            return line
    return ""


def advice_warnings(text):
    warns = []
    if text and _PCT.search(text) and not _DENOM.search(text):
        warns.append("percentage without its denominator: add the raw counts (e.g. '14 of 334') next to the % "
                     "(advice @10JAQK, marketing/X-ADVICE-LOG.md A-denominator)")
    if _CONNECT_REQ.search(text or "") and not _CONNECT_REQ.search(_first_nonempty_line(text)):
        warns.append("connect request must be line 1 (X-STYLE 11/22)")
    return warns

def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    a.add_argument("--poster", default=os.environ.get("ANICCA_POSTER", ""))
    a.add_argument("--platform"); a.add_argument("--account"); a.add_argument("--integration-id")
    a.add_argument("--action", required=True, choices=sorted(MUTATING))
    a.add_argument("--source-url", "--winner-url", dest="source_url", default=os.environ.get("ANICCA_SOURCE_URL", ""))
    a.add_argument("--postiz-payload", help="path to a Postiz /posts JSON body")
    a.add_argument("--now", help="override clock, 'YYYY-MM-DD HH:MM' JST (tests)")
    a.add_argument("--text-file", help="X: file with the exact post text")
    a.add_argument("--recent-json", default=os.environ.get("POST_GATE_X_RECENT", ""),
                   help="X: fresh raw output of x get_users_posts for the account (<=10 min old)")
    a.add_argument("--in-reply-to", default="", help="X: parent post id when posting a reply")
    a.add_argument("--lang", default=os.environ.get("POST_GATE_LANG", ""), help="post language (en/ja)")
    a.add_argument("--kind", default=os.environ.get("POST_GATE_KIND", ""), help="post kind (e.g. connect)")
    a.add_argument("--record-intent", action="store_true",
                   help="X: on OK, record this attempt in team/state/x-post-intents.jsonl (do this right before clicking Post)")
    o = a.parse_args(argv)
    now = dt.datetime.strptime(o.now, "%Y-%m-%d %H:%M").replace(tzinfo=JST) if o.now else None
    try:
        if o.postiz_payload:
            res = check_postiz_payload(json.load(open(o.postiz_payload)), o.poster, o.action, o.source_url, now=now,
                                       lang=o.lang, kind=o.kind)
        else:
            text = open(o.text_file, encoding="utf-8").read() if o.text_file else None
            res = check(o.poster, o.platform or "", o.account or "", o.action, o.source_url,
                        integration_id=o.integration_id, now=now, text=text, recent_json=o.recent_json,
                        in_reply_to=o.in_reply_to, lang=o.lang, kind=o.kind)
            if o.record_intent and norm_platform(o.platform or "") == "x" and "intent" not in res:
                res["intent"] = record_intent(res["account"], res["poster"], text or "", o.in_reply_to, now=now)["at"]
    except Refused as e:
        print(f"POST-GATE REFUSED: {e}")
        return 2
    print("POST-GATE OK: " + json.dumps(res, ensure_ascii=False))
    if not o.postiz_payload and o.text_file:
        for w in advice_warnings(open(o.text_file, encoding="utf-8").read()):
            print("POST-GATE ADVICE-WARN: " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
