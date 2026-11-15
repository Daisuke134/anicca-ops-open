"""List presim log rows that failed to link a post_id.

Reads team/metrics/presim-log.csv (columns include ts_jst, post_id,
text_sha) and reports rows whose post_id is empty or not all digits and
whose ts_jst is older than min_age_h before ``now``.

CLI:
    presim_unlinked.py [CSV] [--now 'YYYY-MM-DD HH:MM']

Prints ``UNLINKED <n>`` then one ``text_sha ts_jst`` per row.
Exits 1 if n > 0, else 0.
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timedelta

DEFAULT_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "metrics",
    "presim-log.csv",
)

TS_FORMAT = "%Y-%m-%d %H:%M"


def _parse_ts(value):
    return datetime.strptime(value.strip(), TS_FORMAT)


def unlinked(rows, now, min_age_h=1):
    """Return rows with a missing/non-digit post_id older than min_age_h.

    ``rows`` is an iterable of dicts with keys ``post_id``, ``text_sha``
    and ``ts_jst``. ``now`` is a datetime. A row is unlinked when its
    post_id is empty or not all digits, and its ts_jst is more than
    min_age_h hours before ``now``.
    """
    cutoff = now - timedelta(hours=min_age_h)
    result = []
    for row in rows:
        post_id = (row.get("post_id") or "").strip()
        if post_id and post_id.isdigit():
            continue
        ts = _parse_ts(row.get("ts_jst", ""))
        if ts < cutoff:
            result.append(row)
    return result


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv", nargs="?", default=DEFAULT_CSV,
                        help="path to presim-log.csv")
    parser.add_argument("--now", default=None,
                        help="current time as 'YYYY-MM-DD HH:MM' "
                             "(default: now)")
    parser.add_argument("--min-age-h", type=float, default=1,
                        dest="min_age_h",
                        help="minimum age in hours (default: 1)")
    args = parser.parse_args(argv)

    now = (_parse_ts(args.now) if args.now
           else datetime.now().replace(second=0, microsecond=0))

    if not os.path.exists(args.csv):  # fail closed: missing evidence is BLOCKED, not 0 (chatgpt review 21:31)
        print("BLOCKED missing %s" % args.csv)
        return 2
    rows = load_rows(args.csv)
    bad = unlinked(rows, now, min_age_h=args.min_age_h)

    print("UNLINKED %d" % len(bad))
    for row in bad:
        print("%s %s" % (row.get("text_sha", ""), row.get("ts_jst", "")))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
