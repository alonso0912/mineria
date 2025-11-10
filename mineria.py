# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# 
# # CONFIGURACIÓN GENERAL
# st.set_page_config(page_title="Dashboard Universitario", layout="wide")
# st.title("🎓 Dashboard de Retención y Satisfacción Estudiantil")
# 
# # CARGAR CSV
# st.sidebar.header("Configuración de datos")
# 
# archivo = st.sidebar.file_uploader("📂 Carga tu archivo CSV (university_student_data.csv)", type=["csv"])
# 
# if archivo is not None:
#     df = pd.read_csv(archivo)
#     st.success("✅ Archivo cargado correctamente.")
# else:
#     st.warning("Por favor, carga el archivo CSV para continuar.")
#     st.stop()
# 
# # Mostrar columnas detectadas
# st.subheader("🔍 Columnas detectadas en el archivo")
# st.dataframe(pd.DataFrame({"Columnas": df.columns}))
# 
# # RENOMBRAR COLUMNAS AUTOMÁTICAMENTE
# renombres = {
#     "Year": "Año",
#     "year": "Año",
#     "Term": "Periodo",
#     "term": "Periodo",
#     "Retention Rate (%)": "Tasa de retencion",
#     "RetentionRate": "Tasa de retencion",
#     "Student Satisfaction (%)": "Puntaje de satisfacción",
#     "Satisfaction": "Puntaje de satisfacción"
# }
# 
# df.rename(columns=renombres, inplace=True)
# 
# # DETECTAR DEPARTAMENTOS
# department_cols = [col for col in df.columns if "Enrolled" in col]
# 
# if len(department_cols) == 0:
#     st.warning(" No se detectaron columnas de departamentos ('*Enrolled'). Se usará 'General' por defecto.")
#     df["Departamento"] = "General"
#     df["Inscritos"] = 1
# else:
#     id_vars = [col for col in df.columns if col not in department_cols]
#     df = df.melt(
#         id_vars=id_vars,
#         value_vars=department_cols,
#         var_name="Departamento",
#         value_name="Inscritos"
#     )
# 
#     # Limpiar nombres de departamentos
#     df['Departamento'] = (df['Departamento']
#                           .str.replace(' Enrolled', '', regex=False)
#                           .str.replace('Engineering', 'Ingeniería')
#                           .str.replace('Business', 'Negocios')
#                           .str.replace('Arts', 'Artes')
#                           .str.replace('Science', 'Ciencias'))
# 
# # VALIDAR COLUMNAS CLAVE
# columnas_requeridas = ["Año", "Periodo", "Tasa de retencion", "Puntaje de satisfacción", "Departamento"]
# faltantes = [col for col in columnas_requeridas if col not in df.columns]
# 
# if faltantes:
#     st.error(f" Faltan las siguientes columnas: {', '.join(faltantes)}")
#     st.stop()
# 
# # FILTROS INTERACTIVOS
# st.sidebar.header("Filtros")
# year = st.sidebar.multiselect("Selecciona Año(s)", sorted(df["Año"].unique()), default=df["Año"].unique())
# department = st.sidebar.multiselect("Selecciona Departamento(s)", df["Departamento"].unique(), default=df["Departamento"].unique())
# term = st.sidebar.multiselect("Selecciona Periodo(s)", df["Periodo"].unique(), default=df["Periodo"].unique())
# 
# # Aplicar filtros
# df_filtered = df[(df["Año"].isin(year)) & (df["Departamento"].isin(department)) & (df["Periodo"].isin(term))]
# 
# # KPIs
# avg_retention = df_filtered["Tasa de retencion"].mean() * 100
# avg_satisfaction = df_filtered["Puntaje de satisfacción"].mean()
# max_retention = df_filtered["Tasa de retencion"].max() * 100
# 
# col1, col2, col3 = st.columns(3)
# col1.metric("Tasa promedio de retención", f"{avg_retention:.1f}%")
# col2.metric("Puntaje promedio de satisfacción", f"{avg_satisfaction:.2f}/5")
# col3.metric("Máxima tasa de retención", f"{max_retention:.1f}%")
# 
# st.markdown("---")
# 
# # GRÁFICA 1 — TENDENCIA
# st.subheader(" Tendencia de la Tasa de Retención por Año")
# fig1, ax1 = plt.subplots(figsize=(8, 4))
# for dept in df_filtered["Departamento"].unique():
#     df_dept = df_filtered[df_filtered["Departamento"] == dept]
#     ax1.plot(df_dept["Año"], df_dept["Tasa de retencion"] * 100, marker="o", label=dept)
# ax1.set_title("Tasa de Retención por Departamento y Año")
# ax1.set_xlabel("Año")
# ax1.set_ylabel("Retención (%)")
# ax1.legend()
# ax1.grid(True)
# st.pyplot(fig1)
# 
# # GRÁFICA 2 — BARRAS
# st.subheader(" Comparación de Satisfacción Promedio por Departamento")
# fig2, ax2 = plt.subplots(figsize=(8, 4))
# df_grouped = df_filtered.groupby("Departamento")["Puntaje de satisfacción"].mean().sort_values()
# ax2.barh(df_grouped.index, df_grouped.values, color="#4CAF50")
# ax2.set_xlabel("Satisfacción Promedio (1–5)")
# ax2.set_ylabel("Departamento")
# st.pyplot(fig2)
# 
# # GRÁFICA 3 — PASTEL
# st.subheader(" Distribución de Registros por Periodo Académico")
# fig3, ax3 = plt.subplots(figsize=(5, 5))
# term_counts = df_filtered["Periodo"].value_counts()
# ax3.pie(term_counts, labels=term_counts.index, autopct="%1.1f%%", startangle=90, colors=["#1E90FF", "#FFA500"])
# ax3.set_title("Proporción de Estudiantes por Periodo")
# st.pyplot(fig3)
# 
# # DATOS 
# tab1, tab2 = st.tabs(["📄 Datos filtrados", "📚 Datos completos"])
# with tab1:
#     st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
# with tab2:
#     st.dataframe(df, use_container_width=True)
# 

