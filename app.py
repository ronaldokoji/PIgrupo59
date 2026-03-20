import pandas as pd
import streamlit as st

st.set_page_config(page_title="Acidentes em SP", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 Acidentes em Rodovias Federais - SP")
st.markdown("### 📊 Análise de acidentes em rodovias federais de São Paulo")

# Ler os dados
df = pd.read_csv("data/acidentes.csv", sep=";", encoding="latin1")

# Filtrar SP
df_sp = df[df["uf"] == "SP"].copy()
df_sp["municipio"] = df_sp["municipio"].str.title()

st.subheader("📊 Dados de São Paulo")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Dados de São Paulo")
    st.dataframe(df_sp.head())

with col2:
    st.subheader("⚠️ Total de mortes")
    total_mortes = df_sp["mortos"].sum()
    st.metric("Total de mortes em SP", total_mortes)

# -------- GRÁFICO POR CIDADE --------
st.subheader("📍 Top 10 cidades com mais acidentes")

acidentes_cidade = df_sp["municipio"].value_counts().head(10).sort_values()
st.bar_chart(acidentes_cidade)
st.subheader("📅 Acidentes por dia da semana")

dias = df_sp["dia_semana"].value_counts()
st.bar_chart(dias)

# -------- HORÁRIO --------
st.subheader("⏰ Acidentes por horário")

df_sp["horario"] = df_sp["horario"].astype(str)
horas = df_sp["horario"].str[:2].value_counts().sort_index()
st.line_chart(horas)
st.subheader("📈 Acidentes ao longo do tempo")

df_sp["data_inversa"] = pd.to_datetime(df_sp["data_inversa"])
acidentes_data = df_sp.groupby("data_inversa").size()

st.line_chart(acidentes_data)

# -------- MORTES --------
st.subheader("⚠️ Total de mortes")

total_mortes = df_sp["mortos"].sum()
st.metric("Total de mortes em SP", total_mortes)

# -------- FILTRO --------
st.sidebar.markdown("## 🎛️ Filtros")

cidade = st.sidebar.selectbox(
    "Escolha uma cidade",
    df_sp["municipio"].unique()
    
)

df_filtrado = df_sp[df_sp["municipio"] == cidade]

st.subheader(f"📌 Dados de {cidade}")
st.dataframe(df_filtrado)
st.markdown("---")
st.markdown("📌 Projeto de Análise de Dados - Acidentes em Rodovias Federais de SP")