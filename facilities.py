import streamlit as st
import pandas as pd
import os

# =========================================
# 1. CONFIGURAÇÕES E DNA VISUAL (PADRÃO OURO)
# =========================================
st.set_page_config(page_title="Facilities Intelligence | VR Software", layout="wide")

# Injeção de CSS para manter a identidade visual
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
# 2. CAMADA DE DADOS (CLEANING & TYPE SAFETY)
# =========================================

def limpar_valor(valor):
    """Garante a Regra Absoluta: Tipagem Forte (Float)"""
    if pd.isna(valor): return 0.0
    s_valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(s_valor)
    except:
        return 0.0

@st.cache_data
def carregar_dados_facilities():
    # Nome do arquivo conforme o seu repositório
    file_name = "FACILITIES - DADOS PARA APRESENTAÇÃO.xlsx - MAR 2026.csv"
    
    if not os.path.exists(file_name):
        return None

    # Leitura bruta para processamento modular
    df_raw = pd.read_csv(file_name, header=None)

    # 1. Extração de Custos Operacionais (Linhas 3 a 7 - Baseado no seu arquivo)
    custos_op = df_raw.iloc[3:7, [1, 2]].copy()
    custos_op.columns = ['Descricao', 'Valor']
    custos_op['Valor'] = custos_op['Valor'].apply(limpar_valor)

    # 2. Extração de Veículos (Linhas 10 a 16)
    veiculos = df_raw.iloc[10:16, [1, 2, 3, 4]].copy()
    veiculos.columns = ['Condutor', 'Valor', 'Contrato', 'Detalhe']
    veiculos['Valor'] = veiculos['Valor'].apply(limpar_valor)

    # 3. Extração de Viagens (Linhas 19 a 25)
    viagens = df_raw.iloc[19:25, [1, 2, 3]].copy()
    viagens.columns = ['Descricao', 'Valor', 'Contexto']
    viagens['Valor'] = viagens['Valor'].apply(limpar_valor)

    return {
        "custos": custos_op,
        "veiculos": veiculos,
        "viagens": viagens
    }

# =========================================
# 3. INTERFACE DE APRESENTAÇÃO
# =========================================

st.markdown('<div class="hero-title">Facilities Intelligence <span style="font-size:1rem; opacity:0.8;">v1.0</span></div>', unsafe_allow_html=True)

dados = carregar_dados_facilities()

if dados:
    # Cálculos para os Cards do Topo
    total_custos = dados['custos']['Valor'].sum()
    total_veiculos = dados['veiculos']['Valor'].sum()
    total_viagens = dados['viagens']['Valor'].sum()
    investimento_total = total_custos + total_veiculos + total_viagens

    # GRID DE CARDS EXECUTIVOS
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'<div class="resumo-card"><span>Gasto Total (Mar/26)</span><div class="resumo-valor">R$ {investimento_total:,.2f}</div><div class="resumo-subtitulo">Consolidado Mensal</div></div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#f59e0b;"><span>Custos Operacionais</span><div class="resumo-valor">R$ {total_custos:,.2f}</div><div class="resumo-subtitulo">Suprimentos e TI</div></div>', unsafe_allow_html=True)
        
    with c3:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#2e7d32;"><span>Logística de Veículos</span><div class="resumo-valor">R$ {total_veiculos:,.2f}</div><div class="resumo-subtitulo">Contratos e Diárias</div></div>', unsafe_allow_html=True)

    with c4:
        st.markdown(f'<div class="resumo-card" style="border-top-color:#3b82f6;"><span>Viagens & Projetos</span><div class="resumo-valor">R$ {total_viagens:,.2f}</div><div class="resumo-subtitulo">Reembolsos e Passagens</div></div>', unsafe_allow_html=True)

    # DETALHAMENTO EM ABAS
    tab1, tab2, tab3 = st.tabs(["📊 Detalhe de Custos", "🚗 Frota e Veículos", "✈️ Viagens"])

    with tab1:
        st.subheader("Custos de Operação Direta")
        st.table(dados['custos'].style.format({"Valor": "R$ {:.2f}"}))

    with tab2:
        st.subheader("Contratos de Veículos Ativos")
        st.dataframe(dados['veiculos'], use_container_width=True)

    with tab3:
        st.subheader("Fluxo de Viagens e Missões")
        st.dataframe(dados['viagens'], use_container_width=True)

else:
    st.error("⚠️ Erro: Ficheiro de dados não encontrado. Verifique o nome do arquivo no repositório.")
    st.info("Dica: O arquivo deve se chamar 'FACILITIES - DADOS PARA APRESENTAÇÃO.xlsx - MAR 2026.csv' e estar na raiz do projeto.")

# Sidebar de Controle (Opcional)
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=VR+SOFTWARE", use_container_width=True)
    st.markdown("---")
    st.write("**Filtros de Visão**")
    unidade = st.selectbox("Unidade", ["Todas", "Recife", "Salvador", "Floripa", "João Pessoa"])
    st.success("Modo de Leitura Ativo")
