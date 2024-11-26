import unittest

import pandas as pd

from similarity_runner.src.impl.filesystem_connector import load_files_from_list
from similarity_runner.src.models.connectors import FileType


def csv_to_parquet(file: str, sep: str = ',') -> str:
    """
    Convert csv file to parquet
    :param file: file to convert
    """
    df = pd.read_csv(file, sep=sep, low_memory=False)
    df.to_parquet(file.replace(".csv", ".parquet"))
    return file.replace(".csv", ".parquet")

class TestLoadFilesFromList(unittest.TestCase):
    def test_load_csv_file(self):
        data, names = load_files_from_list(["./data/netflix_titles.csv"], (FileType.CSV, ))
        self.assertEqual(len(data), 1)
        self.assertEqual(names[0], "./data/netflix_titles")

    def test_load_csv_files(self):
        data, names = load_files_from_list(["./data/netflix_titles.csv", "./data/disney_movies.csv"], (FileType.CSV, ))
        self.assertEqual(len(data), 2)
        self.assertEqual(names[0], "./data/netflix_titles")
        self.assertEqual(names[1], "./data/disney_movies")


    def test_load_parquet_file(self):
        csv_to_parquet("./data/netflix_titles.csv")
        data, names = load_files_from_list(["./data/netflix_titles.parquet"], (FileType.PARQUET, ))
        self.assertEqual(len(data), 1)
        self.assertEqual(names[0], "./data/netflix_titles")

    def test_load_parquet_files(self):
        csv_to_parquet("./data/netflix_titles.csv")
        csv_to_parquet("./data/disney_movies.csv")
        data, names = load_files_from_list(["./data/netflix_titles.parquet", "./data/disney_movies.parquet"], (FileType.PARQUET, ))
        self.assertEqual(len(data), 2)
        self.assertEqual(names[0], "./data/netflix_titles")
        self.assertEqual(names[1], "./data/disney_movies")


    def test_load_csv_and_parquet_files(self):
        csv_to_parquet("./data/netflix_titles.csv")
        data, names = load_files_from_list(["./data/netflix_titles.parquet", "./data/disney_movies.csv"], (FileType.PARQUET, FileType.CSV))
        self.assertEqual(len(data), 2)
        self.assertEqual(names[0], "./data/netflix_titles")
        self.assertEqual(names[1], "./data/disney_movies")
