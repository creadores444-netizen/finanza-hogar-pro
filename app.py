import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de Identidad
st.set_page_config(page_title="Finanza Hogar Pro", layout="wide", page_icon="🏠")

# Estilo personalizado para usar los colores de tu logo (Azul y Dorado)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #002147; color: #D4AF37; font-weight: bold; border-radius: 10px; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Finanza Hogar Pro")
st.subheader("Simulador de Inteligencia Hipotecaria")

# --- PESTAÑAS ---
tab_calc, tab_guia = st.tabs(["🧮 Calculadora de Libertad", "📖 Guía del Experto"])

# --- BARRA LATERAL (ENTRADAS) ---
with st.sidebar:
    st.header("📋 Tus Datos Actuales")
    monto = st.number_input("Saldo de la Deuda ($)", value=200000000, step=1000000)
    tasa_ea = st.number_input("Tasa Efectiva Anual (%)", value=13.0, step=0.1) / 100
    meses_restantes = st.number_input("Meses faltantes", value=180, step=1)
    
    st.header("🚀 Tu Estrategia")
    abono_extra = st.number_input("Abono extra mensual ($)", value=200000, step=50000)
    seguro_actual = st.number_input("Seguro mensual en extracto ($)", value=120000)
    aplicar_endoso = st.checkbox("¿Aplicar ahorro por Endoso?", value=True)

# --- LÓGICA FINANCIERA ---
t_mv = (1 + tasa_ea)**(1/12) - 1
cuota_base = monto * (t_mv * (1 + t_mv)**meses_restantes) / ((1 + t_mv)**meses_restantes - 1)

# Ahorro estimado por endoso (50%)
ahorro_seguro = (seguro_actual * 0.5) if aplicar_endoso else 0
esfuerzo_total = abono_extra + ahorro_seguro

# Simulación con y sin estrategia
def simular(monto_ini, t_mv_val, meses_lim, adicional):
    saldo = monto_ini
    intereses_totales = 0
    meses_contados = 0
    cap_list, int_list = [], []
    
    while saldo > 0 and meses_contados < meses_lim:
        int_mes = saldo * t_mv_val
        cap_mes = (cuota_base - int_mes) + adicional
        if cap_mes > saldo: cap_mes = saldo
        
        intereses_totales += int_mes
        saldo -= cap_mes
        meses_contados += 1
        cap_list.append(cap_mes)
        int_list.append(int_mes)
        
    return intereses_totales, meses_contados, cap_list, int_list

int_sin, meses_sin, _, _ = simular(monto, t_mv, meses_restantes, 0)
int_con, meses_con, c_list, i_list = simular(monto, t_mv, meses_restantes, esfuerzo_total)

ahorro_final = int_sin - int_con
tiempo_ahorrado = meses_restantes - meses_con

# --- PESTAÑA: CALCULADORA ---
with tab_calc:
    c1, c2, c3 = st.columns(3)
    c1.metric("Ahorro en Intereses", f"${ahorro_final:,.0f}")
    c2.metric("Meses Eliminados", f"{tiempo_ahorrado}")
    c3.metric("Nueva Duración", f"{meses_con/12:.1f} años")

    # Gráfico
    fig = go.Figure(data=[
        go.Bar(name='Intereses (Banco)', x=list(range(meses_con)), y=i_list, marker_color='#EF553B'),
        go.Bar(name='Capital (Tu Casa)', x=list(range(meses_con)), y=c_list, marker_color='#00CC96')
    ])
    fig.update_layout(barmode='stack', title="Composición de tu Nueva Cuota")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.header("💡 El Poder del Micro-Emprendimiento")
    st.write("¿Cómo conseguir el dinero para el abono extra?")
    df_emp = pd.DataFrame({
        "Actividad": ["Vender 5 postres/día", "Clases particulares", "Servicio Freelance"],
        "Ingreso Mensual": ["$250,000", "$200,000", "$400,000"],
        "Años borrados": [f"{int(tiempo_ahorrado*1.2)} meses", f"{tiempo_ahorrado} meses", f"{int(tiempo_ahorrado*1.8)} meses"]
    })
    st.table(df_emp)

    st.info("📢 Para aplicar esta estrategia legalmente, necesitas el Kit de Cartas y el Manual PRO.")
    st.link_button("🚀 DESCARGAR KIT DE CARTAS LEGALES (HOTMART)", "https://pay.hotmart.com/TU_LINK")

# --- PESTAÑA: GUÍA ---
with tab_guia:
    st.markdown("""
    ### Guía Rápida para dueños de casa
    1. **Pesos vs UVR:** En Pesos tu cuota es fija. En UVR tu saldo sube con la inflación; aquí los abonos son obligatorios para no perder tu casa.
    2. **El Endoso:** El seguro que te cobra el banco es un negocio para ellos. Al endosar, tú eliges tu aseguradora y ahorras dinero que va directo a tu deuda.
    3. **Días de Oro:** Realiza tus abonos 2 días después del pago de tu cuota mensual para asegurar que todo el dinero vaya a capital.
    """)
