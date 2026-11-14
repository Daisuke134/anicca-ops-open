"""Synthetic binary-action experiment; Python standard library + NumPy only.
Run: python3 sim.py. Settings fixed before the first result inspection.
"""
import json
import math
import time
from pathlib import Path
import numpy as np

SEED = 20261101
T, REPS = 1000, 200
THETA = np.array([0.2, 0.8, -0.6])
ETA = np.ones(3)
RHO, V = 0.1, 1.0
LOW, HIGH = 0.2, 0.8
CHECKPOINTS = [100, 250, 500, 1000]
ALGORITHMS = ['ACTS', 'linear_TS', 'fixed_0.5']
SCENARIOS = ['linear', 'nonlinear', 'time_varying']


def cdf(z):
    # Exact standard-library normal CDF, applied across independent replications.
    return np.array([0.5 * (1 + math.erf(float(x) / math.sqrt(2))) for x in z])


def update(inv, b, x, weight, response):
    # Sherman-Morrison: inverse of B + weight*x*x^T.
    q = np.einsum('rij,rj->ri', inv, x)
    denom = 1 + weight * np.einsum('ri,ri->r', x, q)
    inv -= (weight / denom)[:, None, None] * q[:, :, None] * q[:, None, :]
    b += x * response[:, None]


def run_scenario(seed, scenario):
    rng = np.random.default_rng(seed)
    contexts = rng.normal(size=(T, REPS, 3))
    noise = rng.normal(size=(T, REPS))
    uniforms = rng.random((T, REPS))
    innovations = rng.normal(size=(T, REPS, 3))
    eta = np.ones((REPS, 3))
    inverses = {a: np.tile(np.eye(7 if a == 'linear_TS' else 3), (REPS, 1, 1)) for a in ALGORITHMS}
    bs = {a: np.zeros((REPS, inverses[a].shape[1])) for a in ALGORITHMS}
    cumulative = {a: np.zeros(REPS) for a in ALGORITHMS}
    curves = {a: [] for a in ALGORITHMS}
    for t in range(T):
        c = contexts[t]
        s = np.column_stack((np.ones(REPS), c[:, :2]))
        effect = s @ THETA
        optimal_pi = np.where(effect > 0, HIGH, LOW)
        if scenario == 'linear':
            baseline = c @ ETA
        elif scenario == 'nonlinear':
            baseline = 2.0 * (np.abs(c[:, 0]) < 0.8)
        else:
            # eta_0=ones; first decision uses eta_0, then transitions.
            baseline = np.einsum('ri,ri->r', eta, c)
            eta = math.sqrt(1 - RHO**2) * eta + RHO * innovations[t]
        for a in ALGORITHMS:
            inv, b = inverses[a], bs[a]
            mean = np.einsum('rij,rj->ri', inv, b)
            if a == 'fixed_0.5':
                pi = np.full(REPS, 0.5)
            else:
                mu = mean[:, 4:] if a == 'linear_TS' else mean
                cov = inv[:, 4:, 4:] if a == 'linear_TS' else inv
                variance = V**2 * np.einsum('ri,rij,rj->r', s, cov, s)
                pi = np.clip(cdf(np.einsum('ri,ri->r', s, mu) / np.sqrt(variance)), LOW, HIGH)
            action = (uniforms[t] < pi).astype(float)
            reward = baseline + action * effect + noise[t]
            regret = (optimal_pi - pi) * effect
            assert np.all(regret >= -1e-12)
            cumulative[a] += regret
            if t + 1 in CHECKPOINTS:
                curves[a].append(cumulative[a].copy())
            if a == 'linear_TS':
                x = np.column_stack((np.ones(REPS), c, action[:, None] * s))
                update(inv, b, x, np.ones(REPS), reward)
            else:
                update(inv, b, s, pi * (1 - pi), (action - pi) * reward)
    result = {}
    for a in ALGORITHMS:
        estimate = np.einsum('rij,rj->ri', inverses[a], bs[a])
        if a == 'linear_TS':
            estimate = estimate[:, 4:]
        error = np.linalg.norm(estimate - THETA, axis=1)
        values = cumulative[a]
        result[a] = {
            'mean_regret': float(values.mean()), 'median_regret': float(np.median(values)),
            'sd_regret': float(values.std(ddof=1)), 'mean_theta_error': float(error.mean()),
            'curve_means': {str(t): float(v.mean()) for t, v in zip(CHECKPOINTS, curves[a])},
            'replications': {'final_regret': values.tolist(), 'theta_hat': estimate.tolist(),
                             'theta_error': error.tolist(),
                             'regret_checkpoints': np.stack(curves[a], axis=1).tolist()}}
    return result


def main():
    start = time.perf_counter()
    seeds = np.random.SeedSequence(SEED).spawn(len(SCENARIOS))
    results = {s: run_scenario(seed, s) for s, seed in zip(SCENARIOS, seeds)}
    table = {s: {a: {k: round(results[s][a][k], 4) for k in
              ['mean_regret', 'median_regret', 'sd_regret', 'mean_theta_error']} for a in ALGORITHMS} for s in SCENARIOS}
    out = {'setup': {'seed': SEED, 'T': T, 'replications': REPS, 'context_dimension': 3,
        'effect_dimension': 3, 'nonzero_actions': 1, 'theta': THETA.tolist(), 'eta': ETA.tolist(),
        'rho': RHO, 'eta_initial': ETA.tolist(), 'v': V, 'pi_min': LOW, 'pi_max': HIGH,
        'fixed_pi': 0.5, 'noise_sd': 1, 'nonlinear_height': 2, 'nonlinear_threshold': 0.8,
        'prior_precision': 1, 'prior_mean': 0, 'checkpoints': CHECKPOINTS,
        'date': '2026-11-01', 'rounding_digits': 4},
        'paper': {'title': 'Action Centered Contextual Bandits', 'arxiv': '1711.03596', 'year': 2017,
                  'url': 'https://arxiv.org/abs/1711.03596', 'regret_equation': 8},
        'notes': ['Settings fixed before first run; no result-driven tuning or setup changes.',
          'ACTS binary N=1 specialization: exact Gaussian CDF; B=I+sum pi(1-pi)ss^T; b=sum s(A-pi)r.',
          'Linear TS: unit-noise Bayesian regression with zero mean and identity precision on [1,context,A*s].',
          'Fixed randomization uses ACTS centered estimator solely to report theta error.',
          'Within a scenario, algorithms share context, reward noise and uniform action draws; replications are independent.',
          'Scenarios use separate SeedSequence children; first time-varying decision uses eta_0=ones.',
          'Regret=(optimal_pi-pi)*(s^T theta), using policy probabilities, not realized actions; SD uses ddof=1.',
          'Gaussian features and baselines are unbounded: this is not a verification of the boundedness assumptions in the theorem.',
          'v=1 is a fixed experimental scale, not the theorem-specific exploration schedule.'],
        'results': results, 'article_table': table}
    out['runtime_seconds'] = time.perf_counter() - start
    assert out['runtime_seconds'] < 180
    Path('output.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(table, ensure_ascii=False, indent=2))
    print(f"Runtime: {out['runtime_seconds']:.2f}s")

if __name__ == '__main__':
    main()
