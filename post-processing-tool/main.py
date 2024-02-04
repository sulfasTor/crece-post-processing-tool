from pprint import pprint

import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def post_proces_df(filename):
    try:
        df = pd.read_csv(filename, encoding='utf-8', encoding_errors='ignore')
    except Exception as e:
        raise Exception(f"Something went wrong reading csv: {str(e)}")
    print(df.columns)
    df['LAST_CHANGED'] = pd.to_datetime(df['LAST_CHANGED'])
    df['MES'] = df['LAST_CHANGED'].dt.strftime('%-m')
    df['DIA'] = df['LAST_CHANGED'].dt.strftime('%-d')
    df['LAST_CHANGED'] = df['LAST_CHANGED'].dt.strftime('%d/%m/%Y')
    df = df[ ['LAST_CHANGED', 'MES', 'DIA'] + df.columns[:10].tolist() ]
    print("Succesfully post processed csv")

    return df

def get_member_list(list_id):
    # https://mailchimp.com/developer/marketing/api/list-members/
    members = []
    username = os.environ.get('MAILCHIMP_USERNAME')
    api_key = os.environ.get('MAILCHIMP_API_KEY')
    mailchimp_domain = os.environ.get('MAILCHIMP_DOMAIN', 'us21')
    since_last_changed = (datetime.now()-timedelta(weeks=2)).strftime('%Y-%m-%d %H:%M:$S')
    params = {
        "since_last_changed": since_last_changed,
        "count": "1000",
        "exclude_fields": ['MEMBER_RATING', 'OPTIN_TIME',
                           'OPTIN_IP', 'CONFIRM_TIME', 'CONFIRM_IP', 'LATITUDE', 'LONGITUDE',
                           'GMTOFF', 'DSTOFF', 'TIMEZONE', 'CC', 'REGION', 'LEID',
                           'EUID', 'NOTES', 'TAGS'],
        "offset": "0",
    }
    resp = requests.get(f'https://{mailchimp_domain}.api.mailchimp.com/3.0/lists/{list_id}/members', params=params, auth=(username, api_key))
    print("download members")
    if resp.ok:
        data = resp.json()
    else:
        err = resp.json()
        raise Exception(f"Something went wrong downloading members: {err['title']}: {err['detail']}")
    fields = ['email_address', 'full_name', 'last_changed', 'location', 'merge_fields']
    for m in data['members']:
        members.append({
            f: m[f] for f in fields
        })
    return members

def write_csv(df, out_dir):
    filename = f"{out_dir}/crece_nuevos_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv"
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        raise Exception(f"Couldn't write csv: {str(e)}")
    print("Succesfully wrote CSV")

def main():
    try:
        membs = get_member_list('601b55d9dc')
        df = pd.DataFrame(membs)
        print(df)
        # df = post_proces_df('~/Downloads/subscribed_members_export_0e31a6fce9.csv')
        # write_csv(df, '~/Downloads')
    except Exception as e:
        print(f"FAIL, err: {str(e)}")
        return 1

    return 0

main()
