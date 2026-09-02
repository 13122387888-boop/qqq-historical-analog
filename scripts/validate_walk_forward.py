"""Point-in-time audit proving that future rows cannot affect analog results."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import calculate_analogs as analogs


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "walk_forward_validation.json"
CHECKPOINTS = ("2010-12-31", "2015-12-31", "2020-12-31", "2024-12-31")


def result_signature(result: dict) -> str:
    """Keep only analysis values that must be identical after future rows are poisoned."""
    compact = {
        "current": result["current"],
        "lookbacks": {
            lookback: {
                "current_pattern": payload["current_pattern"],
                "all_regimes": payload["all_regimes"],
                "same_regime": payload["same_regime"],
            }
            for lookback, payload in result["lookbacks"].items()
        },
        "consensus": result["consensus"],
    }
    return json.dumps(compact, sort_keys=True, separators=(",", ":"))


def poison_future_rows(frame: pd.DataFrame, checkpoint: str) -> pd.DataFrame:
    poisoned = frame.copy()
    future_mask = poisoned["Date"] > pd.Timestamp(checkpoint)
    for column in ("Open", "High", "Low", "Close", "Adj Close", "Price", "MA200"):
        if column in poisoned:
            poisoned.loc[future_mask, column] = poisoned.loc[future_mask, column] * 37.0 + 9999.0
    poisoned.attrs.update(frame.attrs)
    return poisoned


def verify_match_cutoffs(result: dict, date_to_index: dict[str, int], as_of_index: int) -> None:
    for payload in result["lookbacks"].values():
        for mode in ("all_regimes", "same_regime"):
            for match in payload[mode]["matches"]:
                match_end_index = date_to_index[match["end_date"]]
                if match_end_index + analogs.FORWARD_DAYS > as_of_index:
                    raise AssertionError(
                        f"Match {match['end_date']} uses forward data beyond the as-of date."
                    )


def main() -> None:
    frame = analogs.load_prices()
    date_to_index = {
        date.strftime("%Y-%m-%d"): index for index, date in enumerate(frame["Date"])
    }
    reports = []

    for checkpoint in CHECKPOINTS:
        baseline = analogs.calculate_all(frame, as_of_date=checkpoint)
        poisoned = analogs.calculate_all(poison_future_rows(frame, checkpoint), as_of_date=checkpoint)
        if result_signature(baseline) != result_signature(poisoned):
            raise AssertionError(f"Future-row mutation changed the {checkpoint} result.")

        current_date = baseline["current"]["date"]
        as_of_index = date_to_index[current_date]
        verify_match_cutoffs(baseline, date_to_index, as_of_index)
        reports.append(
            {
                "requested_as_of_date": checkpoint,
                "effective_trading_date": current_date,
                "available_rows": baseline["data_provenance"]["row_count"],
                "future_mutation_invariant": True,
                "all_matches_have_known_30d_forward_data": True,
                "current_regime": baseline["current"]["market_regime"],
                "lookbacks": {
                    lookback: {
                        "top_match_end_date": payload["all_regimes"]["matches"][0]["end_date"],
                        "top_match_similarity": payload["all_regimes"]["matches"][0]["similarity"],
                        "up_probability_20d": payload["all_regimes"]["statistics"]["20d"]["up_probability"],
                    }
                    for lookback, payload in baseline["lookbacks"].items()
                },
            }
        )
        print(f"PASS {checkpoint} -> {current_date}: future rows cannot change the result")

    report = {
        "algorithm_version": analogs.ALGORITHM_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "passed",
        "checkpoints": reports,
    }
    OUTPUT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

