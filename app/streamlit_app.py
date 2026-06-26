"""Streamlit app for pre-launch campaign revenue forecasting."""

import math
from pathlib import Path
import sys

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import PLANNING_TIME_FEATURES, RAW_DATA_PATH
from src.prediction import predict_campaign_revenue


DEFAULT_INPUTS = {
    "month": 6,
    "week": 24,
    "day_of_week": "Mon",
    "post_hour": 12,
    "season": "Summer",
    "is_holiday": False,
    "is_weekend": False,
    "country": "KSA",
    "market_tier": "Tier 1",
    "account": "Ecom_FashionCo",
    "account_type": "Brand",
    "platform": "Meta",
    "placement": "Feed",
    "funnel_stage": "Conversion",
    "objective": "Sales",
    "theme": "Promo",
    "spend": 1000.0,
}

FALLBACK_OPTIONS = {
    "day_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "season": ["Winter", "Spring", "Summer", "Fall"],
    "country": [
        "KSA",
        "United Arab Emirates",
        "Qatar",
        "Kuwait",
        "Bahrain",
        "Oman",
        "Egypt",
        "Jordan",
        "Lebanon",
        "Morocco",
        "Iraq",
        "Yemen",
    ],
    "market_tier": ["Tier 1", "Tier 2", "Tier 3"],
    "account": [
        "B2B_SaaSCloud",
        "Ecom_ElectroHub",
        "Ecom_FashionCo",
        "Education_Academy",
        "FMCG_Foodies",
        "Fintech_AppX",
        "Travel_SkyTrip",
    ],
    "account_type": ["Brand", "Creator"],
    "platform": [
        "Meta",
        "TikTok",
        "Google Search",
        "Google Display",
        "LinkedIn",
        "Snapchat",
    ],
    "placement": [
        "Feed",
        "Stories",
        "Reels",
        "In-Feed",
        "Spark",
        "Search",
        "Display",
        "YouTube",
        "PMax",
        "Message Ads",
        "Spotlight",
    ],
    "funnel_stage": ["Awareness", "Consideration", "Conversion"],
    "objective": ["Reach", "Traffic", "Sales", "Leads", "Engagement", "Video Views"],
    "theme": [
        "Promo",
        "Seasonal",
        "Product Launch",
        "Brand Story",
        "Educational",
        "Influencer",
        "Retargeting",
        "UGC",
    ],
}


@st.cache_data(show_spinner=False)
def load_planning_options() -> dict[str, list[str]]:
    """Load categorical choices from the local dataset when it is available."""
    if not RAW_DATA_PATH.exists():
        return FALLBACK_OPTIONS

    data = pd.read_csv(RAW_DATA_PATH, usecols=PLANNING_TIME_FEATURES)
    options = FALLBACK_OPTIONS.copy()

    for feature in FALLBACK_OPTIONS:
        if feature in data.columns:
            values = data[feature].dropna().astype(str).sort_values().unique().tolist()
            if values:
                options[feature] = values

    return options


def build_input_dataframe(inputs: dict[str, object]) -> pd.DataFrame:
    """Create a one-row DataFrame in the exact planning-time feature order."""
    ordered_inputs = {feature: inputs[feature] for feature in PLANNING_TIME_FEATURES}
    return pd.DataFrame([ordered_inputs])


def initialize_form_state(options: dict[str, list[str]]) -> None:
    """Set initial widget values while respecting available selectbox options."""
    for feature, default in DEFAULT_INPUTS.items():
        if feature not in st.session_state:
            if feature in options and default not in options[feature]:
                st.session_state[feature] = options[feature][0]
            else:
                st.session_state[feature] = default


def reset_form(options: dict[str, list[str]]) -> None:
    """Restore form widgets to sensible defaults."""
    for feature, default in DEFAULT_INPUTS.items():
        if feature in options and default not in options[feature]:
            st.session_state[feature] = options[feature][0]
        else:
            st.session_state[feature] = default

    st.session_state.pop("latest_prediction", None)
    st.session_state.pop("latest_input_dataframe", None)


def validate_campaign_inputs(inputs: dict[str, object]) -> list[str]:
    """Return user-friendly validation messages for campaign planning inputs."""
    errors = []

    if not 1 <= int(inputs["month"]) <= 12:
        errors.append("Month must be between 1 and 12.")
    if not 1 <= int(inputs["week"]) <= 53:
        errors.append("Week must be between 1 and 53.")
    if not 0 <= int(inputs["post_hour"]) <= 23:
        errors.append("Post hour must be between 0 and 23.")
    if not math.isfinite(float(inputs["spend"])):
        errors.append("Planned spend must be a valid number.")
    elif float(inputs["spend"]) < 0:
        errors.append("Planned spend cannot be negative.")

    return errors


st.set_page_config(
    page_title="Campaign Revenue Forecaster",
    layout="centered",
)

options = load_planning_options()
initialize_form_state(options)

st.title("Revenue Forecast")
st.caption("Plan a campaign and estimate expected revenue before launch.")

header_left, header_right = st.columns([3, 1])
with header_left:
    st.write("Enter the campaign setup below, then generate a forecast.")
with header_right:
    if st.button("Reset form", use_container_width=True):
        reset_form(options)
        st.rerun()

st.divider()

with st.form("campaign_forecast_form"):
    st.subheader("Campaign details")

    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown("#### Timing")
        st.slider(
            "Month",
            min_value=1,
            max_value=12,
            step=1,
            key="month",
            help="Calendar month planned for the campaign launch.",
        )
        st.slider(
            "Week",
            min_value=1,
            max_value=53,
            step=1,
            key="week",
            help="Calendar week planned for the campaign launch.",
        )
        st.selectbox(
            "Day of week",
            options["day_of_week"],
            key="day_of_week",
            help="Planned day for the campaign post or launch.",
        )
        st.slider(
            "Post hour",
            min_value=0,
            max_value=23,
            step=1,
            key="post_hour",
            help="Hour of day in 24-hour format.",
        )
        st.selectbox(
            "Season",
            options["season"],
            key="season",
            help="Season associated with the planned launch date.",
        )

        st.markdown("#### Budget")
        st.number_input(
            "Planned spend",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="spend",
            help="Planned media spend for the campaign.",
        )

    with right_col:
        st.markdown("#### Market")
        st.selectbox(
            "Country",
            options["country"],
            key="country",
            help="Primary market for the campaign.",
        )
        st.selectbox(
            "Market tier",
            options["market_tier"],
            key="market_tier",
            help="Market priority tier used during planning.",
        )
        st.selectbox(
            "Account",
            options["account"],
            key="account",
            help="Account or client profile for the campaign.",
        )
        st.selectbox(
            "Account type",
            options["account_type"],
            key="account_type",
            help="Type of account running the campaign.",
        )

        st.markdown("#### Channel and strategy")
        st.selectbox(
            "Platform",
            options["platform"],
            key="platform",
            help="Digital platform selected for the campaign.",
        )
        st.selectbox(
            "Placement",
            options["placement"],
            key="placement",
            help="Ad placement or inventory type.",
        )
        st.selectbox(
            "Funnel stage",
            options["funnel_stage"],
            key="funnel_stage",
            help="Marketing funnel stage targeted by the campaign.",
        )
        st.selectbox(
            "Objective",
            options["objective"],
            key="objective",
            help="Primary campaign objective.",
        )
        st.selectbox(
            "Theme",
            options["theme"],
            key="theme",
            help="Creative or messaging theme.",
        )

    st.markdown("#### Calendar flags")
    flag_col_1, flag_col_2 = st.columns(2)
    with flag_col_1:
        st.checkbox(
            "Holiday",
            key="is_holiday",
            help="Select if the campaign launches on or around a holiday.",
        )
    with flag_col_2:
        st.checkbox(
            "Weekend",
            key="is_weekend",
            help="Select if the campaign launches on a weekend.",
        )

    submitted = st.form_submit_button("Predict Revenue", type="primary")

if submitted:
    campaign_inputs = {
        "month": int(st.session_state["month"]),
        "week": int(st.session_state["week"]),
        "day_of_week": st.session_state["day_of_week"],
        "post_hour": int(st.session_state["post_hour"]),
        "season": st.session_state["season"],
        "is_holiday": int(st.session_state["is_holiday"]),
        "is_weekend": int(st.session_state["is_weekend"]),
        "country": st.session_state["country"],
        "market_tier": st.session_state["market_tier"],
        "account": st.session_state["account"],
        "account_type": st.session_state["account_type"],
        "platform": st.session_state["platform"],
        "placement": st.session_state["placement"],
        "funnel_stage": st.session_state["funnel_stage"],
        "objective": st.session_state["objective"],
        "theme": st.session_state["theme"],
        "spend": float(st.session_state["spend"]),
    }

    validation_errors = validate_campaign_inputs(campaign_inputs)
    if validation_errors:
        st.session_state.pop("latest_prediction", None)
        st.session_state.pop("latest_input_dataframe", None)
        for validation_error in validation_errors:
            st.error(validation_error)
    else:
        try:
            input_dataframe = build_input_dataframe(campaign_inputs)
            prediction = predict_campaign_revenue(input_dataframe)[0]
        except FileNotFoundError:
            st.session_state.pop("latest_prediction", None)
            st.session_state.pop("latest_input_dataframe", None)
            st.error(
                "The forecast model is not available yet. "
                "Train or add the saved model first."
            )
        except ValueError as error:
            st.session_state.pop("latest_prediction", None)
            st.session_state.pop("latest_input_dataframe", None)
            st.error(f"Please review the campaign inputs. {error}")
        except Exception as error:
            st.session_state.pop("latest_prediction", None)
            st.session_state.pop("latest_input_dataframe", None)
            st.error(f"Forecast could not be generated. Details: {error}")
        else:
            st.session_state["latest_prediction"] = prediction
            st.session_state["latest_input_dataframe"] = input_dataframe

if "latest_prediction" in st.session_state:
    st.divider()
    st.subheader("Forecast")
    st.success("Revenue forecast ready.")

    metric_col, note_col = st.columns([2, 1])
    with metric_col:
        with st.container(border=True):
            st.metric(
                "Predicted revenue",
                f"${st.session_state['latest_prediction']:,.2f}",
            )
    with note_col:
        with st.container(border=True):
            st.metric(
                "Planned spend",
                f"${st.session_state['latest_input_dataframe']['spend'].iloc[0]:,.2f}",
            )
            st.caption("Use the forecast to compare campaign plans before launch.")

    with st.expander("Debug information", expanded=False):
        st.dataframe(
            st.session_state["latest_input_dataframe"],
            hide_index=True,
            use_container_width=True,
        )
