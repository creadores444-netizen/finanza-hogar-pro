import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de la Página
st.set_page_config(page_title="Finanza Hogar Pro", layout="wide", page_icon="🏠")

# --- FUNCIÓN PARA IMAGEN DE FONDO ---
def agregar_fondo():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                        url("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Tarjetas de datos legibles */
        [data-testid="stVerticalBlock"] > div {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 25px;
            border-radius: 15px;
            color: #002147;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        }}
        /* Estilo para los títulos */
        h1, h2, h3 {{
            color: #002147 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

agregar_fondo()

# --- EL RESTO DE TU CÓDIGO (Calculadora, pestañas, etc.) ---
st.title("🛡️ Finanza Hogar Pro")
st.subheader("Simulador de Inteligencia Hipotecaria")

# (Aquí sigue el resto del código que ya teníamos de la calculadora...)
# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Tus Datos Actuales")
    monto = st.number_input("Saldo de la Deuda ($)", value=200000000, step=1000000)
    tasa_ea = st.number_input("Tasa Efectiva Anual (%)", value=13.0, step=0.1) / 100
    meses_restantes = st.number_input("Meses faltantes", value=180, step=1)
    
    st.header("🚀 Tu Estrategia")
    abono_extra = st.number_input("Abono extra mensual ($)", value=200000, step=50000)
    seguro_actual = st.number_input("Seguro mensual en extracto ($)", value=120000)
    aplicar_endoso = st.checkbox("¿Aplicar ahorro por Endoso (Seguro)?", value=True)

# Lógica matemática básica
t_mv = (1 + tasa_ea)**(1/12) - 1
cuota_base = monto * (t_mv * (1 + t_mv)**meses_restantes) / ((1 + t_mv)**meses_restantes - 1)
ahorro_seguro = (seguro_actual * 0.5) if aplicar_endoso else 0
esfuerzo_total = abono_extra + ahorro_seguro

def simular(monto_ini, t_mv_val, meses_lim, adicional):
    saldo = monto_ini
    int_totales, meses_contados = 0, 0
    cap_list, int_list = [], []
    while saldo > 0 and meses_contados < meses_lim:
        int_mes = saldo * t_mv_val
        cap_mes = (cuota_base - int_mes) + adicional
        if cap_mes > saldo: cap_mes = saldo
        int_totales += int_mes
        saldo -= cap_mes
        meses_contados += 1
        cap_list.append(cap_mes)
        int_list.append(int_mes)
    return int_totales, meses_contados, cap_list, int_list

int_sin, meses_sin, _, _ = simular(monto, t_mv, meses_restantes, 0)
int_con, meses_con, c_list, i_list = simular(monto, t_mv, meses_restantes, esfuerzo_total)

# Pestañas
tab_calc, tab_seguros, tab_guia = st.tabs(["🧮 Calculadora", "🛡️ Seguros", "📖 Guía"])

with tab_calc:
    c1, c2, c3 = st.columns(3)
    c1.metric("Ahorro en Intereses", f"${(int_sin - int_con):,.0f}")
    c2.metric("Meses Eliminados", f"{meses_restantes - meses_con}")
    c3.metric("Nueva Duración", f"{meses_con/12:.1f} años")
    
    fig = go.Figure(data=[
        go.Bar(name='Intereses', x=list(range(meses_con)), y=i_list, marker_color='#EF553B'),
        go.Bar(name='Capital', x=list(range(meses_con)), y=c_list, marker_color='#00CC96')
    ])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.link_button("🚀 DESCARGAR KIT DE CARTAS LEGALES (HOTMART)", "https://pay.hotmart.com/TU_LINK")
