"""Tests for xqueue_simrank.py — inline markdown + fake scorer, no subprocess."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import xqueue_simrank as xs

MD = """# X Queue — 2026-11-15

### First post title
Text:
This is the first post body and it is definitely longer than twenty characters.
Second line of the first post body for good measure.
Video: https://example.com/v1

### Tiny post
Text:
short

### Second post title
Text:
The second post body is also quite long, well over twenty characters here.
First reply: someone said hi
Source: https://example.com/src

## Other section

### Third post title
Text:
Third post body text, again comfortably longer than twenty characters total.
Media: attached image
"""


def test_parse_posts_extracts_bodies():
    posts = xs.parse_posts(MD)
    assert [p['title'] for p in posts] == ['First post title', 'Second post title', 'Third post title']
    first = posts[0]
    assert first['line'] == 3
    assert 'Second line of the first post body' in first['text']
    assert 'Video:' not in first['text']


def test_parse_posts_line_numbers():
    posts = xs.parse_posts(MD)
    assert posts[0]['line'] == 3
    assert posts[1]['line'] == 13
    assert posts[2]['line'] == 21


def test_parse_posts_stops_at_prefixes_and_headings():
    posts = xs.parse_posts(MD)
    assert 'First reply' not in posts[1]['text']
    assert 'Source:' not in posts[1]['text']
    assert 'Other section' not in posts[2]['text']
    assert 'Media:' not in posts[2]['text']


def test_parse_posts_skips_short_text():
    posts = xs.parse_posts(MD)
    assert all(p['title'] != 'Tiny post' for p in posts)


def test_parse_posts_start_line():
    posts = xs.parse_posts(MD, start_line=13)
    assert [p['title'] for p in posts] == ['Second post title', 'Third post title']
    posts = xs.parse_posts(MD, start_line=20)
    assert [p['title'] for p in posts] == ['Third post title']


def test_parse_posts_empty():
    assert xs.parse_posts('') == []
    assert xs.parse_posts('### No text post\n') == []
    assert xs.parse_posts('# only h1\n\n## h2\n') == []


def test_rank_sorts_by_scorer_desc():
    posts = [
        dict(line=1, title='a', text='aaaa'),
        dict(line=2, title='b', text='bbbbbb'),
        dict(line=3, title='c', text='cc'),
    ]
    scores = {'aaaa': 1, 'bbbbbb': 9, 'cc': 5}
    ranked = xs.rank(posts, lambda t: scores[t])
    assert [p['title'] for p in ranked] == ['b', 'c', 'a']


def test_rank_scorer_receives_text():
    seen = []
    posts = [dict(line=1, title='x', text='hello world this is long')]
    xs.rank(posts, lambda t: seen.append(t) or 0)
    assert seen == ['hello world this is long']


def test_main_cli_with_fake_scorer(tmp_path, monkeypatch, capsys):
    f = tmp_path / 'queue.md'
    f.write_text(MD, encoding='utf-8')
    monkeypatch.setattr(xs, 'presim_scorer', lambda t: len(t))
    xs.main([str(f)])
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 3
    for line in out:
        parts = line.split(' ', 2)
        float(parts[0])
        assert parts[1].startswith('L')
        int(parts[1][1:])
    # longest text first
    assert 'First post title' in out[0]


def test_main_cli_start_flag(tmp_path, monkeypatch, capsys):
    f = tmp_path / 'queue.md'
    f.write_text(MD, encoding='utf-8')
    monkeypatch.setattr(xs, 'presim_scorer', lambda t: 1)
    xs.main([str(f), '--start', '13'])
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 2
    assert all('First post title' not in l for l in out)


def test_presim_scorer_parses_first_json_line(monkeypatch):
    class R:
        stdout = 'noise line\n{"pred_impr": 123, "other": 1}\n{"pred_impr": 999}\n'
    monkeypatch.setattr(xs.subprocess, 'run', lambda *a, **k: R())
    assert xs.presim_scorer('some text') == 123.0


def test_presim_scorer_no_json_returns_zero(monkeypatch):
    class R:
        stdout = 'no json here\n'
    monkeypatch.setattr(xs.subprocess, 'run', lambda *a, **k: R())
    assert xs.presim_scorer('some text') == 0.0
