import csv
import math
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import x_presim


EN_TEXT = "Shipped a new paywall flow in 3 days. Revenue is up 12% this week."
JA_TEXT = "新しいエージェントを公開しました。売上が12%上がっています。"


def test_feats_language_detection():
    assert x_presim.feats(JA_TEXT)['lang'] == 'ja'
    assert x_presim.feats(EN_TEXT)['lang'] == 'en'
    # mixed: any CJK character triggers ja
    assert x_presim.feats("Hello 世界")['lang'] == 'ja'


def test_feats_flags():
    f = x_presim.feats("Check https://example.com for details. Hi @alice!")
    assert f['link'] is True
    assert f['mention'] is True
    assert f['nums'] == 0
    assert f['question'] is False

    f2 = x_presim.feats("We made 2,500 downloads in 7 days. Why?")
    assert f2['link'] is False
    assert f2['mention'] is False
    assert f2['nums'] >= 2
    assert f2['question'] is True
    # hook_num: first line contains a digit
    assert f2['hook_num'] is True


def test_feats_hook_short():
    short = "one line hook\nsecond line"
    assert x_presim.feats(short)['hook_short'] is True
    long = "x" * 100 + "\nsecond"
    assert x_presim.feats(long)['hook_short'] is False


def test_heuristic_panel_one_row_per_persona():
    panel = x_presim.heuristic_panel(EN_TEXT)
    assert len(panel) == len(x_presim.PERSONAS)
    assert {r['persona'] for r in panel} == {p['name'] for p in x_presim.PERSONAS}
    for r in panel:
        assert 0 <= r['stop'] <= 1
        assert 0 <= r['like'] <= 1
        assert 0 <= r['reply'] <= 1
        assert 0 <= r['follow'] <= 1
        assert r['why']


def test_aggregate_higher_stop_gives_higher_impr():
    base = 1000.0
    low = [dict(persona=p['name'], stop=0.01, like=0.0, reply=0.0, follow=0.0)
           for p in x_presim.PERSONAS]
    high = [dict(r, stop=0.5) for r in low]
    a_low = x_presim.aggregate(low, base, lang='*')
    a_high = x_presim.aggregate(high, base, lang='*')
    assert a_high['pred_impr'] > a_low['pred_impr']


def test_aggregate_impr_clamped():
    base = 1000.0
    # absurdly high stop -> still clamped to 4x
    tiny = [dict(persona=p['name'], stop=0.001, like=0.0, reply=0.0, follow=0.0)
            for p in x_presim.PERSONAS]
    huge = [dict(r, stop=1.0) for r in tiny]
    lo = x_presim.aggregate(tiny, base, lang='*')
    hi = x_presim.aggregate(huge, base, lang='*')
    assert lo['pred_impr'] >= 0.25 * base
    assert hi['pred_impr'] <= 4.0 * base
    assert lo['pred_impr'] == pytest.approx(0.25 * base, abs=1)
    assert hi['pred_impr'] == pytest.approx(4.0 * base, abs=1)


def test_aggregate_top_weak_fields():
    panel = x_presim.heuristic_panel(EN_TEXT)
    a = x_presim.aggregate(panel, 1000.0, lang='en')
    assert a['top_persona'] in {p['name'] for p in x_presim.PERSONAS}
    assert a['weak_persona'] in {p['name'] for p in x_presim.PERSONAS}
    assert a['top_persona'] != a['weak_persona'] or len(panel) == 1
    assert a['stop_rate'] > 0
    for k in ('pred_likes', 'pred_replies', 'pred_follows'):
        assert k in a and a[k] >= 0


def _write_metrics(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['account', 'format', 'impressions', 'age_h'])
        w.writeheader()
        for r in rows:
            w.writerow(r)


def test_baseline_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(x_presim, 'METRICS', str(tmp_path / 'nope.csv'))
    assert x_presim.baseline('anyaccount') == 50.0


def test_baseline_median_qualifying_rows(tmp_path, monkeypatch):
    csv_path = tmp_path / 'metrics.csv'
    _write_metrics(csv_path, [
        dict(account='acc1', format='post', impressions='100', age_h='30'),
        dict(account='acc1', format='post', impressions='200', age_h='48'),
        dict(account='acc1', format='post', impressions='300', age_h='72'),
        dict(account='acc1', format='post', impressions='400', age_h='96'),
        # excluded: young
        dict(account='acc1', format='post', impressions='99999', age_h='1'),
        # excluded: bad formats
        dict(account='acc1', format='reply', impressions='99999', age_h='48'),
        dict(account='acc1', format='profile', impressions='99999', age_h='48'),
        dict(account='acc1', format='retweet', impressions='99999', age_h='48'),
        dict(account='acc1', format='self_reply_link', impressions='99999', age_h='48'),
        # excluded: other account
        dict(account='acc2', format='post', impressions='88888', age_h='48'),
    ])
    monkeypatch.setattr(x_presim, 'METRICS', str(csv_path))
    # median of [100,200,300,400] = 250.0
    assert x_presim.baseline('acc1') == 250.0


def test_baseline_no_qualifying_rows(tmp_path, monkeypatch):
    csv_path = tmp_path / 'metrics.csv'
    _write_metrics(csv_path, [
        dict(account='acc1', format='reply', impressions='500', age_h='48'),
    ])
    monkeypatch.setattr(x_presim, 'METRICS', str(csv_path))
    assert x_presim.baseline('acc1') == 50.0


def _write_presim_log(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=x_presim.FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in x_presim.FIELDS})


def _log_row(**kw):
    base = dict(ts_jst='2026-01-01 00:00', surface='x', account='acc', post_id='', text_sha='',
                backend='heuristic', baseline_impr='100', stop_rate='0.1',
                pred_impr='100', pred_likes='1', pred_replies='0.1', pred_follows='0.1',
                top_persona='p', weak_persona='q', fix_hint='',
                actual_impr='100', actual_likes='1', actual_replies='', actual_follows='',
                abs_log_err_impr='0.5', abs_log_err_likes='0.3',
                text_preview=EN_TEXT)
    base.update(kw)
    return base


@pytest.fixture
def presim_log(tmp_path, monkeypatch):
    csv_path = tmp_path / 'presim-log.csv'
    _write_presim_log(csv_path, [
        _log_row(surface='x', backend='heuristic', abs_log_err_impr='0.2', abs_log_err_likes='0.1',
                 text_preview=EN_TEXT),
        _log_row(surface='y', backend='heuristic', abs_log_err_impr='0.6', abs_log_err_likes='0.5',
                 text_preview=JA_TEXT),
        _log_row(surface='x', backend='codex', abs_log_err_impr='1.0', abs_log_err_likes='0.9',
                 text_preview=JA_TEXT),
    ])
    monkeypatch.setattr(x_presim, 'LOG', str(csv_path))
    return csv_path


def test_report_default_groups_by_backend(presim_log, capsys):
    x_presim.report()
    out = capsys.readouterr().out
    lines = out.strip().split('\n')
    assert len(lines) == 2
    assert lines[0].startswith('codex: n=1 ')
    assert 'impr=1.00' in lines[0] and 'likes=0.90' in lines[0]
    assert lines[1].startswith('heuristic: n=2 ')
    assert 'impr=0.40' in lines[1] and 'likes=0.30' in lines[1]


def test_report_by_surface(presim_log, capsys):
    x_presim.report(by='surface')
    out = capsys.readouterr().out
    lines = out.strip().split('\n')
    assert len(lines) == 2
    assert lines[0].startswith('x: n=2 ')
    assert 'impr=0.60' in lines[0] and 'likes=0.50' in lines[0]
    assert lines[1].startswith('y: n=1 ')
    assert 'impr=0.60' in lines[1] and 'likes=0.50' in lines[1]


def test_report_by_lang(presim_log, capsys):
    x_presim.report(by='lang')
    out = capsys.readouterr().out
    lines = out.strip().split('\n')
    assert len(lines) == 2
    assert lines[0].startswith('en: n=1 ')
    assert 'impr=0.20' in lines[0] and 'likes=0.10' in lines[0]
    assert lines[1].startswith('ja: n=2 ')
    assert 'impr=0.80' in lines[1] and 'likes=0.70' in lines[1]


CONNECT_TEXT = "I want to meet more people shipping indie apps. つながりたい"


def test_connect_baseline_too_few_rows(tmp_path):
    csv_path = tmp_path / 'presim-log.csv'
    _write_presim_log(csv_path, [
        _log_row(actual_impr='400', text_preview=CONNECT_TEXT),
        # zero/negative actuals don't count
        _log_row(actual_impr='0', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='-5', text_preview=CONNECT_TEXT),
        # non-connect rows don't count
        _log_row(actual_impr='9999', text_preview=EN_TEXT),
    ])
    assert x_presim.connect_baseline(str(csv_path)) is None


def test_connect_baseline_median(tmp_path):
    csv_path = tmp_path / 'presim-log.csv'
    _write_presim_log(csv_path, [
        _log_row(actual_impr='400', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='600', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='800', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='9999', text_preview=EN_TEXT),
        _log_row(actual_impr='9999', text_preview=JA_TEXT + "？"),
    ])
    assert x_presim.connect_baseline(str(csv_path)) == 600.0


def test_connect_baseline_missing_file(tmp_path):
    assert x_presim.connect_baseline(str(tmp_path / 'nope.csv')) is None


def test_score_uses_connect_baseline_for_connect_text(tmp_path, monkeypatch):
    csv_path = tmp_path / 'presim-log.csv'
    _write_presim_log(csv_path, [
        _log_row(actual_impr='400', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='600', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='800', text_preview=CONNECT_TEXT),
    ])
    monkeypatch.setattr(x_presim, 'LOG', str(csv_path))
    monkeypatch.setattr(x_presim, 'METRICS', str(tmp_path / 'missing-metrics.csv'))
    (row, _) = x_presim.score([dict(id='1', text=CONNECT_TEXT)], 'acc', 'heuristic', 'x', write=False)[0]
    assert row['baseline_impr'] == 600.0


def test_score_keeps_account_baseline_for_non_connect_text(tmp_path, monkeypatch):
    csv_path = tmp_path / 'presim-log.csv'
    _write_presim_log(csv_path, [
        _log_row(actual_impr='400', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='600', text_preview=CONNECT_TEXT),
        _log_row(actual_impr='800', text_preview=CONNECT_TEXT),
    ])
    monkeypatch.setattr(x_presim, 'LOG', str(csv_path))
    monkeypatch.setattr(x_presim, 'METRICS', str(tmp_path / 'missing-metrics.csv'))
    (row, _) = x_presim.score([dict(id='2', text=EN_TEXT)], 'acc', 'heuristic', 'x', write=False)[0]
    assert row['baseline_impr'] == 50.0


def test_le_zero_for_equal():
    assert x_presim.le(10, 10) == 0
    assert x_presim.le(0, 0) == 0


def test_le_symmetric_log_space():
    a, b = 10, 40
    assert x_presim.le(a, b) == pytest.approx(x_presim.le(b, a))
    # roughly |log ratio|: log(41/11) ~ 1.315
    assert x_presim.le(a, b) == pytest.approx(abs(math.log(41 / 11)), abs=0.001)
    # larger gap -> larger error
    assert x_presim.le(10, 100) > x_presim.le(10, 40)
