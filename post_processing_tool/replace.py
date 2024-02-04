import os
from datetime import datetime

import pandas as pd


def post_proces_df(filename):
    try:
        df = pd.read_csv(filename, encoding="utf-8", encoding_errors="ignore")
    except Exception as e:
        raise Exception(f"Something went wrong reading csv: {str(e)}")
    print(f'### Found csv with columns: {", ".join(df.columns.tolist())}')
    df["LAST_CHANGED"] = pd.to_datetime(df["LAST_CHANGED"])
    df["MES"] = df["LAST_CHANGED"].dt.strftime("%-m")
    df["DIA"] = df["LAST_CHANGED"].dt.strftime("%-d")
    df["LAST_CHANGED"] = df["LAST_CHANGED"].dt.strftime("%d/%m/%Y")
    df = df[["LAST_CHANGED", "MES", "DIA"] + df.columns[:10].tolist()]
    print(f"Succesfully post processed csv: {filename}")

    return df


def write_csv(df, out_dir):
    filename = f'crece_nuevos_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.csv'
    full_path = os.path.join(out_dir, filename)
    try:
        df.to_csv(full_path, index=False)
    except Exception as e:
        raise Exception(f"Couldn't write csv: {str(e)}")
    print(f"### Succesfully wrote CSV at path: {full_path}")
