# 📈 Marketing Campaign Revenue Predictor

Proyecto de **Machine Learning** desarrollado durante el Bootcamp de Inteligencia Artificial cuyo objetivo es predecir los ingresos esperados de campañas de marketing digital mediante técnicas de regresión.

La solución incluye el ciclo completo de un proyecto de Machine Learning: análisis del dataset, EDA, entrenamiento de modelos, optimización, despliegue mediante Streamlit y dockerización.

**🌐 Demo:** https://ai-project-regression-marketing-nfcaunp8mbcgqybcz3wr74.streamlit.app/

---

# 🎯 Objetivo

Desarrollar un modelo capaz de estimar el **Revenue** de una campaña antes de su lanzamiento utilizando información disponible durante la fase de planificación.

Aunque inicialmente el proyecto se planteó como una **Regresión Lineal**, tras comparar diferentes algoritmos de regresión se seleccionó un **Random Forest Regressor optimizado**, al ofrecer un mejor rendimiento predictivo.

---

# 🛠 Tecnologías

* Python
* Pandas
* NumPy
* Scikit-Learn
* RandomizedSearchCV
* Matplotlib
* Streamlit
* Joblib
* Docker
* Git & GitHub

---

# 📂 Estructura del proyecto

```text
.
├── app/
│   └── streamlit_app.py
├── data/
│   ├── digital_marketing_dataset_30k.csv
│   ├── data_dictionary.csv
│   └── README_DATASET.md
├── docs/
├── models/
│   └── campaign_revenue_forecast_model.joblib
├── notebooks/
├── src/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🤖 Modelo desarrollado

El flujo completo del modelo incluye:

* Limpieza y preparación de datos.
* Imputación de valores faltantes.
* Escalado de variables numéricas.
* Codificación One-Hot de variables categóricas.
* Pipeline de Scikit-Learn.
* Entrenamiento de modelos de regresión.
* Optimización mediante **RandomizedSearchCV**.
* Exportación del modelo entrenado mediante Joblib.

Modelo final:

**Optimized Random Forest Regressor**

---

# 📊 Resultados

## Métricas de evaluación

| Métrica |      Valor |
| ------- | ---------: |
| MAE     |     177.58 |
| MSE     | 1.35 × 10⁶ |
| RMSE    |    1160.78 |
| R²      |      0.850 |

El modelo explica aproximadamente el **85 % de la variabilidad del Revenue**.

---

## 📉 Control del overfitting

| Métrica         |   Valor |
| --------------- | ------: |
| Training R²     |  0.9688 |
| Testing R²      |  0.8483 |
| Overfitting Gap |  0.1204 |
| Overfitting (%) | 12.04 % |

Durante el proyecto se monitorizó el comportamiento del modelo comparando entrenamiento y prueba para controlar el sobreajuste antes de seleccionar la versión final.

---

## 🔍 Variables más importantes

El análisis de Feature Importance mostró que las variables con mayor influencia sobre la predicción fueron:

1. Número de conversiones
2. Número de clics
3. Objetivo: Leads
4. Objetivo: Sales
5. Inversión (Spend)

Las diez variables más importantes concentran aproximadamente el **96 % de la importancia acumulada** del modelo.

---

# 🚀 Instalación

Clonar el repositorio:

```bash
git clone <repository_url>
cd ai-project-regression-marketing
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# 💾 Archivos necesarios

La aplicación requiere:

```text
data/digital_marketing_dataset_30k.csv

models/campaign_revenue_forecast_model.joblib
```

---

# ▶️ Ejecutar la aplicación

```bash
streamlit run app/streamlit_app.py
```

Abrir:

```
http://localhost:8501
```

---

# 🐳 Docker

Construir la imagen:

```bash
docker build -t marketing-regression-app .
```

Ejecutar el contenedor:

```bash
docker run -p 8501:8501 marketing-regression-app
```

---

# ☁️ Despliegue

El proyecto se encuentra desplegado mediante **Streamlit Community Cloud**.

Además, dispone de una versión completamente **dockerizada**, preparada para su despliegue en cualquier plataforma compatible con Docker.

---

# 📌 Estado del proyecto

Versión entregada:

**MVP v0.1**

Incluye:

* ✅ Dataset documentado
* ✅ Exploratory Data Analysis (EDA)
* ✅ Feature Engineering
* ✅ Modelado de regresión
* ✅ Comparación de modelos
* ✅ Optimización del modelo
* ✅ Evaluación mediante métricas
* ✅ Aplicación desarrollada con Streamlit
* ✅ Dockerización
* ✅ Despliegue
* ✅ Documentación

---

# 🔮 Próximas mejoras

* Historial de predicciones.
* Base de datos.
* Dashboard interactivo.
* Exportación de informes.
* Monitorización del modelo.
* Reentrenamiento automático.
* Sistema de autenticación.

---

# 👩‍💻 Autora

**Gabriela Granja**

Bootcamp de Inteligencia Artificial

2026
