import unittest

from similarity.DataFrameMetadata import DataFrameMetadata
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator
from similarity.comparing_all_tables.comparing import ComparatorForDatasets
from similarity.functions import load__csv_files_from_folder


class TestSum(unittest.TestCase):
    corr_doubles = {
        "aircraft-data_nov_dec": ("Airplane_Cleaned",),
        "Airplane_Cleaned": ("aircraft-data_nov_dec",),
        "autoscout24-germany-dataset": ("CARS_1", "USA_cars_datasets"),
        "CARS_1": ("autoscout24-germany-dataset", "USA_cars_datasets"),
        "USA_cars_datasets": ("autoscout24-germany-dataset", "CARS_1"),
        "disney_movies": ("imdb_top_1000", "netflix_titles"),
        "imdb_top_1000": ("disney_movies", "netflix_titles"),
        "netflix_titles": ("disney_movies", "imdb_top_1000"),
        "exchange_rates": ("Sales_Transaction10000", "transaction_data"),
        "Sales_Transaction10000": ("exchange_rates", "transaction_data"),
        "transaction_data": ("exchange_rates", "Sales_Transaction10000")
    }

    def print_correlation(self, res):
        correct_count = 0
        for key, value in res.items():
            if value in self.corr_doubles[key]:
                correct_count += 1
        print(f"Accuracy is {correct_count * len(res) / 100}")
        return correct_count * len(res) / 100
        # self.assertLessEqual(0.8, correct_count * len(res) / 100, "Message")

    def create_metadata(self):
        database, names = load__csv_files_from_folder("../data")  # load data
        metadata: dict[str, DataFrameMetadata] = dict()  # define metadata
        for dataframe, name in zip(database, names):  # create the metadata
            metadata[name] = DataFrameMetadataCreator(dataframe).compute_correlation(
                0.5).create_column_embeddings().get_metadata()
        # to_hash = ""
        # m = hashlib.sha256()
        # for name, valee in metadata.items():
        #     m.update(valee.hash())
        #     to_hash = f"{to_hash}|{name}{valee.hash()}"
        # # print(f"hashed: {hash(to_hash)} , {hash(to_hash)}")
        # # print(f"not_hashed: {to_hash}")
        # print(f"hash from hashlib: {m.hexdigest()}")
        return metadata

    def test_cross_compare(self):
        metadata = self.create_metadata()

        comparator = ComparatorForDatasets(metadata)  # compare
        res = comparator.cross_compare()
        corr1 = self.print_correlation(res)

        comparator2 = ComparatorForDatasets(metadata)  # compare
        res2 = comparator2.cross_compare()
        corr2 = self.print_correlation(res2)

        self.assertEqual(corr1, corr2)

        print("Column names")
        res = comparator.cross_compare_column_names()
        corr1 = self.print_correlation(res)


# if __name__ == '__main__':
#     unittest.main()
