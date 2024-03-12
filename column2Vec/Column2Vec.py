import re

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


def column2vec_as_sentence(column: pd.Series, model: SentenceTransformer):
    """
    Convert a column to a vector

    Make one string from all the items in the column. Convert string to a vector by sentence transformer.
    """
    sentence = [str(column.tolist()).replace("\'", "").replace("]", "").replace("[", "")]
    return model.encode(sentence)[0]

def column2vec_avg(column: pd.Series,  model: SentenceTransformer):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the average of all the vectors
    """
    uniq_column = column.unique()
    column_clean = pd.Series(uniq_column).apply(lambda x: re.sub("[^(0-9 |a-z)]", " ", str(x).lower())).values
    encoded_columns = model.encode(column_clean)
    to_ret = np.mean(encoded_columns, axis=0)
    return to_ret
