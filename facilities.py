@st.cache_data
def carregar_dados_facilities():
    # Nome simplificado para evitar erros de servidor
    file_name = "dados_marco_2026.csv"
    
    if not os.path.exists(file_name):
        # Tenta procurar qualquer arquivo que contenha 'MAR 2026' caso o nome mude
        arquivos_no_repo = os.listdir('.')
        for f in arquivos_no_repo:
            if "MAR 2026" in f and f.endswith(".csv"):
                file_name = f
                break
        else:
            return None

    # Leitura com tratamento de erro
    try:
        df_raw = pd.read_csv(file_name, header=None)
        
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
    except Exception as e:
        st.error(f"Erro ao ler o ficheiro: {e}")
        return None
