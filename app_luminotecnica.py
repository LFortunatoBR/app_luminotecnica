import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Validador NBR - Arquitetura", layout="centered")

# ==========================================
# 1. SISTEMA DE SEGURANÇA (LOGIN)
# ==========================================
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["senha_acesso"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Digite a senha para acessar:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Digite a senha para acessar:", type="password", on_change=password_entered, key="password")
        st.error("Senha incorreta.")
        return False
    return True

if not check_password():
    st.stop()

# ==========================================
# 2. BANCO DE DADOS NBR (Baseado na sua planilha)
# ==========================================
dados_ambientes = {
    "Lavabo": {"m2_min": 2.5, "pe_direito_min": 2.2, "ugrl": 25, "ra": 80, "lux_ideal": 100},
    "Banheiro Social": {"m2_min": 3.0, "pe_direito_min": 2.2, "ugrl": 25, "ra": 80, "lux_ideal": 100},
    "Banheiro Suíte": {"m2_min": 4.0, "pe_direito_min": 2.2, "ugrl": 25, "ra": 80, "lux_ideal": 100},
    "Quartos Solteiro": {"m2_min": 9.0, "pe_direito_min": 2.5, "ugrl": 22, "ra": 80, "lux_ideal": 100},
    "Quartos Casal": {"m2_min": 12.0, "pe_direito_min": 2.5, "ugrl": 22, "ra": 80, "lux_ideal": 100},
    "Salas": {"m2_min": 12.0, "pe_direito_min": 2.5, "ugrl": 22, "ra": 80, "lux_ideal": 100},
    "Copa/Cozinha": {"m2_min": 6.0, "pe_direito_min": 2.5, "ugrl": 22, "ra": 80, "lux_ideal": 200},
    "Áreas de Serviço": {"m2_min": 3.0, "pe_direito_min": 2.2, "ugrl": 22, "ra": 80, "lux_ideal": 100},
    "Garagens": {"m2_min": 12.5, "pe_direito_min": 2.3, "ugrl": 28, "ra": 40, "lux_ideal": 75}
}

# ==========================================
# 3. INTERFACE DO APLICATIVO
# ==========================================
st.title("📐 Validador de Projetos e Luminotécnica (NBR)")
st.write("Verificação de exigências mínimas arquitetônicas e cálculo de iluminação.")

# --- Seleção e Entradas ---
st.header("1. Dados do Projeto")
ambiente_selecionado = st.selectbox("Selecione o Ambiente:", list(dados_ambientes.keys()))

col1, col2 = st.columns(2)
with col1:
    area_proj = st.number_input("Área Projetada (m²)", min_value=0.1, value=10.0, step=0.5)
with col2:
    pe_direito_proj = st.number_input("Pé Direito (m)", min_value=1.0, value=2.6, step=0.1)

# Extrair as regras
regras = dados_ambientes[ambiente_selecionado]

# --- Validação Arquitetônica ---
st.header("2. Validação Arquitetônica")
val_area = "✅ Aprovado" if area_proj >= regras["m2_min"] else f"❌ Reprovado (Mínimo: {regras['m2_min']}m²)"
val_pe = "✅ Aprovado" if pe_direito_proj >= regras["pe_direito_min"] else f"❌ Reprovado (Mínimo: {regras['pe_direito_min']}m)"

st.write(f"- **Área do Ambiente:** {val_area}")
st.write(f"- **Pé Direito:** {val_pe}")

# --- Cálculo Luminotécnico ---
st.header("3. Dimensionamento de Iluminação")
st.subheader("Exigências NBR ISO 8995-1")
st.info(f"**Índice de Ofuscamento (UGRL):** {regras['ugrl']} | **Repro. de Cor (Ra):** {regras['ra']} | **Lux Ideal:** {regras['lux_ideal']} lux")

# Cálculos
lumens_necessarios = area_proj * regras["lux_ideal"]
eficiencia_led_comum = 100 # lm/W
potencia_total_led = lumens_necessarios / eficiencia_led_comum

st.metric("Fluxo Luminoso Total Necessário", f"{lumens_necessarios:,.0f} Lúmens".replace(",", "."))
st.write(f"Potência total estimada em LED Comum (100lm/W): **{math.ceil(potencia_total_led)} Watts**")

# Dimensionamento de Luminárias
watts_por_luminaria = st.slider("Potência da luminária LED escolhida (W):", 5, 50, 15)
qtd_luminarias = math.ceil(potencia_total_led / watts_por_luminaria)
st.success(f"Você precisará de **{qtd_luminarias} luminária(s)** de {watts_por_luminaria}W para atingir a norma.")

# --- Calculadora de Fita de LED ---
st.header("4. Calculadora de Fita de LED")
with st.expander("Dimensionar Fonte para Fita de LED"):
    col3, col4 = st.columns(2)
    with col3:
        w_metro = st.number_input("Potência da Fita (W/m):", value=14.4)
    with col4:
        metragem_fita = st.number_input("Metragem usada (m):", value=5.0)
    
    potencia_fita_total = w_metro * metragem_fita
    potencia_com_folga = potencia_fita_total * 1.30 # +30% de segurança da sua planilha
    
    st.warning(f"Consumo Total da Fita: **{potencia_fita_total:.1f}W**")
    st.success(f"Compre uma fonte de no mínimo: **{math.ceil(potencia_com_folga)}W** (já com 30% de margem de segurança).")
