import streamlit as st
import pandas as pd
import plotly.express as px
import uuid

st.set_page_config(page_title="Simulator Trader Horse AB", layout="wide")
st.title("🏇 Simulator Trader Horse AB")

st.markdown("""
#### Simulador de Corridas com Dados Reais
Envie um arquivo CSV completo de corrida (como fornecido por sites especializados) e visualize análises interativas baseadas nas **odds** dos cavalos.
""")

# Upload do CSV
uploaded_file = st.file_uploader("📁 Envie seu arquivo CSV completo de corrida", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Verificação automática das colunas essenciais
        if 'Horse' in df.columns and 'Odds' in df.columns:
            df["Nome"] = df["Horse"]
            df["Odd"] = df["Odds"]
        else:
            st.error("O CSV não contém as colunas 'Horse' e 'Odds'. Verifique seu arquivo.")
            st.stop()

        # Simulação simples baseada nas odds (quanto menor a odd, maior a chance)
        df["Probabilidade"] = 1 / df["Odd"]
        df["Probabilidade"] /= df["Probabilidade"].sum()

        n_simulacoes = st.slider("🔁 Número de corridas a simular", 1000, 10000, 5000, step=500)

        resultados = {nome: 0 for nome in df["Nome"]}

        for _ in range(n_simulacoes):
            vencedor = df.sample(weights=df["Probabilidade"], n=1).iloc[0]["Nome"]
            resultados[vencedor] += 1

        df_resultados = pd.DataFrame.from_dict(resultados, orient='index', columns=['Vitórias'])
        df_resultados["% Vitórias"] = 100 * df_resultados["Vitórias"] / n_simulacoes
        df_resultados = df_resultados.sort_values("Vitórias", ascending=False).reset_index().rename(columns={"index": "Cavalo"})

        # Tabela com os dados extras
        st.subheader("📊 Tabela de Resultados")
        st.dataframe(df_resultados, use_container_width=True)

        # Gráfico interativo com todos os dados dos cavalos como hover
        df_merged = df.merge(df_resultados, left_on="Nome", right_on="Cavalo")
        df_merged["Info"] = df_merged.apply(lambda row: f"Idade: {row['HorseAge']} | Jockey: {row['Jockey']} | Treinador: {row['Trainer']}\nPista: {row['Track']} | Peso: {row['Weight_Pounds']} | Classe: {row['Class']}", axis=1)

        fig = px.bar(df_merged, x="Cavalo", y="% Vitórias", hover_data=["Info"], title="🏆 Desempenho Simulado por Cavalo")
        st.plotly_chart(fig, use_container_width=True)

        # Download dos resultados
        csv_download = df_resultados.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar resultados em CSV", csv_download, file_name="resultados_simulacao.csv")

        # Histórico (pode ser expandido para banco de dados futuramente)
        st.markdown(f"🗃️ ID único da simulação: `{uuid.uuid4()}`")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Envie um arquivo CSV para iniciar a simulação.")
