# Model Card: NBA Injury-Risk & Career-Longevity Decision Support

## Summary

This project explores whether publicly available, historical NBA data can support estimates of player injury risk over time. The modeling design described in the project README uses a discrete-time hazard formulation, temporal validation, competing risks, recurrent-event features, and post-deployment monitoring.

This card describes the intended interpretation of the project. It does not certify clinical validity, operational readiness, or predictive performance.

## Intended use

- Educational and research exploration of longitudinal sports data.
- Demonstrating temporal validation, calibration, leakage checks, and model monitoring.
- Supporting aggregate analysis of risk patterns for transparent discussion.

## Out-of-scope use

Do not use these estimates to:
- Diagnose, treat, or make medical decisions about an athlete.
- Determine whether an individual is fit to play or should be withheld from competition.
- Make contract, salary, insurance, employment, or other high-impact decisions.
- Claim that a training, workload, or recovery intervention will prevent injury.

The model is observational. Feature attribution and all-else-equal counterfactuals are not causal evidence.

## Target and prediction unit

The intended prediction unit is a player-period row in a longitudinal person-period dataset. The event definition, prediction horizon, censoring rules, and competing-event definitions must be read from the versioned data-building code and final report before interpreting any metric. Do not infer a precise clinical injury definition from a generic label such as "injury."

## Data considerations

Public sports datasets can contain:
- Inconsistent injury descriptions and reporting practices across teams, seasons, and sources.
- Missing, delayed, or retrospectively corrected records.
- Differences in player role, minutes, age, and exposure that affect observed event rates.
- Selection effects: players with more public reporting or longer careers may be represented differently.

Record source URLs, retrieval dates, raw snapshot hashes, transformation versions, and label-mapping decisions for every analysis release. Synthetic data are for software checks only and must never be represented as real-world model evidence.

## Evaluation principles

Prefer temporal holdouts that simulate future deployment over random row-level splits. Report at minimum:
- AUPRC alongside the event prevalence.
- ROC-AUC as a ranking metric, not a probability-quality metric.
- Brier score and calibration plots or tables.
- Performance by season and relevant subgroups where sample sizes permit.
- Baseline comparisons and uncertainty intervals.

A single headline metric is insufficient. Repeated observations from the same player require player-aware reasoning when constructing splits and uncertainty estimates.

## Fairness and subgroup review

Evaluate errors and calibration across meaningful groups when data quality and sample size permit. Potential dimensions include age bands, position/role, season, and exposure bands. Suppress or qualify small cells. Public injury data may not support reliable demographic fairness analysis; absence of evidence is not evidence of equal performance.

## Explainability and causal limits

SHAP values describe how a fitted model uses features; they do not establish that a feature causes injury. Counterfactual outputs are model-implied sensitivity analyses under assumptions, not intervention effects. Fixed characteristics must not be presented as actionable levers. Any proposed intervention requires a separate causal design and domain review.

## Monitoring and change control

Monitor input drift, label delay, calibration, discrimination, and subgroup performance separately. Drift alone is not proof of model failure. Retraining should require a documented trigger, a frozen evaluation set, a comparison against the currently approved model, and a reproducible release record.

## Release checklist

- [ ] Data provenance and label definition documented.
- [ ] No player-period leakage across temporal evaluation boundaries.
- [ ] Synthetic and real-data outputs clearly distinguished.
- [ ] Baselines, calibration, and uncertainty reported.
- [ ] Subgroup limitations disclosed.
- [ ] Causal and medical-use limitations displayed alongside predictions.
- [ ] Reproduction instructions and dependency versions recorded.

## Disclaimer

This is an educational decision-support prototype, not a medical device and not a validated clinical or team-operational tool.
