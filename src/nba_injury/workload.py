"""Leakage-aware player workload features from game-level minutes.

Each output row describes workload known immediately BEFORE that row's game.
The current game's minutes are never included in its own features.
This module is intentionally independent of the project's training pipeline
until the canonical game-log schema and person-period join are confirmed.
"""
from __future__ import annotations

from typing import Iterable

import pandas as pd


_REQUIRED = {"player_id", "game_date", "minutes"}


def build_workload_features(
    games: pd.DataFrame,
    *,
    windows: Iterable[int] = (7, 14, 30),
) -> pd.DataFrame:
    """Return one pre-game workload feature row per input game.

    Parameters
    ----------
    games:
        Game-level table with player_id, game_date, and minutes. A player may
        have multiple games on one date; rows are ordered stably as supplied.
        Missing minutes are treated as zero minutes for load sums but still
        count as a game appearance. Remove DNP rows upstream if they are not
        represented as appearances in the source.
    windows:
        Positive integer look-back windows in calendar days. The interval is
        [game_date - window, game_date), so same-day/current-game minutes and
        future games are excluded.

    Returns
    -------
    DataFrame
        Original columns plus days_since_last_game, is_back_to_back, and
        games_played_prior_{N}d / minutes_played_prior_{N}d features.
        Original row order and index are preserved.
    """
    missing = _REQUIRED.difference(games.columns)
    if missing:
        raise ValueError(f"games is missing required columns: {sorted(missing)}")

    normalized_windows = tuple(sorted(set(windows)))
    if not normalized_windows or any(
        not isinstance(w, int) or isinstance(w, bool) or w <= 0
        for w in normalized_windows
    ):
        raise ValueError("windows must contain positive integers")

    result = games.copy()
    result["_workload_original_order"] = range(len(result))
    result["_workload_date"] = pd.to_datetime(result["game_date"], errors="coerce")
    if result["_workload_date"].isna().any():
        raise ValueError("game_date contains missing or invalid dates")

    result["_workload_minutes"] = pd.to_numeric(result["minutes"], errors="coerce").fillna(0.0)
    if (result["_workload_minutes"] < 0).any():
        raise ValueError("minutes cannot be negative")

    result = result.sort_values(
        ["player_id", "_workload_date", "_workload_original_order"],
        kind="mergesort",
    )

    result["days_since_last_game"] = float("nan")
    result["is_back_to_back"] = 0
    for window in normalized_windows:
        result[f"games_played_prior_{window}d"] = 0
        result[f"minutes_played_prior_{window}d"] = 0.0

    for _, player_rows in result.groupby("player_id", sort=False, dropna=False):
        dates = player_rows["_workload_date"].to_numpy(dtype="datetime64[ns]")
        minutes = player_rows["_workload_minutes"].to_numpy(dtype=float)
        row_indices = player_rows.index.to_list()

        for position, row_index in enumerate(row_indices):
            current_date = dates[position]
            if position:
                gap = (current_date - dates[position - 1]) / pd.Timedelta(days=1)
                result.at[row_index, "days_since_last_game"] = float(gap)
                result.at[row_index, "is_back_to_back"] = int(gap <= 1.0)

            for window in normalized_windows:
                cutoff = current_date - pd.Timedelta(days=window)
                # searchsorted(..., side="left") excludes every game on the
                # current date, preventing same-day/current-game leakage.
                start = dates.searchsorted(cutoff, side="left")
                end = dates.searchsorted(current_date, side="left")
                prior_minutes = minutes[start:end]
                result.at[row_index, f"games_played_prior_{window}d"] = int(end - start)
                result.at[row_index, f"minutes_played_prior_{window}d"] = float(prior_minutes.sum())

    result = result.sort_values("_workload_original_order", kind="mergesort")
    return result.drop(
        columns=[
            "_workload_original_order",
            "_workload_date",
            "_workload_minutes",
        ]
    )
