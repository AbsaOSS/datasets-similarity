import os
import unittest
import time

import pandas as pd
from sentence_transformers import SentenceTransformer

from column2Vec.impl.Column2Vec import (column2vec_as_sentence, column2vec_as_sentence_clean,
                                        column2vec_as_sentence_clean_uniq, column2vec_avg,
                                        column2vec_weighted_avg, column2vec_sum,
                                        column2vec_weighted_sum, cache)
from column2Vec.impl.functions import get_nonnumerical_data, get_clusters, compute_distances

from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator
from similarity.Types import NONNUMERICAL

SKIP_CLUSTERS = True
SKIP_SIMILAR = False
# MODEL = 'all-mpnet-base-v2'  # bert-base-nli-mean-tokens
MODEL = 'bert-base-nli-mean-tokens'  #
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def vectors_are_same(vec1, vec2):
    for i, j in zip(vec1, vec2):
        if i != j:
            return False
    return True


def get_vectors(function, data):
    start = time.time()
    result = {}
    count = 1
    for key in data:
        # print("Processing column: " + key + " " + str(round((count / len(data)) * 100, 2)) + "%")
        result[key] = function(data[key], SentenceTransformer(MODEL), key)
        count += 1
    end = time.time()
    print(f"ELAPSED TIME :{end - start}")
    return result


def get_data(files):
    result = {}
    index = 0
    for i in files:
        index += 1
        data = pd.read_csv(i)
        metadata_creator = (DataFrameMetadataCreator(data).
                            compute_advanced_structural_types().
                            compute_column_kind())
        metadata1 = metadata_creator.get_metadata()
        column_names = metadata1.get_column_names_by_type(NONNUMERICAL)
        for name in column_names:
            #     print(f" {i} : {name}")
            result[name + str(index)] = data[name]
    return result


class TestSimilarityOfVectors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = SentenceTransformer(MODEL)
        file_m2 = os.path.join(THIS_DIR, os.pardir, 'data/netflix_titles.csv')
        # make an array of all the files
        files = [file_m2]
        cls.data = get_nonnumerical_data(files)
        stop = 0
        for i in cls.data:
            if stop == 0:
                cls.first = cls.data[i]
            if stop == 1:
                cls.second = cls.data[i]
            if stop == 2:
                cls.third = cls.data[i]
            stop += 1

    def test_column2vec_as_sentence(self):
        model = SentenceTransformer(MODEL)
        self.assertTrue(
            vectors_are_same(column2vec_as_sentence(self.first, model, "a"),
                             column2vec_as_sentence(self.first, self.model, "b")))
        self.assertTrue(vectors_are_same(column2vec_as_sentence(self.second, model, "c"),
                                         column2vec_as_sentence(self.second, self.model, "d")))
        self.assertTrue(
            vectors_are_same(column2vec_as_sentence(self.third, model, "e"),
                             column2vec_as_sentence(self.third, self.model, "f")))

    def test_column2vec_as_sentence_clean(self):
        model = SentenceTransformer(MODEL)
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean(self.first, model, "g"),
                                         column2vec_as_sentence_clean(self.first, self.model, "h")))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean(self.second, model, "i"),
                                         column2vec_as_sentence_clean(self.second, self.model, "j")))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean(self.third, model, "k"),
                                         column2vec_as_sentence_clean(self.third, self.model, "l")))

    def test_column2vec_as_sentence_clean_uniq(self):
        model = SentenceTransformer(MODEL)
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean_uniq(self.first, model, "m"),
                                         column2vec_as_sentence_clean_uniq(self.first, self.model, "n")))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean_uniq(self.second, model, "o"),
                                         column2vec_as_sentence_clean_uniq(self.second, self.model, "p")))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean_uniq(self.third, model, "q"),
                                         column2vec_as_sentence_clean_uniq(self.third, self.model, "r")))

    def test_column2vec_avg(self):
        model = SentenceTransformer(MODEL)
        self.assertTrue(vectors_are_same(column2vec_avg(self.first, model, "v"),
                                         column2vec_avg(self.first, self.model, "s")))
        # self.assertTrue(vectors_are_same(column2vec_avg(self.second, model), column2vec_avg(self.second, self.model)))
        # self.assertTrue(vectors_are_same(column2vec_avg(self.third, model), column2vec_avg(self.third, self.model)))

    def test_column2vec_weighted_avg(self):
        model = SentenceTransformer(MODEL)
        self.assertTrue(vectors_are_same(column2vec_weighted_avg(self.first, model, "u"),
                                         column2vec_weighted_avg(self.first, self.model, "w")))
        # self.assertTrue(vectors_are_same(column2vec_weighted_avg(self.second, model),
        # column2vec_weighted_avg(self.second, self.model)))
        # self.assertTrue(vectors_are_same(column2vec_weighted_avg(self.third, model),
        # column2vec_weighted_avg(self.third, self.model)))

    def test_column2vec_sum(self):
        model = SentenceTransformer(MODEL)
        self.assertTrue(vectors_are_same(column2vec_sum(self.first, model, "x"),
                                         column2vec_sum(self.first, self.model, "y")))

    def test_column2vec_weighted_sum(self):
        model = SentenceTransformer(MODEL)
        self.assertTrue(vectors_are_same(column2vec_weighted_sum(self.first, model, "z"),
                                         column2vec_weighted_sum(self.first, self.model, "ab")))


class TestClustersAreAlwaysSame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clusters_MC_Copilot = {
            1: ["flight", "tail_number"],
            2: ["reg_expiration", "reg_owner", "vin", "title_status"],
            3: ["manufacturer", "model", "make", "brand", "Model", "Company"],
            4: ["Engine Type", "Multi Engine", "TP mods", "gear", "transmission_type", "fuel_type", "body_type"],
            5: ["reg_state", "reg_city", "country", "state"],
            6: ["offerType", "Gross"],
            7: ["Series_Title", "Overview", "title", "description", "type", "listed_in"],
            8: ["rating", "duration", "date_added"],
            9: ["Poster_Link", "Director", "Star2", "Star3", "Star1", "Star4", "show_id", "cast", "director"],
            10: ["condition", "color"],
            11: ["Genre"]
        }
        file_a1 = os.path.join(THIS_DIR, os.pardir, 'data/aircraft-data_nov_dec.csv')
        file_a2 = os.path.join(THIS_DIR, os.pardir, 'data/Airplane_Cleaned.csv')
        file_c1 = os.path.join(THIS_DIR, os.pardir, 'data/autoscout24-germany-dataset.csv')
        file_c2 = os.path.join(THIS_DIR, os.pardir, 'data/CARS_1.csv')
        file_c3 = os.path.join(THIS_DIR, os.pardir, 'data/USA_cars_datasets.csv')
        file_m1 = os.path.join(THIS_DIR, os.pardir, 'data/imdb_top_1000.csv')
        file_m2 = os.path.join(THIS_DIR, os.pardir, 'data/netflix_titles.csv')
        # make an array of all the files
        cls.files = [file_a1, file_a2, file_c1, file_c2, file_c3, file_m1, file_m2]
        cls.data = get_nonnumerical_data(cls.files)
        cache.off()

    def test_column2vec_as_sentence(self):
        vectors_sentence = get_vectors(column2vec_as_sentence, self.data)
        clusters1 = get_clusters(vectors_sentence, 11)
        clusters2 = get_clusters(vectors_sentence, 11)
        clusters3 = get_clusters(vectors_sentence, 11)
        self.assertTrue(vectors_are_same(clusters1, clusters2))
        self.assertTrue(vectors_are_same(clusters1, clusters3))
        self.assertTrue(vectors_are_same(clusters3, clusters2))

    def test_column2vec_as_sentence_clean(self):
        vectors_sentence = get_vectors(column2vec_as_sentence_clean, self.data)
        clusters1 = get_clusters(vectors_sentence, 11)
        clusters2 = get_clusters(vectors_sentence, 11)
        clusters3 = get_clusters(vectors_sentence, 11)
        self.assertTrue(vectors_are_same(clusters1, clusters2))
        self.assertTrue(vectors_are_same(clusters1, clusters3))
        self.assertTrue(vectors_are_same(clusters3, clusters2))

    def test_column2vec_as_sentence_clean_uniq(self):
        vectors_sentence = get_vectors(column2vec_as_sentence_clean_uniq, self.data)
        clusters1 = get_clusters(vectors_sentence, 11)
        clusters2 = get_clusters(vectors_sentence, 11)
        clusters3 = get_clusters(vectors_sentence, 11)
        self.assertTrue(vectors_are_same(clusters1, clusters2))
        self.assertTrue(vectors_are_same(clusters1, clusters3))
        self.assertTrue(vectors_are_same(clusters3, clusters2))

    @unittest.skipIf(SKIP_CLUSTERS, "Skipping test_column2vec_avg ...")
    def test_column2vec_avg(self):
        vectors_sentence = get_vectors(column2vec_avg, self.data)
        clusters1 = get_clusters(vectors_sentence, 11)
        clusters2 = get_clusters(vectors_sentence, 11)
        clusters3 = get_clusters(vectors_sentence, 11)
        self.assertTrue(vectors_are_same(clusters1, clusters2))
        self.assertTrue(vectors_are_same(clusters1, clusters3))
        self.assertTrue(vectors_are_same(clusters3, clusters2))

    @unittest.skipIf(SKIP_CLUSTERS, "Skipping test_column2vec_weighted_avg ...")
    def test_column2vec_weighted_avg(self):
        vectors_sentence = get_vectors(column2vec_weighted_avg, self.data)
        clusters1 = get_clusters(vectors_sentence, 11)
        clusters2 = get_clusters(vectors_sentence, 11)
        clusters3 = get_clusters(vectors_sentence, 11)
        self.assertTrue(vectors_are_same(clusters1, clusters2))
        self.assertTrue(vectors_are_same(clusters1, clusters3))
        self.assertTrue(vectors_are_same(clusters3, clusters2))


class TestSimilarColumnsCopilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clusters_MC_Copilot = {
            1: ["flight", "tail_number"],
            2: ["reg_expiration", "reg_owner", "vin", "title_status"],
            3: ["manufacturer", "model", "make", "brand", "Model", "Company"],
            4: ["Engine Type", "Multi Engine", "TP mods", "gear", "transmission_type", "fuel_type", "body_type"],
            5: ["reg_state", "reg_city", "country", "state"],
            6: ["offerType", "Gross"],
            7: ["Series_Title", "Overview", "title", "description", "type", "listed_in"],
            8: ["rating", "duration", "date_added"],
            9: ["Poster_Link", "Director", "Star2", "Star3", "Star1", "Star4", "show_id", "cast", "director"],
            10: ["condition", "color"],
            11: ["Genre"]
        }
        file_a1 = os.path.join(THIS_DIR, os.pardir, 'data/aircraft-data_nov_dec.csv')
        file_a2 = os.path.join(THIS_DIR, os.pardir, 'data/Airplane_Cleaned.csv')
        file_c1 = os.path.join(THIS_DIR, os.pardir, 'data/autoscout24-germany-dataset.csv')
        file_c2 = os.path.join(THIS_DIR, os.pardir, 'data/CARS_1.csv')
        file_c3 = os.path.join(THIS_DIR, os.pardir, 'data/USA_cars_datasets.csv')
        file_m1 = os.path.join(THIS_DIR, os.pardir, 'data/imdb_top_1000.csv')
        file_m2 = os.path.join(THIS_DIR, os.pardir, 'data/netflix_titles.csv')
        # make an array of all the files
        cls.files = [file_a1, file_a2, file_c1, file_c2, file_c3, file_m1, file_m2]
        cls.data = get_nonnumerical_data(cls.files)
        cache.off()

    def get_cluster_num(self, name):
        for number, names in self.clusters_MC_Copilot.items():
            if name in names:
                return number

        return None  # Return None if the name is not found

    def print_accuracy(self, distances, name):
        overall = 0
        for key, row in distances.items():
            sorted_array = dict(sorted(row.items(), key=lambda a: a[1]))

            nearest_elements = list(sorted_array.keys())
            nearest_num = list(sorted_array.values())
            cluster_num = self.get_cluster_num(nearest_elements[0][:-1])
            if cluster_num is None:
                break
            accuracy = 0
            for key2, item in zip(nearest_elements[1:], nearest_num[1:]):
                if item > 0.4:
                    break
                if key2[:-1] in self.clusters_MC_Copilot[cluster_num]:
                    accuracy += (1 - item)
                else:
                    accuracy -= (1 - item)
            overall += accuracy
            # print(f"{key}: {nearest_elements[:6]},    accuracy {accuracy}")
        print(f"\t {name} \nAccuracy: {overall}")

    def test_column2vec_as_sentence(self):
        vectors_sentence = get_vectors(column2vec_as_sentence, self.data)
        distances = compute_distances(vectors_sentence)
        self.print_accuracy(distances, "AS SENTENCE")

    def test_column2vec_as_sentence_clean(self):
        vectors_sentence = get_vectors(column2vec_as_sentence_clean, self.data)
        distances = compute_distances(vectors_sentence)
        self.print_accuracy(distances, "AS SENTENCE CLEAN")

    def test_column2vec_as_sentence_clean_uniq(self):
        vectors_sentence = get_vectors(column2vec_as_sentence_clean_uniq, self.data)
        distances = compute_distances(vectors_sentence)
        self.print_accuracy(distances, "AS SENTENCE CLEAN UNIQ")

    @unittest.skipIf(SKIP_SIMILAR, "Skipping test_column2vec_avg ...")
    def test_column2vec_avg(self):
        vectors_sentence = get_vectors(column2vec_avg, self.data)
        distances = compute_distances(vectors_sentence)
        self.print_accuracy(distances, "AVG")

    @unittest.skipIf(SKIP_SIMILAR, "Skipping test_column2vec_weighted_avg ...")
    def test_column2vec_weighted_avg(self):
        vectors_sentence = get_vectors(column2vec_weighted_avg, self.data)
        distances = compute_distances(vectors_sentence)
        self.print_accuracy(distances, "WEIGHTED AVG")

    @unittest.skipIf(SKIP_SIMILAR, "Skipping test_column2vec_avg ...")
    def test_column2vec_sum(self):
        vectors_sentence = get_vectors(column2vec_sum, self.data)
        distances = compute_distances(vectors_sentence)
        self.print_accuracy(distances, "SUM")

    @unittest.skipIf(SKIP_SIMILAR, "Skipping test_column2vec_weighted_avg ...")
    def test_column2vec_weighted_sum(self):
        vectors_sentence = get_vectors(column2vec_weighted_sum, self.data)
        distances = compute_distances(vectors_sentence)
        self.print_accuracy(distances, "WEIGHTED SUM")


if __name__ == '__main__':
    unittest.main()
