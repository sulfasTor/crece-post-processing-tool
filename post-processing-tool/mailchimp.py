import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def get_member_list_df():
    # https://mailchimp.com/developer/marketing/api/list-members/
    members = []
    username = os.environ.get('MAILCHIMP_USERNAME')
    api_key = os.environ.get('MAILCHIMP_API_KEY')
    mailchimp_domain = os.environ.get('MAILCHIMP_DOMAIN', 'us21')
    list_id = os.environ.get('MAILCHIMP_LIST_ID', '601b55d9dc')
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
    df = pd.DataFrame(members)
    df['last_changed'] = pd.to_datetime(df['last_changed'])
    df['month'] = df['last_changed'].dt.strftime('%-m')
    df['day'] = df['last_changed'].dt.strftime('%-d')
    df['last_changed'] = df['last_changed'].dt.strftime('%d/%m/%Y')
    df = df[ ['last_changed', 'month', 'day'] + [f for f in fields if f != 'last_changed'] ]

    return df
