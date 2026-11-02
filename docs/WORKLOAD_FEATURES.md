# Workload and fatigue feature layer

## What this adds

`nba_injury.workload.build_workload_features` converts player-game minutes into
pre-game workload history. It is designed to be joined to a game-level or
player-period modeling table using the player identifier and prediction date.

The function expects a game log with:

| Column | Meaning |
|---|---|
| `player_id` | Stable player identifier |
| `game_date` | Local game date (parseable by pandas) |
| `minutes` | Minutes played in that game |

Example:

```python
import pandas as pd
from nba_injury.workload import build_workload_features

games = pd.read_csv("player_game_logs.csv")
workload = build_workload_features(games)
```

## Features

All look-back windows are calendar-day windows and exclude the prediction
game's date. This is deliberate: a prediction made before tip-off must not
use minutes from the game it is predicting.

- `games_played_prior_7d/14d/30d`: prior appearances in each window.
- `minutes_played_prior_7d/14d/30d`: minutes accumulated in each window.
- `days_since_last_game`: calendar-day gap from the previous appearance.
- `is_back_to_back`: 1 when the previous appearance was one calendar day ago.

The output preserves the original row order and index. Missing minutes are
treated as zero in load sums; upstream data preparation should distinguish
DNPs from missing records where possible.

## Modeling and health-informatics cautions

These are workload proxies, not direct measurements of physiological fatigue,
recovery, tissue stress, or readiness. Public box-score data generally do not
provide sleep, soreness, practice load, travel burden, or individualized
recovery information.

Do not interpret a high minutes total or a back-to-back flag as proof that an
injury will occur. Workload-injury relationships are context-dependent and
observational. In particular:

- Evaluate workload features against the existing age/minutes baseline and
  without changing the temporal split.
- Add them only to training folds using data available at each prediction time.
- Report incremental AUPRC, Brier score, calibration, and season-level
  uncertainty—not only feature importance.
- Check performance by position/role and minutes exposure where sample sizes
  support it.
- Avoid treating a single acute:chronic workload ratio threshold as a clinical
  decision rule.
- Do not describe model-implied risk differences as the causal effect of
  reducing minutes or adding rest.

## Integration status

This is a tested, standalone feature-engineering layer. It is not yet wired
into the canonical person-period builder or hazard-model feature list because
the current connected repository view did not expose those source files for
inspection. Integration should be a separate change after confirming the
actual game-log schema, player/date keys, and prediction timestamp semantics.
