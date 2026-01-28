import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de la Página
st.set_page_config(page_title="Finanza Hogar Pro", layout="wide", page_icon="🏠")

# Estilo visual (Azul y Dorado)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #002147; color: #D4AF37; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Finanza Hogar Pro")
st.subheader("Simulador de Inteligencia Hipotecaria")

# --- BARRA LATERAL (ENTRADAS DE DATOS) ---
with st.sidebar:
    st.header("📋 Tus Datos Actuales")
    monto = st.number_input("Saldo de la Deuda ($)", value=200000000, step=1000000)
    tasa_ea = st.number_input("Tasa Efectiva Anual (%)", value=13.0, step=0.1) / 100
    meses_restantes = st.number_input("Meses faltantes", value=180, step=1)
    
    st.header("🚀 Tu Estrategia")
    abono_extra = st.number_input("Abono extra mensual ($)", value=200000, step=50000)
    seguro_actual = st.number_input("Seguro mensual en extracto ($)", value=120000)
    aplicar_endoso = st.checkbox("¿Aplicar ahorro por Endoso (Seguro)?", value=True)

# --- LÓGICA MATEMÁTICA ---
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

# --- PESTAÑAS (Aquí se agrupa TODO) ---
tab_calc, tab_seguros, tab_guia = st.tabs(["🧮 Calculadora de Libertad", "🛡️ Estrategia de Seguros", "📖 Guía del Experto"])

with tab_calc:
    c1, c2, c3 = st.columns(3)
    c1.metric("Ahorro en Intereses", f"${(int_sin - int_con):,.0f}")
    c2.metric("Meses Eliminados", f"{meses_restantes - meses_con}")
    c3.metric("Nueva Duración", f"{meses_con/12:.1f} años")

    fig = go.Figure(data=[
        go.Bar(name='Intereses (Banco)', x=list(range(meses_con)), y=i_list, marker_color='#EF553B'),
        go.Bar(name='Capital (Tu Casa)', x=list(range(meses_con)), y=c_list, marker_color='#00CC96')
    ])
    fig.update_layout(barmode='stack', title="Composición de tu Nueva Cuota")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.header("💡 El Poder del Micro-Emprendimiento")
    df_emp = pd.DataFrame({
        "Actividad": ["Vender 5 postres/día", "Clases particulares", "Servicio Freelance"],
        "Ingreso Mensual": ["$250,000", "$200,000", "$400,000"],
        "Años borrados (Est.)": [f"{int((meses_restantes - meses_con)*1.2)} meses", f"{meses_restantes - meses_con} meses", f"{int((meses_restantes - meses_con)*1.8)} meses"]
    })
    st.table(df_emp)

with tab_seguros:
    st.header("🛡️ El Negocio Oculto del Banco")
    st.write(f"Al endosar tu seguro, recuperas aproximadamente **${ahorro_seguro:,.0f}** cada mes.")
    st.info("Este dinero no se gasta, se usa para pagar el capital de tu casa automáticamente.")
    st.write("1. Busca una aseguradora externa.\n2. Presenta la póliza al banco.\n3. El banco debe aceptarla por ley.")

with tab_guia:
    st.header("📖 Guía Rápida para dueños de casa")
    st.markdown("""
    1. **Pesos vs UVR:** En Pesos tu cuota es fija. En UVR tu saldo sube con la inflación.
    2. **Días de Oro:** Realiza tus abonos 2 días después del pago de tu cuota para que el 100% vaya a capital.
    3. **La Ley 546 de 1999:** Es tu escudo legal para pagar antes sin multas.
    """)
    with st.expander("❓ Preguntas Frecuentes (FAQ)"):
        st.write("¿Es legal? Sí, es un derecho constitucional en Colombia.")
        st.write("¿El banco se puede negar? No, si cumples los requisitos de la Ley de Vivienda.")

st.markdown("---")
st.link_button("🚀 DESCARGAR KIT DE CARTAS LEGALES (HOTMART)", "https://pay.hotmart.com/TU_LINK")
