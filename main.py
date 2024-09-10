import argparse
import pathlib

from post_processing_tool import (
    FileProcessorApp,
    create_tk_root,
    get_member_list_df,
    post_process_df,
    write_csv,
    write_html,
    generate_report,
)


def setup_args():
    parser = argparse.ArgumentParser(
        prog="crece-post-processing-tool",
        description="This tool execute specific tasks for team CRECE. A GUI is provided if console flag is not set.",
    )
    parser.add_argument("-i", "--input_file", type=pathlib.Path, help="If download flag is not set pass a path to csv")
    parser.add_argument("-o", "--output_dir", default=".", help="Output directory")
    parser.add_argument("-d", "--download", action="store_true", help="If set download data from Mailchimp. Environment variables are required.")
    parser.add_argument("-c", "--console", action="store_true", default=False, help="If set don't start user interface")
    parser.add_argument("-r", "--report_template", type=pathlib.Path, help="Path to report template.")

    return parser.parse_args()


def main():
    args = setup_args()
    try:
        if not args.console:
            root = create_tk_root()
            FileProcessorApp(root, post_process_df)
            root.mainloop()
        else:
            if args.download:
                df = get_member_list_df()
                write_csv(df, args.output_dir)
            else:
                if not args.input_file:
                    raise Exception(
                        "Input file not provided. Please add flag -i, --input_file [FILE_NAME]"
                    )
                df, _ = post_process_df(args.input_file, args.output_dir)

            if args.report_template:
                report = generate_report(df, str(args.report_template))
                write_html(report, "index.html")
            else:
                print("Skipping report since it was not provided.")
    except Exception as e:
        raise e
    return 0


if __name__ == "__main__":
    main()
