"""Calculate QQQ historical analogs without using forward data in similarity."""

from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "qqq.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "analogs.json"
SOURCE_PATH = PROJECT_ROOT / "data" / "source.json"

LOOKBACKS = (10, 15, 20, 30)
FORWARD_HORIZONS = (5, 10, 20, 30)
FORWARD_DAYS = 30
TOP_MATCHES = 20
MIN_MATCH_DISTANCE = 20

# Monotonic score transforms. These are similarity display scales, not probabilities.
PRICE_RMSE_SCALE = 5.0
RETURN_RMSE_SCALE = 0.02
PRICE_WEIGHT = 0.70
RETURN_WEIGHT = 0.30
SCHEMA_VERSION = "1.1"
ALGORITHM_VERSION = "1.1.0"


def as_float(value: float, digits: int = 8) -> float:
    return round(float(value), digits)


def load_prices() -> pd.DataFrame:
    frame = pd.read_csv(INPUT_PATH)
    frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
    for column in ("Open", "High", "Low", "Close", "Adj Close", "Volume"):
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")

    price_column = "Adj Close" if "Adj Close" in frame and frame["Adj Close"].notna().any() else "Close"
    frame = (
        frame.dropna(subset=["Date", price_column, "Close"])
        .drop_duplicates(subset="Date", keep="last")
        .sort_values("Date")
    )
    frame = frame[(frame[price_column] > 0) & (frame["Close"] > 0)].copy()
    frame["Price"] = frame[price_column].astype(float)
    frame["MA200"] = frame["Price"].rolling(200, min_periods=200).mean()
    frame.reset_index(drop=True, inplace=True)
    frame.attrs["price_column"] = price_column
    if len(frame) < 260:
        raise RuntimeError("At least 260 clean trading days are required.")
    return frame


def normalize(prices: np.ndarray) -> np.ndarray:
    return prices / prices[0] * 100.0


def daily_returns(prices: np.ndarray) -> np.ndarray:
    return prices[1:] / prices[:-1] - 1.0


def rmse(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(left - right))))


def score_from_rmse(distance: float, scale: float) -> float:
    return float(100.0 * np.exp(-distance / scale))


def market_regime(price: float, ma200: float) -> str:
    return "bull" if price > ma200 else "bear"


def build_candidate(
    frame: pd.DataFrame,
    prices: np.ndarray,
    current_normalized: np.ndarray,
    current_returns: np.ndarray,
    lookback: int,
    end_index: int,
) -> dict:
    start_index = end_index - lookback + 1
    historical_prices = prices[start_index : end_index + 1]
    historical_normalized = normalize(historical_prices)
    price_rmse = rmse(current_normalized, historical_normalized)
    return_rmse = rmse(current_returns, daily_returns(historical_prices))
    price_score = score_from_rmse(price_rmse, PRICE_RMSE_SCALE)
    return_score = score_from_rmse(return_rmse, RETURN_RMSE_SCALE)
    similarity = PRICE_WEIGHT * price_score + RETURN_WEIGHT * return_score

    return {
        "end_index": end_index,
        "start_index": start_index,
        "similarity": similarity,
        "price_rmse": price_rmse,
        "return_rmse": return_rmse,
        "price_score": price_score,
        "return_score": return_score,
        "market_regime": market_regime(prices[end_index], frame.iloc[end_index]["MA200"]),
    }


def select_independent_matches(candidates: Iterable[dict]) -> list[dict]:
    selected: list[dict] = []
    for candidate in sorted(candidates, key=lambda item: item["similarity"], reverse=True):
        if all(abs(candidate["end_index"] - match["end_index"]) > MIN_MATCH_DISTANCE for match in selected):
            selected.append(candidate)
        if len(selected) == TOP_MATCHES:
            break
    return selected


def enrich_match(frame: pd.DataFrame, prices: np.ndarray, lookback: int, candidate: dict, rank: int) -> dict:
    start_index = candidate["start_index"]
    end_index = candidate["end_index"]
    end_price = prices[end_index]
    pattern_prices = prices[start_index : end_index + 1]
    future_prices = prices[end_index : end_index + FORWARD_DAYS + 1]
    forward_path = future_prices / end_price - 1.0
    running_peak = np.maximum.accumulate(future_prices)
    drawdowns = future_prices / running_peak - 1.0

    return {
        "rank": rank,
        "start_date": frame.iloc[start_index]["Date"].strftime("%Y-%m-%d"),
        "end_date": frame.iloc[end_index]["Date"].strftime("%Y-%m-%d"),
        "similarity": as_float(candidate["similarity"], 4),
        "rmse": as_float(candidate["price_rmse"]),
        "return_rmse": as_float(candidate["return_rmse"]),
        "price_similarity": as_float(candidate["price_score"], 4),
        "return_similarity": as_float(candidate["return_score"], 4),
        "market_regime": candidate["market_regime"],
        "pattern": [as_float(value, 6) for value in normalize(pattern_prices)],
        "historical_path": [as_float(value, 8) for value in (pattern_prices / end_price - 1.0)],
        "forward_path": [as_float(value, 8) for value in forward_path],
        "returns": {
            f"{horizon}d": as_float(forward_path[horizon]) for horizon in FORWARD_HORIZONS
        },
        "max_drawdown_30d": as_float(np.min(drawdowns)),
        "max_gain_30d": as_float(np.max(future_prices / end_price - 1.0)),
    }


def calculate_statistics(matches: list[dict]) -> dict:
    statistics: dict[str, dict] = {}
    for horizon in FORWARD_HORIZONS:
        values = np.array([match["returns"][f"{horizon}d"] for match in matches], dtype=float)
        statistics[f"{horizon}d"] = {
            "up_probability": as_float(np.mean(values > 0)),
            "average": as_float(np.mean(values)),
            "median": as_float(np.median(values)),
            "best": as_float(np.max(values)),
            "worst": as_float(np.min(values)),
        }
    statistics["median_max_drawdown_30d"] = as_float(
        np.median([match["max_drawdown_30d"] for match in matches])
    )
    statistics["median_max_gain_30d"] = as_float(
        np.median([match["max_gain_30d"] for match in matches])
    )
    return statistics


def calculate_distribution(matches: list[dict]) -> list[dict]:
    paths = np.array([match["forward_path"] for match in matches], dtype=float)
    result = []
    for day in range(FORWARD_DAYS + 1):
        p10, p25, median, p75, p90 = np.percentile(paths[:, day], [10, 25, 50, 75, 90])
        result.append(
            {
                "day": day,
                "p10": as_float(p10),
                "p25": as_float(p25),
                "median": as_float(median),
                "p75": as_float(p75),
                "p90": as_float(p90),
            }
        )
    return result


def calculate_mode(
    frame: pd.DataFrame,
    prices: np.ndarray,
    current_normalized: np.ndarray,
    current_returns: np.ndarray,
    current_regime: str,
    lookback: int,
    same_regime_only: bool,
) -> dict:
    # end_index + 30 must exist. Similarity only reads through end_index.
    candidates = []
    for end_index in range(max(lookback - 1, 199), len(frame) - FORWARD_DAYS):
        candidate = build_candidate(
            frame,
            prices,
            current_normalized,
            current_returns,
            lookback,
            end_index,
        )
        if same_regime_only and candidate["market_regime"] != current_regime:
            continue
        candidates.append(candidate)

    selected = select_independent_matches(candidates)
    if not selected:
        raise RuntimeError(f"No eligible {lookback}D matches were found.")
    matches = [
        enrich_match(frame, prices, lookback, candidate, rank)
        for rank, candidate in enumerate(selected, start=1)
    ]
    return {
        "matches": matches,
        "statistics": calculate_statistics(matches),
        "forward_distribution": calculate_distribution(matches),
    }


def consensus_label(up_probability: float) -> str:
    if up_probability >= 0.60:
        return "bullish"
    if up_probability < 0.40:
        return "bearish"
    return "neutral"


def calculate_consensus(lookbacks: dict, mode: str) -> dict:
    windows = {}
    labels = []
    for lookback in LOOKBACKS:
        stats = lookbacks[str(lookback)][mode]["statistics"]["20d"]
        label = consensus_label(stats["up_probability"])
        labels.append(label)
        windows[str(lookback)] = {
            "signal": label,
            "up_probability_20d": stats["up_probability"],
            "median_return_20d": stats["median"],
        }
    if labels.count("bullish") >= 3:
        overall = "bullish"
    elif labels.count("bearish") >= 3:
        overall = "bearish"
    else:
        overall = "mixed"
    return {"overall": overall, "windows": windows}


def calculate_all(frame: pd.DataFrame, as_of_date: str | None = None) -> dict:
    frame_attrs = frame.attrs.copy()
    if as_of_date is not None:
        cutoff = pd.Timestamp(as_of_date)
        frame = frame.loc[frame["Date"] <= cutoff].copy()
        frame.reset_index(drop=True, inplace=True)
        frame.attrs.update(frame_attrs)
        if len(frame) < 260:
            raise RuntimeError(f"Not enough data on or before {as_of_date}.")

    prices = frame["Price"].to_numpy(dtype=float)
    current_price = prices[-1]
    current_ma200 = float(frame.iloc[-1]["MA200"])
    current_regime = market_regime(current_price, current_ma200)
    lookbacks: dict[str, dict] = {}

    for lookback in LOOKBACKS:
        current_prices = prices[-lookback:]
        current_normalized = normalize(current_prices)
        current_return_path = current_prices / current_prices[-1] - 1.0
        lookbacks[str(lookback)] = {
            "current_pattern": [as_float(value, 6) for value in current_normalized],
            "current_path": [as_float(value, 8) for value in current_return_path],
            "current_dates": [date.strftime("%Y-%m-%d") for date in frame["Date"].iloc[-lookback:]],
            "current_return": as_float(current_prices[-1] / current_prices[0] - 1.0),
            "all_regimes": calculate_mode(
                frame,
                prices,
                current_normalized,
                daily_returns(current_prices),
                current_regime,
                lookback,
                False,
            ),
            "same_regime": calculate_mode(
                frame,
                prices,
                current_normalized,
                daily_returns(current_prices),
                current_regime,
                lookback,
                True,
            ),
        }

    source_metadata: dict = {}
    if SOURCE_PATH.exists():
        source_metadata = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    data_source = source_metadata.get("source", "Unknown")
    csv_sha256 = source_metadata.get("csv_sha256")
    if csv_sha256 is None and INPUT_PATH.exists():
        csv_sha256 = hashlib.sha256(INPUT_PATH.read_bytes()).hexdigest()
    generated_at = datetime.now(timezone.utc).isoformat()

    return {
        "schema_version": SCHEMA_VERSION,
        "algorithm_version": ALGORITHM_VERSION,
        "ticker": "QQQ",
        "data_source": data_source,
        "data_provenance": {
            "source": data_source,
            "price_field": frame.attrs.get("price_column", source_metadata.get("price_field", "Unknown")),
            "price_field_note": source_metadata.get("price_field_note", ""),
            "adjustment": source_metadata.get("adjustment", "Unknown"),
            "start_date": frame.iloc[0]["Date"].strftime("%Y-%m-%d"),
            "end_date": frame.iloc[-1]["Date"].strftime("%Y-%m-%d"),
            "row_count": len(frame),
            "fetched_at": source_metadata.get("fetched_at"),
            "generated_at": generated_at,
            "csv_sha256": csv_sha256,
        },
        "generated_at": generated_at,
        "last_updated": frame.iloc[-1]["Date"].strftime("%Y-%m-%d"),
        "methodology": {
            "price_weight": PRICE_WEIGHT,
            "return_weight": RETURN_WEIGHT,
            "price_rmse_scale": PRICE_RMSE_SCALE,
            "return_rmse_scale": RETURN_RMSE_SCALE,
            "min_match_distance": MIN_MATCH_DISTANCE,
            "top_matches": TOP_MATCHES,
            "forward_days": FORWARD_DAYS,
            "similarity_formula": "0.70 * price_similarity + 0.30 * return_similarity",
            "score_transform": "100 * exp(-rmse / scale)",
        },
        "current": {
            "price": as_float(current_price, 4),
            "date": frame.iloc[-1]["Date"].strftime("%Y-%m-%d"),
            "market_regime": current_regime,
            "ma200": as_float(current_ma200, 4),
        },
        "lookbacks": lookbacks,
        "consensus": {
            mode: calculate_consensus(lookbacks, mode) for mode in ("all_regimes", "same_regime")
        },
    }


def print_debug(result: dict) -> None:
    current = result["current"]
    view = result["lookbacks"]["15"]["all_regimes"]
    print("QQQ Historical Analog")
    print(f"Current Date: {current['date']}")
    print(f"Current Price: {current['price']:.2f}")
    print(f"Current Regime: {current['market_regime'].title()}")
    print("\nLookback: 15D\n")
    print("Top Matches:")
    for match in view["matches"]:
        print(
            f"{match['rank']:>2}. {match['start_date']} to {match['end_date']}  "
            f"Similarity: {match['similarity']:.2f}%  20D: {match['returns']['20d']:+.2%}"
        )
    print("\nStatistics:")
    for horizon in FORWARD_HORIZONS:
        stats = view["statistics"][f"{horizon}d"]
        print(f"{horizon:>2}D Up Probability: {stats['up_probability']:.1%}")


def main() -> None:
    frame = load_prices()
    result = calculate_all(frame)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print_debug(result)
    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
