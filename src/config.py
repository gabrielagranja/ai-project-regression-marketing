"""Project configuration and reusable constants."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"

RAW_DATA_PATH = DATA_DIR / "digital_marketing_dataset_30k.csv"
MODEL_PATH = MODELS_DIR / "revenue_model.pkl"

TARGET_COLUMN = "revenue"
RANDOM_STATE = 42
TEST_SIZE = 0.20

EXCLUDED_COLUMNS = [
    TARGET_COLUMN,
    "date",
    "ad_id",
    "ad_name",
    "campaign_id",
    "campaign_name",
    "ad_group_id",
    "ad_group_name",
]

RF_PARAM_DISTRIBUTIONS = {
    "model__n_estimators": [100, 150],
    "model__max_depth": [10, 15, 20],
    "model__min_samples_split": [5, 10, 15],
    "model__min_samples_leaf": [2, 4, 6],
    "model__max_features": ["sqrt", "log2", 0.7],
}
