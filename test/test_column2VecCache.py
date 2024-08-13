import os
import unittest
import time

from sentence_transformers import SentenceTransformer

from column2Vec.impl.Column2Vec import (cache,
                                        column2vec_as_sentence,
                                        column2vec_as_sentence_clean,
                                        column2vec_as_sentence_clean_uniq,
                                        column2vec_avg,
                                        column2vec_weighted_sum,
                                        column2vec_sum,
                                        column2vec_weighted_avg)
from column2Vec.impl.functions import get_nonnumerical_data

MODEL = 'bert-base-nli-mean-tokens'
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def time_measure_function(func, text: list, model, key: str):
    start = time.time()
    func(text, model, key)
    end = time.time()
    return end - start

class TestRunCache(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.model = SentenceTransformer(MODEL)
        fileM2 = os.path.join(THIS_DIR, os.pardir, 'data/netflix_titles.csv')
        # make an array of all the files
        files = [fileM2]
        self.data = get_nonnumerical_data(files)
        for i in self.data:
            self.first = self.data[i].head(100)
            break
        cache.set_file("generated/test.csv")
        self.model = SentenceTransformer(MODEL)

    def setUp(self):
        cache.clear_cache()
        cache.clear_persistent_cache()
        cache.on()

    def test_column2vec_as_sentence(self):

        first = time_measure_function(column2vec_as_sentence, self.first, self.model,  "a")

        second = time_measure_function(column2vec_as_sentence, self.first, self.model,  "a")
        cache.off()
        third = time_measure_function(column2vec_as_sentence, self.first, self.model,  "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_as_sentence_clean(self):

        first = time_measure_function(column2vec_as_sentence_clean, self.first, self.model, "a")

        second = time_measure_function(column2vec_as_sentence_clean, self.first, self.model, "a")

        cache.off()
        third = time_measure_function(column2vec_as_sentence_clean, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)

    def test_column2vec_as_sentence_clean_uniq(self):

        first = time_measure_function(column2vec_as_sentence_clean_uniq, self.first, self.model, "a")

        second = time_measure_function(column2vec_as_sentence_clean_uniq, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_as_sentence_clean_uniq, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)

    def test_column2vec_avg(self):

        first = time_measure_function(column2vec_avg, self.first, self.model, "a")

        second = time_measure_function(column2vec_avg, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_avg, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_weighted_avg(self):

        first = time_measure_function(column2vec_weighted_avg, self.first, self.model, "a")

        second = time_measure_function(column2vec_weighted_avg, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_weighted_avg, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")

        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_sum(self):

        first = time_measure_function(column2vec_sum, self.first, self.model, "a")

        second = time_measure_function(column2vec_sum, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_sum, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")

        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_weighted_sum(self):

        first = time_measure_function(column2vec_weighted_sum, self.first, self.model, "a")

        second = time_measure_function(column2vec_weighted_sum, self.first, self.model, "a")

        cache.off()
        third = time_measure_function(column2vec_weighted_sum, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")

        self.assertGreater(first, second)
        self.assertGreater(third, second)

class TestPersistentCache(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.model = SentenceTransformer(MODEL)
        fileM2 = os.path.join(THIS_DIR, os.pardir, 'data/netflix_titles.csv')
        # make an array of all the files
        files = [fileM2]
        self.data = get_nonnumerical_data(files)
        skip = True
        for i in self.data:
            if skip:
                skip = False
                continue
            self.first = self.data[i].head(100)
            break
        cache.set_file("cache_test.csv")
        self.model = SentenceTransformer(MODEL)

    def setUp(self):
        cache.clear_cache()
        cache.clear_persistent_cache()
        cache.on()

    def test_column2vec_as_sentence(self):

        first = time_measure_function(column2vec_as_sentence, self.first, self.model,  "a")
        cache.save_persistently()
        cache.clear_cache()

        second = time_measure_function(column2vec_as_sentence, self.first, self.model,  "a")
        cache.off()
        third = time_measure_function(column2vec_as_sentence, self.first, self.model,  "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_as_sentence_clean(self):

        first = time_measure_function(column2vec_as_sentence_clean, self.first, self.model, "a")
        cache.save_persistently()
        cache.clear_cache()

        second = time_measure_function(column2vec_as_sentence_clean, self.first, self.model, "a")

        cache.off()
        third = time_measure_function(column2vec_as_sentence_clean, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)

    def test_column2vec_as_sentence_clean_uniq(self):

        first = time_measure_function(column2vec_as_sentence_clean_uniq, self.first, self.model, "a")
        cache.save_persistently()
        cache.clear_cache()

        second = time_measure_function(column2vec_as_sentence_clean_uniq, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_as_sentence_clean_uniq, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)

    def test_column2vec_avg(self):

        first = time_measure_function(column2vec_avg, self.first, self.model, "a")
        cache.save_persistently()
        cache.clear_cache()

        second = time_measure_function(column2vec_avg, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_avg, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")
        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_weighted_avg(self):

        first = time_measure_function(column2vec_weighted_avg, self.first, self.model, "a")
        cache.save_persistently()
        cache.clear_cache()

        second = time_measure_function(column2vec_weighted_avg, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_weighted_avg, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")

        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_sum(self):

        first = time_measure_function(column2vec_sum, self.first, self.model, "a")
        cache.save_persistently()
        cache.clear_cache()

        second = time_measure_function(column2vec_sum, self.first, self.model, "a")
        cache.off()
        third = time_measure_function(column2vec_sum, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")

        self.assertGreater(first, second)
        self.assertGreater(third, second)


    def test_column2vec_weighted_sum(self):

        first = time_measure_function(column2vec_weighted_sum, self.first, self.model, "a")
        cache.save_persistently()
        cache.clear_cache()

        second = time_measure_function(column2vec_weighted_sum, self.first, self.model, "a")

        cache.off()
        third = time_measure_function(column2vec_weighted_sum, self.first, self.model, "a")

        print(f"{first} : {second} : {third}")

        self.assertGreater(first, second)
        self.assertGreater(third, second)

if __name__ == '__main__':
    unittest.main()
