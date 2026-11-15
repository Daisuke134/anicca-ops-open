#!/usr/bin/env python3
"""xqueue_simrank.py — parse an X queue markdown file into posts and rank them.

A post starts at a `### <title>` line. Its text is the lines after a line that
is exactly `Text:`, up to (not including) the first line starting with Video,
Image, First reply, Source, Visual, Reply or Media, or the next `###`/`## `
heading. Posts whose text is shorter than 20 chars are skipped.

Usage
  python3 team/scripts/xqueue_simrank.py FILE [--start N]
"""
import argparse, json, os, subprocess, sys

STOP_PREFIXES = ('Video', 'Image', 'First reply', 'Source', 'Visual', 'Reply', 'Media')
MIN_TEXT_LEN = 20
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRESIM = os.path.join('team', 'scripts', 'x_presim.py')


def parse_posts(md, start_line=1):
    """Return [{line, title, text}] for each `### <title>` post at/after start_line.

    line is the 1-based line number of the `###` heading. text is the joined
    body after the `Text:` line, stripped; posts with text < 20 chars skipped.
    """
    posts = []
    lines = md.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        if not raw.startswith('### ') or i + 1 < start_line:
            i += 1
            continue
        lineno = i + 1
        title = raw[4:].strip()
        i += 1
        text_lines = []
        in_text = False
        while i < n:
            line = lines[i]
            stripped = line.strip()
            if stripped == 'Text:':
                in_text = True
            elif in_text and (stripped.startswith(STOP_PREFIXES)
                              or line.startswith('###') or line.startswith('## ')):
                break
            elif not in_text and (line.startswith('###') or line.startswith('## ')):
                break
            if in_text:
                text_lines.append(line)
            i += 1
        text = '\n'.join(text_lines).strip()
        if len(text) >= MIN_TEXT_LEN:
            posts.append(dict(line=lineno, title=title, text=text))
    return posts


def rank(posts, scorer):
    """Return posts sorted by scorer(text) descending (scorer injectable)."""
    return sorted(posts, key=lambda p: scorer(p['text']), reverse=True)


def presim_scorer(text):
    """Default scorer: pred_impr from x_presim.py score --dry (first JSON line)."""
    try:
        r = subprocess.run(
            ['python3', PRESIM, 'score', '--account', 'diceai0',
             '--text', text, '--dry'],
            capture_output=True, text=True, cwd=ROOT, timeout=600)
    except Exception:
        return 0.0
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            return float(json.loads(line).get('pred_impr', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
    return 0.0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Rank X queue posts by predicted impressions.')
    ap.add_argument('file')
    ap.add_argument('--start', type=int, default=1, help='1-based line to start scanning at')
    args = ap.parse_args(argv)
    with open(args.file, encoding='utf-8') as fh:
        md = fh.read()
    posts = parse_posts(md, start_line=args.start)
    scored = [(presim_scorer(p['text']), p) for p in posts]
    scored.sort(key=lambda t: t[0], reverse=True)
    for score, p in scored:
        print(f"{score:g} L{p['line']} {p['title']}")


if __name__ == '__main__':
    main()
