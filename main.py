import argparse
import pathlib

from post_processing_tool import FileProcessorApp, post_proces_df, write_csv, get_member_list_df, create_tk_root

def setup_args():
    parser = argparse.ArgumentParser(
        prog="crece-post-processing-tool",
        description="This tool does specific task for crece team",
    )
    parser.add_argument("-i", "--input_file", type=pathlib.Path)
    parser.add_argument("-o", "--output_dir", default=".")
    parser.add_argument("-d", "--download", action="store_true")
    parser.add_argument("-c", "--console", action="store_true", default=False)

    return parser.parse_args()

def main():
    args = setup_args()
    try:
        if not args.console:
            root = create_tk_root()
            FileProcessorApp(root, post_proces_df)
            root.mainloop()
        else:
            if args.download:
                df = get_member_list_df()
                write_csv(df, args.output_dir)
            else:
                if not args.input_file:
                    raise Exception("Input file not provided. Please add flag -i, --input_file [FILE_NAME]")
                df, _ = post_proces_df(args.input_file, args.output_dir)
    except Exception as e:
        print(f"FAIL, err: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    main()
