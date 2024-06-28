import os
import pickle
import time

import pandas as pd
from sentence_transformers import SentenceTransformer

from column2Vec.Column2Vec import column2vec_as_sentence, column2vec_as_sentence_clean, \
    column2vec_as_sentence_clean_uniq, column2vec_weighted_sum, column2vec_sum, column2vec_weighted_avg, column2vec_avg, \
    cache
from column2Vec.functions import get_nonnumerical_data
from column2Vec.reaserch.generate_report import generate_report, generate_time_report
from config import configure
from constants import warning_enable
from similarity.Comparator import cosine_sim

FUNCTIONS = [column2vec_as_sentence, column2vec_as_sentence_clean, column2vec_as_sentence_clean_uniq,
             column2vec_avg, column2vec_weighted_avg, column2vec_sum, column2vec_weighted_sum]
MODEL = 'paraphrase-multilingual-mpnet-base-v2'#'bert-base-nli-mean-tokens'
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
model = SentenceTransformer(MODEL)

# otestovani stability pokazde stejne vysledky
def stability_test(column1: pd.Series, function, key):

    emb1 = function(column1, model, key)
    emb2 = function(column1, model, key+"s1")
    emb3 = function(column1, model, key+"s2")
    first_second = cosine_sim(emb3, emb2)
    whole_second = cosine_sim(emb1, emb2)
    whole_first = cosine_sim(emb3, emb1)
    # all_same = emb1.any() == emb2 and emb3 == emb1
    if first_second != 1 or whole_second != 1 or whole_first != 1 : #or not all_same:
        return False, f"For {key}:\n is not stable\n"
    return True, f"For {key}: is stable\n"


# otestovani podobnosti sloupcu se stejnym vektorem
def similarity_test(column1: pd.Series, function, key: str):
    pass


# otestovani ze nestejne sloupce(vektory) jsou dostatecne daleko
def non_similar_test(column1: pd.Series, function, key: str):
    pass

def time_test(column1: pd.Series, function, key: str):
    cache.set_file("no_file.txt")
    cache.clear_cache()
    start = time.time()
    function(column1, model, key)
    end = time.time()
    return True, (end - start)


# sloupce ktere maji jen cast dat by meli byt stejne jako sloupce cele
def partial_column_test(column1: pd.Series, function, key: str) -> (bool, str):
    length = column1.size
    first_half = column1.head(int(length / 2))
    second_half = column1.tail(int(length / 2))

    emb1 = function(column1, model, key)
    emb2 = function(first_half, model, key+str(1))
    emb3 = function(second_half, model, key+str(2))
    first_second = cosine_sim(emb3, emb2)
    whole_second = cosine_sim(emb1, emb2)
    whole_first = cosine_sim(emb3, emb1)
    if first_second != 1 or whole_second != 1 or whole_first != 1:
        print((f"For {key}, {function}:\n whole column and first half: {whole_first}\n "
                       f"whole column and second half: {whole_second}\n first half"
                       f" and second half: {first_second}\n"))
        return False, (whole_first, whole_second, first_second)
    else:
        return True, f"For {key}:\n is stable\n"


def test_func(data, test_type):
    i = 0
    result = dict()
    for name in data.keys():
        result[name] = dict()
        # print(f"--- Start Column: {name} ---\n")
        # print("AS SENTENCE")
        result[name]["SENTENCE"] = test_type(data[name], column2vec_as_sentence, name)
        # print("AS CLEAR SENTENCE")
        result[name]["CLEAR SENT."] = test_type(data[name], column2vec_as_sentence_clean, name)
        # print("AS CLEAR UNIQUE SENTENCE")
        result[name]["CLEAR UNIQ SENT."] = test_type(data[name], column2vec_as_sentence_clean_uniq, name)
        # print("AVERAGE")
        result[name]["AVERAGE"] = test_type(data[name], column2vec_avg, name)
        # print("WEIGHTED AVERAGE")
        result[name]["W. AVERAGE"] = test_type(data[name], column2vec_weighted_avg, name)
        # print("SUM")
        result[name]["SUM"] = test_type(data[name], column2vec_sum, name)
        # print("WEIGHTED SUM")
        result[name]["W. SUM"] = test_type(data[name], column2vec_weighted_sum, name)
        i += 1
        cache.save_persistently()
        cache.clear_cache()
    return result
    # partitial_column_test()
    # print(f"vypsano: {i}, data {len(data)}")


def read_data():
    try:
        with open('nonnumerical_data.pkl', 'rb') as f:
            data = pickle.load(f)
        print("FILE READ")
    except FileNotFoundError:
        print("GENERATING")
        ## todo files from both dir
        fileA1 = os.path.join(THIS_DIR, os.pardir, '../data/aircraft-data_nov_dec.csv')
        fileA2 = os.path.join(THIS_DIR, os.pardir, '../data/Airplane_Cleaned.csv')
        fileC1 = os.path.join(THIS_DIR, os.pardir, '../data/autoscout24-germany-dataset.csv')
        fileC2 = os.path.join(THIS_DIR, os.pardir, '../data/CARS_1.csv')
        fileC3 = os.path.join(THIS_DIR, os.pardir, '../data/USA_cars_datasets.csv')
        fileM1 = os.path.join(THIS_DIR, os.pardir, '../data/imdb_top_1000.csv')
        fileM2 = os.path.join(THIS_DIR, os.pardir, '../data/netflix_titles.csv')

        files = [fileA1, fileA2, fileC1, fileC2, fileC3, fileM1, fileM2]
        data = get_nonnumerical_data(files)

        with open('nonnumerical_data.pkl', 'wb') as f:
            pickle.dump(data, f)
    return data
def run_fun():
    data = read_data()
    cache.set_file("cache_remv.txt")
    generate_time_report(test_func(data, time_test), "REP_time_test")
    # generate_report(test_func(data, @ ), "REP_partial_column_test")
    # generate_report(test_func(data, stability_test), "REP_stability_test")

configure()
warning_enable.change_status(True)

run_fun()