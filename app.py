# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 15:49:33 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO
import datetime

st.set_page_config(page_title="Postulación a la ASF", layout="wide")

# ====== 1. Autenticación Básica (Simulada) ======
def autenticar():
    st.sidebar.title("🔐 Acceso privado")
    usuario = st.sidebar.text_input("Usuario", value="", max_chars=20)
    password = st.sidebar.text_input("Contraseña", type="password")

    if usuario == "javier" and password == "asf1234":
        return True
    elif usuario != "" and password != "":
        st.sidebar.error("❌ Usuario o contraseña incorrectos")
        return False
    else:
        return None

autenticado = autenticar()

if autenticado:

    # ====== 2. Datos simulados con fechas ======
    #st.set_page_config(page_title="Postulación a la ASF", layout="wide")
    st.title("📄 Postulación técnica a la Auditoría Superior de la Federación (ASF)")
    st.markdown("""
    Esta aplicación demuestra mis habilidades en desarrollo con **Python**, gestión de datos, visualización interactiva y automatización de reportes.  
    💼 Adaptada a los requerimientos de la vacante publicada por la ASF para el puesto de *Programador*.
    """)

    def generar_datos():
        acciones = ["AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "NVDA", "META", "PEP", "KO", "NFLX"]
        precios = np.round(np.random.uniform(100, 1000, len(acciones)), 2)
        volumen = np.round(np.random.uniform(20, 150, len(acciones)), 1)
        fechas = pd.date_range(datetime.date.today() - pd.Timedelta("10D"), periods=len(acciones), freq='D')
        return pd.DataFrame({
            "Acción": acciones,
            "Precio (USD)": precios,
            "Volumen (M)": volumen,
            "Fecha": fechas
        })

    df = generar_datos()

    # ====== Filtros por Fecha ======
    st.sidebar.markdown("## 📅 Filtros por Fecha")
    fecha_inicio = st.sidebar.date_input("Fecha de inicio", df["Fecha"].min())
    fecha_fin = st.sidebar.date_input("Fecha de fin", df["Fecha"].max())
    df = df[(df["Fecha"] >= pd.to_datetime(fecha_inicio)) & (df["Fecha"] <= pd.to_datetime(fecha_fin))]

    # ====== Tabla Interactiva ======
    st.subheader("🧮 Tabla interactiva (editable)")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationPageSize=10)
    gb.configure_default_column(editable=True)
    gb.configure_selection("multiple", use_checkbox=True)
    grid_options = gb.build()

    AgGrid(df, gridOptions=grid_options, height=350, theme="balham-dark")

    # ====== 3. Comentarios Inteligentes ======
    st.subheader("🧠 Análisis automático")
    if not df.empty:
        accion_top = df.loc[df["Precio (USD)"].idxmax()]
        st.success(f"🔎 La acción más cara es **{accion_top['Acción']}** con ${accion_top['Precio (USD)']:.2f}")
        
        if (df["Precio (USD)"] > 900).any():
            st.warning("⚠️ Algunas acciones superan los $900 USD. Considera revisar su desempeño.")
        if (df["Volumen (M)"] > 140).any():
            st.info("📈 Hay acciones con alto volumen de operación (más de 140M).")

    else:
        st.warning("⚠️ No hay datos dentro del rango de fechas seleccionado.")

    # ====== Gráficos ======
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Gráfico de precios por acción")
        fig = px.bar(df, x="Acción", y="Precio (USD)", color="Acción", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📉 Gráfico de volumen de operaciones")
        fig2 = px.line(df, x="Acción", y="Volumen (M)", markers=True, line_shape="spline")
        st.plotly_chart(fig2, use_container_width=True)

    # ====== Descarga Excel ======
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Datos")
        return output.getvalue()

    st.download_button(
        label="📥 Descargar Excel con datos simulados",
        data=to_excel(df),
        file_name="datos_postulacion_asf.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ====== Footer ======
    st.markdown("---")
    st.info("""
    Esta app fue desarrollada en Python,
    simulando un entorno de desarrollo empresarial orientado a análisis y visualización de datos con PostgreSQL.

    👨‍💻 Autor: Javier Horacio Pérez Ricárdez  
    📍 CDMX  
    📧 jahoperez@gmail.com
    """)

elif autenticado == False:
    st.stop()
else:
    st.warning("🔐 Inicia sesión para acceder a la app")
