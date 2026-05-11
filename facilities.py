import streamlit as st
import pandas as pd
import os

# =========================================
# 1. CONFIGURAÇÕES E DNA VISUAL (PADRÃO OURO)
# =========================================
st.set_page_config(page_title="Facilities Intelligence | VR Software", layout="wide")

# Estilização Profissional para Apresentação à Diretoria
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
    
    /* Ajuste para Tabelas */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================================
# 2. FUNÇÕES DE SUPORTE (CLEANING)
# =========================================

def limpar_valor(valor):
    """Converte strings financeiras (R$ 1.234,56) em Float puro"""
    if pd.isna(valor): return 0.0
    s_valor = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(s_valor)
    except:
        return 0.0

@st.cache_data
def carregar_dados_facilities():
    # Nome do arquivo atualizado conforme sua instrução
    file_name = "facilities_2026.csv"
    
    if not os.path.exists(file_name):
        return None

    try:
        # Leitura bruta do CSV (sem header para mapeamento manual de linhas)
        df_raw = pd.read_csv(file_name, header=None)

        # 1. Extração de Custos Operacionais (Linhas 3 a 7)
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
            "viagens": viagens,
            "file_name": file_name
        }
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        return None

# =========================================
# 3. INTERFACE PRINCIPAL
# =========================================

st.markdown('<div class="hero-title">Facilities Intelligence <span style="font-size:1rem; opacity:0.8;">v1.0</span></div>', unsafe_allow_html=True)

dados = carregar_dados_facilities()

if dados:
    # Consolidação de Valores
    total_custos = dados['custos']['Valor'].sum()
    total_veiculos = dados['veiculos']['Valor'].sum()
    total_viagens = dados['viagens']['Valor'].sum()
    investimento_total = total_custos + total_veiculos + total_viagens

    # GRID DE CARDS SUPERIORES
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'''<div class="resumo-card"><span>Investimento Total</span>
                    <div class="resumo-valor">R$ {investimento_total:,.2f}</div>
                    <div class="resumo-subtitulo">Mês de Referência: Março</div></div>''', unsafe_allow_html=True)
    
    with c2:
        st.markdown(f'''<div class="resumo-card" style="border-top-color:#f59e0b;"><span>Operacional</span>
                    <div class="resumo-valor">R$ {total_custos:,.2f}</div>
                    <div class="resumo-subtitulo">Compras e Manutenção</div></div>''', unsafe_allow_html=True)
        
    with c3:
        st.markdown(f'''<div class="resumo-card" style="border-top-color:#2e7d32;"><span>Logística</span>
                    <div class="resumo-valor">R$ {total_veiculos:,.2f}</div>
                    <div class="resumo-subtitulo">Contratos de Veículos</div></div>''', unsafe_allow_html=True)

    with c4:
        st.markdown(f'''<div class="resumo-card" style="border-top-color:#3b82f6;"><span>Viagens</span>
                    <div class="resumo-valor">R$ {total_viagens:,.2f}</div>
                    <div class="resumo-subtitulo">Reembolsos e Projetos</div></div>''', unsafe_allow_html=True)

    # VISUALIZAÇÃO DETALHADA
    st.write("---")
    tab1, tab2, tab3 = st.tabs(["📊 Custos Fixos/Variáveis", "🚗 Gestão de Frota", "✈️ Relatório de Viagens"])

    with tab1:
        st.subheader("Detalhamento de Compras e Manutenção")
        st.dataframe(dados['custos'], use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Controle de Veículos por Condutor")
        st.dataframe(dados['veiculos'], use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Análise de Deslocamentos")
        st.dataframe(dados['viagens'], use_container_width=True, hide_index=True)

    # Rodapé Técnico
    st.caption(f"Base de dados: {dados['file_name']} | Sistema de Leitura Automática Ativo")

else:
    st.error("⚠️ Ficheiro 'facilities_2026.csv' não encontrado no servidor.")
    st.info("Certifique-se de que o arquivo foi subido na raiz do repositório GitHub.")
    if st.button("Verificar ficheiros no repositório"):
        st.code(os.listdir('.'))

# Sidebar para Filtros Futuros
with st.sidebar:
    st.title("Menu de Controle")
    st.info("Projeto: Facilities Intelligence")
    if st.button("Limpar Cache"):
        st.cache_data.clear()
