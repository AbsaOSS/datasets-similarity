import unittest
import time

import pandas as pd
from sentence_transformers import SentenceTransformer

from column2Vec.Column2Vec import column2vec_as_sentence, column2vec_as_sentence_clean, \
    column2vec_as_sentence_clean_uniq, column2vec_avg, column2vec_weighted_avg
from column2Vec.functions import get_data, get_clusters
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator
from similarity.Types import NONNUMERICAL


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
        print("Processing column: " + key + " " + str(round((count/len(data))*100, 2)) + "%")
        result[key] = function(data[key], SentenceTransformer('bert-base-nli-mean-tokens'))
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
            print(f" {i} : {name}")
            result[name + str(index)] = data[name]
    return result


class TestSimilarityOfVectors(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        fileM2 = "../data/netflix_titles.csv"
        # make an array of all the files
        files = [fileM2]
        self.data = get_data(files)
        stop = 0
        for i in self.data:
            if stop == 0:
                self.first = self.data[i]
            if stop == 1:
                self.second = self.data[i]
            if stop == 2:
                self.third = self.data[i]
            stop += 1

    def test_column2vec_as_sentence(self):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.assertTrue(vectors_are_same(column2vec_as_sentence(self.first, model), column2vec_as_sentence(self.first, self.model)))
        self.assertTrue(vectors_are_same(column2vec_as_sentence(self.second, model), column2vec_as_sentence(self.second, self.model)))
        self.assertTrue(vectors_are_same(column2vec_as_sentence(self.third, model), column2vec_as_sentence(self.third, self.model)))

    def test_column2vec_as_sentence_clean(self):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean(self.first, model), column2vec_as_sentence_clean(self.first, self.model)))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean(self.second, model), column2vec_as_sentence_clean(self.second, self.model)))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean(self.third, model), column2vec_as_sentence_clean(self.third, self.model)))

    def test_column2vec_as_sentence_clean_uniq(self):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean_uniq(self.first, model), column2vec_as_sentence_clean_uniq(self.first, self.model)))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean_uniq(self.second, model), column2vec_as_sentence_clean_uniq(self.second, self.model)))
        self.assertTrue(vectors_are_same(column2vec_as_sentence_clean_uniq(self.third, model), column2vec_as_sentence_clean_uniq(self.third, self.model)))


    def test_column2vec_avg(self):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.assertTrue(vectors_are_same(column2vec_avg(self.first, model), column2vec_avg(self.first, self.model)))
        # self.assertTrue(vectors_are_same(column2vec_avg(self.second, model), column2vec_avg(self.second, self.model)))
        # self.assertTrue(vectors_are_same(column2vec_avg(self.third, model), column2vec_avg(self.third, self.model)))

    def test_column2vec_weighted_avg(self):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.assertTrue(vectors_are_same(column2vec_weighted_avg(self.first, model), column2vec_weighted_avg(self.first, self.model)))
        # self.assertTrue(vectors_are_same(column2vec_weighted_avg(self.second, model), column2vec_weighted_avg(self.second, self.model)))
        # self.assertTrue(vectors_are_same(column2vec_weighted_avg(self.third, model), column2vec_weighted_avg(self.third, self.model)))


class TestClusters(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.clusters_MC_Copilot = {
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
        fileA1 = "../data/aircraft-data_nov_dec.csv"
        fileA2 = "../data/Airplane_Cleaned.csv"
        fileC1 = "../data/autoscout24-germany-dataset.csv"
        fileC2 = "../data/CARS_1.csv"
        fileC3 = "../data/USA_cars_datasets.csv"
        fileM1 = "../data/imdb_top_1000.csv"
        fileM2 = "../data/netflix_titles.csv"
        # make an array of all the files
        self.files = [fileA1, fileA2, fileC1, fileC2, fileC3, fileM1, fileM2]
        self.data = get_data(self.files)

    def test_column2vec_as_sentence(self):
        vectors_sentence = get_vectors(column2vec_as_sentence, self.data)
        clusters1 = get_clusters(vectors_sentence, 12)
        clusters2 = get_clusters(vectors_sentence, 12)
        clusters3 = get_clusters(vectors_sentence, 12)
        self.assertTrue(vectors_are_same(clusters1, clusters2))
        self.assertTrue(vectors_are_same(clusters1, clusters3))
        self.assertTrue(vectors_are_same(clusters3, clusters2))








if __name__ == '__main__':
    unittest.main()