import pandas as pd
from datetime import datetime

def post_proces_df(filename):
    df = pd.read_csv(filename, encoding='utf-8', encoding_errors='ignore')
    df['LAST_CHANGED'] = pd.to_datetime(df['LAST_CHANGED'])
    df['MES'] = df['LAST_CHANGED'].dt.strftime('%-m')
    df['DIA'] = df['LAST_CHANGED'].dt.strftime('%-d')
    df['LAST_CHANGED'] = df['LAST_CHANGED'].dt.strftime('%d/%m/%Y')
    df = df[ ['LAST_CHANGED', 'MES', 'DIA'] + df.columns[:10].tolist() ]
    print("Succesfully post processed csv")

    return df

def write_csv(df, out_dir):
    filename = f"{out_dir}/crece_nuevos_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv"
    df.to_csv(filename, index=False)
    print("Succesfully wrote CSV")

def main():
    df = post_proces_df('~/Downloads/subscribed_members_export_0e31a6fce9.csv')
    write_csv(df, '~/Downloads')
    return 0

main()