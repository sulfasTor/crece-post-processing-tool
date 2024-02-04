import pandas as pd

from mailchimp import get_member_list_df
from replace import post_proces_df, write_csv


def main():
    try:
        df = get_member_list_df()
        print(df)
        # df = post_proces_df('~/Downloads/subscribed_members_export_0e31a6fce9.csv')
        # write_csv(df, '~/Downloads')
    except Exception as e:
        print(f"FAIL, err: {str(e)}")
        return 1

    return 0


main()
