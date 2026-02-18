import streamlit as st
import pandas as pd
import os
from traffic_analyzer import TrafficDataProcessor

st.set_page_config(layout="wide")

st.title("Dashboard de Análise de Simulação de Tráfego")
st.write("Faça o upload de um ou mais arquivos de relatório (.xls) para visualizar os resultados consolidados.")

# Uploader de arquivos
uploaded_files = st.file_uploader("Escolha os arquivos .xls", accept_multiple_files=True, type=['xls'])

if uploaded_files:
    # Diretório temporário para salvar os uploads
    temp_dir = "/home/ubuntu/temp_uploads"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Salvar arquivos para que o processador possa lê-los
    for uploaded_file in uploaded_files:
        with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

    # Processar os arquivos no diretório temporário
    processor = TrafficDataProcessor()
    results_df = processor.run(temp_dir)

    if results_df is not None and not results_df.empty:
        st.success(f"{len(uploaded_files)} arquivo(s) processado(s) com sucesso!")

        # Filtrar apenas os dados de sumário
        summary_df = results_df[results_df['Intervalo'] == 'Summary'].copy()

        if not summary_df.empty:
            st.header("Resultados do Sumário")
            st.write("Esta tabela mostra os valores consolidados para cada seção e direção nos arquivos processados.")
            
            # Renomear colunas para melhor visualização
            summary_df.rename(columns={
                'Secao': 'Seção',
                'Direcao': 'Direção',
                'Atraso_Total_min': 'Atraso Total (min)',
                'Atraso_Medio_seg_veic': 'Atraso Médio (s/veic)',
                'Tempo_Parada_min': 'Tempo de Parada (min)',
                'Tempo_Parada_Medio_seg_veic': 'Tempo de Parada Médio (s/veic)',
                'Num_Paradas': 'Nº de Paradas',
                'Media_Paradas_veic': 'Média de Paradas/veic'
            }, inplace=True)

            # Apresentar a tabela de sumário
            st.dataframe(summary_df)

            st.header("Visualização Gráfica do Sumário")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Atraso Médio por Direção")
                st.bar_chart(summary_df, x='Direcao', y='Atraso Médio (s/veic)')

            with col2:
                st.subheader("Número de Paradas por Direção")
                st.bar_chart(summary_df, x='Direcao', y='Nº de Paradas')

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Atraso Total (min) por Direção")
                st.bar_chart(summary_df, x='Direcao', y='Atraso Total (min)')

            with col4:
                st.subheader("Tempo de Parada Total (min) por Direção")
                st.bar_chart(summary_df, x='Direcao', y='Tempo de Parada (min)')

        else:
            st.warning("Nenhuma linha de 'Summary' foi encontrada nos arquivos processados.")

        # Opcional: Mostrar todos os dados
        if st.checkbox("Mostrar todos os dados (incluindo intervalos)"):
            st.header("Dados Completos")
            st.dataframe(results_df)
    else:
        st.error("Não foi possível processar os arquivos. Verifique o formato e o conteúdo.")

    # Limpar arquivos temporários
    for uploaded_file in uploaded_files:
        os.remove(os.path.join(temp_dir, uploaded_file.name))
    os.rmdir(temp_dir)
else:
    st.info("Aguardando o upload dos arquivos...")
