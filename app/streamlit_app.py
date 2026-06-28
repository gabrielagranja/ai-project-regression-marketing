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
    "country": "Spain",
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
       "Spain",
        "Portugal",
        "France",
        "Italy",
        "Germany",
        "Netherlands",
        "Belgium",
        "United Kingdom",
        "Ireland",
        "Switzerland",
        "United States",
        "Canada",
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

USE_DATASET_OPTIONS = False

@st.cache_data(show_spinner=False)
def load_planning_options() -> dict[str, list[str]]:
    """Load categorical choices from the local dataset when it is available."""

    if not USE_DATASET_OPTIONS:
        return FALLBACK_OPTIONS

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
    page_title="Predictor Inteligente de Campañas de Marketing",
    layout="centered",
)

st.markdown(
    """
    Complete los datos principales de la campaña y pulse **Calcular predicción**.

    La predicción debe interpretarse como una estimación orientativa para apoyar la toma
    de decisiones, no como un resultado garantizado.
    """
)
options = load_planning_options()
initialize_form_state(options)

st.title("Predictor Inteligente de Campañas de Marketing")
st.caption("Herramienta de apoyo para estimar los ingresos potenciales de una campaña antes de invertir presupuesto publicitario.")

header_left, header_right = st.columns([3, 1])
with header_left:
    st.write("Complete la confirguración de la campaña a continuación y luego genere una pronóstico de ingresos antes del lanzamiento.")
with header_right:
    if st.button("Reestablecer formulario", use_container_width=True):
        reset_form(options)
        st.rerun()

st.divider()

with st.form("campaign_forecast_form"):
    st.subheader("Configuración de la campaña")

    left_col, right_col = st.columns(2, gap="large")

    with left_col:
        st.markdown("#### Calendario")
        st.slider(
            "Mes",
            min_value=1,
            max_value=12,
            step=1,
            key="month",
            help="Mes previsto de la campaña.",
        )
        st.slider(
            "Semana",
            min_value=1,
            max_value=53,
            step=1,
            key="week",
            help="Semana del calendario planificada para el lanzamiento de la campaña.",
        )
        st.selectbox(
            "Día de la semana",
            options["day_of_week"],
            key="day_of_week",
            help="Día planificado para la publicación o lanzamiento de la campaña.",
        )
        st.slider(
            "Hora de publicación",
            min_value=0,
            max_value=23,
            step=1,
            key="post_hour",
            help="Hora del día en formato de 24 horas.",
        )
        st.selectbox(
            "Estación",
            options["season"],
            key="season",
            help="Estación asociada con la fecha de lanzamiento planificada.",
        )

        st.markdown("#### Budget")
        st.number_input(
            "Gasto planificado",
            min_value=0.0,
            step=100.0,
            format="%.2f",
            key="spend",
            help="Gasto planificado en medios para la campaña.",
        )

    with right_col:
        st.markdown("#### Mercado y cuenta")
        st.selectbox(
            "País",
            options["country"],
            key="country",
            help="Mercado principal para la campaña.",
        )
        st.selectbox(
            "Nivel de mercado",
            options["market_tier"],
            key="market_tier",
            help="Nivel de prioridad del mercado utilizado durante la planificación.",
        )
        st.selectbox(
            "Cuenta",
            options["account"],
            key="account",
            help="Cuenta o perfil de cliente para la campaña.",
        )
        st.selectbox(
            "Tipo de cuenta",
            options["account_type"],
            key="account_type",
            help="Tipo de cuenta que ejecuta la campaña.",
        )

        st.markdown("#### Canal y creatividad")
        st.selectbox(
            "Plataforma digital",
            options["platform"],
            key="platform",
            help="Plataforma digital seleccionada para la campaña.",
        )
        st.selectbox(
            "Ubicación del anuncio",
            options["placement"],
            key="placement",
            help="Ubicación del anuncio o tipo de inventario.",
        )
        st.selectbox(
            "Etapa del embudo",
            options["funnel_stage"],
            key="funnel_stage",
            help="Etapa del embudo de marketing apuntada por la campaña.",
        )
        st.selectbox(
            "Objetivo",
            options["objective"],
            key="objective",
            help="Objetivo principal de la campaña.",
        )
        st.selectbox(
            "Creatividad o tema del mensaje",
            options["theme"],
            key="theme",
            help="Tema creativo o de mensaje.",
        )

    st.markdown("#### Consideraciones de tiempo")
    flag_col_1, flag_col_2 = st.columns(2)
    with flag_col_1:
        st.checkbox(
            "Fiesta",
            key="is_holiday",
            help="Seleccionar si la campaña se lanza en o alrededor de un feriado.",
        )
    with flag_col_2:
        st.checkbox(
            "Fin de semana",
            key="is_weekend",
            help="Seleccionar si la campaña se lanza en un fin de semana.",
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
                "El modelo de pronóstico no está disponible aún. "
                "Entrena o agrega el modelo guardado primero."
            )
        except ValueError as error:
            st.session_state.pop("latest_prediction", None)
            st.session_state.pop("latest_input_dataframe", None)
            st.error(f"Por favor, revise los inputs de la campaña. {error}")
        except Exception as error:
            st.session_state.pop("latest_prediction", None)
            st.session_state.pop("latest_input_dataframe", None)
            st.error(f"No se pudo generar el pronóstico. Detalles: {error}")
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
                "Ingresos pronosticados",
                f"${st.session_state['latest_prediction']:,.2f}",
            )
    with note_col:
        with st.container(border=True):
            st.metric(
                "Gasto planeado",
                f"${st.session_state['latest_input_dataframe']['spend'].iloc[0]:,.2f}",
            )
            st.caption("Use the forecast to compare campaign plans before launch.")
    with st.expander("Resumen de la campaña", expanded=False):

        datos = st.session_state["latest_input_dataframe"].iloc[0]

    st.markdown("### Calendario")
    st.write(f"Mes: {datos['month']}")
    st.write(f"Semana: {datos['week']}")
    st.write(f"Día: {datos['day_of_week']}")
    st.write(f"Hora de publicación: {datos['post_hour']}:00")

    st.markdown("### Mercado")
    st.write(f"País: {datos['country']}")
    st.write(f"Nivel de mercado: {datos['market_tier']}")

    st.markdown("### Campaña")
    st.write(f"Cuenta: {datos['account']}")
    st.write(f"Tipo de cuenta: {datos['account_type']}")
    st.write(f"Plataforma: {datos['platform']}")
    st.write(f"Ubicación: {datos['placement']}")

    st.markdown("### Estrategia")
    st.write(f"Objetivo: {datos['objective']}")
    st.write(f"Embudo: {datos['funnel_stage']}")
    st.write(f"Tema: {datos['theme']}")

    st.markdown("### Presupuesto")
    st.write(f"Inversión prevista: ${datos['spend']:,.2f}")

    st.markdown("### Condiciones")
    st.write(f"Festivo: {'Sí' if datos['is_holiday'] else 'No'}")
    st.write(f"Fin de semana: {'Sí' if datos['is_weekend'] else 'No'}")

    st.divider()

st.divider()

st.subheader("Acerca de la aplicación")

st.info(
    "Esta aplicación corresponde a la versión 1.0 del proyecto. "
    "Se trata de un Producto Mínimo Viable (MVP) desarrollado para demostrar "
    "el funcionamiento de un modelo de Machine Learning aplicado a la predicción "
    "de ingresos en campañas de marketing."
)

st.markdown("""
**Roadmap de evolución**

- Historial de predicciones
- Base de datos
- Dashboard interactivo
- Comparación entre campañas
- Exportación de informes
- Monitorización del modelo (MLOps)
""")

st.caption(
    "Proyecto de Machine Learning Regression | Desarrollado por Gabriela Granja | Bootcamp IA | 2026"
)