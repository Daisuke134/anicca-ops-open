#!/usr/bin/env python3
"""Summarize App Store taps, X impressions, and ASC Anicca installs by channel."""

import csv
import json
import os
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "metrics", "attribution", "e2e-2026-11-22.csv")
X_PATH = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "metrics", "x", "diceai0-originals-14d-2026-11-22.json")
MD_PATH = os.path.join(HERE, "..", "metrics", "installs-by-channel-latest.md")
CUTOFF = "2026-11-08"

CHANNELS = [
    "X",
    "Instagram",
    "TikTok",
    "YouTube",
    "Bluesky",
    "Mastodon",
    "LinkedIn",
    "Other",
]

INSTALLS_UNKNOWN = "unknown: install events carry no ct"


def channel_for(ct):
    ct = ct.lower()
    if ct.startswith("x"):
        return "X"
    if ct.startswith("instagram") or ct.startswith("ig_"):
        return "Instagram"
    if ct.startswith("tt") or ct.startswith("tiktok"):
        return "TikTok"
    if ct.startswith("youtube") or ct.startswith("yt_"):
        return "YouTube"
    if ct.startswith("bluesky"):
        return "Bluesky"
    if ct.startswith("mastodon"):
        return "Mastodon"
    if ct.startswith("linkedin"):
        return "LinkedIn"
    return "Other"


def to_int(value):
    return int(float(value))


def main():
    # (date, ct) -> last value seen, from taps rows for the 14-day window.
    taps_by_date_ct = OrderedDict()
    asc_installs = defaultdict(int)

    with open(CSV_PATH, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["date"] < CUTOFF:
                continue

            if row["layer"] == "taps" and row["key"].startswith("app_store_click/"):
                ct = row["key"].split("/", 1)[1]
                taps_by_date_ct[(row["date"], ct)] = to_int(row["value"])

            elif (
                row["layer"] == "installs"
                and row["source"] == "ASC"
                and row["product"] == "Anicca"
            ):
                asc_installs[row["metric"]] += to_int(row["value"])

    taps_by_channel = defaultdict(int)
    for (_, ct), value in taps_by_date_ct.items():
        taps_by_channel[channel_for(ct)] += value

    with open(X_PATH, encoding="utf-8") as handle:
        posts = json.load(handle)

    total_impressions = 0
    link_posts = 0
    link_post_impressions = 0
    for post in posts:
        impressions = to_int(post.get("public_metrics", {}).get("impression_count", 0))
        total_impressions += impressions

        is_link_post = False
        for url in post.get("entities", {}).get("urls", []):
            target = url.get("unwound_url") or url.get("expanded_url") or ""
            if "ct=" in target:
                is_link_post = True
                break

        if is_link_post:
            link_posts += 1
            link_post_impressions += impressions

    x_taps = taps_by_channel.get("X", 0)
    if link_post_impressions:
        x_taps_per_1000 = x_taps / link_post_impressions * 1000
    else:
        x_taps_per_1000 = 0.0

    lines = [
        "| channel | human App Store taps (14d) | installs attributed |",
        "| --- | ---: | --- |",
    ]
    for channel in CHANNELS:
        lines.append(
            "| {} | {} | {} |".format(
                channel, taps_by_channel.get(channel, 0), INSTALLS_UNKNOWN
            )
        )

    table = "\n".join(lines)
    installs_summary = ", ".join(
        "{}={}".format(metric, asc_installs[metric])
        for metric in sorted(asc_installs)
    )

    report_lines = [
        table,
        "",
        "X impressions total: {}".format(total_impressions),
        "X link posts: {}".format(link_posts),
        "X taps per 1000 impressions on link-carrying posts: {:.3f}".format(x_taps_per_1000),
        "X taps per 1000 impressions on all posts: {:.3f}".format(x_taps / total_impressions * 1000 if total_impressions else 0.0),
        "ASC Anicca installs by metric: {}".format(installs_summary),
    ]

    output = "\n".join(report_lines)
    print(output)

    with open(MD_PATH, "w", encoding="utf-8") as handle:
        handle.write(table + "\n")


if __name__ == "__main__":
    main()
