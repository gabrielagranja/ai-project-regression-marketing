"""Evaluation utilities for regression models."""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_regression(y_true, y_pred):
    """Return common regression metrics for revenue prediction."""
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    return {
        "MAE": float(mae),
        "MSE": float(mse),
        "RMSE": float(rmse),
        "R2": float(r2),
    }


def regression_metrics_frame(y_true, y_pred, model_name=None):
    """Return regression metrics as a one-row DataFrame."""
    metrics = evaluate_regression(y_true, y_pred)

    if model_name is not None:
        metrics = {"Model": model_name, **metrics}

    return pd.DataFrame([metrics])


def calculate_residuals(y_true, y_pred):
    """Calculate residuals as actual revenue minus predicted revenue."""
    return np.asarray(y_true) - np.asarray(y_pred)


def overfitting_summary(model, features_train, target_train, features_test, target_test):
    """Compare train and test R2 scores for a fitted model."""
    train_predictions = model.predict(features_train)
    test_predictions = model.predict(features_test)

    train_r2 = r2_score(target_train, train_predictions)
    test_r2 = r2_score(target_test, test_predictions)
    gap = train_r2 - test_r2

    return pd.DataFrame(
        [
            {"Metric": "Training R2", "Value": train_r2},
            {"Metric": "Testing R2", "Value": test_r2},
            {"Metric": "Overfitting Gap", "Value": gap},
            {"Metric": "Overfitting Gap (%)", "Value": gap * 100},
        ]
    )
