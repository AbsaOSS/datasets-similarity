import unittest

from src.functions_runner import load_files_from_list, csv_to_parquet
from src.models import FileType


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
