# =========================================
# 📊 Dashboard de Retención y Satisfacción Estudiantil
# =========================================

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 🧩 Evitar error de "inotify instance limit reached"
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

# ============================
# ⚙️ CONFIGURACIÓN DE LA APP
# ============================
st.set_page_config(page_title="Dashboard Universitario", layout="wide")
st.title("🎓 Dashboard de Retención y Satisfacción Estudiantil")
st.markdown("Analiza los datos de retención y satisfacción de estudiantes por departamento y periodo académico.")

# ============================
# 📂 CARGA DE DATOS
# ============================

# Ruta directa al archivo CSV en GitHub (ajústala a tu usuario/repositorio si es distinto)
csv_url = "https://raw.githubusercontent.com/alonso0912/mineria/main/university_student_data.csv"

try:
    df = pd.read_csv(csv_url)
    st.success("✅ Datos cargados correctamente desde GitHub.")
except Exception as e:
    st.error(f"❌ Error al cargar los datos: {e}")
    st.stop()

# Mostrar columnas detectadas
st.sidebar.subheader("🧠 Vista previa de los datos")
st.sidebar.dataframe(df.head())

# ============================
# 🧹 LIMPIEZA Y RENOMBRADO
# ============================

# Normalizar nombres de columnas
df.columns = [col.strip() for col in df.columns]

# Renombrar columnas comunes si vienen en inglés
df.rename(columns={
    "Year": "Año",
    "Term": "Periodo",
    "Retention Rate (%)": "Tasa de retencion",
    "Student Satisfaction (%)": "Puntaje de satisfacción"
}, inplace=True)

# Identificar columnas de departamentos
dept_cols = [c for c in df.columns if "Enrolled" in c]

if not dept_cols:
    st.error("⚠️ No se encontraron columnas con 'Enrolled' en el CSV.")
    st.stop()

# Convertir a formato largo (para graficar por departamento)
df = df.melt(
    id_vars=["Año", "Periodo", "Tasa de retencion", "Puntaje de satisfacción"],
    value_vars=dept_cols,
    var_name="Departamento",
    value_name="Inscritos"
)

# Limpiar nombres de departamentos
df["Departamento"] = (df["Departamento"]
                      .str.replace(" Enrolled", "", regex=False)
                      .str.replace("Engineering", "Ingeniería")
                      .str.replace("Business", "Negocios")
                      .str.replace("Arts", "Artes")
                      .str.replace("Science", "Ciencias"))

# ============================
# 🎛️ FILTROS INTERACTIVOS
# ============================
st.sidebar.header("🎚️ Filtros de visualización")

años = st.sidebar.multiselect("Selecciona Año(s)", sorted(df["Año"].unique()), default=df["Año"].unique())
deptos = st.sidebar.multiselect("Selecciona Departamento(s)", sorted(df["Departamento"].unique()), default=df["Departamento"].unique())
periodos = st.sidebar.multiselect("Selecciona Periodo(s)", sorted(df["Periodo"].unique()), default=df["Periodo"].unique())

df_filtrado = df[
    (df["Año"].isin(años)) &
    (df["Departamento"].isin(deptos)) &
    (df["Periodo"].isin(periodos))
]

# ============================
# 📈 MÉTRICAS PRINCIPALES
# ============================
col1, col2, col3 = st.columns(3)
col1.metric("📊 Tasa Promedio de Retención", f"{df_filtrado['Tasa de retencion'].mean():.2%}")
col2.metric("⭐ Satisfacción Promedio", f"{df_filtrado['Puntaje de satisfacción'].mean():.2f}/5")
col3.metric("🎯 Máxima Retención", f"{df_filtrado['Tasa de retencion'].max():.2%}")

st.markdown("---")

# ============================
# 📊 GRÁFICA 1 - TENDENCIA DE RETENCIÓN
# ============================
st.subheader("📈 Tendencia de Retención por Año y Departamento")

fig1, ax1 = plt.subplots(figsize=(8, 4))
for dept in df_filtrado["Departamento"].unique():
    subset = df_filtrado[df_filtrado["Departamento"] == dept]
    ax1.plot(subset["Año"], subset["Tasa de retencion"], marker="o", label=dept)
ax1.set_xlabel("Año")
ax1.set_ylabel("Retención (%)")
ax1.legend(title="Departamento")
ax1.grid(True)
st.pyplot(fig1)

# ============================
# 📊 GRÁFICA 2 - SATISFACCIÓN PROMEDIO POR DEPARTAMENTO
# ============================
st.subheader("🏫 Satisfacción Promedio por Departamento")

fig2, ax2 = plt.subplots(figsize=(8, 4))
satisfaccion = df_filtrado.groupby("Departamento")["Puntaje de satisfacción"].mean().sort_values()
ax2.barh(satisfaccion.index, satisfaccion.values, color="#4CAF50")
ax2.set_xlabel("Satisfacción (1–5)")
ax2.set_ylabel("Departamento")
st.pyplot(fig2)

# ============================
# 📊 GRÁFICA 3 - DISTRIBUCIÓN POR PERIODO
# ============================
st.subheader("📅 Distribución de Registros por Periodo")

fig3, ax3 = plt.subplots(figsize=(5, 5))
periodos_counts = df_filtrado["Periodo"].value_counts()
ax3.pie(periodos_counts, labels=periodos_counts.index, autopct="%1.1f%%", startangle=90, colors=["#1E90FF", "#FFA500"])
ax3.set_title("Proporción de Estudiantes por Periodo")
st.pyplot(fig3)

# ============================
# 📑 DATOS
# ============================
st.markdown("### 📄 Datos Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

st.markdown("---")
st.caption("Desarrollado con ❤️ en Streamlit | Dashboard educativo interactivo")



