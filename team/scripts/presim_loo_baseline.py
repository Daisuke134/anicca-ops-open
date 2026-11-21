"""Leave-one-out impression baselines for presim connect posts."""

from statistics import median


def loo_baselines(posts):
    """Return {post_id: baseline} where baseline is the median of the
    impressions of all other posts in `posts`.

    Each post is a mapping with an "id" (or "post_id") key and an
    "impressions" key.
    """
    values = []
    for post in posts:
        pid = post.get("id", post.get("post_id"))
        values.append((pid, post["impressions"]))

    result = {}
    for pid, _ in values:
        others = [imp for other_pid, imp in values if other_pid != pid]
        result[pid] = median(others)
    return result
