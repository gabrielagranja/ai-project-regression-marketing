"""Prediction utilities for trained revenue models."""

from pathlib import Path

import joblib
import pandas as pd

from src.config import MODEL_PATH


def load_model(model_path=None):
    """Load a trained revenue prediction model.

    Parameters
    ----------
    model_path : str or pathlib.Path, optional
        Path to a serialized sklearn-compatible model pipeline.
    """
    resolved_model_path = Path(model_path) if model_path is not None else MODEL_PATH

    if not resolved_model_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {resolved_model_path}")

    return joblib.load(resolved_model_path)


def save_model(model, model_path=None):
    """Persist a trained model pipeline for later prediction use."""
    resolved_model_path = Path(model_path) if model_path is not None else MODEL_PATH
    resolved_model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, resolved_model_path)
    return resolved_model_path


def predict_revenue(input_data, model=None):
    """Predict revenue for one or more rows of input features.

    `input_data` may be a pandas DataFrame, a dict representing one row, or a
    list of dicts. The loaded model is expected to be a fitted sklearn-compatible
    estimator or pipeline exposing `predict`.
    """
    if model is None:
        model = load_model()

    if isinstance(input_data, pd.DataFrame):
        features = input_data
    elif isinstance(input_data, dict):
        features = pd.DataFrame([input_data])
    else:
        features = pd.DataFrame(input_data)

    if features.empty:
        raise ValueError("Input data contains no rows to predict.")

    predictions = model.predict(features)
    return predictions
