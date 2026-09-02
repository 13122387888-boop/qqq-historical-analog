"""Select and evaluate a conservative V2 QQQ analog probability model.

Hyperparameters are selected only on 2010-2022 point-in-time forecasts sampled
every five trading days.  After the configuration is locked, it is evaluated
daily on the 2023+ retrospective holdout.  The displayed probability is shrunk
toward the same-MA200-regime base rate whenever analog evidence is unreliable.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import backtest_walk_forward as v1_backtest
import calculate_analogs as analogs


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "v2_model.json"
SCHEMA_VERSION = "1.0"
MODEL_VERSION = "2.0.0"
DEVELOPMENT_END = pd.Timestamp("2022-12-31")
HOLDOUT_START = pd.Timestamp("2023-01-01")
TUNING_STRIDE = 5
TOP_K_VALUES = (10, 20, 30)
KERNELS = (("equal", None), ("distance", 8.0))
ALPHAS = (0.0, 0.25, 0.5, 0.75, 1.0)
STABILITY_PENALTY = 0.25

PROFILES = (
    {"id": "v1_blend", "price_weight": 0.70, "return_weight": 0.30, "regime_weight": 0.00},
    {"id": "shape_equal", "price_weight": 0.50, "return_weight": 0.50, "regime_weight": 0.00},
    {"id": "balanced_soft", "price_weight": 0.45, "return_weight": 0.35, "regime_weight": 0.20},
    {"id": "trend_soft", "price_weight": 0.55, "return_weight": 0.20, "regime_weight": 0.25},
    {"id": "return_soft", "price_weight": 0.25, "return_weight": 0.50, "regime_weight": 0.25},
    {"id": "regime_aware", "price_weight": 0.35, "return_weight": 0.25, "regime_weight": 0.40},
    {"id": "returns_only", "price_weight": 0.00, "return_weight": 1.00, "regime_weight": 0.00},
)


def as_float(value: float, digits: int = 8) -> float:
    return round(float(value), digits)


def prepare_frame(frame: pd.DataFrame) -> pd.DataFrame:
    prepared = frame.copy()
    prices = prepared["Price"]
    prepared["MA50"] = prices.rolling(50, min_periods=50).mean()
    log_returns = np.log(prices / prices.shift(1))
    prepared["Vol20"] = log_returns.rolling(20, min_periods=20).std(ddof=0) * np.sqrt(252)
    prepared["Drawdown60"] = prices / prices.rolling(60, min_periods=60).max() - 1.0
    prepared["PriceMA200Gap"] = prices / prepared["MA200"] - 1.0
    prepared["MA50MA200Gap"] = prepared["MA50"] / prepared["MA200"] - 1.0
    return prepared


def regime_features(frame: pd.DataFrame) -> np.ndarray:
    """Soft state vector with fixed, interpretable economic scales."""
    return np.column_stack(
        [
            frame["PriceMA200Gap"].to_numpy(dtype=float) / 0.10,
            frame["MA50MA200Gap"].to_numpy(dtype=float) / 0.05,
            frame["Vol20"].to_numpy(dtype=float) / 0.15,
            frame["Drawdown60"].to_numpy(dtype=float) / 0.10,
        ]
    )


def component_scores(
    normalized_windows: np.ndarray,
    return_windows: np.ndarray,
    state_features: np.ndarray,
    candidate_rows: np.ndarray,
    candidate_ends: np.ndarray,
    current_row: int,
    current_index: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    price_distance = np.sqrt(
        np.mean(np.square(normalized_windows[candidate_rows] - normalized_windows[current_row]), axis=1)
    )
    return_distance = np.sqrt(
        np.mean(np.square(return_windows[candidate_rows] - return_windows[current_row]), axis=1)
    )
    state_distance = np.sqrt(
        np.mean(np.square(state_features[candidate_ends] - state_features[current_index]), axis=1)
    )
    return (
        100.0 * np.exp(-price_distance / analogs.PRICE_RMSE_SCALE),
        100.0 * np.exp(-return_distance / analogs.RETURN_RMSE_SCALE),
        100.0 * np.exp(-state_distance),
    )


def blended_scores(components: tuple[np.ndarray, np.ndarray, np.ndarray], profile: dict) -> np.ndarray:
    price_score, return_score, state_score = components
    return (
        profile["price_weight"] * price_score
        + profile["return_weight"] * return_score
        + profile["regime_weight"] * state_score
    )


def select_positions(scores: np.ndarray, end_indices: np.ndarray, top_k: int) -> np.ndarray:
    selected_positions: list[int] = []
    selected_ends: list[int] = []
    for position in np.argsort(scores)[::-1]:
        end_index = int(end_indices[position])
        if all(abs(end_index - prior) > analogs.MIN_MATCH_DISTANCE for prior in selected_ends):
            selected_positions.append(int(position))
            selected_ends.append(end_index)
        if len(selected_positions) == top_k:
            break
    if len(selected_positions) != top_k:
        raise RuntimeError(f"Could not select {top_k} independent analogs.")
    return np.asarray(selected_positions, dtype=int)


def outcome_weights(scores: np.ndarray, kernel: str, temperature: float | None) -> np.ndarray:
    if kernel == "equal":
        return np.full(len(scores), 1.0 / len(scores))
    raw = np.exp((scores - np.max(scores)) / float(temperature))
    return raw / np.sum(raw)


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    order = np.argsort(values)
    sorted_values = values[order]
    cumulative = np.cumsum(weights[order])
    return float(np.interp(quantile, cumulative, sorted_values))


def baseline_probabilities(
    forward_returns: dict[int, np.ndarray],
    regimes: np.ndarray,
    current_index: int,
) -> dict[int, float]:
    eligible_ends = np.arange(199, current_index - analogs.FORWARD_DAYS + 1)
    same_regime = regimes[eligible_ends] == regimes[current_index]
    return {
        horizon: float(np.mean(forward_returns[horizon][eligible_ends[same_regime]] > 0))
        for horizon in analogs.FORWARD_HORIZONS
    }


def robust_development_score(
    probability: np.ndarray,
    baseline: np.ndarray,
    outcome: np.ndarray,
    years: np.ndarray,
) -> tuple[float, int, list[dict]]:
    loss_advantage = np.square(baseline - outcome) - np.square(probability - outcome)
    yearly = []
    for year in np.unique(years):
        mask = years == year
        yearly.append({"year": int(year), "brier_advantage": float(np.mean(loss_advantage[mask]))})
    advantages = np.asarray([item["brier_advantage"] for item in yearly])
    score = float(np.mean(advantages) - STABILITY_PENALTY * np.std(advantages))
    return score, int(np.sum(advantages > 0)), yearly


def configuration_id(profile: dict, top_k: int, kernel: str) -> str:
    return f"{profile['id']}__k{top_k}__{kernel}"


def collect_predictions(
    frame: pd.DataFrame,
    lookback: int,
    mode: str,
    evaluation_indices: np.ndarray,
    configs: list[dict],
) -> tuple[dict[str, np.ndarray], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    prices = frame["Price"].to_numpy(dtype=float)
    regimes = np.where(prices > frame["MA200"].to_numpy(dtype=float), "bull", "bear")
    state_features = regime_features(frame)
    normalized_windows, return_windows = v1_backtest.make_window_matrices(prices, lookback)
    forward_returns = {
        horizon: prices[horizon:] / prices[:-horizon] - 1.0
        for horizon in analogs.FORWARD_HORIZONS
    }
    predictions = {
        config["id"]: np.empty((len(evaluation_indices), len(analogs.FORWARD_HORIZONS)), dtype=float)
        for config in configs
    }
    baselines = np.empty((len(evaluation_indices), len(analogs.FORWARD_HORIZONS)), dtype=float)
    realized = np.empty_like(baselines)

    configs_by_profile: dict[str, list[dict]] = {}
    for config in configs:
        configs_by_profile.setdefault(config["profile"]["id"], []).append(config)

    for row_number, current_index in enumerate(evaluation_indices):
        cutoff = current_index - analogs.FORWARD_DAYS
        candidate_ends = np.arange(max(lookback - 1, 199), cutoff + 1)
        candidate_rows = candidate_ends - lookback + 1
        current_row = current_index - lookback + 1
        components = component_scores(
            normalized_windows,
            return_windows,
            state_features,
            candidate_rows,
            candidate_ends,
            current_row,
            current_index,
        )
        available = np.arange(len(candidate_ends))
        if mode == "same_regime":
            available = np.flatnonzero(regimes[candidate_ends] == regimes[current_index])

        baseline = baseline_probabilities(forward_returns, regimes, current_index)
        for horizon_number, horizon in enumerate(analogs.FORWARD_HORIZONS):
            baselines[row_number, horizon_number] = baseline[horizon]
            realized[row_number, horizon_number] = forward_returns[horizon][current_index]

        for profile in PROFILES:
            if profile["id"] not in configs_by_profile:
                continue
            profile_scores = blended_scores(components, profile)
            maximum_positions = select_positions(
                profile_scores[available], candidate_ends[available], max(TOP_K_VALUES)
            )
            ranked_available = available[maximum_positions]
            for config in configs_by_profile[profile["id"]]:
                chosen = ranked_available[: config["top_k"]]
                weights = outcome_weights(
                    profile_scores[chosen], config["kernel"], config["temperature"]
                )
                for horizon_number, horizon in enumerate(analogs.FORWARD_HORIZONS):
                    outcomes = forward_returns[horizon][candidate_ends[chosen]]
                    predictions[config["id"]][row_number, horizon_number] = float(
                        np.sum(weights * (outcomes > 0))
                    )

    dates = frame["Date"].iloc[evaluation_indices].dt.strftime("%Y-%m-%d").to_numpy()
    years = frame["Date"].iloc[evaluation_indices].dt.year.to_numpy()
    return predictions, baselines, realized, dates, years


def build_search_space() -> list[dict]:
    configs = []
    for profile in PROFILES:
        for top_k in TOP_K_VALUES:
            for kernel, temperature in KERNELS:
                configs.append(
                    {
                        "id": configuration_id(profile, top_k, kernel),
                        "profile": profile,
                        "top_k": top_k,
                        "kernel": kernel,
                        "temperature": temperature,
                    }
                )
    return configs


def select_configuration(
    configs: list[dict],
    predictions: dict[str, np.ndarray],
    baselines: np.ndarray,
    realized: np.ndarray,
    years: np.ndarray,
) -> tuple[dict, dict, list[dict]]:
    outcomes = (realized > 0).astype(float)
    ranked_configs = []
    config_horizon_details: dict[str, dict] = {}
    for config in configs:
        horizon_details = {}
        horizon_scores = []
        for horizon_number, horizon in enumerate(analogs.FORWARD_HORIZONS):
            analog_probability = predictions[config["id"]][:, horizon_number]
            baseline = baselines[:, horizon_number]
            outcome = outcomes[:, horizon_number]
            alpha_candidates = []
            for alpha in ALPHAS:
                probability = baseline + alpha * (analog_probability - baseline)
                score, positive_years, yearly = robust_development_score(
                    probability, baseline, outcome, years
                )
                alpha_candidates.append(
                    {
                        "alpha": alpha,
                        "selection_score": score,
                        "positive_years": positive_years,
                        "yearly": yearly,
                        "brier": float(np.mean(np.square(probability - outcome))),
                        "baseline_brier": float(np.mean(np.square(baseline - outcome))),
                    }
                )
            best_alpha = sorted(
                alpha_candidates,
                key=lambda item: (-item["selection_score"], item["alpha"]),
            )[0]
            horizon_details[f"{horizon}d"] = best_alpha
            horizon_scores.append(best_alpha["selection_score"])

        objective = float(np.mean(horizon_scores))
        ranked_configs.append(
            {
                "id": config["id"],
                "objective": objective,
                "profile": config["profile"],
                "top_k": config["top_k"],
                "kernel": config["kernel"],
                "temperature": config["temperature"],
            }
        )
        config_horizon_details[config["id"]] = horizon_details

    ranked_configs.sort(
        key=lambda item: (
            -item["objective"],
            item["profile"]["regime_weight"],
            abs(item["top_k"] - 20),
            item["kernel"] != "equal",
        )
    )
    champion = ranked_configs[0]
    return champion, config_horizon_details[champion["id"]], ranked_configs[:10]


def evaluate_probabilities(
    probability: np.ndarray,
    baseline: np.ndarray,
    realized_return: np.ndarray,
    dates: np.ndarray,
    seed: int,
) -> dict:
    outcome = (realized_return > 0).astype(float)
    model_losses = np.square(probability - outcome)
    baseline_losses = np.square(baseline - outcome)
    advantage = baseline_losses - model_losses
    ci_low, ci_high = v1_backtest.moving_block_ci(advantage, seed)
    model_brier = float(np.mean(model_losses))
    baseline_brier = float(np.mean(baseline_losses))
    years = np.asarray([date[:4] for date in dates])
    positive_years = 0
    yearly = []
    for year in np.unique(years):
        mask = years == year
        skill = 1.0 - float(np.mean(model_losses[mask])) / float(np.mean(baseline_losses[mask]))
        yearly.append({"year": int(year), "brier_skill_vs_regime": as_float(skill)})
        positive_years += skill > 0
    if model_brier < baseline_brier and ci_low > 0:
        verdict = "validated_edge"
    elif model_brier < baseline_brier:
        verdict = "promising_not_conclusive"
    else:
        verdict = "no_observed_edge"
    return {
        "sample_count": int(len(probability)),
        "v2_brier": as_float(model_brier),
        "regime_brier": as_float(baseline_brier),
        "brier_skill_vs_regime": as_float(1.0 - model_brier / baseline_brier),
        "brier_advantage_vs_regime_ci95": [as_float(ci_low), as_float(ci_high)],
        "direction_hit_rate": as_float(np.mean((probability >= 0.5) == outcome)),
        "positive_skill_years": int(positive_years),
        "evaluated_years": int(len(np.unique(years))),
        "verdict": verdict,
        "yearly": yearly,
    }


def selected_config_predictions(
    frame: pd.DataFrame,
    lookback: int,
    mode: str,
    evaluation_indices: np.ndarray,
    champion: dict,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    config = {
        "id": champion["id"],
        "profile": champion["profile"],
        "top_k": champion["top_k"],
        "kernel": champion["kernel"],
        "temperature": champion["temperature"],
    }
    predictions, baselines, realized, dates, _ = collect_predictions(
        frame, lookback, mode, evaluation_indices, [config]
    )
    return predictions[config["id"]], baselines, realized, dates


def current_forecast(
    frame: pd.DataFrame,
    lookback: int,
    mode: str,
    champion: dict,
    horizon_details: dict,
) -> dict:
    prices = frame["Price"].to_numpy(dtype=float)
    regimes = np.where(prices > frame["MA200"].to_numpy(dtype=float), "bull", "bear")
    features = regime_features(frame)
    normalized_windows, return_windows = v1_backtest.make_window_matrices(prices, lookback)
    forward_returns = {
        horizon: prices[horizon:] / prices[:-horizon] - 1.0
        for horizon in analogs.FORWARD_HORIZONS
    }
    current_index = len(frame) - 1
    cutoff = current_index - analogs.FORWARD_DAYS
    candidate_ends = np.arange(max(lookback - 1, 199), cutoff + 1)
    candidate_rows = candidate_ends - lookback + 1
    components = component_scores(
        normalized_windows,
        return_windows,
        features,
        candidate_rows,
        candidate_ends,
        current_index - lookback + 1,
        current_index,
    )
    scores = blended_scores(components, champion["profile"])
    available = np.arange(len(candidate_ends))
    if mode == "same_regime":
        available = np.flatnonzero(regimes[candidate_ends] == regimes[current_index])
    chosen_within = select_positions(
        scores[available], candidate_ends[available], champion["top_k"]
    )
    chosen = available[chosen_within]
    selected_ends = candidate_ends[chosen]
    weights = outcome_weights(scores[chosen], champion["kernel"], champion["temperature"])
    baselines = baseline_probabilities(forward_returns, regimes, current_index)
    horizons = {}
    statistics = {}
    for horizon in analogs.FORWARD_HORIZONS:
        outcomes = forward_returns[horizon][selected_ends]
        analog_probability = float(np.sum(weights * (outcomes > 0)))
        alpha = horizon_details[f"{horizon}d"]["alpha"]
        calibrated = baselines[horizon] + alpha * (analog_probability - baselines[horizon])
        horizons[f"{horizon}d"] = {
            "analog_probability": as_float(analog_probability),
            "regime_probability": as_float(baselines[horizon]),
            "calibrated_probability": as_float(calibrated),
            "analog_evidence_weight": as_float(alpha),
            "weighted_median_return": as_float(weighted_quantile(outcomes, weights, 0.5)),
            "weighted_p25_return": as_float(weighted_quantile(outcomes, weights, 0.25)),
            "weighted_p75_return": as_float(weighted_quantile(outcomes, weights, 0.75)),
        }
        statistics[f"{horizon}d"] = {
            "up_probability": as_float(analog_probability),
            "calibrated_up_probability": as_float(calibrated),
            "regime_probability": as_float(baselines[horizon]),
            "analog_evidence_weight": as_float(alpha),
            "average": as_float(np.sum(weights * outcomes)),
            "median": as_float(weighted_quantile(outcomes, weights, 0.5)),
            "best": as_float(np.max(outcomes)),
            "worst": as_float(np.min(outcomes)),
        }

    matches = []
    forward_paths = []
    max_drawdowns = []
    for rank, (position, end_index, analysis_weight) in enumerate(
        zip(chosen, selected_ends, weights), start=1
    ):
        start_index = end_index - lookback + 1
        pattern_prices = prices[start_index : end_index + 1]
        future_prices = prices[end_index : end_index + analogs.FORWARD_DAYS + 1]
        forward_path = future_prices / prices[end_index] - 1.0
        running_peak = np.maximum.accumulate(future_prices)
        drawdowns = future_prices / running_peak - 1.0
        max_drawdown = float(np.min(drawdowns))
        forward_paths.append(forward_path)
        max_drawdowns.append(max_drawdown)
        matches.append(
            {
                "rank": rank,
                "start_date": frame.iloc[start_index]["Date"].strftime("%Y-%m-%d"),
                "end_date": frame.iloc[end_index]["Date"].strftime("%Y-%m-%d"),
                "similarity": as_float(scores[position], 4),
                "price_similarity": as_float(components[0][position], 4),
                "return_similarity": as_float(components[1][position], 4),
                "regime_similarity": as_float(components[2][position], 4),
                "analysis_weight": as_float(analysis_weight, 8),
                "market_regime": str(regimes[end_index]),
                "pattern": [as_float(value, 6) for value in analogs.normalize(pattern_prices)],
                "historical_path": [
                    as_float(value, 8) for value in pattern_prices / prices[end_index] - 1.0
                ],
                "forward_path": [as_float(value, 8) for value in forward_path],
                "returns": {
                    f"{horizon}d": as_float(forward_returns[horizon][end_index])
                    for horizon in analogs.FORWARD_HORIZONS
                },
                "max_drawdown_30d": as_float(max_drawdown),
                "max_gain_30d": as_float(np.max(future_prices / prices[end_index] - 1.0)),
            }
        )

    forward_path_matrix = np.asarray(forward_paths)
    distribution = []
    for day in range(analogs.FORWARD_DAYS + 1):
        values = forward_path_matrix[:, day]
        distribution.append(
            {
                "day": day,
                "p10": as_float(weighted_quantile(values, weights, 0.10)),
                "p25": as_float(weighted_quantile(values, weights, 0.25)),
                "median": as_float(weighted_quantile(values, weights, 0.50)),
                "p75": as_float(weighted_quantile(values, weights, 0.75)),
                "p90": as_float(weighted_quantile(values, weights, 0.90)),
            }
        )
    statistics["median_max_drawdown_30d"] = as_float(
        weighted_quantile(np.asarray(max_drawdowns), weights, 0.5)
    )
    statistics["median_max_gain_30d"] = as_float(
        weighted_quantile(
            np.asarray([match["max_gain_30d"] for match in matches]), weights, 0.5
        )
    )
    return {
        "as_of_date": frame.iloc[current_index]["Date"].strftime("%Y-%m-%d"),
        "effective_sample_size": as_float(1.0 / np.sum(np.square(weights)), 4),
        "selected_matches": matches,
        "horizons": horizons,
        "display_view": {
            "matches": matches,
            "statistics": statistics,
            "forward_distribution": distribution,
        },
    }


def main() -> None:
    frame = prepare_frame(analogs.load_prices())
    configs = build_search_space()
    development_indices = np.flatnonzero(
        (frame["Date"] >= v1_backtest.BACKTEST_START).to_numpy()
        & (frame["Date"] <= DEVELOPMENT_END).to_numpy()
        & (np.arange(len(frame)) <= len(frame) - analogs.FORWARD_DAYS - 1)
    )[::TUNING_STRIDE]
    full_indices = np.flatnonzero(
        (frame["Date"] >= v1_backtest.BACKTEST_START).to_numpy()
        & (np.arange(len(frame)) <= len(frame) - analogs.FORWARD_DAYS - 1)
    )
    development_mask = frame["Date"].iloc[full_indices].le(DEVELOPMENT_END).to_numpy()
    holdout_mask = frame["Date"].iloc[full_indices].ge(HOLDOUT_START).to_numpy()

    selections = {}
    seed = 20260902
    for lookback in analogs.LOOKBACKS:
        selections[str(lookback)] = {}
        for mode in ("all_regimes", "same_regime"):
            print(f"Tuning {lookback}D / {mode} on {len(development_indices)} dates")
            predictions, baselines, realized, _, years = collect_predictions(
                frame, lookback, mode, development_indices, configs
            )
            champion, horizon_details, leaderboard = select_configuration(
                configs, predictions, baselines, realized, years
            )
            print(
                f"  champion {champion['id']} objective {champion['objective']:+.6f}; "
                f"alphas {[horizon_details[f'{h}d']['alpha'] for h in analogs.FORWARD_HORIZONS]}"
            )
            daily_analog, daily_baseline, daily_realized, daily_dates = selected_config_predictions(
                frame, lookback, mode, full_indices, champion
            )
            backtest_results = {}
            for horizon_number, horizon in enumerate(analogs.FORWARD_HORIZONS):
                alpha = horizon_details[f"{horizon}d"]["alpha"]
                calibrated = daily_baseline[:, horizon_number] + alpha * (
                    daily_analog[:, horizon_number] - daily_baseline[:, horizon_number]
                )
                backtest_results[f"{horizon}d"] = {
                    "development": evaluate_probabilities(
                        calibrated[development_mask],
                        daily_baseline[development_mask, horizon_number],
                        daily_realized[development_mask, horizon_number],
                        daily_dates[development_mask],
                        seed,
                    ),
                    "holdout": evaluate_probabilities(
                        calibrated[holdout_mask],
                        daily_baseline[holdout_mask, horizon_number],
                        daily_realized[holdout_mask, horizon_number],
                        daily_dates[holdout_mask],
                        seed + 1,
                    ),
                }
                seed += 2
            selections[str(lookback)][mode] = {
                "champion": {
                    **champion,
                    "objective": as_float(champion["objective"]),
                },
                "horizon_calibration": {
                    horizon: {
                        "alpha": details["alpha"],
                        "selection_score": as_float(details["selection_score"]),
                        "positive_years": details["positive_years"],
                        "evaluated_years": len(details["yearly"]),
                        "development_brier": as_float(details["brier"]),
                        "development_regime_brier": as_float(details["baseline_brier"]),
                    }
                    for horizon, details in horizon_details.items()
                },
                "leaderboard": [
                    {**item, "objective": as_float(item["objective"])} for item in leaderboard
                ],
                "backtest": backtest_results,
                "current_forecast": current_forecast(
                    frame, lookback, mode, champion, horizon_details
                ),
            }

    result = {
        "schema_version": SCHEMA_VERSION,
        "model_version": MODEL_VERSION,
        "source_algorithm_version": analogs.ALGORITHM_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "completed",
        "selection_policy": {
            "development_period": "2010-01-04 to 2022-12-30",
            "holdout_period": "2023-01-03 to 2026-07-21",
            "tuning_frequency": f"every {TUNING_STRIDE} trading days",
            "final_evaluation_frequency": "every trading day",
            "primary_metric": "Brier advantage versus same-MA200-regime baseline",
            "objective": "mean annual Brier advantage minus 0.25 times annual standard deviation",
            "probability_formula": "regime_probability + alpha * (analog_probability - regime_probability)",
            "soft_regime_features": [
                "price / MA200 gap",
                "MA50 / MA200 gap",
                "20D annualized volatility",
                "60D drawdown",
            ],
            "top_k_values": list(TOP_K_VALUES),
            "alpha_values": list(ALPHAS),
            "profiles": list(PROFILES),
            "kernels": [kernel for kernel, _ in KERNELS],
            "holdout_not_used_for_selection": True,
        },
        "selections": selections,
    }
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    default = result["selections"]["30"]["all_regimes"]
    print("Default 30D all-regimes holdout:")
    for horizon in analogs.FORWARD_HORIZONS:
        metrics = default["backtest"][f"{horizon}d"]["holdout"]
        print(
            f"  {horizon:>2}D V2 Brier {metrics['v2_brier']:.4f} "
            f"skill {metrics['brier_skill_vs_regime']:+.2%} {metrics['verdict']}"
        )
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
