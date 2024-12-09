import unittest

from similarity_runner.src.impl.filesystem_connector import FilesystemConnector, FSConnectorSettings


class TestFileSystemConnector(unittest.TestCase):
    def test_get_data_files(self):
        connector = FilesystemConnector()
        settings = FSConnectorSettings(files_paths="../data/netflix_titles.csv,../data/disney_movies.csv",
                                       directory_paths="",
                                       filetypes="csv")
        res = connector.get_data(settings)
        connector.close()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].source_name, "../data/netflix_titles")
        self.assertEqual(res[1].source_name, "../data/disney_movies")

    def test_get_data_folder(self):
        connector = FilesystemConnector()
        settings = FSConnectorSettings(files_paths="",
                                       directory_paths="../data",
                                       filetypes="csv")
        data = connector.get_data(settings)
        connector.close()
        self.assertEqual(len(data), 13)
