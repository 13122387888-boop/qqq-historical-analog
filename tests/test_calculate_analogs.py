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
import backtest_walk_forward as backtest  # noqa: E402
import optimize_similarity_v2 as optimizer  # noqa: E402


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

    def test_backtest_selection_matches_v1_separation_rule(self) -> None:
        scores = np.arange(25.0, 0.0, -1.0)
        end_indices = 100 + np.arange(25) * 21
        positions = backtest.select_match_positions(scores, end_indices)
        self.assertEqual(positions.tolist(), list(range(analogs.TOP_MATCHES)))


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

    def test_predictive_backtest_contract(self) -> None:
        report_path = PROJECT_ROOT / "data" / "backtest.json"
        self.assertTrue(report_path.exists())
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "completed")
        self.assertEqual(report["algorithm_version"], analogs.ALGORITHM_VERSION)
        self.assertEqual(report["setup"]["known_outcome_lag_days"], analogs.FORWARD_DAYS)
        for lookback in analogs.LOOKBACKS:
            for mode in ("all_regimes", "same_regime"):
                for horizon in analogs.FORWARD_HORIZONS:
                    result = report["results"][str(lookback)][mode][f"{horizon}d"]
                    for period in ("walk_forward", "development", "holdout"):
                        metrics = result[period]
                        self.assertGreater(metrics["sample_count"], 0)
                        self.assertGreaterEqual(metrics["analog_brier"], 0)
                        self.assertLessEqual(metrics["analog_brier"], 1)
                        self.assertIn(
                            metrics["verdict"],
                            ("validated_edge", "promising_not_conclusive", "no_observed_edge"),
                        )

    def test_v2_optimisation_contract(self) -> None:
        report_path = PROJECT_ROOT / "data" / "v2_model.json"
        self.assertTrue(report_path.exists())
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "completed")
        self.assertEqual(report["model_version"], optimizer.MODEL_VERSION)
        self.assertTrue(report["selection_policy"]["holdout_not_used_for_selection"])
        for lookback in analogs.LOOKBACKS:
            for mode in ("all_regimes", "same_regime"):
                selection = report["selections"][str(lookback)][mode]
                champion = selection["champion"]
                self.assertIn(champion["top_k"], optimizer.TOP_K_VALUES)
                self.assertIn(champion["kernel"], {item[0] for item in optimizer.KERNELS})
                current = selection["current_forecast"]
                self.assertEqual(len(current["selected_matches"]), champion["top_k"])
                self.assertAlmostEqual(
                    sum(match["analysis_weight"] for match in current["selected_matches"]),
                    1.0,
                    places=6,
                )
                self.assertEqual(
                    len(current["display_view"]["forward_distribution"]),
                    analogs.FORWARD_DAYS + 1,
                )
                for horizon in analogs.FORWARD_HORIZONS:
                    forecast = current["horizons"][f"{horizon}d"]
                    self.assertGreaterEqual(forecast["calibrated_probability"], 0)
                    self.assertLessEqual(forecast["calibrated_probability"], 1)
                    self.assertIn(forecast["analog_evidence_weight"], optimizer.ALPHAS)
                    holdout = selection["backtest"][f"{horizon}d"]["holdout"]
                    self.assertGreater(holdout["sample_count"], 0)

    def test_ui_requires_validated_holdout_edge_for_directional_labels(self) -> None:
        app_source = (PROJECT_ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn(
            'selection.backtest?.["20d"]?.holdout?.verdict === "validated_edge"',
            app_source,
        )
        self.assertIn('signal_inconclusive: "Inconclusive"', app_source)


if __name__ == "__main__":
    unittest.main()
