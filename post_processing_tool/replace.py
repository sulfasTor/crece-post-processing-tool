import pandas as pd
from datetime import datetime

def post_proces_df(filename):
    try:
        df = pd.read_csv(filename, encoding="utf-8", encoding_errors="ignore")
    except Exception as e:
        raise Exception(f"Something went wrong reading csv: {str(e)}")
    print(df.columns)
    df["LAST_CHANGED"] = pd.to_datetime(df["LAST_CHANGED"])
    df["MES"] = df["LAST_CHANGED"].dt.strftime("%-m")
    df["DIA"] = df["LAST_CHANGED"].dt.strftime("%-d")
    df["LAST_CHANGED"] = df["LAST_CHANGED"].dt.strftime("%d/%m/%Y")
    df = df[ ["LAST_CHANGED", "MES", "DIA"] + df.columns[:10].tolist() ]
    print("Succesfully post processed csv")

    return df


def write_csv(df, out_dir):
    filename = f'{out_dir}/crece_nuevos_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.csv'
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        raise Exception(f"Couldn't write csv: {str(e)}")
    print("Succesfully wrote CSV")