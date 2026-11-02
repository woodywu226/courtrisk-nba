# Reproducibility and Experiment Tracking

This guide describes the evidence that should accompany an analysis run so another person can reproduce it and understand exactly what changed.

## 1. Separate data modes

The project supports two fundamentally different workflows:

| Mode | Purpose | Permitted interpretation |
|---|---|---|
| Synthetic | Exercise pipeline, gates, and offline development | Software behavior only |
| Real | Analyze frozen public-source snapshots | Empirical results, subject to data and design limitations |

Never combine synthetic and real observations in one evaluation dataset. Label every generated report with its data mode.

## 2. Freeze inputs

For each real-data run, retain a manifest containing:

- Source name and source URL.
- Retrieval timestamp (UTC).
- Start and end dates requested.
- Raw file path and SHA-256 checksum.
- Parser and label-map version.
- Number of records retrieved, retained, rejected, and deduplicated.
- Any manual adjudication and its rationale.

Treat raw snapshots as immutable. A correction should create a new snapshot/version rather than silently overwrite the original.

## 3. Record the experiment

Each model run should record:

- Git commit SHA and working-tree status.
- Python version and dependency lock/version information.
- Data-manifest identifier.
- Feature set and prediction cutoff.
- Training and test season ranges.
- Random seeds and model hyperparameters.
- Event prevalence and number of players/player-periods.
- Baseline and candidate metrics.
- Calibration results and subgroup sample sizes.

A compact JSON record is preferable to relying on notebook output or terminal history.

## 4. Validate temporal integrity

Before fitting:
1. Assert that every training observation precedes the evaluation window.
2. Assert that features are available as of each prediction timestamp.
3. Ensure target construction does not use information from after that timestamp.
4. Check whether the same player's repeated rows create dependence across the split.
5. Fit imputers, encoders, scaling, and feature selection on training data only.

Document any exception explicitly. A model that performs well because it has seen future information is not a useful forecasting model.

## 5. Report more than one metric

Include event prevalence with AUPRC, and report ROC-AUC, Brier score, and calibration. Compare against simple baselines. Where feasible, use player-clustered or season-aware uncertainty estimates rather than treating every player-period row as independent.

If the event count is small, disclose the resulting uncertainty and avoid over-interpreting subgroup differences.

## 6. Preserve the evidence

A reproducible release should contain:

- The data manifest (without redistributing data where licensing prohibits it).
- Experiment configuration.
- Machine-readable metrics.
- Human-readable report with limitations.
- Gate/test results.
- Git commit identifier.

Do not commit private credentials, restricted source data, or personally sensitive information.

## 7. Suggested run record

```json
{
  "run_id": "2026-11-02-real-stage4-v1",
  "data_mode": "real",
  "git_commit": "REPLACE_WITH_COMMIT_SHA",
  "python_version": "RECORD_AT_RUNTIME",
  "data_manifest": "RECORD_MANIFEST_ID",
  "prediction_cutoff": "RECORD_CUTOFF",
  "train_seasons": ["RECORD_RANGE"],
  "test_seasons": ["RECORD_RANGE"],
  "event_prevalence": null,
  "metrics": {
    "auprc": null,
    "roc_auc": null,
    "brier": null
  },
  "notes": "Record limitations and deviations here."
}
```

Replace placeholders with measured values; never invent metrics or claim a run occurred when it did not.
