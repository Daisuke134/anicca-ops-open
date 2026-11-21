import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('attribution_daily_apps', Path(__file__).parents[1] / 'attribution-daily.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_app_arg_and_cache():
    default = module.parse_args([])
    assert default.app == '6755129214'
    assert default.cache.endswith('/aff-funnel')  # Anicca keeps its original cache (daily cron)
    other = module.parse_args(['--app', '6759667221', '--cache', '/tmp/test'])
    assert other.cache == '/tmp/test/6759667221'


def test_unpublished_days_are_unknown(tmp_path):
    args = module.parse_args(['--app', '6759667221', '--cache', str(tmp_path), '--start', '2026-11-13', '--end', '2026-11-14'])
    report = module.render_app(args)
    assert '| 2026-11-13 | unknown (unpublished or unavailable) | unknown (unpublished or unavailable) | unknown (unpublished or unavailable) |' in report


def test_territory_and_app_isolation(tmp_path):
    import json
    args = module.parse_args(['--app', '6759667221', '--cache', str(tmp_path), '--start', '2026-11-13', '--end', '2026-11-14'])
    cache = Path(args.cache)
    cache.mkdir()
    rows = [dict(Date='2026-11-13', Territory='US', Event='Impression', Counts='7', _proc='2026-11-14', **{'App Apple Identifier': '6759667221'}), dict(Date='2026-11-13', Territory='JP', Event='Impression', Counts='99', _proc='2026-11-14', **{'App Apple Identifier': 'other'})]
    (cache / 'discovery.json').write_text(json.dumps(rows))
    report = module.render_app(args)
    assert '| US | 7 | 0 | unknown |' in report
    assert '| JP |' not in report
    assert '| 2026-11-14 | unknown (unpublished or unavailable)' in report
