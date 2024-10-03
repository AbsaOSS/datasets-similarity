"""
This file is a part of the similarityRunner package.
It is used to run the similarity pipeline from console.
"""
import sys


from models.connector_models import FSConnectorSettings, FileType as ft
from models.user_models import SimilaritySettings, MetadataSettings, ComparatorType as ct, RunType
import runner as r


def get_arg(index, message) -> str:
    """
    Get argument from a command line
    :param index: index of an argument
    :param message:  a message to print if argument is not found
    """
    try:
        return sys.argv[index]
    except IndexError:
        print(message)
        sys.exit(1)


if __name__ == "__main__":
    directory = get_arg(1, "Add path to directory")
    run_type = get_arg(2, "Add run type, all metadata, similarity")  # all, metadata, similarity
    comparator_type = get_arg(3, "Add comparator type: by_column, by_type ")  # by_type, by_column
    settings = SimilaritySettings(
        connector=FSConnectorSettings(file_type=(ft.CSV, ft.PARQUET), files_paths=[], directory_paths=[directory]),
        metadata=MetadataSettings(all=True, kinds=True, types=True, embeddings=True),
        run_type=RunType(run_type),
        comparator_type=ct.BY_COLUMN if comparator_type == "by_column" else ct.BY_TYPE,
    )
    result = r.run(settings)
    print(result)
