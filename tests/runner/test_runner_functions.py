import os
import unittest

import pandas as pd

from similarity_runner.src.impl.filesystem_connector import load_files_from_list
from similarity_runner.src.models.connectors import FileType

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def csv_to_parquet(file: str, sep: str = ',') -> str:
    """
    Convert csv file to parquet
    :param file: file to convert
    """
    df = pd.read_csv(file, sep=sep, low_memory=False)
    df.to_parquet(file.replace(".csv", ".parquet"))
    return file.replace(".csv", ".parquet")

class TestLoadFilesFromList(unittest.TestCase):
    def setUp(self):
        self.netflix_file = os.path.join(THIS_DIR, '../data/netflix_titles.csv')
        self.netflix_file_parquet = os.path.join(THIS_DIR, '../data/netflix_titles.parquet')
        self.disney_file = os.path.join(THIS_DIR, '../data/disney_movies.csv')
        self.disney_file_parquet = os.path.join(THIS_DIR, '../data/disney_movies.parquet')
        self.dir = os.path.join(THIS_DIR, '../data')

    def test_load_csv_file(self):
        res = load_files_from_list([self.netflix_file], (FileType.CSV,))
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].source_name, self.netflix_file.replace(".csv", ""))

    def test_load_csv_files(self):
        res = load_files_from_list([self.netflix_file, self.disney_file], (FileType.CSV,))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].source_name, self.netflix_file.replace(".csv", ""))
        self.assertEqual(res[1].source_name, self.disney_file.replace(".csv", ""))


    def test_load_parquet_file(self):
        csv_to_parquet(self.netflix_file)
        res = load_files_from_list([self.netflix_file_parquet], (FileType.PARQUET, ))
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].source_name, self.netflix_file_parquet.replace(".parquet", ""))

    def test_load_parquet_files(self):
        csv_to_parquet(self.netflix_file)
        csv_to_parquet(self.disney_file)
        res = load_files_from_list([self.netflix_file_parquet, self.disney_file_parquet], (FileType.PARQUET, ))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].source_name, self.netflix_file_parquet.replace(".parquet", ""))
        self.assertEqual(res[1].source_name, self.disney_file_parquet.replace(".parquet", ""))


    def test_load_csv_and_parquet_files(self):
        csv_to_parquet(self.netflix_file)
        res = load_files_from_list([self.netflix_file_parquet, self.disney_file], (FileType.PARQUET, FileType.CSV))
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].source_name, self.netflix_file_parquet.replace(".parquet", ""))
        self.assertEqual(res[1].source_name, self.disney_file.replace(".csv", ""))
