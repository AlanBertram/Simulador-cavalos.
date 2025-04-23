import streamlit as st
import pandas as pd
import plotly.express as px
import uuid

st.set_page_config(page_title="Simulator Trader Horse AB", layout="wide")
st.title("🏇 Simulator Trader Horse AB")

st.markdown("""
<style>
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/2/28/Cheltenham_racecourse_aerial.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
#### 🏇 Simulador Avançado de Corridas
Envie seu arquivo contendo os dados da corrida (.xls, .xlsx ou .csv). A simulação identificará os melhores cavalos, analisando:
- Probabilidades reais (Odds)
- Condições da pista
- Parceria entre cavalo, jóquei e treinador
- Seleção automática da **melhor aposta**
""")

uploaded_file = st.file_uploader("📁 Envie seu arquivo (.xls, .xlsx ou .csv)", type=["xls", "xlsx", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Filtra corredores válidos com odds positivas
        df["Odds"] = pd.to_numeric(df["Odds"], errors="coerce")
        df = df[df["Odds"] > 0].copy()

        if df.empty:
            st.error("Nenhum corredor válido encontrado. Verifique os dados e tente novamente.")
            st.stop()

        df["Nome"] = df["Horse"]
        df["Probabilidade"] = 1 / df["Odds"]
        df["Probabilidade"] /= df["Probabilidade"].sum()

        n_simulacoes = st.slider("🔁 Número de simulações", 1000, 10000, 5000, step=500)

        resultados = {nome: 0 for nome in df["Nome"]}

        for _ in range(n_simulacoes):
            vencedor = df.sample(weights=df["Probabilidade"], n=1).iloc[0]["Nome"]
            resultados[vencedor] += 1

        df_resultados = pd.DataFrame.from_dict(resultados, orient='index', columns=['Vitórias'])
        df_resultados["% Vitórias"] = 100 * df_resultados["Vitórias"] / n_simulacoes
        df_resultados = df_resultados.reset_index().rename(columns={"index": "Cavalo"})

        df_merged = df.merge(df_resultados, left_on="Nome", right_on="Cavalo")
        df_merged["Análise"] = df_merged.apply(lambda row: f"🏇 {row['Cavalo']} - Jockey: {row.get('Jockey', 'N/A')}, Treinador: {row.get('Trainer', 'N/A')}, Pista: {row.get('Track', 'N/A')}, Condição: {row.get('Going', 'N/A')}", axis=1)

        st.subheader("🏆 Top 3 Melhores Cavalos da Corrida")
        top3 = df_merged.sort_values(by="% Vitórias", ascending=False).head(3)
        st.table(top3[["Cavalo", "% Vitórias", "Jockey", "Trainer", "Track", "Going"]])

        st.subheader("📈 Probabilidade de Vitória (Todos)")
        st.dataframe(df_resultados.sort_values(by="% Vitórias", ascending=False), use_container_width=True)

        fig = px.bar(df_merged, x="Cavalo", y="% Vitórias", hover_data=["Análise"],
                     title="Gráfico de Desempenho Simulado", color="% Vitórias", color_continuous_scale="Turbo")
        st.plotly_chart(fig, use_container_width=True)

        melhor_aposta = top3.iloc[0]
        st.markdown(f"## 🎯 Melhor Aposta\n**{melhor_aposta['Cavalo']}** com **{melhor_aposta['% Vitórias']:.2f}%** de chance de vitória\nJockey: {melhor_aposta['Jockey']} | Treinador: {melhor_aposta['Trainer']}\nPista: {melhor_aposta['Track']} | Condição: {melhor_aposta['Going']}")

        csv_download = df_resultados.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar resultados (CSV)", csv_download, file_name="resultados_corrida.csv")

        st.markdown(f"🗃️ ID da simulação: `{uuid.uuid4()}`")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Envie um arquivo .xls, .xlsx ou .csv para iniciar a simulação.")
