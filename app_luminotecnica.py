import streamlit as st
import pandas as pd
import math
import os

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
# 2. BANCO DE DADOS NBR E LUMINÁRIAS
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
    "Garagens": {"m2_min": 12.5, "pe_direito_min": 2.3, "ugrl": 28, "ra": 40, "lux_ideal": 75},
    "Escritório / Home Office": {"m2_min": 6.0, "pe_direito_min": 2.5, "ugrl": 19, "ra": 80, "lux_ideal": 300}
}

ARQUIVO_DB = "luminarias_db.csv"

# Se o arquivo não existir, cria com o catálogo completo
if not os.path.exists(ARQUIVO_DB):
    dados_iniciais = pd.DataFrame({
        "Modelo": [
            # Família: Painéis Quadrados (Plafons de Embutir)
            "Painel LED Embutir Quadrado 12x12cm (Micro)",
            "Painel LED Embutir Quadrado 17x17cm",
            "Painel LED Embutir Quadrado 22x22cm (Padrão Antigo 20x20)",
            "Painel LED Embutir Quadrado 30x30cm",
            "Painel LED Embutir Quadrado 40x40cm",
            "Painel LED Embutir Quadrado 60x60cm (Modular)",
            # Família: Painéis Redondos (Downlights de Embutir)
            "Painel LED Embutir Redondo Ø 12cm",
            "Painel LED Embutir Redondo Ø 17cm",
            "Painel LED Embutir Redondo Ø 22cm",
            "Painel LED Embutir Redondo Ø 30cm",
            # Família: Spots e Técnicos
            "Spot Dicróica MR16 (Luz de Destaque)",
            "Spot PAR20 (Pé-direito até 3m)",
            "Spot LED IP65 (Área de Chuveiro/Vapor)",
            "Balizador LED de Parede/Degrau (Escadas)",
            # Família: Lineares e Altura Dupla
            "Perfil de LED Embutir - Linear (por Metro)",
            "Pendente Linear/Tubular (Pé-direito 4m)",
            "Luminária High Bay Industrial (Pé-direito 6m+)"
        ],
        "Potência (W)": [
            6.0, 12.0, 18.0, 24.0, 36.0, 48.0,  # Quadrados
            6.0, 12.0, 18.0, 24.0,              # Redondos
            5.0, 7.0, 7.0, 2.0,                 # Spots/Balizador
            14.4, 40.0, 100.0                   # Lineares/Altos
        ],
        "Fluxo Luminoso (lm)": [
            420.0, 840.0, 1260.0, 1680.0, 2520.0, 3840.0, # Quadrados
            420.0, 840.0, 1260.0, 1680.0,                 # Redondos
            400.0, 525.0, 560.0, 100.0,                   # Spots/Balizador
            1200.0, 3200.0, 10000.0                       # Lineares/Altos
        ]
    })
    
    # Calcula a eficiência (lm/W) automaticamente e salva o arquivo
    dados_iniciais["Eficiência (lm/W)"] = (dados_iniciais["Fluxo Luminoso (lm)"] / dados_iniciais["Potência (W)"]).round(1)
    dados_iniciais.to_csv(ARQUIVO_DB, index=False)

df_luminarias = pd.read_csv(ARQUIVO_DB)# ==========================================
# 2. BANCO DE DADOS NBR E LUMINÁRIAS
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
    "Garagens": {"m2_min": 12.5, "pe_direito_min": 2.3, "ugrl": 28, "ra": 40, "lux_ideal": 75},
    "Escritório / Home Office": {"m2_min": 6.0, "pe_direito_min": 2.5, "ugrl": 19, "ra": 80, "lux_ideal": 300}
}

ARQUIVO_DB = "luminarias_db.csv"

# Se o arquivo não existir, cria com o catálogo completo
if not os.path.exists(ARQUIVO_DB):
    dados_iniciais = pd.DataFrame({
        "Modelo": [
            # Família: Painéis Quadrados (Plafons de Embutir)
            "Painel LED Embutir Quadrado 12x12cm (Micro)",
            "Painel LED Embutir Quadrado 17x17cm",
            "Painel LED Embutir Quadrado 22x22cm (Padrão Antigo 20x20)",
            "Painel LED Embutir Quadrado 30x30cm",
            "Painel LED Embutir Quadrado 40x40cm",
            "Painel LED Embutir Quadrado 60x60cm (Modular)",
            # Família: Painéis Redondos (Downlights de Embutir)
            "Painel LED Embutir Redondo Ø 12cm",
            "Painel LED Embutir Redondo Ø 17cm",
            "Painel LED Embutir Redondo Ø 22cm",
            "Painel LED Embutir Redondo Ø 30cm",
            # Família: Spots e Técnicos
            "Spot Dicróica MR16 (Luz de Destaque)",
            "Spot PAR20 (Pé-direito até 3m)",
            "Spot LED IP65 (Área de Chuveiro/Vapor)",
            "Balizador LED de Parede/Degrau (Escadas)",
            # Família: Lineares e Altura Dupla
            "Perfil de LED Embutir - Linear (por Metro)",
            "Pendente Linear/Tubular (Pé-direito 4m)",
            "Luminária High Bay Industrial (Pé-direito 6m+)"
        ],
        "Potência (W)": [
            6.0, 12.0, 18.0, 24.0, 36.0, 48.0,  # Quadrados
            6.0, 12.0, 18.0, 24.0,              # Redondos
            5.0, 7.0, 7.0, 2.0,                 # Spots/Balizador
            14.4, 40.0, 100.0                   # Lineares/Altos
        ],
        "Fluxo Luminoso (lm)": [
            420.0, 840.0, 1260.0, 1680.0, 2520.0, 3840.0, # Quadrados
            420.0, 840.0, 1260.0, 1680.0,                 # Redondos
            400.0, 525.0, 560.0, 100.0,                   # Spots/Balizador
            1200.0, 3200.0, 10000.0                       # Lineares/Altos
        ]
    })
    
    # Calcula a eficiência (lm/W) automaticamente e salva o arquivo
    dados_iniciais["Eficiência (lm/W)"] = (dados_iniciais["Fluxo Luminoso (lm)"] / dados_iniciais["Potência (W)"]).round(1)
    dados_iniciais.to_csv(ARQUIVO_DB, index=False)

df_luminarias = pd.read_csv(ARQUIVO_DB)

# ==========================================
# 3. INTERFACE DO APLICATIVO
# ==========================================
st.title("📐 Validador NBR e Luminotécnica")

st.header("1. Dados do Projeto")
ambiente_selecionado = st.selectbox("Selecione o Ambiente:", list(dados_ambientes.keys()))

col1, col2 = st.columns(2)
with col1:
    area_proj = st.number_input("Área Projetada (m²)", min_value=0.1, value=10.0, step=0.5)
with col2:
    pe_direito_proj = st.number_input("Pé Direito (m)", min_value=1.0, value=2.6, step=0.1)

regras = dados_ambientes[ambiente_selecionado]

st.header("2. Validação Arquitetônica")
val_area = "✅ Aprovado" if area_proj >= regras["m2_min"] else f"❌ Reprovado (Mínimo: {regras['m2_min']}m²)"
val_pe = "✅ Aprovado" if pe_direito_proj >= regras["pe_direito_min"] else f"❌ Reprovado (Mínimo: {regras['pe_direito_min']}m)"
st.write(f"- **Área do Ambiente:** {val_area}")
st.write(f"- **Pé Direito:** {val_pe}")

st.header("3. Cálculo Luminotécnico e Equipamento")
st.info(f"**Ofuscamento (UGRL):** Máx {regras['ugrl']} | **Repro. de Cor (Ra):** {regras['ra']} | **Exigência (Lux):** {regras['lux_ideal']}")

lumens_necessarios = area_proj * regras["lux_ideal"]
st.metric("Fluxo Luminoso Total Necessário", f"{lumens_necessarios:,.0f} Lúmens".replace(",", "."))

# --- Seleção diretamente do Banco de Dados ---
modelo_escolhido = st.selectbox("Selecione a Luminária do Catálogo:", df_luminarias["Modelo"].tolist())
dados_modelo = df_luminarias[df_luminarias["Modelo"] == modelo_escolhido].iloc[0]

# O cálculo agora usa os lúmens reais da peça, garantindo exatidão física
qtd_luminarias = math.ceil(lumens_necessarios / dados_modelo["Fluxo Luminoso (lm)"])

st.success(f"Para atingir a norma, instale: **{qtd_luminarias}x {modelo_escolhido}**")
st.write(f"*(Especificação da peça: {dados_modelo['Potência (W)']}W emitindo {dados_modelo['Fluxo Luminoso (lm)']} lm)*")


st.header("4. Banco de Dados de Luminárias")
st.write("Edite as informações abaixo, adicione novas linhas ou exclua modelos descontinuados.")

# O st.data_editor permite interagir com a tabela como se fosse o Excel
df_editado = st.data_editor(
    df_luminarias, 
    num_rows="dynamic", 
    use_container_width=True,
    hide_index=True
)

if st.button("Salvar Alterações no Catálogo"):
    # Recalcula a eficiência automaticamente ao salvar
    df_editado["Eficiência (lm/W)"] = (df_editado["Fluxo Luminoso (lm)"] / df_editado["Potência (W)"]).round(1)
    df_editado.to_csv(ARQUIVO_DB, index=False)
    st.success("Banco de dados atualizado! A página recarregará com as novas opções.")
    st.rerun()

st.header("5. Calculadora de Fita de LED")
with st.expander("Dimensionar Fonte e Circuito"):
    col3, col4 = st.columns(2)
    with col3:
        w_metro = st.number_input("Potência da Fita (W/m):", value=14.4)
    with col4:
        metragem_fita = st.number_input("Metragem usada (m):", value=5.0)
    
    potencia_fita_total = w_metro * metragem_fita
    potencia_com_folga = potencia_fita_total * 1.30 
    
    st.warning(f"Consumo Total: **{potencia_fita_total:.1f}W**")
    st.success(f"Fonte mínima necessária: **{math.ceil(potencia_com_folga)}W** (+30% folga).")
    
    if metragem_fita <= 5.0:
        st.info("💡 **Tensão Recomendada:** 12V. (Ideal para marcenaria e pequenos recortes; aceita cortes a cada 2,5cm/5cm).")
    else:
        st.info("💡 **Tensão Recomendada:** 24V. (Evita perda de luminosidade no final da fita em trechos longos).")
