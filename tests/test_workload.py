import pandas as pd
import pytest

from nba_injury.workload import build_workload_features


def test_features_use_only_games_before_prediction_game():
    games = pd.DataFrame(
        {
            "player_id": [1, 1, 1, 1],
            "game_date": ["2025-01-01", "2025-01-03", "2025-01-08", "2025-01-09"],
            "minutes": [30, 40, 25, 36],
        }
    )

    result = build_workload_features(games).set_index("game_date")

    # Jan 8 sees Jan 1 and Jan 3 in the prior 7 calendar days.
    assert result.loc["2025-01-08", "games_played_prior_7d"] == 2
    assert result.loc["2025-01-08", "minutes_played_prior_7d"] == 70
    # Jan 9 sees Jan 8, but not its own 36 minutes.
    assert result.loc["2025-01-09", "games_played_prior_7d"] == 2
    assert result.loc["2025-01-09", "minutes_played_prior_7d"] == 65


def test_back_to_back_and_rest_days():
    games = pd.DataFrame(
        {
            "player_id": [7, 7, 7],
            "game_date": ["2025-02-01", "2025-02-02", "2025-02-05"],
            "minutes": [20, 22, 18],
        }
    )
    result = build_workload_features(games)

    assert pd.isna(result.loc[0, "days_since_last_game"])
    assert result.loc[1, "days_since_last_game"] == 1
    assert result.loc[1, "is_back_to_back"] == 1
    assert result.loc[2, "days_since_last_game"] == 3
    assert result.loc[2, "is_back_to_back"] == 0


def test_player_histories_are_isolated_and_input_order_is_preserved():
    games = pd.DataFrame(
        {
            "player_id": [2, 1, 2],
            "game_date": ["2025-03-03", "2025-03-01", "2025-03-01"],
            "minutes": [15, 35, 10],
        },
        index=[8, 3, 9],
    )
    result = build_workload_features(games)

    assert result.index.tolist() == [8, 3, 9]
    assert result.loc[8, "minutes_played_prior_7d"] == 10
    assert result.loc[3, "games_played_prior_7d"] == 0


def test_invalid_inputs_fail_loudly():
    with pytest.raises(ValueError, match="required columns"):
        build_workload_features(pd.DataFrame({"player_id": [1]}))

    with pytest.raises(ValueError, match="invalid dates"):
        build_workload_features(
            pd.DataFrame({"player_id": [1], "game_date": ["not-a-date"], "minutes": [10]})
        )

    with pytest.raises(ValueError, match="negative"):
        build_workload_features(
            pd.DataFrame({"player_id": [1], "game_date": ["2025-01-01"], "minutes": [-1]})
        )


def test_custom_windows_and_missing_minutes():
    games = pd.DataFrame(
        {
            "player_id": [1, 1],
            "game_date": ["2025-04-01", "2025-04-05"],
            "minutes": [None, 30],
        }
    )
    result = build_workload_features(games, windows=(3, 10))

    assert result.loc[1, "games_played_prior_10d"] == 1
    assert result.loc[1, "minutes_played_prior_10d"] == 0
    assert "minutes_played_prior_3d" in result.columns
