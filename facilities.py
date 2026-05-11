import streamlit as st
import pandas as pd
import io

def carregar_dados_marco():
    # Simulando a leitura do arquivo enviado
    file_path = "FACILITIES - DADOS PARA APRESENTAÇÃO.xlsx - MAR 2026.csv"
    df = pd.read_csv(file_path, skiprows=1) # Pula o cabeçalho vazio do DNA da planilha
    
    # Lógica de Limpeza 'Padrão Ouro'
    # Aqui filtramos as seções: *CUSTOS, *VEÍCULOS, *VIAGENS
    custos_op = df.iloc[0:6, [1, 2]] # Colunas DESCRIÇÃO e VALOR
    custos_op.columns = ['Descricao', 'Valor']
    
    # Tratamento de Tipagem Forte (Float) conforme regra absoluta
    custos_op['Valor'] = custos_op['Valor'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)
    
    return custos_op

# UI - DNA VISUAL
st.markdown('<div class="hero-title">Facilities Intelligence - Março 2026</div>', unsafe_allow_html=True)

dados = carregar_dados_marco()
total_mar = dados['Valor'].sum()

# Cards de Resumo Estilizados
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'''
        <div class="resumo-card">
            <span>Total Custos Operacionais</span>
            <div class="resumo-valor">R$ {total_mar:,.2f}</div>
        </div>
    ''', unsafe_allow_html=True)