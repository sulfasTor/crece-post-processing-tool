import argparse
import os
import pathlib
from datetime import datetime, timedelta

import pandas as pd
import requests


def get_member_list_df():
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
        "exclude_fields": [
            "MEMBER_RATING",
            "OPTIN_TIME",
            "OPTIN_IP",
            "CONFIRM_TIME",
            "CONFIRM_IP",
            "LATITUDE",
            "LONGITUDE",
            "GMTOFF",
            "DSTOFF",
            "TIMEZONE",
            "CC",
            "REGION",
            "LEID",
            "EUID",
            "NOTES",
            "TAGS",
        ],
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
    fields = ["email_address", "full_name", "last_changed", "location", "merge_fields"]
    for m in data["members"]:
        members.append({f: m[f] for f in fields})
    df = pd.DataFrame(members)
    df["last_changed"] = pd.to_datetime(df["last_changed"])
    df["month"] = df["last_changed"].dt.strftime("%-m")
    df["day"] = df["last_changed"].dt.strftime("%-d")
    df["last_changed"] = df["last_changed"].dt.strftime("%d/%m/%Y")
    df = df[
        ["last_changed", "month", "day"] + [f for f in fields if f != "last_changed"]
    ]

    return df


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


def setup_args():
    parser = argparse.ArgumentParser(
        prog="crece-post-processing-tool",
        description="This tool does specific task for crece team",
    )
    parser.add_argument("filename", type=pathlib.Path)
    parser.add_argument("out_dir")
    parser.add_argument("-d", "--download", action="store_true")

    return parser.parse_args()


def main():
    args = setup_args()
    try:
        if args.download:
            df = get_member_list_df()
        else:
            df = post_proces_df(args.filename)
        write_csv(df, args.out_dir)
    except Exception as e:
        print(f"FAIL, err: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    main()
