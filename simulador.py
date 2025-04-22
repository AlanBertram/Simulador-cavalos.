
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Simulator Trader Horse AB", layout="wide")

st.title("🏇 Simulator Trader Horse AB")
st.markdown("Simule corridas com base nas odds e visualize os resultados de forma interativa.")

uploaded_file = st.file_uploader("📥 Envie um arquivo CSV com nomes e odds dos cavalos", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'Nome' in df.columns and 'Odd' in df.columns:
        num_simulacoes = st.slider("Número de corridas simuladas", 100, 10000, 1000)
        
        resultados = {nome: [] for nome in df['Nome']}
        
        for _ in range(num_simulacoes):
            probabilidades = 1 / df['Odd']
            probabilidades /= probabilidades.sum()
            chegada = np.random.choice(df['Nome'], size=len(df), replace=False, p=probabilidades)
            for pos, cavalo in enumerate(chegada):
                resultados[cavalo].append(pos + 1)
        
        estatisticas = []
        for cavalo in df['Nome']:
            posicoes = resultados[cavalo]
            estatisticas.append({
                "Cavalo": cavalo,
                "Vitórias": posicoes.count(1),
                "Posição Média": np.mean(posicoes),
                "Desvio Padrão": np.std(posicoes)
            })
        
        stats_df = pd.DataFrame(estatisticas).sort_values("Vitórias", ascending=False)
        st.dataframe(stats_df, use_container_width=True)

        fig = px.bar(stats_df, x="Cavalo", y="Vitórias", title="Vitórias por Cavalo")
        st.plotly_chart(fig, use_container_width=True)

        csv = stats_df.to_csv(index=False).encode('utf-8')
        st.download_button("📤 Baixar resultados em CSV", csv, "resultados_simulador.csv", "text/csv")
    else:
        st.error("O CSV deve conter as colunas: 'Nome' e 'Odd'.")
else:
    st.info("Aguardando envio de um arquivo CSV...")
