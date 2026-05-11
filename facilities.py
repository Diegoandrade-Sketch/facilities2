import streamlit as st
import pandas as pd

# =========================================
# 1. CONFIGURAÇÕES E IDENTIDADE VISUAL
# =========================================
st.set_page_config(page_title="Facilities Intelligence | VR Software", layout="wide")

# CSS Institucional - Foco em Laranja VR e Sobriedade
st.markdown("""
<style>
    :root { 
        --vr-orange: #FF8C00; 
        --vr-dark: #333333;
    }
    
    .main-header {
        background-color: var(--vr-orange);
        color: white;
        padding: 1.5rem;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--vr-orange) !important;
        color: white !important;
    }

    .form-section {
        background-color: #ffffff;
        padding: 20px;
        border: 1px solid #e6e9ef;
        border-radius: 8px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. ESTRUTURA DE DADOS E OPÇÕES
# =========================================

UNIDADES = [
    "VR Recife", "VR Salvador", "VR João Pessoa", "VR Maceio",
    "VR Sergipe", "VR Santa Catarina", "VR Parana", "VR Rio Grande do Sul"
]

CATEGORIAS = ["Veiculos", "Viagens", "Hospedagem", "VExpenses"]

# =========================================
# 3. INTERFACE PRINCIPAL
# =========================================

st.markdown('<div class="main-header"><h1>Facilities Intelligence</h1></div>', unsafe_allow_html=True)

tab_dash, tab_lançamento = st.tabs(["Dashboard de Controle", "Entrada de Dados"])

with tab_lançamento:
    st.subheader("Formulário de Lançamento")
    
    with st.container():
        # Seleção Principal: Unidade e Categoria
        col_und, col_cat = st.columns(2)
        unidade_sel = col_und.selectbox("Unidade Responsável", UNIDADES)
        categoria_sel = col_cat.selectbox("Categoria da Despesa", CATEGORIAS)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        # Formulários Dinâmicos baseados na Categoria Selecionada
        if categoria_sel == "Veiculos":
            c1, c2 = st.columns(2)
            origem = c1.selectbox("Origem do Veiculo", ["Frota", "Locadora"])
            tipo_contrato = c2.selectbox("Tipo do Contrato", ["Mensal", "Anual"])
            
            c3, c4 = st.columns(2)
            condutor = c3.text_input("Nome do Condutor")
            placa = c4.text_input("Placa do Veiculo")
            
            valor = st.number_input("Valor do Lançamento (R$)", min_value=0.0, format="%.2f")

        elif categoria_sel == "Viagens":
            c1, c2 = st.columns(2)
            responsavel = c1.text_input("Responsável pela Viagem")
            tipo_viagem = c2.selectbox("Meio de Transporte", ["Aereo", "Carro"])
            
            valor = st.number_input("Valor Total (R$)", min_value=0.0, format="%.2f")

        elif categoria_sel == "Hospedagem":
            c1, c2 = st.columns(2)
            responsavel = c1.text_input("Responsável pela Hospedagem")
            tipo_hosp = c2.selectbox("Tipo de Acomodação", ["Hotel", "Pousada", "Airbnb"])
            
            valor = st.number_input("Valor da Reserva (R$)", min_value=0.0, format="%.2f")

        elif categoria_sel == "VExpenses":
            c1, c2 = st.columns(2)
            responsavel = c1.text_input("Responsável pelo Lançamento")
            tipo_consumo = c2.text_input("Tipo do Consumo")
            
            valor = st.number_input("Custo Total (R$)", min_value=0.0, format="%.2f")

        st.markdown('</div>', unsafe_allow_html=True)

        # Campo Aberto para Projetos (Solicitado)
        st.markdown("---")
        comparativo_projetos = st.text_area("Comparativo de Projetos", help="Espaço dedicado para análise descritiva e comparativa entre projetos da unidade.")

        # Botão de Ação
        if st.button("Confirmar Lançamento"):
            st.success("Dados processados com sucesso.")
            # Aqui futuramente incluiremos a gravação no Banco de Dados

with tab_dash:
    st.subheader("Consolidado por Unidade")
    # Placeholder para a visualização dos dados que serão lidos do banco
    st.info("O Dashboard será populado conforme os lançamentos forem realizados.")
