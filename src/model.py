"""Model construction and training utilities."""

import time

import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from src.config import RANDOM_STATE, RF_PARAM_DISTRIBUTIONS
from src.evaluation import evaluate_regression


def get_model_candidates(random_state=RANDOM_STATE):
    """Return the regression models compared in the modeling notebook."""
    return {
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(random_state=random_state),
        "Lasso": Lasso(random_state=random_state),
        "ElasticNet": ElasticNet(random_state=random_state),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=random_state,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(random_state=random_state),
    }


def build_model_pipeline(preprocessor, model):
    """Combine preprocessing and estimator steps into one sklearn pipeline."""
    return Pipeline(
        steps=[
            ("preprocessor", clone(preprocessor)),
            ("model", clone(model)),
        ]
    )


def train_model(model_pipeline, features_train, target_train):
    """Fit and return a model pipeline."""
    return model_pipeline.fit(features_train, target_train)


def compare_models(
    preprocessor,
    features_train,
    features_test,
    target_train,
    target_test,
    models=None,
):
    """Train candidate models and return a metrics table sorted by RMSE."""
    candidate_models = models if models is not None else get_model_candidates()
    results = []
    fitted_models = {}

    for model_name, estimator in candidate_models.items():
        pipeline = build_model_pipeline(preprocessor, estimator)
        pipeline.fit(features_train, target_train)
        predictions = pipeline.predict(features_test)
        metrics = evaluate_regression(target_test, predictions)
        metrics["Model"] = model_name
        results.append(metrics)
        fitted_models[model_name] = pipeline

    results_df = pd.DataFrame(results)
    metric_columns = ["Model", "MAE", "MSE", "RMSE", "R2"]
    results_df = results_df[metric_columns].sort_values("RMSE").reset_index(drop=True)

    return results_df, fitted_models


def build_random_forest_pipeline(preprocessor, random_state=RANDOM_STATE, **model_kwargs):
    """Build the Random Forest pipeline used as the project baseline final model."""
    estimator = RandomForestRegressor(
        n_estimators=model_kwargs.pop("n_estimators", 100),
        random_state=random_state,
        n_jobs=model_kwargs.pop("n_jobs", -1),
        **model_kwargs,
    )

    return build_model_pipeline(preprocessor, estimator)


def optimize_random_forest(
    preprocessor,
    features_train,
    target_train,
    *,
    param_distributions=None,
    n_iter=10,
    cv=2,
    scoring="neg_root_mean_squared_error",
    random_state=RANDOM_STATE,
    n_jobs=-1,
    verbose=0,
):
    """Run the RandomizedSearchCV optimization from the modeling workflow."""
    pipeline = build_random_forest_pipeline(preprocessor, random_state=random_state)
    search_space = param_distributions or RF_PARAM_DISTRIBUTIONS

    random_search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=search_space,
        n_iter=n_iter,
        scoring=scoring,
        cv=cv,
        random_state=random_state,
        n_jobs=n_jobs,
        verbose=verbose,
    )

    start_time = time.perf_counter()
    random_search.fit(features_train, target_train)
    optimization_time = time.perf_counter() - start_time

    return random_search, optimization_time
