# Contributing

Thanks for helping improve the NBA Injury-Risk & Career-Longevity project. Contributions should improve reproducibility, correctness, interpretability, or documentation—not simply increase model complexity.

## Before changing code

1. Read `README.md`, `PROJECT_VISION.md`, `BUILD_PLAN.md`, and the relevant stage report.
2. Identify the stage and gate affected by the change.
3. Check whether the change affects the target definition, feature availability time, player-period construction, or temporal split.
4. Add a short entry to `DECISIONS.md` for any non-obvious methodological choice.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m pytest tests/ -q
```

Use the synthetic pipeline for offline development:

```bash
./run_all.sh synthetic
```

Synthetic data validate software behavior only. They are not evidence of predictive performance and must not be used to claim a model passes real-data performance gates.

## Research and modeling rules

- Preserve chronological evaluation. Do not replace temporal validation with a random row split.
- Fit preprocessing only on training data; apply the fitted transformations to later periods.
- Audit every feature for availability at the prediction timestamp.
- Keep player identity and repeated observations in mind when splitting data and estimating uncertainty.
- Compare against simple, exposure-aware baselines before adding complexity.
- Report calibration and event prevalence alongside discrimination metrics.
- Do not interpret SHAP values or model-implied counterfactuals as causal effects.
- Keep optional dependencies optional and provide a graceful, tested fallback where appropriate.

## Tests expected

For a change to feature engineering or labels, add tests for:
- Boundary timestamps and season transitions.
- Missing and malformed values.
- Duplicate records and repeated injury episodes.
- Leakage across the prediction cutoff.
- Stable output schema and deterministic behavior.

For a model change, add tests for:
- Training-only preprocessing.
- Temporal split integrity.
- Probability bounds and finite outputs.
- Baseline comparison and metric edge cases.
- Calibration and subgroup reporting behavior.

For monitoring changes, test delayed labels, small samples, missing periods, and drift without degradation (and degradation without material input drift).

## Pull request checklist

- [ ] Scope and affected stage/gate are stated.
- [ ] Tests added or updated and passing.
- [ ] No real-data claims are based on synthetic data.
- [ ] Data provenance and feature timing are preserved.
- [ ] Metrics include context and appropriate baselines.
- [ ] Limitations and causal interpretation are accurate.
- [ ] Documentation and `DECISIONS.md` updated when needed.

## Commit style

Use concise, imperative commit messages, for example:

- `Add temporal split boundary tests`
- `Document injury-label adjudication rules`
- `Report calibration by season`
