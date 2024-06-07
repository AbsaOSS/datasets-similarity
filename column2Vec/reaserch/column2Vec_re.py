import os

import pandas as pd
from sentence_transformers import SentenceTransformer

from column2Vec.Column2Vec import column2vec_as_sentence, column2vec_as_sentence_clean, \
    column2vec_as_sentence_clean_uniq, column2vec_weighted_sum, column2vec_sum, column2vec_weighted_avg, column2vec_avg
from column2Vec.functions import get_nonnumerical_data
from similarity.Comparator import cosine_sim

FUNCTIONS = [column2vec_as_sentence, column2vec_as_sentence_clean, column2vec_as_sentence_clean_uniq,
             column2vec_avg, column2vec_weighted_avg, column2vec_sum, column2vec_weighted_sum ]
MODEL = 'bert-base-nli-mean-tokens'
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# otestovani stability pokazde stejne vysledky
def stability_test():
    pass

# otestovani podobnosti sloupcu se stejnym vektorem
def similarity_test():
    pass

# otestovani ze nestejne sloupce(vektory) jsou dostatecne daleko
def nonsimilar_test():
    pass

# sloupce ktere maji jen cast dat by meli byt stejne jako sloupce cele
def partitial_column_test(column1:pd.Series, function, key):
    length = column1.size
    first_half = column1.head(int(length/2))
    second_half = column1.tail(int(length/2))
    model = SentenceTransformer(MODEL)

    emb1 = function(column1, model, key)
    emb2 = function(first_half, model, key)
    emb3 = function(second_half, model, key)
    first_second = cosine_sim(emb3, emb2)
    whole_second = cosine_sim(emb1, emb2)
    whole_first = cosine_sim(emb3, emb1)
    if first_second != 1 or whole_second != 1 or whole_first != 1:
        print(f"For {key}:\n whole column and first half: {whole_first}\n"
              f"whole column and second half: {whole_second}\n"
              f"first half and second half: {first_second}\n"
              )




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
i = 0
for name in data.keys():
    print(f"--- Start Column: {name} ---\n")
    print("AS SENTENCE")
    partitial_column_test(data[name], column2vec_as_sentence, name)
    print("AS CLEAR SENTENCE")
    partitial_column_test(data[name], column2vec_as_sentence_clean, name)
    print("AS CLEAR UNIQUE SENTENCE")
    partitial_column_test(data[name], column2vec_as_sentence_clean_uniq, name)
    print("AVERAGE")
    partitial_column_test(data[name], column2vec_avg, name)
    print("WEIGHTED AVERAGE")
    partitial_column_test(data[name], column2vec_weighted_avg, name)
    print("SUM")
    partitial_column_test(data[name], column2vec_sum, name)
    print("WEIGHTED SUM")
    partitial_column_test(data[name], column2vec_weighted_sum, name)
    i+=1
# partitial_column_test()
# print(f"vypsano: {i}, data {len(data)}")