import unittest

from src.connectors.filesystem_connector import FilesystemConnector
from src.models import FSConnectorSettings


class TestFileSystemConnector(unittest.TestCase):
    def test_get_data_files(self):
        connector = FilesystemConnector()
        settings = FSConnectorSettings(files_paths=["./data/netflix_titles.csv",
                                                  "./data/disney_movies.csv"],
                                       directory_paths=[],
                                     file_type=("csv",))
        data, names = connector.get_data(settings)
        connector.close()
        self.assertEqual(len(data), 2)
        self.assertEqual(names[0], "./data/netflix_titles")
        self.assertEqual(names[1], "./data/disney_movies")

    def test_get_data_folder(self):
        connector = FilesystemConnector()
        settings = FSConnectorSettings(files_paths=[],
                                       directory_paths=["./data"],
                                       file_type=("csv",))
        data, _ = connector.get_data(settings)
        connector.close()
        self.assertEqual(len(data), 11)
