#!/usr/bin/env python3
"""Synthetic MRT; python3 + numpy only. Run: python3 sim.py.
All participants available. Target averages decision times uniformly and histories
under the actual randomization policy, not under a reference-policy intervention.
Fixed design, no outcome-driven tuning. Binary X is synthetic engagement.
"""
import os
# Avoid thread overhead for many tiny linear systems; set before numpy import.
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
import json
import time
from pathlib import Path
import numpy as np

SEED, N, T, REPS = 20261031, 50, 100, 500
REF, Z = 0.5, 1.959963984540054


def simulate(rng):
    x = np.empty((N, T))
    a = np.empty_like(x)
    p = np.empty_like(x)
    x[:, 0] = rng.binomial(1, 0.5, N)
    for t in range(T):
        p[:, t] = 0.2 + 0.5 * x[:, t]
        a[:, t] = rng.binomial(1, p[:, t])
        if t + 1 < T:
            x[:, t + 1] = rng.binomial(1, 0.2 + 0.3*x[:, t] + 0.2*a[:, t])
    u = rng.normal(0, 0.5, (N, 1))
    y = (0.5 + 0.8*x + 0.3*np.arange(T)[None, :]/(T-1)
         + a*(0.4 + 0.8*x) + u + rng.normal(0, 1, (N, T)))
    return x.ravel(), a.ravel(), p.ravel(), y.ravel()


def fit(d, y, w):
    """WLS plus person-clustered CR1 sandwich, normal Wald intervals.
    Bread=sum(w dd'); cluster score=sum_t(w d residual).
    CR1=N/(N-1)*(nobs-1)/(nobs-k). No independence of times assumed.
    """
    bread = d.T @ (w[:, None]*d)
    coef = np.linalg.solve(bread, d.T @ (w*y))
    residual = y-d@coef
    scores = (d*(w*residual)[:, None]).reshape(N, T, -1).sum(axis=1)
    inv = np.linalg.inv(bread)
    correction = N/(N-1)*(N*T-1)/(N*T-d.shape[1])
    cov = correction * inv @ (scores.T@scores) @ inv
    return coef, np.sqrt(np.diag(cov))


def main():
    start = time.perf_counter()
    rng = np.random.default_rng(SEED)
    # q_0=.5; q_{t+1}=.2+.3 q_t+.2(.2+.5 q_t)=.24+.4 q_t.
    q = np.empty(T)
    q[0] = 0.5
    for t in range(T-1):
        q[t+1] = 0.24+0.4*q[t]
    marginal = float(0.4+0.8*q.mean())
    truths = {'ols_A_X': marginal, 'ols_A': marginal,
              'wcls_marginal': marginal, 'wcls_beta0': 0.4, 'wcls_beta1': 0.8}
    raw = {key: {'estimate': [], 'se': [], 'ci_low': [], 'ci_high': []} for key in truths}
    for _ in range(REPS):
        x, a, p, y = simulate(rng)
        ones = np.ones_like(x)
        w = np.where(a == 1, REF/p, (1-REF)/(1-p))
        control = np.column_stack((ones, x))  # deliberately omit time; WCLS remains valid
        designs = [(['ols_A_X'], np.column_stack((control, a)), ones, [-1]),
                   (['ols_A'], np.column_stack((ones, a)), ones, [-1]),
                   (['wcls_marginal'], np.column_stack((control, a-REF)), w, [-1]),
                   (['wcls_beta0', 'wcls_beta1'],
                    np.column_stack((control, a-REF, (a-REF)*x)), w, [-2, -1])]
        for names, d, weights, indices in designs:
            b, se = fit(d, y, weights)
            for name, idx in zip(names, indices):
                for field, value in [('estimate', b[idx]), ('se', se[idx]),
                                     ('ci_low', b[idx]-Z*se[idx]), ('ci_high', b[idx]+Z*se[idx])]:
                    raw[name][field].append(float(value))
    summary = {}
    for name, truth in truths.items():
        v = np.array(raw[name]['estimate'])
        summary[name] = {'true_value': truth, 'mean_estimate': float(v.mean()),
                         'bias': float(v.mean()-truth), 'empirical_sd': float(v.std(ddof=1)),
                         'rmse': float(np.sqrt(np.mean((v-truth)**2))),
                         'coverage_95': float(np.mean((np.array(raw[name]['ci_low']) <= truth)
                                                     & (truth <= np.array(raw[name]['ci_high']))))}
    # Rounded numbers used verbatim in article; full precision and all trial data retained.
    display = {name: {k: round(v, 4) for k, v in row.items()} for name, row in summary.items()}
    result = {'metadata': {'seed': SEED, 'N': N, 'T': T, 'replications': REPS,
                           'paper_arxiv': '1601.00237', 'paper_journal_year': 2018,
                           'date': '2026-10-31', 'numpy_version': np.__version__,
                           'ci_percent': 95, 'normal_critical': Z, 'p_reference': REF,
                           'runtime_limit_seconds': 120},
              'model': {'initial_state_probability': 0.5, 'p_intercept': 0.2, 'p_state': 0.5,
                        'p_min': 0.2, 'p_max': 0.7, 'transition_intercept': 0.2,
                        'transition_state': 0.3, 'transition_treatment': 0.2,
                        'baseline_intercept': 0.5, 'baseline_state': 0.8, 'baseline_time': 0.3,
                        'beta0': 0.4, 'beta1': 0.8, 'person_noise_sd': 0.5, 'outcome_noise_sd': 1.0,
                        'q_recursion_intercept': 0.24, 'q_recursion_slope': 0.4},
              'truth': {'q_by_time': q.tolist(), 'mean_q': float(q.mean()),
                        'marginal_effect': marginal, 'beta0': 0.4, 'beta1': 0.8,
                        'method': 'Exact recursion under actual policy; uniform average over T times'},
              'notes': ['Initial fixed setup; no parameter changes after seeing results.',
                        'Intercept-only effect is a time-averaged projection; instantaneous marginal effects vary with q_t.',
                        'X is pretreatment for current A but affected by prior A. Naive adjusted OLS omits A*X.',
                        'Controls are intercept and X; time trend deliberately omitted in all models.',
                        'Reference likelihood ratio uses realized A: .5/p if A=1, .5/(1-p) otherwise.',
                        'CR1 person sandwich with normal Wald intervals, not exact small-sample inference.'],
              'summary': summary, 'article_table': display, 'raw_results': raw}
    elapsed = time.perf_counter()-start
    result['metadata']['elapsed_seconds'] = elapsed
    assert elapsed < 120, 'Runtime exceeded requested limit'
    assert all(np.isfinite(v) for row in summary.values() for v in row.values())
    Path(__file__).with_name('output.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(display, indent=2))
    print(f'Elapsed seconds: {elapsed:.3f}')


if __name__ == '__main__':
    main()
