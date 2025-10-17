import streamlit as st
import datetime
from amortizacion import calcular_amortizacion, generar_pdf
from datetime import datetime as dt

st.set_page_config(page_title="Amortización de Créditos", page_icon="💰", layout="centered")
st.title("💰 Calculadora de Amortización de Créditos")

st.write("Calcula la tabla de pagos de un crédito con **cuota nivelada** e interés sobre saldo.")

monto = st.number_input("Monto del crédito", min_value=0.0, value=10000.0, step=100.0)
cuotas = st.number_input("Número de cuotas", min_value=1, value=12, step=1)
interes = st.number_input("Tasa por periodo (%)", min_value=0.0, value=2.0, step=0.1) / 100
fecha_inicio = st.date_input("Fecha de la primera cuota", datetime.date.today())
moneda = st.text_input("Moneda", "Q")

if st.button("Calcular y generar PDF"):
    df = calcular_amortizacion(monto, cuotas, interes, dt.combine(fecha_inicio, datetime.time()))
    generar_pdf(df, monto, cuotas, interes, "amortizacion.pdf", moneda, dt.now())
    with open("amortizacion.pdf", "rb") as f:
        st.download_button("📥 Descargar PDF", f, file_name="amortizacion.pdf")
