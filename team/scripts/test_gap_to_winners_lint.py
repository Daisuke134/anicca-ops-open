import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import gap_to_winners_lint as lint

GOOD_TABLE = """# Title

Some prose before the table.

| surface | winner (source URL) | practice | ours | gap | change (owner, NOW) | re-measure |
|---|---|---|---|---|---|---|
| App Store / ASO | I am: https://example.com/winner | daily reminders | fixed slots | gap | @gemini copy keywords | re-measure |
| X | levelsio: https://example.com/levelsio | public MRR | followers | gap | @opencode reply | re-measure |
"""

MISSING_URL = """| surface | winner | practice | ours | gap | change | re-measure |
|---|---|---|---|---|---|---|
| App Store / ASO | I am: no link here | daily reminders | fixed slots | gap | @gemini copy keywords | re-measure |
"""

MISSING_OWNER = """| surface | winner | practice | ours | gap | change | re-measure |
|---|---|---|---|---|---|---|
| App Store / ASO | https://example.com/winner | daily reminders | fixed slots | gap | copy keywords, nobody owns this | re-measure |
"""

WRONG_COUNT = """| surface | winner | practice | ours | gap | change | re-measure |
|---|---|---|---|---|---|---|
| App Store / ASO | https://example.com/winner | daily reminders | fixed slots | gap | @gemini copy keywords |
| X | https://example.com/levelsio | public MRR | followers | gap | @opencode reply | re-measure | extra cell |
"""


def write_table(tmp_path, text):
    p = tmp_path / "GAP-TO-WINNERS.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_good_table_passes(tmp_path):
    p = write_table(tmp_path, GOOD_TABLE)
    assert lint.lint_file(p) == []
    assert lint.main([str(p)]) == 0


def test_missing_url_fails(tmp_path):
    p = write_table(tmp_path, MISSING_URL)
    problems = lint.lint_file(p)
    assert len(problems) == 1
    assert "column 2" in problems[0]
    assert lint.main([str(p)]) == 1


def test_missing_owner_fails(tmp_path):
    p = write_table(tmp_path, MISSING_OWNER)
    problems = lint.lint_file(p)
    assert len(problems) == 1
    assert "column 6" in problems[0]
    assert lint.main([str(p)]) == 1


def test_wrong_cell_count_fails(tmp_path):
    p = write_table(tmp_path, WRONG_COUNT)
    problems = lint.lint_file(p)
    assert len(problems) == 2
    assert all("cells" in p for p in problems)
    assert lint.main([str(p)]) == 1


def test_cli_exit_codes(tmp_path, capsys):
    good = write_table(tmp_path / "good", GOOD_TABLE)
    bad = write_table(tmp_path / "bad", MISSING_URL)
    assert lint.main([str(good)]) == 0
    assert lint.main([str(bad)]) == 1
    out = capsys.readouterr().out
    assert "column 2" in out


UPDATE_GOOD = """# Title

| surface | winner (source URL) | practice | ours | gap | change (owner, NOW) | re-measure |
|---|---|---|---|---|---|---|
| App Store / ASO | I am: https://example.com/winner | daily reminders | fixed slots | gap | @gemini copy keywords | re-measure |

## Update log

| item | note | detail | status | change | re-measure |
|---|---|---|---|---|---|
| widget-alpha | shipped fix | qa passed | done | @gemini ship it | re-check next week |
| gadget-beta | shipped fix | qa passed | done | none | re-check next week |

## Other notes

| item | note | detail | status | change | re-measure |
|---|---|---|---|---|---|
| ignored-row | not an update table | x | y | z | w |
"""

UPDATE_BAD_COUNT = """## Update log

| item | note | detail | status | change | re-measure |
|---|---|---|---|---|---|
| widget-alpha | shipped fix | qa passed | done | @gemini ship it |
| gadget-beta | shipped fix | qa passed | done | none | re-check | extra |
"""

UPDATE_BAD_OWNER = """## Update log

| item | note | detail | status | change | re-measure |
|---|---|---|---|---|---|
| widget-alpha | shipped fix | qa passed | done | nobody owns this | re-check next week |
"""


def test_update_table_good_passes(tmp_path):
    p = write_table(tmp_path, UPDATE_GOOD)
    assert lint.lint_file(p) == []
    assert lint.main([str(p)]) == 0


def test_update_table_wrong_cell_count_fails(tmp_path):
    p = write_table(tmp_path, UPDATE_BAD_COUNT)
    problems = lint.lint_file(p)
    assert len(problems) == 2
    assert all("cells" in p for p in problems)
    assert lint.main([str(p)]) == 1


def test_update_table_missing_owner_or_none_fails(tmp_path):
    p = write_table(tmp_path, UPDATE_BAD_OWNER)
    problems = lint.lint_file(p)
    assert len(problems) == 1
    assert "column 5" in problems[0]
    assert lint.main([str(p)]) == 1


def test_update_heading_prefix_variants(tmp_path):
    text = """## Updates for November

| item | note | detail | status | change | re-measure |
|---|---|---|---|---|---|
| widget-alpha | shipped fix | qa passed | done | None | re-check next week |
"""
    p = write_table(tmp_path, text)
    assert lint.lint_file(p) == []


def test_update_section_ends_at_next_heading(tmp_path):
    text = """## Update log

| item | note | detail | status | change | re-measure |
|---|---|---|---|---|---|
| widget-alpha | shipped fix | qa passed | done | @gemini ship it | re-check next week |

## Later section

| surface | winner | practice | ours | gap | change | re-measure |
|---|---|---|---|---|---|---|
| App Store / ASO | https://example.com/winner | daily reminders | fixed slots | gap | @gemini copy keywords | re-measure |
"""
    p = write_table(tmp_path, text)
    assert lint.lint_file(p) == []
