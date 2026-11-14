"""Build a public-safe aggregate of recent Postiz per-post observations."""

METRICS = ("views", "likes", "replies", "reposts")
SCOPE = (
    "Sample of published posts from the Postiz query window, capped at the 5 most recent "
    "posts per connected account and excluding posts newer than 24 hours. Sample sums are "
    "not account-wide totals."
)


def _range(values):
    values = [str(value) for value in values if value]
    return {"from": min(values), "to": max(values)} if values else {"from": None, "to": None}


def _metric(posts, key):
    values = [p.get(key) for p in posts if isinstance(p.get(key), (int, float)) and not isinstance(p.get(key), bool)]
    periods = [((p.get("metric_periods") or {}).get(key)) for p in posts]
    return {
        "sample_sum": sum(values) if values else None,
        "posts_with_value": len(values),
        "posts_missing_value": len(posts) - len(values),
        "period_from": min((str(v) for v in periods if v), default=None),
        "period_to": max((str(v) for v in periods if v), default=None),
    }


def _daily(posts):
    dates = set()
    for post in posts:
        for points in (post.get("metric_series") or {}).values():
            if isinstance(points, list):
                dates.update(str(point["date"]) for point in points if isinstance(point, dict) and point.get("date"))
    dates = sorted(dates)
    out = []
    for date in dates:
        eligible = [post for post in posts if str(post.get("t") or "")[:10] and str(post.get("t") or "")[:10] <= date]
        if not eligible:
            continue
        metrics = {}
        for key in METRICS:
            values = []
            for post in eligible:
                points = [point for point in ((post.get("metric_series") or {}).get(key) or []) if point.get("date") == date]
                if points and isinstance(points[-1].get("value"), (int, float)) and not isinstance(points[-1].get("value"), bool):
                    values.append(points[-1]["value"])
            metrics[key] = {
                "sample_sum": sum(values) if values else None,
                "posts_with_value": len(values),
                "posts_missing_value": len(eligible) - len(values),
            }
        out.append({"date": date, "eligible_posts": len(eligible), "metrics": metrics})
    return out


def summarize_post_metrics(feed):
    feed = feed if isinstance(feed, dict) else {}
    posts = feed.get("posts") if isinstance(feed.get("posts"), dict) else {}
    groups = {}
    accounts = set()
    fetched_at = []
    for post in posts.values():
        if not isinstance(post, dict):
            continue
        platform = str(post.get("platform") or "Unknown")
        groups.setdefault(platform, []).append(post)
        if post.get("account"):
            accounts.add(str(post["account"]))
        fetched_at.append(post.get("fetched_at"))

    platforms = []
    any_missing = False
    for platform in sorted(groups):
        selected = groups[platform]
        metrics = {key: _metric(selected, key) for key in METRICS}
        any_missing |= any(value["posts_missing_value"] for value in metrics.values())
        platforms.append({
            "platform": platform,
            "sampled_posts": len(selected),
            "published_at": _range(post.get("t") for post in selected),
            "observed_at": _range(post.get("fetched_at") for post in selected),
            "metrics": metrics,
            "daily": _daily(selected),
        })

    return {
        "source": "Postiz /analytics/post",
        "status": ("observed" if not any_missing else "partial") if posts else ("observed_empty" if feed.get("built_at") else "unavailable"),
        "observed_at": feed.get("built_at"),
        "query_window": {"from": feed.get("window_start"), "to": feed.get("window_end")},
        "scope": SCOPE,
        "coverage": {"sampled_posts": len(posts), "sampled_accounts": len(accounts)},
        "observed_at_range": _range(fetched_at),
        "platforms": platforms,
    }
