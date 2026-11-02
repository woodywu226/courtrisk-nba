# Workload and fatigue-risk feature experiment

Stage 3 now adds workload features to each player-week row. The prediction
timestamp is the Monday at the beginning of that week; every new workload
feature uses games strictly before that timestamp.

## Features

- Games and minutes in the prior 7, 14, and 30 calendar days.
- Days since the most recent game before the prediction week.
- Number of back-to-back game pairs in the prior seven days.

The original within-week fields remain in the person-period table for backwards
compatibility with downstream analyses. They are not used in the new workload
ablation because they include information from the prediction week.

## Rebuild and evaluate

After Stage 1 and Stage 2 caches are available, rebuild the canonical table:

```bash
PYTHONPATH=src python -m nba_injury.build_person_period
PYTHONPATH=src python -m nba_injury.model_hazard --report-json reports/stage4_metrics.json
```

The Stage 4 JSON now includes `workload_comparison`:

- `workload_baseline_30d`: prior-30-day minutes and games plus prior injury count.
- `workload_enhanced`: the same baseline plus 7/14-day exposure, rest interval,
  and prior-week back-to-back features.

Both models use the same at-risk temporal train/test split, median imputation
fit on training data, standardization, and unweighted logistic regression.
Unweighted fitting is intentional because the comparison reports Brier score
and calibration as well as ranking metrics. Compare AUPRC, ROC-AUC, Brier,
calibration curves, and season-level uncertainty; do not select a model on
AUPRC alone.

## Interpretation limits

These are box-score workload proxies, not direct physiological fatigue,
recovery, sleep, soreness, practice load, or readiness measurements. They are
observational predictors, not evidence that reducing minutes or adding rest
causes fewer injuries. The feature windows are computed within each season's
available game log; early-season windows naturally contain fewer observations.
Do not interpret a missing prior-game history as proof of low fatigue.

The existing Stage 4 models remain in the report for continuity. Their legacy
feature set includes within-week statistics, so the new controlled workload
ablation is the appropriate pre-week comparison for this question.
