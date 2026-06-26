"""Prediction utilities for trained pre-launch revenue forecast models."""

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from src.config import MODEL_PATH, PLANNING_TIME_FEATURES


def resolve_model_path(model_path: Path | str | None = None) -> Path:
    """Return the configured model path or a caller-provided path."""
    return Path(model_path) if model_path is not None else MODEL_PATH


def load_model(model_path: Path | str | None = None) -> Any:
    """Load a trained revenue forecast model.

    Parameters
    ----------
    model_path : str or pathlib.Path, optional
        Path to a serialized sklearn-compatible model pipeline.
    """
    resolved_model_path = resolve_model_path(model_path)

    if not resolved_model_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {resolved_model_path}")

    return joblib.load(resolved_model_path)


def save_model(model: Any, model_path: Path | str | None = None) -> Path:
    """Persist a trained forecast pipeline for later inference."""
    resolved_model_path = resolve_model_path(model_path)
    resolved_model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, resolved_model_path)
    return resolved_model_path


def validate_prediction_input(data: pd.DataFrame) -> None:
    """Validate that prediction input contains all planning-time features."""
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if data.empty:
        raise ValueError("Input data contains no rows to predict.")

    missing_features = [
        feature for feature in PLANNING_TIME_FEATURES if feature not in data.columns
    ]

    if missing_features:
        raise ValueError(
            "Missing required planning-time feature(s): "
            + ", ".join(missing_features)
        )


def prepare_prediction_input(data: pd.DataFrame) -> pd.DataFrame:
    """Return input data restricted to the configured planning-time features."""
    validate_prediction_input(data)
    return data.loc[:, PLANNING_TIME_FEATURES].copy()


def predict_campaign_revenue(
    data: pd.DataFrame,
    model_path: Path | str | None = None,
) -> np.ndarray:
    """Forecast campaign revenue from planning-time campaign inputs.

    This is the public inference API for application code. It loads the persisted
    forecast pipeline, validates the input schema, selects only planning-time
    features, and returns predictions as a NumPy array.
    """
    features = prepare_prediction_input(data)
    model = load_model(model_path=model_path)
    predictions = model.predict(features)

    return np.asarray(predictions)


def predict_revenue(input_data, model=None):
    """Forecast revenue using the legacy prediction helper.

    Prefer `predict_campaign_revenue` for new application code. This function is
    kept for backward compatibility with existing tests and callers that provide
    dict-like or DataFrame campaign inputs.
    """
    if isinstance(input_data, pd.DataFrame):
        data = input_data
    elif isinstance(input_data, dict):
        data = pd.DataFrame([input_data])
    else:
        raise ValueError("Input must be a pandas DataFrame or a dictionary.")

    if model is not None:
        features = prepare_prediction_input(data)
        return np.asarray(model.predict(features))

    return predict_campaign_revenue(data)
