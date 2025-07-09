import os
import unittest

from similarity_runner.src.impl.filesystem_connector import FilesystemConnector, FSConnectorSettings

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestFileSystemConnector(unittest.TestCase):
    def setUp(self):
        self.file1 = os.path.join(THIS_DIR, '../data/netflix_titles.csv')
        self.file2 = os.path.join(THIS_DIR, '../data/disney_movies.csv')
        self.dir = os.path.join(THIS_DIR, '../data')
    def test_get_data_files(self):
        connector = FilesystemConnector()
        settings = FSConnectorSettings(files_paths=self.file1 + "," + self.file2,
                                       directory_paths="",
                                       filetypes="csv")
        res = connector.get_data(settings)
        connector.close()
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].source_name, self.file1.replace(".csv", ""))
        self.assertEqual(res[1].source_name, self.file2.replace(".csv", ""))

    def test_get_data_folder(self):
        connector = FilesystemConnector()
        settings = FSConnectorSettings(files_paths="",
                                       directory_paths=self.dir,
                                       filetypes="csv")
        data = connector.get_data(settings)
        connector.close()
        self.assertEqual(len(data), 13)
