from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
SOURCE_PATH = DATA_DIR / "base_original.csv"
SP_OUTPUT_PATH = DATA_DIR / "base_tratada.csv"
BR_OUTPUT_PATH = DATA_DIR / "base_brasil_tratada.csv"

NUMERIC_COLUMNS = [
    "pessoas",
    "mortos",
    "feridos_leves",
    "feridos_graves",
    "ilesos",
    "ignorados",
    "feridos",
    "veiculos",
]

FLOAT_COLUMNS = ["km", "latitude", "longitude"]
DAY_ORDER = {
    "segunda-feira": 0,
    "terca-feira": 1,
    "terça-feira": 1,
    "quarta-feira": 2,
    "quinta-feira": 3,
    "sexta-feira": 4,
    "sabado": 5,
    "sábado": 5,
    "domingo": 6,
}


def load_source() -> pd.DataFrame:
    return pd.read_csv(SOURCE_PATH, sep=";", encoding="latin-1")


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    text_columns = df.select_dtypes(include="object").columns
    for column in text_columns:
        df[column] = df[column].fillna("").astype(str).str.strip()
    return df


def cast_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)

    for column in FLOAT_COLUMNS:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .replace({"": None, "nan": None})
        )
        df[f"{column}_num"] = pd.to_numeric(df[column], errors="coerce")
    return df


def derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["data"] = pd.to_datetime(df["data_inversa"], errors="coerce")
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["mes_label"] = df["data"].dt.strftime("%Y-%m")
    df["hora"] = pd.to_datetime(df["horario"], format="%H:%M:%S", errors="coerce").dt.hour
    df["faixa_horaria"] = df["hora"].apply(classify_time_window)
    df["acidente_fatal"] = (df["mortos"] > 0).astype(int)
    df["acidente_grave"] = ((df["mortos"] + df["feridos_graves"]) > 0).astype(int)
    df["indice_severidade"] = (
        (df["mortos"] * 5) + (df["feridos_graves"] * 3) + df["feridos_leves"]
    )
    df["dia_semana"] = df["dia_semana"].replace({"terça-feira": "terca-feira", "sábado": "sabado"})
    df["ordem_dia_semana"] = df["dia_semana"].map(DAY_ORDER).fillna(7).astype(int)
    df["data"] = df["data"].dt.strftime("%Y-%m-%d")
    return df


def classify_time_window(hour: float) -> str:
    if pd.isna(hour):
        return "Nao informado"
    if 0 <= hour < 6:
        return "Madrugada"
    if 6 <= hour < 12:
        return "Manha"
    if 12 <= hour < 18:
        return "Tarde"
    return "Noite"


def build_treated_frames(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = normalize_text_columns(df.copy())
    df = cast_numeric_columns(df)
    df = derive_columns(df)
    df = df[df["municipio"] != ""].copy()

    br_df = df.sort_values(["data", "uf", "municipio", "id"]).reset_index(drop=True)
    sp_df = br_df[br_df["uf"] == "SP"].reset_index(drop=True)

    return sp_df, br_df


def save_outputs(sp_df: pd.DataFrame, br_df: pd.DataFrame) -> None:
    sp_df.to_csv(SP_OUTPUT_PATH, sep=";", index=False, encoding="utf-8")
    br_df.to_csv(BR_OUTPUT_PATH, sep=";", index=False, encoding="utf-8")


def main() -> None:
    print("Carregando base original...")
    source_df = load_source()
    print("Gerando bases tratadas para SP e Brasil...")
    sp_df, br_df = build_treated_frames(source_df)
    save_outputs(sp_df, br_df)
    print(f"Base SP gerada com {len(sp_df)} registros em: {SP_OUTPUT_PATH}")
    print(f"Base Brasil gerada com {len(br_df)} registros em: {BR_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
