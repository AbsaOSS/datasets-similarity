"""
This file is used for testing the column2Vec functions.
"""
import os
import pickle
import time
# import streamlit as st

import pandas as pd
from sentence_transformers import SentenceTransformer

from column2Vec.impl.functions import get_nonnumerical_data
from column2Vec.impl.Column2Vec import (column2vec_as_sentence, column2vec_as_sentence_clean,
                                        column2vec_as_sentence_clean_uniq, column2vec_weighted_sum,
                                        column2vec_sum,
                                        column2vec_weighted_avg, column2vec_avg, cache)

from column2Vec.reaserch.generate_report import generate_time_report, generate_sim_report, generate_stability_report, \
    generate_partial_column_report
from config import configure
from constants import warning_enable
from similarity.Comparator import cosine_sim

FUNCTIONS = [column2vec_as_sentence, column2vec_as_sentence_clean, column2vec_as_sentence_clean_uniq,
             column2vec_avg, column2vec_weighted_avg, column2vec_sum, column2vec_weighted_sum]
MODEL = 'paraphrase-multilingual-mpnet-base-v2'  # 'bert-base-nli-mean-tokens'
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
model = SentenceTransformer(MODEL)


def count_embedding(column1: pd.Series, function, key: str) -> pd.Series:
    """
    Count embeddings for column1 using function and key
    """
    return function(column1, model, key)


def stability_test(column1: pd.Series, function, key: str) -> (bool, str):
    """
    Test if function run is stable, it should produce same result every time
    :param column1: column to test
    :param function: function to use
    :param key: key for cache
    """
    emb1 = function(column1, model, key)
    emb2 = function(column1, model, key + "s1")
    emb3 = function(column1, model, key + "s2")
    first_second = cosine_sim(emb3, emb2)
    whole_second = cosine_sim(emb1, emb2)
    whole_first = cosine_sim(emb3, emb1)
    if first_second != 1 or whole_second != 1 or whole_first != 1:
        return False, f"For {key}:\n is not stable\n"
    return True, f"For {key}: is stable\n"


def similarity_test(embeddings: dict) -> dict:
    """
    Compute similarity of columns based on embeddings similarity/distance. It should be 1 for same columns.
    Result from this function will be used in generate_report for counting similar and not similar score.
    :param embeddings: embeddings of columns
    """
    keys = list(embeddings.keys())
    res = dict()
    # Initialize nested dictionaries for each function
    for function in embeddings[list(embeddings.keys())[0]].keys():
        res[function] = dict()

    for column in embeddings.keys():
        for function in embeddings[column].keys():
            for column2 in keys:
                sim = cosine_sim(embeddings[column][function], embeddings[column2][function])
                res[function][column, column2] = sim
                # res[function][column2, column] = sim
        # keys.remove(column)
    return res


def time_test(column1: pd.Series, function, key: str) -> (bool, float):
    """
    Computes how much time it takes to compute embeddings for column using specific function.
    Cache are not used for this test
    :param column1: column to test
    :param function: function to use
    :param key: key for cache
    """
    # cache.set_file("no_file.txt")
    # cache.clear_cache()
    cache.off()
    start = time.time()
    function(column1, model, key)
    end = time.time()
    cache.on()
    return True, (end - start)


def partial_column_test(column1: pd.Series, function, key: str) -> (bool, str):
    """
    Test if column with only part of data is same/similar as column with whole data
    :param column1: column to test
    :param function: function to use
    :param key: key for cache
    :return: tuple of bool and str
    """
    length = column1.size
    first_half = column1.head(int(length / 2))
    second_half = column1.tail(int(length / 2))

    emb1 = function(column1, model, key)
    emb2 = function(first_half, model, key + str(1))
    emb3 = function(second_half, model, key + str(2))
    first_second = cosine_sim(emb3, emb2)
    whole_second = cosine_sim(emb1, emb2)
    whole_first = cosine_sim(emb3, emb1)
    if first_second != 1 or whole_second != 1 or whole_first != 1:
        # print((f"For {key}, {function}:\n whole column and first half: {whole_first}\n "
        #        f"whole column and second half: {whole_second}\n first half"
        #        f" and second half: {first_second}\n"))
        return False, (whole_first, whole_second, first_second)
    else:
        return True, (whole_first, whole_second, first_second)


def test_func(data: dict, test_type: callable) -> dict:
    """
    Test all functions on all columns with specific test_type
    :param data: data to test
    :param test_type: test type to use
    :return: dict of test results
    """
    i = 0
    result = dict()
    for name in data.keys():
        result[name] = dict()
        result[name]["SENT."] = test_type(data[name], column2vec_as_sentence, name)
        result[name]["CLEAR SENT."] = test_type(data[name], column2vec_as_sentence_clean, name)
        result[name]["CL. UNIQ SENT."] = test_type(data[name], column2vec_as_sentence_clean_uniq, name)
        result[name]["AVG"] = test_type(data[name], column2vec_avg, name)
        result[name]["W. AVG"] = test_type(data[name], column2vec_weighted_avg, name)
        result[name]["SUM"] = test_type(data[name], column2vec_sum, name)
        result[name]["W. SUM"] = test_type(data[name], column2vec_weighted_sum, name)
        i += 1
        cache.save_persistently()
        cache.clear_cache()
    return result


def read_data() -> dict:
    """
    Read data from saved file (nonnumerical data from datasets)
     or read data from datasets, pick only nonnumerical data and save them.
    :return: dict of nonnumerical data
    """
    try:
        with open('files/nonnumerical_data.pkl', 'rb') as f:
            data = pickle.load(f)
        print("FILE READ")
    except FileNotFoundError:
        print("GENERATING")
        file_a1 = os.path.join(THIS_DIR, os.pardir, '../data/aircraft-data_nov_dec.csv')
        file_a2 = os.path.join(THIS_DIR, os.pardir, '../data/Airplane_Cleaned.csv')
        file_c1 = os.path.join(THIS_DIR, os.pardir, '../data/autoscout24-germany-dataset.csv')
        file_c2 = os.path.join(THIS_DIR, os.pardir, '../data/CARS_1.csv')
        file_c3 = os.path.join(THIS_DIR, os.pardir, '../data/USA_cars_datasets.csv')
        file_m1 = os.path.join(THIS_DIR, os.pardir, '../data/imdb_top_1000.csv')
        file_m2 = os.path.join(THIS_DIR, os.pardir, '../data/netflix_titles.csv')

        files = [file_a1, file_a2, file_c1, file_c2, file_c3, file_m1, file_m2]
        data = get_nonnumerical_data(files)

        with open('files/nonnumerical_data.pkl', 'wb') as f:
            pickle.dump(data, f)
    return data


def run_fun():
    """
    Run all tests
    """
    # st.title('Column2Vec Report')
    # data_load_state = st.text('Loading data...')
    data = read_data()
    cache.set_file("files/cache.txt")
    generate_time_report(test_func(data, time_test), "REP_time_test")
    # generate_sim_report(similarity_test(test_func(data, count_embedding)), "REP_")
    # generate_partial_column_report(test_func(data, partial_column_test), "REP_partial_column_test")
    # generate_stability_report(test_func(data, stability_test), "REP_stability_test")


configure()
warning_enable.change_status(True)

run_fun()
