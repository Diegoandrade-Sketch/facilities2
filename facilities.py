import streamlit as st
import pandas as pd
import os
import csv

# =========================================
# 1. CONFIGURAÇÕES E DNA VISUAL (PADRÃO OURO)
# =========================================
st.set_page_config(page_title="Facilities Intelligence | VR Software", layout="wide")

# Injeção de CSS para manter a identidade visual de alto impacto
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
    
    /* Estilização de Tabelas para Diretoria */
    .stDataFrame { border-radius: 10px; border: 1px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. CAMADA DE DADOS E RESILIÊNCIA (TYPE SAFETY)
# =========================================

def limpar_valor(valor):
    """Garante a Regra Absoluta: Tipagem Forte (Float)"""
    if pd.isna(valor): return 0.0
    # Remove R$, pontos de milhar, aspas extras e limpa espaços
    s_valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').replace('"', '').strip()
    try:
        return float(s_valor)
    except:
        return 0.0

@st.cache_data
def carregar_dados_facilities():
    file_name = "facilities_2026.csv"
    
    if not os.path.exists(file_name):
        return None

    try:
        # TENTATIVA 1: Padrão Excel Brasileiro (sep=; e encoding latin1)
        # on_bad_lines='skip' ignora linhas corrompidas pelo Excel
        # quoting=csv.QUOTE_NONE impede o erro de 'expected after "'
        try:
            df_raw = pd.read_csv(
                file_name, 
                header=None, 
                encoding='latin1', 
                sep=';', 
                on_bad_lines='skip', 
                engine='c',
                quoting=csv.QUOTE_NONE
            )
            # Se ler apenas uma coluna, tenta com vírgula
            if df_raw.shape[1] == 1:
                df_raw = pd.read_csv(file_name, header=None, encoding='latin1', sep=',', on_bad_lines='skip', engine='c', quoting=csv.QUOTE_NONE)
        except:
            # TENTATIVA 2: Fallback caso o motor C falhe
            df_raw = pd.read_csv(file_name, header=None, encoding='latin1', sep=None, engine='python', on_bad_lines='skip')

        # --- MAPEAMENTO DE BLOCOS (BASE MARÇO 2026) ---
        
        # 1. Custos Operacionais
        custos_op = df_raw.iloc[3:7, [1, 2]].copy()
        custos_op.columns = ['Descrição', 'Valor']
        custos_op['Valor'] = custos_op['Valor'].apply(limpar_valor)

        # 2. Veículos
        veiculos = df_raw.iloc[10:16, [1, 2, 3, 4]].copy()
        veiculos.columns = ['Condutor', 'Valor', 'Contrato', 'Detalhe']
        veiculos['Valor'] = veiculos['Valor'].apply(limpar_valor)

        # 3. Viagens
        viagens = df_raw.iloc[19:25, [1, 2, 3]].copy()
        viagens.columns = ['Descrição', 'Valor', 'Contexto']
        viagens['Valor'] = viagens['Valor'].apply(limpar_valor)

        return {
            "custos": custos_op,
            "veiculos": veiculos,
            "viagens": viagens
        }
    except Exception as e:
        st.error(f"Erro Crítico de Processamento: {e}")
        return None

# =========================================
# 3. INTERFACE DE APRESENTAÇÃO (UI)
# =========================================

st.markdown('<div class="hero-title">Facilities Intelligence</div>', unsafe_allow_html=True)

dados = carregar_dados_facilities()

if dados:
    # Cálculo de Totais para os Cards
    total_c = dados['custos']['Valor'].sum()
    total_v = dados['veiculos']['Valor'].sum()
    total_t = dados['viagens']['Valor'].sum()
    investimento_total = total_c + total_v + total_t

    # GRID DE CARDS EXECUTIVOS
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'<div class="resumo-card"><span>Total Março 2026</span><div class="resumo-valor">R$ {investimento_total:,.2f}</div><div class="resumo-subtitulo">Investimento Geral</div></div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#f59e0b;"><span>Operacional</span><div class="resumo-valor">R$ {total_c:,.2f}</div><div class="resumo-subtitulo">Materiais e Manutenção</div></div>', unsafe_allow_html=True)
        
    with c3:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#2e7d32;"><span>Veículos</span><div class="resumo-valor">R$ {total_v:,.2f}</div><div class="resumo-subtitulo">Logística e Frotas</div></div>', unsafe_allow_html=True)

    with c4:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#3b82f6;"><span>Viagens</span><div class="resumo-valor">R$ {total_t:,.2f}</div><div class="resumo-subtitulo">Reembolsos e Projetos</div></div>', unsafe_allow_html=True)

    # DETALHAMENTO EM ABAS
    st.write("---")
    tab1, tab2, tab3 = st.tabs(["📊 Custos Fixos", "🚗 Frota Ativa", "✈️ Relatório de Viagens"])

    with tab1:
        st.dataframe(dados['custos'], use_container_width=True, hide_index=True)

    with tab2:
        st.dataframe(dados['veiculos'], use_container_width=True, hide_index=True)

    with tab3:
        st.dataframe(dados['viagens'], use_container_width=True, hide_index=True)

else:
    st.warning("⚠️ O arquivo 'facilities_2026.csv' não foi processado. Verifique os logs.")
    if st.button("Listar Arquivos do Repositório"):
        st.code(os.listdir('.'))

# Sidebar Técnica
with st.sidebar:
    st.title("Controle Admin")
    st.info("Projeto: Facilities Read-Only")
    if st.button("Recarregar"):
        st.cache_data.clear()
        st.rerun()
