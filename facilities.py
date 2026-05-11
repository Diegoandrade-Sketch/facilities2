import streamlit as st
import pandas as pd

# =========================================
# 1. DNA VISUAL VR SOFTWARE (ORANGE)
# =========================================
st.set_page_config(page_title="Facilities Launchpad", layout="wide")

st.markdown("""
<style>
    :root { --vr-orange: #FF8C00; }
    .main-header {
        background: linear-gradient(90deg, #FF8C00, #FFA500);
        color: white; padding: 1.5rem; border-radius: 10px;
        text-align: center; margin-bottom: 2rem;
    }
    .stRadio > div { gap: 20px; }
    .stButton>button {
        background-color: var(--vr-orange); color: white;
        width: 100%; border-radius: 8px; height: 3em; font-weight: bold;
    }
    .form-container {
        background-color: #f9f9f9; padding: 2rem;
        border-radius: 15px; border-left: 5px solid var(--vr-orange);
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. NAVEGAÇÃO E LÓGICA DE TELA
# =========================================
st.markdown('<div class="main-header"><h1>Facilities Intelligence</h1><p>Módulo de Lançamento Operacional</p></div>', unsafe_allow_html=True)

# Menu Superior Estilizado
menu = st.tabs(["📊 Dashboard Executivo", "📝 Novo Lançamento", "⚙️ Painel Admin"])

with menu[1]: # Aba de Lançamento
    st.subheader("Registro de Nova Despesa")
    
    # Seleção de Categoria (O Grupo que você sugeriu)
    categoria = st.radio(
        "Selecione o tipo de despesa para abrir o formulário:",
        ["🏢 Operacional", "🚗 Veículos", "✈️ Viagens"],
        horizontal=True
    )
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Formulários Dinâmicos (Modularização)
    if categoria == "🏢 Operacional":
        st.info("Formulário de Suprimentos, Materiais e Manutenção Predial")
        col1, col2 = st.columns(2)
        unidade = col1.selectbox("Unidade", ["Recife", "Salvador", "Cuiabá", "Floripa", "JP"])
        data_c = col2.date_input("Data da Compra")
        descricao = st.text_input("Descrição da Despesa", placeholder="Ex: Manutenção de Filtro de Água")
        valor = st.number_input("Valor total (R$)", min_value=0.0, format="%.2f")

    elif categoria == "🚗 Veículos":
        st.info("Formulário de Gestão de Frota, Aluguéis e Combustível")
        col1, col2 = st.columns(2)
        condutor = col1.text_input("Nome do Condutor / Responsável")
        contrato = col2.selectbox("Tipo de Contrato", ["Mensal", "Diária", "Manutenção Corretiva"])
        valor = st.number_input("Valor da Fatura (R$)", min_value=0.0, format="%.2f")
        detalhe = st.text_area("Observações do Veículo")

    elif categoria == "✈️ Viagens":
        st.info("Formulário de Missões Técnicas, Vexpenses e Deslocamentos")
        col1, col2 = st.columns(2)
        analista = col1.text_input("Analista em Missão")
        projeto = col2.text_input("Código do Projeto / Cidade")
        valor = st.number_input("Custo Total da Missão (R$)", min_value=0.0, format="%.2f")
        col_v1, col_v2 = st.columns(2)
        col_v1.checkbox("Hospedagem inclusa?")
        col_v2.checkbox("Deslocamento por KM?")

    st.markdown('</div>', unsafe_allow_html=True)

    # Botão de Ação com Feedback
    if st.button("🚀 SALVAR REGISTRO"):
        with st.spinner('Sincronizando com o banco de dados...'):
            # Aqui entrará a lógica SQL mais tarde
            st.success(f"Lançamento de {categoria} realizado com sucesso!")
            st.balloons()

with menu[0]:
    st.write("Visualização do Dashboard (Em desenvolvimento...)")

with menu[2]:
    st.write("Configurações do Banco de Dados PostgreSQL")
