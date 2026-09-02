"""Run a point-in-time walk-forward evaluation of the published V1 analog model.

The backtest intentionally keeps the current 70/30 similarity formula and equal-
weighted Top 20 selection unchanged.  Its job is measurement, not optimisation.
Every forecast only uses analog outcomes that were fully known on that date.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import calculate_analogs as analogs


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "backtest.json"
BACKTEST_SCHEMA_VERSION = "1.0"
BACKTEST_VERSION = "1.0.0"
BACKTEST_START = pd.Timestamp("2010-01-01")
HOLDOUT_START = pd.Timestamp("2023-01-01")
BLOCK_LENGTH = 30
BOOTSTRAP_SAMPLES = 500
CALIBRATION_EDGES = np.array([0.0, 0.4, 0.5, 0.6, 0.7, 1.000001])


def as_float(value: float, digits: int = 8) -> float:
    return round(float(value), digits)


def select_match_positions(scores: np.ndarray, end_indices: np.ndarray) -> np.ndarray:
    """Return positions using the exact V1 greedy separation rule."""
    selected_positions: list[int] = []
    selected_ends: list[int] = []
    for position in np.argsort(scores)[::-1]:
        end_index = int(end_indices[position])
        if all(abs(end_index - prior) > analogs.MIN_MATCH_DISTANCE for prior in selected_ends):
            selected_positions.append(int(position))
            selected_ends.append(end_index)
        if len(selected_positions) == analogs.TOP_MATCHES:
            break
    if len(selected_positions) != analogs.TOP_MATCHES:
        raise RuntimeError("Not enough independent analogs for a walk-forward forecast.")
    return np.asarray(selected_positions, dtype=int)


def make_window_matrices(prices: np.ndarray, lookback: int) -> tuple[np.ndarray, np.ndarray]:
    windows = np.lib.stride_tricks.sliding_window_view(prices, lookback)
    normalized = windows / windows[:, :1] * 100.0
    returns = windows[:, 1:] / windows[:, :-1] - 1.0
    return normalized, returns


def candidate_scores(
    normalized_windows: np.ndarray,
    return_windows: np.ndarray,
    candidate_rows: np.ndarray,
    current_row: int,
) -> np.ndarray:
    price_distance = np.sqrt(
        np.mean(np.square(normalized_windows[candidate_rows] - normalized_windows[current_row]), axis=1)
    )
    return_distance = np.sqrt(
        np.mean(np.square(return_windows[candidate_rows] - return_windows[current_row]), axis=1)
    )
    price_score = 100.0 * np.exp(-price_distance / analogs.PRICE_RMSE_SCALE)
    return_score = 100.0 * np.exp(-return_distance / analogs.RETURN_RMSE_SCALE)
    return analogs.PRICE_WEIGHT * price_score + analogs.RETURN_WEIGHT * return_score


def empty_record() -> dict[str, list]:
    return {
        "dates": [],
        "model_probability": [],
        "model_median_return": [],
        "p10": [],
        "p25": [],
        "p75": [],
        "p90": [],
        "unconditional_probability": [],
        "regime_probability": [],
        "realized_return": [],
    }


def append_forecast(
    record: dict[str, list],
    date: str,
    analog_outcomes: np.ndarray,
    unconditional_probability: float,
    regime_probability: float,
    realized_return: float,
) -> None:
    p10, p25, median, p75, p90 = np.percentile(analog_outcomes, [10, 25, 50, 75, 90])
    record["dates"].append(date)
    record["model_probability"].append(float(np.mean(analog_outcomes > 0)))
    record["model_median_return"].append(float(median))
    record["p10"].append(float(p10))
    record["p25"].append(float(p25))
    record["p75"].append(float(p75))
    record["p90"].append(float(p90))
    record["unconditional_probability"].append(float(unconditional_probability))
    record["regime_probability"].append(float(regime_probability))
    record["realized_return"].append(float(realized_return))


def calibration_table(probability: np.ndarray, outcome: np.ndarray) -> list[dict]:
    rows = []
    for lower, upper in zip(CALIBRATION_EDGES[:-1], CALIBRATION_EDGES[1:]):
        mask = (probability >= lower) & (probability < upper)
        if not np.any(mask):
            continue
        rows.append(
            {
                "range": f"{lower:.1f}-{min(upper, 1.0):.1f}",
                "count": int(np.sum(mask)),
                "mean_forecast": as_float(np.mean(probability[mask])),
                "actual_up_rate": as_float(np.mean(outcome[mask])),
            }
        )
    return rows


def moving_block_ci(values: np.ndarray, seed: int) -> tuple[float, float]:
    """Moving-block bootstrap CI for the mean of overlapping forecast losses."""
    if len(values) < 2:
        value = float(values[0]) if len(values) else float("nan")
        return value, value
    block = min(BLOCK_LENGTH, len(values))
    blocks_needed = int(np.ceil(len(values) / block))
    max_start = len(values) - block + 1
    rng = np.random.default_rng(seed)
    samples = np.empty(BOOTSTRAP_SAMPLES, dtype=float)
    offsets = np.arange(block)
    for sample in range(BOOTSTRAP_SAMPLES):
        starts = rng.integers(0, max_start, size=blocks_needed)
        indices = (starts[:, None] + offsets).ravel()[: len(values)]
        samples[sample] = float(np.mean(values[indices]))
    return float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))


def evaluate_record(record: dict[str, list], mask: np.ndarray, seed: int) -> dict:
    probability = np.asarray(record["model_probability"], dtype=float)[mask]
    median_return = np.asarray(record["model_median_return"], dtype=float)[mask]
    p10 = np.asarray(record["p10"], dtype=float)[mask]
    p25 = np.asarray(record["p25"], dtype=float)[mask]
    p75 = np.asarray(record["p75"], dtype=float)[mask]
    p90 = np.asarray(record["p90"], dtype=float)[mask]
    unconditional = np.asarray(record["unconditional_probability"], dtype=float)[mask]
    regime = np.asarray(record["regime_probability"], dtype=float)[mask]
    realized_return = np.asarray(record["realized_return"], dtype=float)[mask]
    outcome = (realized_return > 0).astype(float)

    model_losses = np.square(probability - outcome)
    unconditional_losses = np.square(unconditional - outcome)
    regime_losses = np.square(regime - outcome)
    model_brier = float(np.mean(model_losses))
    unconditional_brier = float(np.mean(unconditional_losses))
    regime_brier = float(np.mean(regime_losses))
    loss_advantage = regime_losses - model_losses
    ci_low, ci_high = moving_block_ci(loss_advantage, seed)
    calibration_error = float(np.mean(np.abs(probability - outcome)))

    years = np.asarray([date[:4] for date in np.asarray(record["dates"])[mask]])
    year_results = []
    for year in np.unique(years):
        year_mask = years == year
        analog_year_brier = float(np.mean(model_losses[year_mask]))
        regime_year_brier = float(np.mean(regime_losses[year_mask]))
        year_results.append(
            {
                "year": int(year),
                "sample_count": int(np.sum(year_mask)),
                "brier_skill_vs_regime": as_float(1.0 - analog_year_brier / regime_year_brier),
            }
        )

    positive_years = sum(item["brier_skill_vs_regime"] > 0 for item in year_results)
    if model_brier < regime_brier and ci_low > 0:
        verdict = "validated_edge"
    elif model_brier < regime_brier:
        verdict = "promising_not_conclusive"
    else:
        verdict = "no_observed_edge"

    return {
        "sample_count": int(len(probability)),
        "analog_brier": as_float(model_brier),
        "unconditional_brier": as_float(unconditional_brier),
        "regime_brier": as_float(regime_brier),
        "brier_skill_vs_unconditional": as_float(1.0 - model_brier / unconditional_brier),
        "brier_skill_vs_regime": as_float(1.0 - model_brier / regime_brier),
        "brier_advantage_vs_regime_ci95": [as_float(ci_low), as_float(ci_high)],
        "direction_hit_rate": as_float(np.mean((probability >= 0.5) == outcome)),
        "median_return_mae": as_float(np.mean(np.abs(median_return - realized_return))),
        "interval_50_coverage": as_float(np.mean((realized_return >= p25) & (realized_return <= p75))),
        "interval_50_mean_width": as_float(np.mean(p75 - p25)),
        "interval_80_coverage": as_float(np.mean((realized_return >= p10) & (realized_return <= p90))),
        "interval_80_mean_width": as_float(np.mean(p90 - p10)),
        "mean_absolute_probability_error": as_float(calibration_error),
        "calibration": calibration_table(probability, outcome),
        "positive_skill_years": positive_years,
        "evaluated_years": len(year_results),
        "yearly": year_results,
        "verdict": verdict,
    }


def period_mask(dates: np.ndarray, period: str) -> np.ndarray:
    timestamps = pd.to_datetime(dates)
    if period == "development":
        return np.asarray(timestamps < HOLDOUT_START)
    if period == "holdout":
        return np.asarray(timestamps >= HOLDOUT_START)
    return np.ones(len(dates), dtype=bool)


def run_backtest(frame: pd.DataFrame) -> dict:
    prices = frame["Price"].to_numpy(dtype=float)
    dates = frame["Date"].to_numpy()
    date_strings = frame["Date"].dt.strftime("%Y-%m-%d").to_numpy()
    regimes = np.where(prices > frame["MA200"].to_numpy(dtype=float), "bull", "bear")
    evaluation_indices = np.flatnonzero(
        (frame["Date"] >= BACKTEST_START).to_numpy()
        & (np.arange(len(frame)) <= len(frame) - analogs.FORWARD_DAYS - 1)
    )
    if not len(evaluation_indices):
        raise RuntimeError("No dates are available for the configured backtest period.")

    forward_returns = {
        horizon: np.divide(prices[horizon:], prices[:-horizon]) - 1.0
        for horizon in analogs.FORWARD_HORIZONS
    }
    baseline_cache: dict[int, dict[int, tuple[float, float]]] = {}
    for current_index in evaluation_indices:
        eligible_ends = np.arange(199, current_index - analogs.FORWARD_DAYS + 1)
        if not len(eligible_ends):
            continue
        same_regime = regimes[eligible_ends] == regimes[current_index]
        baseline_cache[int(current_index)] = {}
        for horizon in analogs.FORWARD_HORIZONS:
            outcomes = forward_returns[horizon][eligible_ends]
            regime_outcomes = outcomes[same_regime]
            baseline_cache[int(current_index)][horizon] = (
                float(np.mean(outcomes > 0)),
                float(np.mean(regime_outcomes > 0)),
            )

    records: dict[tuple[int, str, int], dict[str, list]] = {
        (lookback, mode, horizon): empty_record()
        for lookback in analogs.LOOKBACKS
        for mode in ("all_regimes", "same_regime")
        for horizon in analogs.FORWARD_HORIZONS
    }

    for lookback in analogs.LOOKBACKS:
        normalized_windows, return_windows = make_window_matrices(prices, lookback)
        for count, current_index in enumerate(evaluation_indices, start=1):
            cutoff = current_index - analogs.FORWARD_DAYS
            candidate_ends = np.arange(max(lookback - 1, 199), cutoff + 1)
            if len(candidate_ends) < analogs.TOP_MATCHES:
                continue
            candidate_rows = candidate_ends - lookback + 1
            current_row = current_index - lookback + 1
            scores = candidate_scores(
                normalized_windows, return_windows, candidate_rows, current_row
            )
            mode_positions = {
                "all_regimes": np.arange(len(candidate_ends)),
                "same_regime": np.flatnonzero(regimes[candidate_ends] == regimes[current_index]),
            }
            for mode, available_positions in mode_positions.items():
                if len(available_positions) < analogs.TOP_MATCHES:
                    continue
                chosen_within_mode = select_match_positions(
                    scores[available_positions], candidate_ends[available_positions]
                )
                selected_ends = candidate_ends[available_positions[chosen_within_mode]]
                for horizon in analogs.FORWARD_HORIZONS:
                    outcomes = forward_returns[horizon][selected_ends]
                    unconditional_probability, regime_probability = baseline_cache[int(current_index)][horizon]
                    append_forecast(
                        records[(lookback, mode, horizon)],
                        date_strings[current_index],
                        outcomes,
                        unconditional_probability,
                        regime_probability,
                        forward_returns[horizon][current_index],
                    )
            if count % 500 == 0:
                print(f"{lookback}D: {count}/{len(evaluation_indices)} dates")

    results: dict[str, dict] = {}
    seed = 20260902
    for lookback in analogs.LOOKBACKS:
        results[str(lookback)] = {}
        for mode in ("all_regimes", "same_regime"):
            results[str(lookback)][mode] = {}
            for horizon in analogs.FORWARD_HORIZONS:
                record = records[(lookback, mode, horizon)]
                record_dates = np.asarray(record["dates"])
                horizon_result = {}
                for period in ("walk_forward", "development", "holdout"):
                    mask = period_mask(record_dates, period)
                    horizon_result[period] = evaluate_record(record, mask, seed)
                    seed += 1
                results[str(lookback)][mode][f"{horizon}d"] = horizon_result

    first_date = date_strings[evaluation_indices[0]]
    final_date = date_strings[evaluation_indices[-1]]
    holdout_date = date_strings[evaluation_indices[frame["Date"].iloc[evaluation_indices].ge(HOLDOUT_START).to_numpy()][0]]
    return {
        "schema_version": BACKTEST_SCHEMA_VERSION,
        "backtest_version": BACKTEST_VERSION,
        "algorithm_version": analogs.ALGORITHM_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "completed",
        "setup": {
            "evaluation_start": first_date,
            "evaluation_end": final_date,
            "development_period": f"{first_date} to 2022-12-31",
            "holdout_period": f"{holdout_date} to {final_date}",
            "evaluation_frequency": "every trading day",
            "lookbacks": list(analogs.LOOKBACKS),
            "forward_horizons": list(analogs.FORWARD_HORIZONS),
            "top_matches": analogs.TOP_MATCHES,
            "minimum_match_separation_days": analogs.MIN_MATCH_DISTANCE,
            "known_outcome_lag_days": analogs.FORWARD_DAYS,
            "candidate_rule": "candidate_end + 30 trading days <= forecast_date",
            "overlapping_forecasts": "retained; uncertainty uses moving-block bootstrap",
            "bootstrap_block_days": BLOCK_LENGTH,
            "bootstrap_samples": BOOTSTRAP_SAMPLES,
            "primary_metric": "Brier score; lower is better",
            "primary_baseline": "point-in-time up probability in the same MA200 regime",
        },
        "results": results,
    }


def main() -> None:
    frame = analogs.load_prices()
    result = run_backtest(frame)
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    example = result["results"]["30"]["all_regimes"]["20d"]["holdout"]
    print(
        "30D / all regimes / 20D holdout: "
        f"Brier {example['analog_brier']:.4f}, "
        f"skill vs regime {example['brier_skill_vs_regime']:+.2%}, "
        f"verdict {example['verdict']}"
    )
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
