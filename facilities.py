import streamlit as st
import pandas as pd
import os

# =========================================
# 1. CONFIGURAÇÕES E DNA VISUAL (PADRÃO OURO)
# =========================================
st.set_page_config(page_title="Facilities Intelligence | VR Software", layout="wide")

# Injeção de CSS para manter a identidade visual e profissionalismo
st.markdown("""
<style>
    :root { --primary: #1e3a8a; --accent: #2e7d32; }
    .hero-title {
        font-size: 2.2rem; font-weight: 800; color: white;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
        text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .resumo-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        border-top: 5px solid var(--primary);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1rem;
    }
    .resumo-valor { font-size: 1.8rem; font-weight: 800; color: var(--primary); }
    .resumo-subtitulo { font-size: 0.85rem; color: #666; text-transform: uppercase; margin-top: 5px; }
    
    /* Estilização de Tabelas */
    .stDataFrame { border: 1px solid #e5e7eb; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. CAMADA DE DADOS E TYPE SAFETY
# =========================================

def limpar_valor(valor):
    """Regra Absoluta: Tipagem Forte (Float) para valores monetários"""
    if pd.isna(valor): return 0.0
    # Limpa símbolos, pontos de milhar e converte vírgula decimal
    s_valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(s_valor)
    except:
        return 0.0

@st.cache_data
def carregar_dados_facilities():
    # Nome do ficheiro conforme atualizado no GitHub
    file_name = "facilities_2026.csv"
    
    if not os.path.exists(file_name):
        return None

    try:
        # CORREÇÃO DE ENCODING E SEPARADOR
        # latin1: resolve o erro de utf-8 (acentos do Excel Windows)
        # sep=None: detecta automaticamente se é vírgula ou ponto-e-vírgula
        df_raw = pd.read_csv(file_name, header=None
