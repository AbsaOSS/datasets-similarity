from itertools import compress

from similarity.DataFrameMetadata import DataFrameMetadata, CategoricalMetadata
from similarity.Types import Types
from typing import Optional

import pandas as pd
import numpy as np
import os
import re
from sentence_transformers import SentenceTransformer
import gensim.downloader as api


# def get_world_embedding(world):
#     # takes 3-10 minutes to load
#     global wv
#     if not wv:
#         wv = api.load('word2vec-google-news-300')
#     return wv[world]


# sbert_model: Optional[SentenceTransformer] = None
#
#
# def get_sbert_model() -> SentenceTransformer:
#     global sbert_model
#     if not sbert_model:
#         sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
#     return sbert_model


def load__csv_files_from_folder(folder: str) -> (list[pd.DataFrame], list[str]):
    """
    it loads cvs files from folder and returns list of loaded dataframe and list of names
    :param folder: from which we load the files
    :return: two lists
    """
    data = []
    names = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            data.append(pd.read_csv(folder + "/" + file))
            names.append(file.replace(".csv", ""))
    return data, names

def create_string_from_columns(database: list[pd.DataFrame], table_names: list[str]) -> (list[str], list[str]):
    """
    For each column in each table in database it creates string from that column.
    :param database: all tables
    :param table_names: all names of tables
    :return: list of strings representing column, list of string of the same length representing names of table for each column
    """
    sentences = []
    sentences_datasets = []
    for table, name in zip(database, table_names):
        for column in table.columns:
            sentences.append(
                str(table[column].tolist()).replace("\'", "").replace("]", "").replace("[", ""))  # column to string
            sentences_datasets.append(name)
    return sentences, sentences_datasets


