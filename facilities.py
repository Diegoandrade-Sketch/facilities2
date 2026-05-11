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
        df_raw = pd.read_csv(file_name, header=None, encoding='latin1', sep=None, engine='python')

        # Mapeamento de Blocos (Base: Estrutura MARÇO 2026)
        
        # 1. Custos Operacionais (Linhas 3 a 7)
        custos_op = df_raw.iloc[3:7, [1, 2]].copy()
        custos_op.columns = ['Descrição', 'Valor']
        custos_op['Valor'] = custos_op['Descrição'].apply(lambda x: df_raw[df_raw[1] == x][2].values[0] if x in df_raw[1].values else 0)
        # Re-limpeza para garantir float
        custos_op['Valor'] = custos_op['Valor'].apply(limpar_valor)

        # 2. Veículos (Linhas 10 a 16)
        veiculos = df_raw.iloc[10:16, [1, 2, 3, 4]].copy()
        veiculos.columns = ['Condutor', 'Valor', 'Contrato', 'Detalhe']
        veiculos['Valor'] = veiculos['Valor'].apply(limpar_valor)

        # 3. Viagens (Linhas 19 a 25)
        viagens = df_raw.iloc[19:25, [1, 2, 3]].copy()
        viagens.columns = ['Descrição', 'Valor', 'Contexto']
        viagens['Valor'] = viagens['Valor'].apply(limpar_valor)

        return {
            "custos": custos_op,
            "veiculos": veiculos,
            "viagens": viagens,
            "raw": df_raw
        }
    except Exception as e:
        st.error(f"Erro Crítico de Processamento: {e}")
        return None

# =========================================
# 3. INTERFACE PRINCIPAL (UI)
# =========================================

st.markdown('<div class="hero-title">Facilities Intelligence <span style="font-size:0.9rem; font-weight:normal;">| Dashboards Executivos</span></div>', unsafe_allow_html=True)

dados = carregar_dados_facilities()

if dados:
    # Cálculos para os Cards de Resumo
    v_custos = dados['custos']['Valor'].sum()
    v_veiculos = dados['veiculos']['Valor'].sum()
    v_viagens = dados['viagens']['Valor'].sum()
    v_total = v_custos + v_veiculos + v_viagens

    # Layout de Cards (Padrão Ouro)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'<div class="resumo-card"><span>Total Consolidado</span><div class="resumo-valor">R$ {v_total:,.2f}</div><div class="resumo-subtitulo">Mensal (Mar/26)</div></div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#f59e0b;"><span>Op. & Suprimentos</span><div class="resumo-valor">R$ {v_custos:,.2f}</div><div class="resumo-subtitulo">Custos Fixos</div></div>', unsafe_allow_html=True)
        
    with c3:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#2e7d32;"><span>Logística Frota</span><div class="resumo-valor">R$ {v_veiculos:,.2f}</div><div class="resumo-subtitulo">Contratos Veículos</div></div>', unsafe_allow_html=True)

    with c4:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#3b82f6;"><span>Viagens & Projetos</span><div class="resumo-valor">R$ {v_viagens:,.2f}</div><div class="resumo-subtitulo">Reembolsos e Viagens</div></div>', unsafe_allow_html=True)

    # Abas de Detalhamento
    st.write("### Detalhes Financeiros")
    tab1, tab2, tab3 = st.tabs(["📊 Custos Operacionais", "🚗 Gestão de Veículos", "✈️ Relatórios de Viagem"])

    with tab1:
        st.dataframe(dados['custos'], use_container_width=True, hide_index=True)

    with tab2:
        st.dataframe(dados['veiculos'], use_container_width=True, hide_index=True)

    with tab3:
        st.dataframe(dados['viagens'], use_container_width=True, hide_index=True)

else:
    st.warning("⚠️ Aguardando sincronização do ficheiro 'facilities_2026.csv'.")
    if st.button("Verificar Repositório"):
        st.code(os.listdir('.'))

# Sidebar para informações adicionais
with st.sidebar:
    st.title("Facilities Admin")
    st.info("Sistema em modo de leitura (Read-Only)")
    if st.button("Recarregar Dados"):
        st.cache_data.clear()
        st.rerun()
