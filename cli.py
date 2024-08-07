import argparse


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass

def cache_args(subparser):
    parser_foo = subparser.add_parser('cache')
    parser_foo.add_argument("-f", "--cache-file", help="path to cache file", nargs=1)
    parser_foo.add_argument("-s", "--save", help="save cache persistently", action="store_true")
    parser_foo.add_argument("--off", help="Turn off cache", action="store_true")


def metadata_creator_args(parser):
    parser.add_argument("-e", "--embeddings",
                        help="Metadata: compute embeddings, specify embedding function",
                        nargs=1,
                        default="sentence_clean_uniq",
                        choices=["sentence", "sentence_clean", "sentence_clean_uniq", "avg", "sum", "weighted_avg",
                                 "weighted_sum"]
                        )
    parser.add_argument("-k", "--kind",
                        help="Metadata: set compute kinds to true",
                        action="store_true"
                        )
    parser.add_argument("-t", "--types",
                        help="""Metadata: set compute types to true
Pick types to compute:
    basic: numerical, date, nonnumerical
    advanced: int, float, date, nonnumerical
    structural: int, float.human, float.computer, date, word, multiple, sentence, phrase...""",
                        nargs=1,
                        default="basic",
                        choices=["basic", "advanced", "structural"]

                        )


def init_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dataset similarity tool",
                                     formatter_class=CustomFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-inF", "--input-files", help="path or paths to input files", nargs='+')
    group.add_argument("-inD", "--directory", help="directory with input files", nargs=1)

    subparser = parser.add_subparsers(help="cache options")
    cache_args(subparser)
    metadata_creator_args(parser)

    return parser


def parse_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    if args.input_files:
        print(f"Input files are {args.input_files}")
    if args.directory:
        print(f"Directory is {args.directory}")
    if args.cache_file:
        print(f"Cache file is {args.cache_file}")
    if args.save:
        print("Cache will be saved")
    if args.off:
        print("Cache is turned off")


if __name__ == "__main__":
    parse_args(init_args())
