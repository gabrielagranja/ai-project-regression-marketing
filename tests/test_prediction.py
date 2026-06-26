import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.config import MODEL_PATH, PLANNING_TIME_FEATURES
from src.model import build_model_pipeline
from src.prediction import (
    load_model,
    predict_campaign_revenue,
    predict_revenue,
    prepare_prediction_input,
    save_model,
    validate_prediction_input,
)
from src.preprocessing import build_preprocessor_from_features


def make_campaign_data():
    return pd.DataFrame(
        {
            "month": [1, 2, 3, 4],
            "week": [1, 5, 9, 13],
            "day_of_week": ["Mon", "Tue", "Wed", "Thu"],
            "post_hour": [9, 12, 15, 18],
            "season": ["Winter", "Winter", "Spring", "Spring"],
            "is_holiday": [0, 0, 1, 0],
            "is_weekend": [0, 0, 0, 0],
            "country": ["KSA", "UAE", "Qatar", "KSA"],
            "market_tier": ["Tier 1", "Tier 1", "Tier 2", "Tier 1"],
            "account": ["A", "B", "C", "A"],
            "account_type": ["Brand", "Creator", "Brand", "Brand"],
            "platform": ["Meta", "TikTok", "Google Search", "Meta"],
            "placement": ["Feed", "In-Feed", "Search", "Stories"],
            "funnel_stage": [
                "Awareness",
                "Consideration",
                "Conversion",
                "Conversion",
            ],
            "objective": ["Reach", "Traffic", "Sales", "Leads"],
            "theme": ["Promo", "Seasonal", "Launch", "Promo"],
            "spend": [100.0, 250.0, 500.0, 350.0],
            "clicks": [100, 250, 700, 450],
            "conversions": [0, 2, 30, 12],
        }
    )


def make_forecast_pipeline():
    data = make_campaign_data()
    features = data.loc[:, PLANNING_TIME_FEATURES]
    target = pd.Series([0.0, 120.0, 2500.0, 900.0], name="revenue")
    preprocessor, _, _ = build_preprocessor_from_features(features)
    pipeline = build_model_pipeline(
        preprocessor,
        RandomForestRegressor(n_estimators=5, random_state=42),
    )
    return pipeline.fit(features, target)


class PredictionApiTests(unittest.TestCase):
    def test_save_model_and_load_model(self):
        model = make_forecast_pipeline()

        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / MODEL_PATH.name
            saved_path = save_model(model, model_path=model_path)
            loaded_model = load_model(model_path=model_path)

        self.assertEqual(saved_path, model_path)
        self.assertTrue(hasattr(loaded_model, "predict"))

    def test_valid_prediction_returns_numpy_array_with_input_length(self):
        model = make_forecast_pipeline()
        data = make_campaign_data().head(3)

        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = Path(temp_dir) / MODEL_PATH.name
            save_model(model, model_path=model_path)
            predictions = predict_campaign_revenue(data, model_path=model_path)

        self.assertIsInstance(predictions, np.ndarray)
        self.assertEqual(len(predictions), len(data))
        self.assertTrue(np.isfinite(predictions).all())

    def test_invalid_input_type_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Input must be a pandas DataFrame"):
            validate_prediction_input({"spend": 100.0})

    def test_missing_required_columns_raise_value_error(self):
        data = make_campaign_data().drop(columns=["spend", "theme"])

        with self.assertRaisesRegex(
            ValueError,
            "Missing required planning-time feature",
        ):
            prepare_prediction_input(data)

    def test_prepare_prediction_input_selects_only_planning_features(self):
        data = make_campaign_data()

        prepared = prepare_prediction_input(data)

        self.assertEqual(prepared.columns.tolist(), PLANNING_TIME_FEATURES)
        self.assertNotIn("clicks", prepared.columns)
        self.assertNotIn("conversions", prepared.columns)
        
    def test_legacy_predict_revenue_accepts_dict_input(self):
        model = make_forecast_pipeline()
        data = make_campaign_data().iloc[0].to_dict()

        predictions = predict_revenue(data, model=model)

        self.assertIsInstance(predictions, np.ndarray)
        self.assertEqual(len(predictions), 1)
        self.assertTrue(np.isfinite(predictions).all())


if __name__ == "__main__":
    unittest.main()
