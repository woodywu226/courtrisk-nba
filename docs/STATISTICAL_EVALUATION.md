# Statistical Evaluation Standards

This document defines how to interpret and communicate model performance. It is a reporting standard, not a claim that every analysis currently implements every item.

## Prediction target first

Every report must state:
- What constitutes an injury event and which events are excluded.
- The prediction unit (for example, player-week or player-season).
- The prediction horizon and the exact time at which features are observed.
- How recurrent injuries, competing career exits, and censoring are handled.
- The event prevalence in each evaluation period.

Without these details, a metric is not interpretable.

## Discrimination

Report AUPRC and ROC-AUC together with the number of positive events and event prevalence. AUPRC is prevalence-dependent; compare it with the prevalence baseline. ROC-AUC measures ranking and does not establish useful probability estimates.

Avoid accuracy as a headline metric when events are rare. A classifier can achieve high accuracy by predicting no events.

## Probability quality

Report Brier score and calibration, preferably with:
- A reliability table or plot.
- Calibration intercept and slope when estimable.
- The number of observations and events per bin.
- A comparison with a constant-rate baseline.

Do not rely on expected calibration error alone; it depends on binning choices and can conceal local miscalibration.

## Baselines

At minimum compare against:
1. Constant hazard / event prevalence.
2. A simple exposure-aware baseline using available age and playing-time variables.
3. The candidate model.

All baselines must use the same training/evaluation boundaries and information cutoff.

## Temporal evaluation

Use chronological evaluation to mimic forecasting. Report the exact seasons or dates used for training, validation, and test. Never tune model choices on the final test window.

Repeated player-period rows are not independent observations. Where feasible, quantify uncertainty with player-clustered resampling or another dependence-aware method. If this is not feasible, explicitly state that row-level intervals may be too narrow.

## Subgroups

Predefine relevant subgroups rather than searching for favorable slices after evaluation. Potential slices include age band, role/position, season, and playing-time exposure. For each slice report sample size, event count, discrimination, and calibration where estimable.

Suppress or qualify small cells. Do not interpret noisy subgroup gaps as evidence of fairness or unfairness.

## Decision thresholds

If a threshold is discussed, state who would use it, what action it triggers, the expected false-positive and false-negative consequences, and how the threshold was selected. Do not imply that a threshold is operationally safe without prospective evaluation and domain review.

## Required narrative

A strong results section answers:
- Does the model improve on simple baselines?
- Are predicted probabilities calibrated?
- Does performance persist in later seasons?
- Which groups or contexts have weak evidence?
- What uncertainty remains?
- What decisions should explicitly not be made from this result?

A model that fails to beat a baseline is still a valid research finding when reported transparently.
