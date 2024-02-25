import os
import requests
import pandas as pd
from datetime import datetime, timedelta


def get_member_list_df():
    # https://mailchimp.com/developer/marketing/api/list-members/list-members-info/
    # https://mailchimp.com/developer/marketing/api/list-members/
    members = []
    username = os.environ.get("MAILCHIMP_USERNAME")
    api_key = os.environ.get("MAILCHIMP_API_KEY")
    mailchimp_domain = os.environ.get("MAILCHIMP_DOMAIN", "us21")
    list_id = os.environ.get("MAILCHIMP_LIST_ID", "601b55d9dc")
    since_last_changed = (datetime.now() - timedelta(weeks=2)).strftime(
        "%Y-%m-%d %H:%M:$S"
    )
    params = {
        "since_last_changed": since_last_changed,
        "count": "1000",
        # "fields": [
        #     "LAST_CHANGED",
        #     "EMAIL_ADDRESS",
        #     "MERGE_FIELDS"
        # ],
        "offset": "0",
    }
    resp = requests.get(
        f"https://{mailchimp_domain}.api.mailchimp.com/3.0/lists/{list_id}/members",
        params=params,
        auth=(username, api_key),
    )
    print("### Downloaded members")
    if resp.ok:
        data = resp.json()
    else:
        err = resp.json()
        raise Exception(
            f'Something went wrong downloading members: {err["title"]}: {err["detail"]}'
        )
    if len(data["members"]) == 0:
        return None
    fields = [
        "last_changed",
        "email_address"
    ]
    merge_fields = {
        "FNAME": "NAME",
        "LNAME": "LAST_NAME",
        "MMERGE7": "CITY", # Ciudad
        "MMERGE3": "CAMPUS", # Camous
        "PHONE": "PHONE",
        "MMERGE5": "IN_SITE", # Formato
        "MMERGE6": "STATE", # Estado
        "MMERGE8": "PRAYER_REQUEST", # Pedido de oracion
        "MMERGE9": "FIRST_TIME", # Primera vez en MV
    }
    for m in data['members']:
        mb = {
            k: m.get(k) for k in fields
        }
        mb.update({
            v: m['merge_fields'].get(k) for k, v in merge_fields.items()
        })
        members.append(mb)

    df = pd.DataFrame(members)
    df["last_changed"] = pd.to_datetime(df["last_changed"])
    df["month"] = df["last_changed"].dt.strftime("%-m")
    df["day"] = df["last_changed"].dt.strftime("%-d")
    df["last_changed"] = df["last_changed"].dt.strftime("%d/%m/%Y")

    return df
