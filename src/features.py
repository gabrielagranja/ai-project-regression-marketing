"""Feature reporting utilities for trained sklearn pipelines."""

import pandas as pd


def get_transformed_feature_names(model_pipeline, preprocessor_step="preprocessor"):
    """Return feature names produced by the preprocessing step of a pipeline."""
    preprocessor = model_pipeline.named_steps.get(preprocessor_step)
    if preprocessor is None:
        raise ValueError(f"Pipeline does not contain a `{preprocessor_step}` step.")

    if not hasattr(preprocessor, "get_feature_names_out"):
        raise TypeError("The preprocessor does not expose get_feature_names_out().")

    return preprocessor.get_feature_names_out()


def get_feature_importance(
    model_pipeline,
    *,
    preprocessor_step="preprocessor",
    model_step="model",
):
    """Create a feature importance table from a fitted tree-based pipeline."""
    model = model_pipeline.named_steps.get(model_step)
    if model is None:
        raise ValueError(f"Pipeline does not contain a `{model_step}` step.")

    if not hasattr(model, "feature_importances_"):
        raise TypeError("The model does not expose feature_importances_.")

    feature_names = get_transformed_feature_names(
        model_pipeline,
        preprocessor_step=preprocessor_step,
    )

    importance = pd.DataFrame(
        {
            "Feature": feature_names,
            "Importance": model.feature_importances_,
        }
    )

    importance = importance.sort_values("Importance", ascending=False).reset_index(
        drop=True
    )
    importance["Cumulative Importance"] = importance["Importance"].cumsum()

    return importance
