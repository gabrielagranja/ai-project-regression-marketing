"""Preprocessing utilities aligned with the modeling notebook workflow."""

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import EXCLUDED_COLUMNS, RANDOM_STATE, TARGET_COLUMN, TEST_SIZE


def prepare_features_and_target(data, target_column=TARGET_COLUMN, excluded_columns=None):
    """Create feature matrix and target vector from a raw dataset."""
    if target_column not in data.columns:
        raise ValueError(f"Target column `{target_column}` is not present in the data.")

    excluded = excluded_columns if excluded_columns is not None else EXCLUDED_COLUMNS
    columns_to_drop = [column for column in excluded if column in data.columns]

    features = data.drop(columns=columns_to_drop)
    target = data[target_column]

    return features, target


def identify_feature_types(features):
    """Return numerical and categorical feature column names."""
    numerical_features = features.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = features.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    return numerical_features, categorical_features


def build_preprocessor(numerical_features, categorical_features):
    """Build the sklearn preprocessing transformer used before modeling."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numerical_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )


def build_preprocessor_from_features(features):
    """Identify column types and return a fitted-ready preprocessing transformer."""
    numerical_features, categorical_features = identify_feature_types(features)
    preprocessor = build_preprocessor(numerical_features, categorical_features)

    return preprocessor, numerical_features, categorical_features


def split_features_target(
    features,
    target,
    *,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
):
    """Split feature matrix and target vector for model evaluation."""
    return train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
    )
