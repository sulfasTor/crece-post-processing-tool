import argparse
import pathlib

from mailchimp import get_member_list_df
from replace import post_proces_df, write_csv


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


main()
