import sys

import pandas as pd

from similarity.Comparator import Comparator, SizeComparator, IncompleteColumnsComparator, KindComparator, \
    ColumnNamesEmbeddingsComparator
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator


def create_metadata(data):
    return (DataFrameMetadataCreator(data).
            compute_advanced_structural_types().
            compute_column_kind().compute_column_names_embeddings()).get_metadata()


def compare_datasets(path1, path2):
    data1 = pd.read_csv(path1)
    data2 = pd.read_csv(path2)
    metadata1 = create_metadata(data1)
    metadata2 = create_metadata(data2)
    compartor = (Comparator().add_comparator_type(SizeComparator()).
                 add_comparator_type(IncompleteColumnsComparator())
                 .add_comparator_type(KindComparator())
                 .add_comparator_type(ColumnNamesEmbeddingsComparator()))
    return compartor.compare(metadata1, metadata2)

if __name__ == '__main__':
    files = sys.argv[1:]
    print(files)
    for file1 in files:
        for file2 in files:
            if file1 != file2:
                distance = compare_datasets(file1, file2)
                print(f"{file1} |< >| {file2} = {distance}")
    if len(files) == 0:
        distance = compare_datasets('data/netflix_titles.csv', 'data/imdb_top_1000.csv')
        print(f"'data/netflix_titles.csv' |< >| 'data/imdb_top_1000.csv' = {distance}")
