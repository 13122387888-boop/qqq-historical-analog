from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import calculate_analogs as analogs  # noqa: E402


class AlgorithmTests(unittest.TestCase):
    def test_normalize_rebases_first_price_to_100(self) -> None:
        values = analogs.normalize(np.array([400.0, 404.0, 402.0, 410.0]))
        np.testing.assert_allclose(values, [100.0, 101.0, 100.5, 102.5])

    def test_similarity_does_not_read_forward_prices(self) -> None:
        length = 280
        dates = pd.bdate_range("2020-01-01", periods=length)
        prices = 100 + np.linspace(0, 30, length) + np.sin(np.arange(length) / 4)
        frame = pd.DataFrame({"Date": dates, "MA200": np.full(length, 95.0)})
        lookback = 15
        end_index = 220
        current_prices = prices[-lookback:].copy()
        current_normalized = analogs.normalize(current_prices)
        current_returns = analogs.daily_returns(current_prices)

        before = analogs.build_candidate(
            frame, prices.copy(), current_normalized, current_returns, lookback, end_index
        )
        mutated = prices.copy()
        mutated[end_index + 1 :] *= 7.0
        after = analogs.build_candidate(
            frame, mutated, current_normalized, current_returns, lookback, end_index
        )

        self.assertEqual(before["similarity"], after["similarity"])
        self.assertEqual(before["price_rmse"], after["price_rmse"])
        self.assertEqual(before["return_rmse"], after["return_rmse"])

    def test_match_deduplication_uses_trading_day_distance(self) -> None:
        candidates = [
            {"end_index": 100, "similarity": 99.0},
            {"end_index": 105, "similarity": 98.0},
            {"end_index": 121, "similarity": 97.0},
            {"end_index": 142, "similarity": 96.0},
        ]
        selected = analogs.select_independent_matches(candidates)
        self.assertEqual([item["end_index"] for item in selected], [100, 121, 142])


class GeneratedOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads((PROJECT_ROOT / "data" / "analogs.json").read_text(encoding="utf-8"))
        cls.prices = pd.read_csv(PROJECT_ROOT / "data" / "qqq.csv")
        cls.date_to_index = {date: index for index, date in enumerate(cls.prices["Date"])}

    def test_every_view_has_independent_complete_matches(self) -> None:
        for lookback in analogs.LOOKBACKS:
            lookback_data = self.payload["lookbacks"][str(lookback)]
            self.assertEqual(len(lookback_data["current_pattern"]), lookback)
            for mode in ("all_regimes", "same_regime"):
                matches = lookback_data[mode]["matches"]
                self.assertEqual(len(matches), analogs.TOP_MATCHES)
                indices = [self.date_to_index[match["end_date"]] for match in matches]
                for position, left in enumerate(indices):
                    self.assertTrue(all(abs(left - right) > analogs.MIN_MATCH_DISTANCE for right in indices[position + 1 :]))
                for match in matches:
                    self.assertEqual(len(match["pattern"]), lookback)
                    self.assertEqual(len(match["forward_path"]), analogs.FORWARD_DAYS + 1)
                    self.assertLessEqual(self.date_to_index[match["end_date"]] + analogs.FORWARD_DAYS, len(self.prices) - 1)

    def test_consensus_contains_all_windows(self) -> None:
        for mode in ("all_regimes", "same_regime"):
            self.assertEqual(set(self.payload["consensus"][mode]["windows"]), {"10", "15", "20", "30"})

    def test_data_provenance_matches_csv(self) -> None:
        csv_path = PROJECT_ROOT / "data" / "qqq.csv"
        provenance = self.payload["data_provenance"]
        self.assertEqual(self.payload["schema_version"], analogs.SCHEMA_VERSION)
        self.assertEqual(self.payload["algorithm_version"], analogs.ALGORITHM_VERSION)
        self.assertEqual(provenance["row_count"], len(self.prices))
        self.assertEqual(provenance["start_date"], self.prices.iloc[0]["Date"])
        self.assertEqual(provenance["end_date"], self.prices.iloc[-1]["Date"])
        self.assertEqual(provenance["csv_sha256"], hashlib.sha256(csv_path.read_bytes()).hexdigest())

    def test_walk_forward_validation_passed(self) -> None:
        report_path = PROJECT_ROOT / "data" / "walk_forward_validation.json"
        self.assertTrue(report_path.exists())
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "passed")
        self.assertEqual(len(report["checkpoints"]), 4)
        for checkpoint in report["checkpoints"]:
            self.assertTrue(checkpoint["future_mutation_invariant"])
            self.assertTrue(checkpoint["all_matches_have_known_30d_forward_data"])


if __name__ == "__main__":
    unittest.main()
