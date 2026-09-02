"""Maintain a prospective shadow ledger for a frozen 30D drawdown challenger.

The command is deliberately idempotent and issues at most one forecast: the latest
observation in data/qqq.csv.  It never backfills missed forecast dates.  Existing
pending forecasts are settled once 30 newer trading days are present in the CSV.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import backtest_walk_forward as backtest
import calculate_analogs as analogs
import optimize_similarity_v2 as v2


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "shadow_validation.json"
SCHEMA_VERSION = "1.0"
MODEL_VERSION = "shadow-dd3-internal-ridge-1.0.0"
HORIZON = 30
EVENT_THRESHOLD = -0.03
RIDGE = 10.0
TRAINING_STRIDE = 5
MIN_MATURED_FORECASTS = 252


def as_float(value: float, digits: int = 8) -> float:
    return round(float(value), digits)


def future_drawdown(prices: np.ndarray, start_index: int) -> float:
    future = prices[start_index : start_index + HORIZON + 1]
    running_peak = np.maximum.accumulate(future)
    return float(np.min(future / running_peak - 1.0))


def logit(probability: float | np.ndarray) -> float | np.ndarray:
    clipped = np.clip(probability, 0.01, 0.99)
    return np.log(clipped / (1.0 - clipped))


def sigmoid(score: float | np.ndarray) -> float | np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(score, -30.0, 30.0)))


def baseline_probability(
    prices: np.ndarray,
    regimes: np.ndarray,
    current_index: int,
) -> float:
    eligible = np.arange(199, current_index - HORIZON + 1)
    same_regime = eligible[regimes[eligible] == regimes[current_index]]
    outcomes = np.asarray(
        [future_drawdown(prices, int(index)) <= EVENT_THRESHOLD for index in same_regime],
        dtype=float,
    )
    return float(np.mean(outcomes))


def raw_features(
    frame: pd.DataFrame,
    prices: np.ndarray,
    regimes: np.ndarray,
    current_index: int,
) -> np.ndarray:
    baseline = baseline_probability(prices, regimes, current_index)
    internal = v2.regime_features(frame)[current_index]
    return np.concatenate(([float(logit(baseline))], internal))


def logistic_objective(features: np.ndarray, outcome: np.ndarray, beta: np.ndarray) -> float:
    score = np.clip(features @ beta, -30.0, 30.0)
    likelihood = np.sum(np.logaddexp(0.0, score) - outcome * score)
    return float(likelihood + 0.5 * RIDGE * np.sum(np.square(beta[1:])))


def fit_logistic(features: np.ndarray, outcome: np.ndarray) -> np.ndarray:
    beta = np.zeros(features.shape[1], dtype=float)
    event_rate = float(np.clip(np.mean(outcome), 0.01, 0.99))
    beta[0] = float(logit(event_rate))
    penalty = np.eye(features.shape[1]) * RIDGE
    penalty[0, 0] = 0.0
    current_objective = logistic_objective(features, outcome, beta)
    for _ in range(100):
        probability = np.asarray(sigmoid(features @ beta))
        weights = np.maximum(probability * (1.0 - probability), 1e-6)
        gradient = features.T @ (probability - outcome) + penalty @ beta
        hessian = features.T @ (weights[:, None] * features) + penalty
        step = np.linalg.solve(hessian + np.eye(features.shape[1]) * 1e-9, gradient)
        multiplier = 1.0
        accepted = False
        while multiplier >= 1e-6:
            candidate = beta - multiplier * step
            candidate_objective = logistic_objective(features, outcome, candidate)
            if candidate_objective <= current_objective:
                beta = candidate
                current_objective = candidate_objective
                accepted = True
                break
            multiplier *= 0.5
        if not accepted or float(np.max(np.abs(multiplier * step))) < 1e-8:
            break
    return beta


def train_frozen_model(frame: pd.DataFrame) -> dict:
    prices = frame["Price"].to_numpy(dtype=float)
    regimes = np.where(prices > frame["MA200"].to_numpy(dtype=float), "bull", "bear")
    latest_mature_index = len(frame) - HORIZON - 1
    indices = np.flatnonzero(
        frame["Date"].ge(backtest.BACKTEST_START).to_numpy()
        & (np.arange(len(frame)) <= latest_mature_index)
    )[::TRAINING_STRIDE]
    feature_rows = np.vstack(
        [raw_features(frame, prices, regimes, int(index)) for index in indices]
    )
    outcomes = np.asarray(
        [future_drawdown(prices, int(index)) <= EVENT_THRESHOLD for index in indices],
        dtype=float,
    )
    means = np.mean(feature_rows, axis=0)
    stds = np.std(feature_rows, axis=0)
    stds[stds < 1e-8] = 1.0
    scaled = (feature_rows - means) / stds
    design = np.column_stack([np.ones(len(scaled)), scaled])
    beta = fit_logistic(design, outcomes)
    return {
        "model_version": MODEL_VERSION,
        "status": "frozen_challenger",
        "target": "30-trading-day peak-to-trough drawdown at or below -3%",
        "horizon_trading_days": HORIZON,
        "event_threshold": EVENT_THRESHOLD,
        "feature_names": [
            "same-MA200-regime baseline log-odds",
            "price / MA200 gap",
            "MA50 / MA200 gap",
            "20D annualized volatility",
            "60D drawdown",
        ],
        "ridge_penalty": RIDGE,
        "coefficients": [as_float(value, 12) for value in beta],
        "feature_means": [as_float(value, 12) for value in means],
        "feature_stds": [as_float(value, 12) for value in stds],
        "training_stride_trading_days": TRAINING_STRIDE,
        "training_sample_count": int(len(indices)),
        "training_start": frame.iloc[int(indices[0])]["Date"].strftime("%Y-%m-%d"),
        "training_end": frame.iloc[int(indices[-1])]["Date"].strftime("%Y-%m-%d"),
        "architecture_selection": "2010-2018 development; 2019-2022 validation",
        "refit_policy": "Frozen before prospective issuance; no refit during shadow test",
    }


def predict(model: dict, feature_row: np.ndarray) -> float:
    means = np.asarray(model["feature_means"], dtype=float)
    stds = np.asarray(model["feature_stds"], dtype=float)
    beta = np.asarray(model["coefficients"], dtype=float)
    scaled = (feature_row - means) / stds
    design = np.concatenate(([1.0], scaled))
    return float(sigmoid(design @ beta))


def settle_records(records: list[dict], frame: pd.DataFrame) -> None:
    prices = frame["Price"].to_numpy(dtype=float)
    date_to_index = {
        date.strftime("%Y-%m-%d"): index for index, date in enumerate(frame["Date"])
    }
    for record in records:
        if record["status"] != "pending":
            continue
        start_index = date_to_index.get(record["forecast_date"])
        if start_index is None or start_index + HORIZON >= len(frame):
            continue
        realized = future_drawdown(prices, start_index)
        outcome = float(realized <= EVENT_THRESHOLD)
        record.update(
            {
                "status": "matured",
                "target_end_date": frame.iloc[start_index + HORIZON]["Date"].strftime("%Y-%m-%d"),
                "realized_max_drawdown": as_float(realized),
                "event_occurred": bool(outcome),
                "challenger_brier": as_float(
                    (float(record["challenger_probability"]) - outcome) ** 2
                ),
                "baseline_brier": as_float(
                    (float(record["baseline_probability"]) - outcome) ** 2
                ),
            }
        )


def issue_latest_forecast(payload: dict, frame: pd.DataFrame) -> bool:
    forecast_date = frame.iloc[-1]["Date"].strftime("%Y-%m-%d")
    if any(record["forecast_date"] == forecast_date for record in payload["records"]):
        return False
    prices = frame["Price"].to_numpy(dtype=float)
    regimes = np.where(prices > frame["MA200"].to_numpy(dtype=float), "bull", "bear")
    current_index = len(frame) - 1
    feature_row = raw_features(frame, prices, regimes, current_index)
    baseline = baseline_probability(prices, regimes, current_index)
    challenger = predict(payload["frozen_model"], feature_row)
    payload["records"].append(
        {
            "forecast_date": forecast_date,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "status": "pending",
            "target_end_date": None,
            "horizon_trading_days": HORIZON,
            "event_threshold": EVENT_THRESHOLD,
            "market_regime": str(regimes[current_index]),
            "baseline_probability": as_float(baseline),
            "challenger_probability": as_float(challenger),
            "feature_snapshot": {
                name: as_float(value)
                for name, value in zip(payload["frozen_model"]["feature_names"], feature_row)
            },
        }
    )
    return True


def evaluation_summary(records: list[dict], seed: int = 20260902) -> dict:
    matured = [record for record in records if record["status"] == "matured"]
    pending = [record for record in records if record["status"] == "pending"]
    summary = {
        "matured_forecasts": len(matured),
        "pending_forecasts": len(pending),
        "minimum_matured_forecasts": MIN_MATURED_FORECASTS,
        "promotion_status": "waiting_for_forward_evidence",
        "challenger_brier": None,
        "baseline_brier": None,
        "brier_skill_vs_regime": None,
        "brier_advantage_ci95": None,
    }
    if not matured:
        return summary
    challenger_losses = np.asarray([record["challenger_brier"] for record in matured])
    baseline_losses = np.asarray([record["baseline_brier"] for record in matured])
    advantage = baseline_losses - challenger_losses
    summary.update(
        {
            "challenger_brier": as_float(np.mean(challenger_losses)),
            "baseline_brier": as_float(np.mean(baseline_losses)),
            "brier_skill_vs_regime": as_float(
                1.0 - np.mean(challenger_losses) / np.mean(baseline_losses)
            ),
        }
    )
    if len(matured) >= 2:
        low, high = backtest.moving_block_ci(advantage, seed)
        summary["brier_advantage_ci95"] = [as_float(low), as_float(high)]
        if len(matured) >= MIN_MATURED_FORECASTS and low > 0:
            summary["promotion_status"] = "eligible_for_model_review"
    return summary


def new_payload(frame: pd.DataFrame) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "shadow_only",
        "purpose": "Prospective evidence collection; never used by the official outlook",
        "issuance_policy": "Latest available observation only; never backfill missed forecasts",
        "promotion_policy": {
            "minimum_matured_forecasts": MIN_MATURED_FORECASTS,
            "required_ci_rule": "95% moving-block bootstrap lower bound above zero",
            "automatic_promotion": False,
        },
        "frozen_model": train_frozen_model(frame),
        "records": [],
    }


def load_frame() -> pd.DataFrame:
    return v2.prepare_frame(analogs.load_prices())


def main() -> None:
    frame = load_frame()
    if OUTPUT_PATH.exists():
        payload = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        if payload.get("frozen_model", {}).get("model_version") != MODEL_VERSION:
            raise RuntimeError("Existing shadow ledger uses a different frozen model version.")
    else:
        payload = new_payload(frame)
    settle_records(payload["records"], frame)
    issued = issue_latest_forecast(payload, frame)
    payload["evaluation"] = evaluation_summary(payload["records"])
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    payload["source_data"] = {
        "end_date": frame.iloc[-1]["Date"].strftime("%Y-%m-%d"),
        "row_count": int(len(frame)),
        "csv_sha256": hashlib.sha256((PROJECT_ROOT / "data" / "qqq.csv").read_bytes()).hexdigest(),
    }
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    latest = payload["records"][-1]
    print(
        f"Shadow ledger: {payload['evaluation']['matured_forecasts']} matured, "
        f"{payload['evaluation']['pending_forecasts']} pending; "
        f"{'issued' if issued else 'kept'} {latest['forecast_date']} at "
        f"{latest['challenger_probability']:.1%}."
    )
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
