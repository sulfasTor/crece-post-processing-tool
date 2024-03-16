import os
import requests
import pandas as pd
from datetime import datetime, timedelta

_RESULTS_LIMIT=1000
_MAX_PAGINATION_ITERATIONS=10

def get_member_list_df():
    data = get_member_list()
    df = create_df(data)

    return df

def paginate_request(mailchimp_domain, list_id, params, auth):
    data = {"members": [], "total_items": 0}
    offset = 0
    iterations = 0
    params["offset"] = 0
    params["count"] = _RESULTS_LIMIT
    while True:
        resp = requests.get(
            f"https://{mailchimp_domain}.api.mailchimp.com/3.0/lists/{list_id}/members",
            params=params,
            auth=auth,
        )
        if resp.ok:
            d = resp.json()
        else:
            err = resp.json()
            raise Exception(
                f'Something went wrong downloading members: {err["title"]}: {err["detail"]}'
            )
        data["members"].extend(d["members"])
        params["offset"] = len(data["members"])
        if int(d["total_items"]) <= _RESULTS_LIMIT or iterations >= _MAX_PAGINATION_ITERATIONS:
            break
        iterations += 1

    return data

def get_member_list():
    # https://mailchimp.com/developer/marketing/api/list-members/list-members-info/
    # https://mailchimp.com/developer/marketing/api/list-members/
    username = os.environ.get("MAILCHIMP_USERNAME")
    api_key = os.environ.get("MAILCHIMP_API_KEY")
    mailchimp_domain = os.environ.get("MAILCHIMP_DOMAIN", "us21")
    list_id = os.environ.get("MAILCHIMP_LIST_ID", "601b55d9dc")
    since_last_changed = (datetime.now() - timedelta(weeks=105)).strftime(
        "%Y-%m-%d %H:%M:$S"
    )
    params = {
        "since_last_changed": since_last_changed,
        "fields": "total_items,members.last_changed,members.email_address,members.merge_fields",
    }
    data = paginate_request(mailchimp_domain, list_id, params, (username, api_key))
    print(f'### Downloaded {len(data["members"])} members')

    if len(data["members"]) == 0:
        return None

    return data


def create_df(data):
    fields = [
        "last_changed",
        "email_address"
    ]
    merge_fields = {
        "FNAME": "NAME",
        "LNAME": "LAST_NAME",
        "MMERGE7": "CITY", # Ciudad
        "MMERGE3": "CAMPUS", # Campus
        "PHONE": "PHONE",
        "MMERGE5": "IN_SITE", # Formato
        "MMERGE6": "STATE", # Estado
        "MMERGE8": "PRAYER_REQUEST", # Pedido de oracion
        "MMERGE9": "FIRST_TIME", # Primera vez en MV
    }
    members = []
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
    df.sort_values(by=["last_changed"], ascending=False, inplace=True)

    df = df[["last_changed", "day", "month", "NAME", "LAST_NAME", "email_address", "PHONE", "CITY", "CAMPUS", "IN_SITE", "STATE", "PRAYER_REQUEST", "FIRST_TIME"]]

    return df