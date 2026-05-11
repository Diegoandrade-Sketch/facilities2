import streamlit as st
import pandas as pd
import os

# =========================================
# 1. DNA VISUAL (PADRÃO OURO)
# =========================================
st.set_page_config(page_title="Facilities Intelligence | VR Software", layout="wide")

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
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. CAMADA DE DADOS (CLEANING)
# =========================================

def limpar_valor(valor):
    if pd.isna(valor): return 0.0
    s_valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(s_valor)
    except:
        return 0.0

@st.cache_data
def carregar_dados_facilities():
    # Procura o arquivo automaticamente para evitar erro de nome
    target_file = "dados_marco_2026.csv"
    
    if not os.path.exists(target_file):
        # Fallback: procura qualquer arquivo que contenha 'MAR 2026'
        for f in os.listdir('.'):
            if "MAR 2026" in f and f.endswith(".csv"):
                target_file = f
                break
        else:
            return None

    try:
        df_raw = pd.read_csv(target_file, header=None)
        
        # Filtros baseados na estrutura da planilha de Março
        custos_op = df_raw.iloc[3:7, [1, 2]].copy()
        custos_op.columns = ['Descricao', 'Valor']
        custos_op['Valor'] = custos_op['Valor'].apply(limpar_valor)

        veiculos = df_raw.iloc[10:16, [1, 2, 3, 4]].copy()
        veiculos.columns = ['Condutor', 'Valor', 'Contrato', 'Detalhe']
        veiculos['Valor'] = veiculos['Valor'].apply(limpar_valor)

        viagens = df_raw.iloc[19:25, [1, 2, 3]].copy()
        viagens.columns = ['Descricao', 'Valor', 'Contexto']
        viagens['Valor'] = viagens['Valor'].apply(limpar_valor)

        return {"custos": custos_op, "veiculos": veiculos, "viagens": viagens}
    except Exception:
        return None

# =========================================
# 3. INTERFACE PRINCIPAL
# =========================================

st.markdown('<div class="hero-title">Facilities Intelligence</div>', unsafe_allow_html=True)

dados = carregar_dados_facilities()

if dados:
    total_custos = dados['custos']['Valor'].sum()
    total_veiculos = dados['veiculos']['Valor'].sum()
    total_viagens = dados['viagens']['Valor'].sum()
    investimento_total = total_custos + total_veiculos + total_viagens

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="resumo-card"><span>Total Março</span><div class="resumo-valor">R$ {investimento_total:,.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#f59e0b;"><span>Operacional</span><div class="resumo-valor">R$ {total_custos:,.2f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#2e7d32;"><span>Veículos</span><div class="resumo-valor">R$ {total_veiculos:,.2f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#3b82f6;"><span>Viagens</span><div class="resumo-valor">R$ {total_viagens:,.2f}</div></div>', unsafe_allow_html=True)

    st.subheader("📊 Detalhamento de Custos")
    st.dataframe(dados['custos'], use_container_width=True)
else:
    st.warning("⚠️ Arquivo de dados não encontrado no repositório.")
