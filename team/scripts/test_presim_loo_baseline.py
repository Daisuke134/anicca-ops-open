"""Tests for the presim connect LOO baseline function."""

from presim_loo_baseline import loo_baselines


CONNECT_POSTS = [
    {"id": "2121745740913430569", "impressions": 3731},
    {"id": "2121910087383949396", "impressions": 2482},
    {"id": "2121608771445064174", "impressions": 473},
]


def test_loo_baselines_connect_posts():
    baselines = loo_baselines(CONNECT_POSTS)
    assert baselines["2121745740913430569"] == 1477.5
    assert baselines["2121910087383949396"] == 2102.0
    assert baselines["2121608771445064174"] == 3106.5
