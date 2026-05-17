from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
SP_DATA_PATH = DATA_DIR / "base_tratada.csv"
BR_DATA_PATH = DATA_DIR / "base_brasil_tratada.csv"
MIN_BR_ACCIDENTS = 30
MIN_CITY_ACCIDENTS = 15

SEVERITY_HELP = (
    "Indice de severidade = 5 x mortos + 3 x feridos graves + 1 x feridos leves. "
    "Ele sintetiza o peso humano dos acidentes sem depender de bases externas."
)


def render_dashboard() -> None:
    st.set_page_config(
        page_title="Acidentes em Rodovias Federais de SP",
        layout="wide",
    )
    sp_df, br_df = load_data()

    st.title("Acidentes em Rodovias Federais de Sao Paulo")
    st.caption(
        "Painel academico com foco em SP e benchmark nacional construido a partir da base local do projeto."
    )

    render_context(sp_df, br_df)
    filtered_sp, filtered_br = render_filters(sp_df, br_df)
    render_kpis(filtered_sp)
    render_comparison(filtered_sp, filtered_br)
    render_time_analysis(filtered_sp)
    render_risk_panels(filtered_sp)
    render_geography(filtered_sp)
    render_detail_table(filtered_sp)


@st.cache_data(show_spinner="Carregando bases tratadas...")
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    sp_df = pd.read_csv(SP_DATA_PATH, sep=";")
    br_df = pd.read_csv(BR_DATA_PATH, sep=";")

    for df in (sp_df, br_df):
        df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")

    return sp_df, br_df


def render_context(sp_df: pd.DataFrame, br_df: pd.DataFrame) -> None:
    start_date = br_df["data"].min()
    end_date = br_df["data"].max()
    if pd.isna(start_date) or pd.isna(end_date):
        period_label = "Periodo indisponivel"
    else:
        period_label = f"{start_date:%d/%m/%Y} a {end_date:%d/%m/%Y}"

    st.info(
        "Recorte principal: acidentes em rodovias federais no estado de Sao Paulo. "
        "Benchmark: distribuicoes nacionais calculadas sobre a mesma base local."
    )
    st.markdown(
        f"**Cobertura efetiva da base versionada:** {period_label}. "
        "As metricas respeitam apenas o periodo realmente presente no repositório."
    )


def render_filters(
    sp_df: pd.DataFrame, br_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    st.sidebar.header("Filtros")

    months = sorted(sp_df["mes_label"].dropna().unique().tolist())
    selected_months = st.sidebar.multiselect(
        "Meses",
        options=months,
        default=months,
    )

    br_options = sorted([value for value in sp_df["br"].dropna().unique().tolist() if value != ""])
    selected_brs = st.sidebar.multiselect(
        "Rodovias (BR)",
        options=br_options,
        default=br_options,
    )

    class_options = sorted(sp_df["classificacao_acidente"].dropna().unique().tolist())
    selected_classes = st.sidebar.multiselect(
        "Classificacao",
        options=class_options,
        default=class_options,
    )

    phase_options = sorted(sp_df["fase_dia"].dropna().unique().tolist())
    selected_phases = st.sidebar.multiselect(
        "Fase do dia",
        options=phase_options,
        default=phase_options,
    )

    city_options = sorted(sp_df["municipio"].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "Municipios de SP",
        options=city_options,
        default=city_options,
    )

    sp_mask = (
        sp_df["mes_label"].isin(selected_months)
        & sp_df["br"].isin(selected_brs)
        & sp_df["classificacao_acidente"].isin(selected_classes)
        & sp_df["fase_dia"].isin(selected_phases)
        & sp_df["municipio"].isin(selected_cities)
    )
    br_mask = (
        br_df["mes_label"].isin(selected_months)
        & br_df["br"].isin(selected_brs)
        & br_df["classificacao_acidente"].isin(selected_classes)
        & br_df["fase_dia"].isin(selected_phases)
    )

    filtered_sp = sp_df.loc[sp_mask].copy()
    filtered_br = br_df.loc[br_mask].copy()

    if filtered_sp.empty:
        st.warning("Os filtros selecionados nao retornaram acidentes em SP.")

    return filtered_sp, filtered_br


def render_kpis(df: pd.DataFrame) -> None:
    st.subheader("Indicadores principais")

    total_accidents = len(df)
    total_deaths = int(df["mortos"].sum()) if not df.empty else 0
    severe_injuries = int(df["feridos_graves"].sum()) if not df.empty else 0
    severity_index = int(df["indice_severidade"].sum()) if not df.empty else 0
    fatal_rate = safe_rate(df["acidente_fatal"].sum(), total_accidents)
    severe_rate = safe_rate(df["acidente_grave"].sum(), total_accidents)

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("Acidentes em SP", f"{total_accidents:,}".replace(",", "."))
    col2.metric("Mortes registradas", f"{total_deaths:,}".replace(",", "."))
    col3.metric("Feridos graves", f"{severe_injuries:,}".replace(",", "."))
    col4.metric("Indice de severidade", f"{severity_index:,}".replace(",", "."))
    col5.metric("Taxa de fatalidade", format_percent(fatal_rate))
    col6.metric("Taxa de acidentes graves", format_percent(severe_rate))

    st.caption(SEVERITY_HELP)


def render_comparison(sp_df: pd.DataFrame, br_df: pd.DataFrame) -> None:
    st.subheader("SP x Brasil")

    col1, col2, col3 = st.columns(3)
    col1.metric("Participacao de SP no total filtrado", format_percent(safe_rate(len(sp_df), len(br_df))))
    col2.metric(
        "Taxa fatal em SP",
        format_percent(safe_rate(sp_df["acidente_fatal"].sum(), len(sp_df))),
        delta=delta_percent(
            safe_rate(sp_df["acidente_fatal"].sum(), len(sp_df)),
            safe_rate(br_df["acidente_fatal"].sum(), len(br_df)),
        ),
    )
    col3.metric(
        "Taxa grave em SP",
        format_percent(safe_rate(sp_df["acidente_grave"].sum(), len(sp_df))),
        delta=delta_percent(
            safe_rate(sp_df["acidente_grave"].sum(), len(sp_df)),
            safe_rate(br_df["acidente_grave"].sum(), len(br_df)),
        ),
    )

    line_col, bar_col = st.columns((1.4, 1))
    with line_col:
        st.markdown("**Evolucao mensal de acidentes**")
        monthly_sp = (
            sp_df.groupby("mes_label", as_index=False)
            .size()
            .rename(columns={"size": "SP"})
        )
        monthly_br = (
            br_df.groupby("mes_label", as_index=False)
            .size()
            .rename(columns={"size": "Brasil"})
        )
        monthly = monthly_sp.merge(monthly_br, on="mes_label", how="outer").fillna(0)
        monthly = monthly.sort_values("mes_label")
        if monthly.empty:
            st.info("Sem dados para a comparacao mensal com os filtros atuais.")
        else:
            st.line_chart(monthly.set_index("mes_label"))

    with bar_col:
        st.markdown("**Severidade por fase do dia**")
        phase_compare = pd.concat(
            [
                build_share_table(sp_df, "fase_dia", "SP"),
                build_share_table(br_df, "fase_dia", "Brasil"),
            ],
            ignore_index=True,
        )
        if phase_compare.empty:
            st.info("Sem dados para a comparacao por fase do dia.")
        else:
            st.bar_chart(
                phase_compare.pivot(index="fase_dia", columns="escopo", values="participacao")
            )


def render_time_analysis(df: pd.DataFrame) -> None:
    st.subheader("Padroes temporais e causas")

    left_col, right_col = st.columns((1.2, 1))

    with left_col:
        st.markdown("**Mapa de calor: dia da semana x hora**")
        heatmap = (
            df.pivot_table(
                index="dia_semana",
                columns="hora",
                values="id",
                aggfunc="count",
                fill_value=0,
            )
            .reindex(
                [
                    "segunda-feira",
                    "terca-feira",
                    "quarta-feira",
                    "quinta-feira",
                    "sexta-feira",
                    "sabado",
                    "domingo",
                ],
                fill_value=0,
            )
        )
        if heatmap.empty:
            st.info("Sem dados suficientes para o mapa de calor.")
        else:
            st.dataframe(heatmap, width="stretch")

    with right_col:
        st.markdown("**Janelas criticas do dia**")
        critical_windows = (
            df.groupby("faixa_horaria", as_index=False)
            .agg(
                acidentes=("id", "count"),
                acidentes_graves=("acidente_grave", "sum"),
                acidentes_fatais=("acidente_fatal", "sum"),
            )
        )
        if critical_windows.empty:
            st.info("Sem dados suficientes para avaliar janelas criticas.")
        else:
            critical_windows["taxa_grave"] = critical_windows.apply(
                lambda row: safe_rate(row["acidentes_graves"], row["acidentes"]), axis=1
            )
            critical_windows["taxa_fatal"] = critical_windows.apply(
                lambda row: safe_rate(row["acidentes_fatais"], row["acidentes"]), axis=1
            )
            st.dataframe(
                critical_windows.sort_values("taxa_grave", ascending=False),
                width="stretch",
                hide_index=True,
            )

    st.markdown("**Causas com maior risco**")
    cause_risk = (
        df.groupby("causa_acidente", as_index=False)
        .agg(
            acidentes=("id", "count"),
            acidentes_graves=("acidente_grave", "sum"),
            acidentes_fatais=("acidente_fatal", "sum"),
            indice_severidade=("indice_severidade", "sum"),
        )
    )
    if cause_risk.empty:
        st.info("Sem dados para o ranking de causas.")
        return

    cause_risk = cause_risk[cause_risk["acidentes"] >= 20].copy()
    cause_risk["taxa_grave"] = cause_risk.apply(
        lambda row: safe_rate(row["acidentes_graves"], row["acidentes"]), axis=1
    )
    cause_risk["taxa_fatal"] = cause_risk.apply(
        lambda row: safe_rate(row["acidentes_fatais"], row["acidentes"]), axis=1
    )
    cause_risk = cause_risk.sort_values(
        ["taxa_grave", "indice_severidade"], ascending=False
    ).head(10)
    st.dataframe(cause_risk, width="stretch", hide_index=True)


def render_risk_panels(df: pd.DataFrame) -> None:
    st.subheader("Hotspots e fatores de risco")

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("**Rodovias com maior criticidade**")
        br_risk = build_risk_table(df, "br", MIN_BR_ACCIDENTS)
        if br_risk.empty:
            st.info("Sem volume suficiente para ranquear rodovias.")
        else:
            st.dataframe(br_risk.head(10), width="stretch", hide_index=True)

    with right_col:
        st.markdown("**Municipios com maior criticidade**")
        city_risk = build_risk_table(df, "municipio", MIN_CITY_ACCIDENTS)
        if city_risk.empty:
            st.info("Sem volume suficiente para ranquear municipios.")
        else:
            st.dataframe(city_risk.head(10), width="stretch", hide_index=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Top tipos de acidente**")
        top_types = df["tipo_acidente"].value_counts().head(10)
        if top_types.empty:
            st.info("Sem dados para os tipos de acidente.")
        else:
            st.bar_chart(top_types)
    with c2:
        st.markdown("**Clima e severidade**")
        weather = (
            df.groupby("condicao_metereologica", as_index=False)
            .agg(acidentes=("id", "count"), indice_severidade=("indice_severidade", "sum"))
            .sort_values("indice_severidade", ascending=False)
            .head(10)
        )
        if weather.empty:
            st.info("Sem dados para o clima.")
        else:
            st.bar_chart(weather.set_index("condicao_metereologica"))
    with c3:
        st.markdown("**Urbano x nao urbano**")
        urban = (
            df.groupby("uso_solo", as_index=False)
            .agg(
                acidentes=("id", "count"),
                acidentes_graves=("acidente_grave", "sum"),
                indice_severidade=("indice_severidade", "sum"),
            )
            .set_index("uso_solo")
        )
        if urban.empty:
            st.info("Sem dados para o recorte urbano.")
        else:
            st.bar_chart(urban)


def render_geography(df: pd.DataFrame) -> None:
    st.subheader("Distribuicao geografica")
    map_df = df.dropna(subset=["latitude_num", "longitude_num"])[
        ["latitude_num", "longitude_num", "municipio", "br", "indice_severidade"]
    ].rename(columns={"latitude_num": "lat", "longitude_num": "lon"})
    if map_df.empty:
        st.info("Sem coordenadas validas para exibir o mapa.")
        return
    st.map(map_df, size="indice_severidade", color="#c2410c", width="stretch")


def render_detail_table(df: pd.DataFrame) -> None:
    st.subheader("Tabela analitica")
    selected_columns = [
        "data",
        "municipio",
        "br",
        "causa_acidente",
        "tipo_acidente",
        "classificacao_acidente",
        "fase_dia",
        "uso_solo",
        "mortos",
        "feridos_graves",
        "feridos_leves",
        "indice_severidade",
    ]
    if df.empty:
        st.info("Sem registros para exibir na tabela final.")
        return
    st.dataframe(
        df[selected_columns].sort_values("data"), width="stretch", hide_index=True
    )


def build_share_table(df: pd.DataFrame, column: str, scope_label: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[column, "participacao", "escopo"])
    grouped = df[column].value_counts(normalize=True).mul(100).round(2).rename("participacao")
    table = grouped.reset_index().rename(columns={"index": column})
    table["escopo"] = scope_label
    return table


def build_risk_table(df: pd.DataFrame, dimension: str, min_accidents: int) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    risk = (
        df.groupby(dimension, as_index=False)
        .agg(
            acidentes=("id", "count"),
            mortos=("mortos", "sum"),
            feridos_graves=("feridos_graves", "sum"),
            indice_severidade=("indice_severidade", "sum"),
        )
    )
    risk = risk[risk["acidentes"] >= min_accidents].copy()
    if risk.empty:
        return risk

    risk["taxa_fatal"] = risk.apply(
        lambda row: safe_rate(row["mortos"], row["acidentes"]), axis=1
    )
    risk["taxa_grave"] = risk.apply(
        lambda row: safe_rate(row["mortos"] + row["feridos_graves"], row["acidentes"]),
        axis=1,
    )
    return risk.sort_values(
        ["taxa_grave", "indice_severidade", "acidentes"], ascending=False
    )


def safe_rate(numerator: float, denominator: float) -> float:
    if not denominator:
        return 0.0
    return float(numerator) / float(denominator)


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def delta_percent(current: float, baseline: float) -> str:
    delta = (current - baseline) * 100
    return f"{delta:+.1f} p.p."


if __name__ == "__main__":
    render_dashboard()
