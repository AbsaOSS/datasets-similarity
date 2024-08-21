"""
This file contains argument parser, and it is creating a configuration file.
"""
import argparse
import configparser


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    """
    Custom formatter for argparse, to be able to use both RawTextHelpFormatter (for a formating help message)
    and ArgumentDefaultsHelpFormatter (for default help)
    """
    pass


def cache_args(subparser):
    """
    Add arguments for cache
    """
    parser_foo = subparser.add_parser('cache')
    parser_foo.add_argument("-f", "--cache-file", help="path to cache file", nargs=1)
    parser_foo.add_argument("-s", "--save", help="save cache persistently", action="store_true")
    parser_foo.add_argument("--off", help="Turn off cache", action="store_true")


def metadata_creator_args(parser: argparse.ArgumentParser):
    """
    Adds argument for choosing embedding function
    Adds argument for choosing types granularity

    :param parser : argparse.ArgumentParser
    """
    parser.add_argument("-e", "--embeddings",
                        help="Metadata: compute embeddings, specify embedding function",
                        nargs='?',
                        const='sentence_clean_uniq',
                        default="sentence_clean_uniq",
                        choices=["sentence", "sentence_clean", "sentence_clean_uniq", "avg", "sum", "weighted_avg",
                                 "weighted_sum"]
                        )
    parser.add_argument("-t", "--types",
                        help="""Metadata: set compute types to true
Pick types to compute:
    basic: numerical, date, nonnumerical
    advanced: int, float, date, nonnumerical
    structural: int, float.human, float.computer, date, word, multiple, sentence, phrase...""",
                        nargs='?',
                        const='basic',
                        default="basic",
                        choices=["basic", "advanced", "structural"]
                        )


def comparator_args(parser: argparse.ArgumentParser):
    """
    Add arguments for comparator

    :param parser : argparse.ArgumentParser
    """
    parser.add_argument("-ct", "--comparator-type",
                        help="type of comparator",
                        nargs='?',
                        const='basic',
                        choices=["basic", "by_column"],
                        )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-set", "--settings",
                       help="""set what to compare
all: will use all settings, if you want to exclude some settings use -ex                 
                        """,
                       nargs='+',
                       default="all",
                       choices=["all", "column_embeddings", "categorical", "size", "exact_names", "name_embeddings",
                                "incomplete", "kind"]
                       )
    group.add_argument("-ex", "--exclude",
                       help="""exclude some settings""",
                       nargs='+',
                       choices=["column_embeddings", "categorical", "size", "exact_names", "name_embeddings",
                                "incomplete", "kind"]
                       )


def init_args() -> argparse.ArgumentParser:
    """
    Creates argument parser with arguments for input files, cache, metadata creator and comparator
    """
    parser = argparse.ArgumentParser(description="Dataset similarity tool",
                                     formatter_class=CustomFormatter)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-inF", "--input-files", help="path or paths to input files", nargs='+')
    group.add_argument("-inD", "--directory", help="directory with input files", nargs=1)

    subparser = parser.add_subparsers(help="cache options")
    cache_args(subparser)
    metadata_creator_args(parser)
    comparator_args(parser)

    return parser


def set_all(config: configparser.ConfigParser, to: str):
    """
    Set all settings arguments to 'to' (Yes No)
    :param config : config parser
    :param to : Yes or No
    """
    config['Embeddings']['names'] = to
    config['Embeddings']['column'] = to
    config['Comparator']['categorical'] = to
    config['Comparator']['size'] = to
    config['Comparator']['exact_names'] = to
    config['Comparator']['incomplete'] = to
    config['Comparator']['kind'] = to


def set_any(config: configparser.ConfigParser, to: str, settings):
    """
   Set every argument present in settings to 'to' (Yes No)
   :param config : config parser
   :param to : Yes or No
   :param settings: list of settings
    """
    if 'name_embeddings' in settings:
        config['Embeddings']['names'] = to
    if 'column_embeddings' in settings:
        config['Embeddings']['column'] = to
    if 'categorical' in settings:
        config['Comparator']['categorical'] = to
    if 'size' in settings:
        config['Comparator']['size'] = to
    if 'exact_names' in settings:
        config['Comparator']['exact_names'] = to
    if 'incomplete' in settings:
        config['Comparator']['incomplete'] = to
    if 'kind' in settings:
        config['Comparator']['kind'] = to


def parse_args(parser: argparse.ArgumentParser):
    """
    Parse arguments from input
    :param parser : argparse.ArgumentParser
    """
    args = parser.parse_args()
    config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    config.read_file(open('configuration.ini'))
    print("CONFIG FILE ", config['Embeddings']['names'])  # -> "/path/name/"
    # config['DEFAULT']['path'] = '/var/shared/'  # update
    # config['DEFAULT']['default_message'] = 'Hey! help me!!'  # create

    if args.input_files:
        print(f"Input files are {args.input_files}")
        config['Input']['path_files'] = str(args.input_files)
        config['Input']['file'] = "Yes"
        config['Input']['directory'] = "No"
    if args.directory:
        print(f"Directory is {args.directory}")
        config['Input']['path'] = args.directory
        config['Input']['file'] = "No"
        config['Input']['directory'] = "Yes"
    if args.embeddings:
        print(f"Embeddings are {args.embeddings}")
        config['Embeddings']['type'] = args.embeddings
    if args.types:
        print(f"Types are {args.types}")
        config['Types']['type'] = args.types
    if args.comparator_type:
        print(f"Comparator type is {args.comparator_type}")
        config['Comparator']['type'] = args.comparator_type
    if args.settings:
        print(f"Settings are {args.settings}")
        if 'all' in args.settings:
            set_all(config, 'Yes')
        else:
            set_all(config, 'No')
        set_any(config, 'Yes', args.settings)

    if args.exclude:
        set_all(config, 'Yes')
        print(f"Excluded settings are {args.exclude}")
        set_any(config, 'No', args.settings)

    config.write(open('configuration.ini', 'w'))


if __name__ == "__main__":
    parse_args(init_args())
