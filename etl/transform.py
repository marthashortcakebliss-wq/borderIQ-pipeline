import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def extract_tariffs() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "sample_tariffs.csv", dtype={"hs_code": str})
    df["effective_date"] = pd.to_datetime(df["effective_date"])
    return df


def extract_freight_rates() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "sample_freight_rates.csv")
    df["quote_date"] = pd.to_datetime(df["quote_date"])
    return df


def extract_disruptions() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "sample_disruptions.csv")
    df["reported_date"] = pd.to_datetime(df["reported_date"])
    df["resolved_date"] = pd.to_datetime(df["resolved_date"], errors="coerce")
    return df
