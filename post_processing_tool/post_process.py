import os
from datetime import datetime

import pandas as pd


def post_process_df(filename: str, out_dir: str):
    try:
        df = pd.read_csv(filename, encoding="utf-8", encoding_errors="ignore")
    except Exception as e:
        raise Exception(f"Something went wrong reading csv: {str(e)}")
    print(f'### Found csv with columns: {", ".join(df.columns.tolist())}')
    df["last_changed"] = pd.to_datetime(df["LAST_CHANGED"], format="%Y-%m-%d %H:%M:%S")
    df.sort_values(by=["last_changed"], ascending=False, inplace=True)
    df["MES"] = df["last_changed"].dt.strftime("%-m")
    df["DIA"] = df["last_changed"].dt.strftime("%-d")
    df["last_changed"] = df["last_changed"].dt.strftime("%d/%m/%Y")
    df = df[["last_changed", "MES", "DIA"] + df.columns[:10].tolist()]

    rename_fields = {
        "Nombre": "NAME",
        "Apellido": "LAST_NAME",
        "Ciudad": "CITY",  # Ciudad
        "Campus": "CAMPUS",  # Campus
        "Teléfono": "PHONE",
        "¿Desde qué ubicación conectaste con nosotros?": "IN_SITE",  # Formato
        "Si seleccionaste otro, menciona desde donde.": "STATE",  # Estado
        "Petición de oración": "PRAYER_REQUEST",  # Pedido de oracion
        "CUENTANOS DE TI": "FIRST_TIME",
    }
    df.rename(columns=rename_fields, inplace=True)

    print(f"Succesfully post processed csv: {filename}")
    full_path = write_csv(df, out_dir)
    return df, full_path


def write_csv(df: pd.DataFrame, out_dir: str):
    if df is None:
        raise Exception("Couldn't write csv: Empty dataframe.")
    filename = f'crece_nuevos_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.csv'
    full_path = os.path.join(out_dir, filename)
    try:
        df.to_csv(full_path, index=False)
    except Exception as e:
        raise Exception(f"Couldn't write csv: {str(e)}")
    print(f"### Succesfully wrote CSV at path: {full_path}")
    return full_path
