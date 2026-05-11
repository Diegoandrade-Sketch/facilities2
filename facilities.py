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
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. CAMADA DE DADOS
# =========================================

def limpar_valor(valor):
    if pd.isna(valor): return 0.0
    s_valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(s_valor)
    except:
        return 0.0

@st.cache_data
def carregar_dados():
    # NOME EXATO QUE DEVE ESTAR NO GITHUB
    nome_prioritario = "dados_marco_2026.csv"
    
    # 1. Tenta o nome exato
    if os.path.exists(nome_prioritario):
        target = nome_prioritario
    else:
        # 2. Se não achar, procura qualquer CSV que tenha "MAR 2026"
        arquivos = [f for f in os.listdir('.') if f.endswith('.csv')]
        fallback = [f for f in arquivos if "MAR 2026" in f.upper()]
        if fallback:
            target = fallback[0]
        else:
            return None

    try:
        # Leitura considerando o cabeçalho na linha 2 (skiprows=1)
        df_raw = pd.read_csv(target, header=None)
        
        # Mapeamento Inteligente baseado na estrutura MAR 2026
        # Custos Operacionais
        custos = df_raw.iloc[3:7, [1, 2]].copy()
        custos.columns = ['Descricao', 'Valor']
        custos['Valor'] = custos['Valor'].apply(limpar_valor)

        # Veículos
        veic = df_raw.iloc[10:16, [1, 2, 3, 4]].copy()
        veic.columns = ['Condutor', 'Valor', 'Contrato', 'Detalhe']
        veic['Valor'] = veic['Valor'].apply(limpar_valor)

        return {"custos": custos, "veiculos": veic, "arquivo_lido": target}
    except Exception as e:
        st.error(f"Erro na leitura: {e}")
        return None

# =========================================
# 3. INTERFACE
# =========================================

st.markdown('<div class="hero-title">Facilities Intelligence</div>', unsafe_allow_html=True)

dados = carregar_dados()

if dados:
    total = dados['custos']['Valor'].sum() + dados['veiculos']['Valor'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="resumo-card"><span>Total Consolidado</span><div class="resumo-valor">R$ {total:,.2f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.info(f"Lendo arquivo: {dados['arquivo_lido']}")

    st.subheader("📊 Detalhe de Custos Operacionais")
    st.table(dados['custos'])
    
    st.subheader("🚗 Gestão de Veículos")
    st.dataframe(dados['veiculos'], use_container_width=True)
else:
    st.error("⚠️ Arquivo 'dados_marco_2026.csv' não encontrado.")
    st.write("Arquivos presentes no seu GitHub atualmente:")
    st.code(os.listdir('.'))
