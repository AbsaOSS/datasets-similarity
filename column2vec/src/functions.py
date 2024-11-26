"""
Functions usefull for column2Vec.
"""

import time
from typing import Any
from collections.abc import Callable

import numpy as np
import pandas as pd
import plotly.express as px
from sentence_transformers import (
    SentenceTransformer,
)
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

from constants import trained_model
from similarity_framework.src.impl.comparator.utils import cosine_sim
from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_framework.src.models.types_ import NONNUMERICAL


def get_nonnumerical_data(
    files: list[str],
) -> dict[str, list]:
    """
    Reads all csv files (which name is in files). Creates metadata for them.
    Save only nonnumerical columns into dictionary. Key is a name of column.
    Value is column.
    :param files: List names of csv files
    :return: dictionary of all tables.
    """
    result = {}
    index = 0
    for i in files:
        index += 1
        data = pd.read_csv(i)
        metadata_creator = TypeMetadataCreator().compute_advanced_structural_types().compute_column_kind()
        metadata1 = metadata_creator.get_metadata(MetadataCreatorInput(dataframe=data))
        column_names = metadata1.get_column_names_by_type(NONNUMERICAL)
        for name in column_names:
            print(f" {i} : {name}")
            result[name + str(index)] = data[name]
    return result


def get_vectors(
    function: Callable[
        [pd.Series, SentenceTransformer, str],
        list,
    ],
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Creates embedding vectors from column by using one of
     the column2Vec implementations.
    It also prints progress percent and elapsed time.
    :param function: Is one of the column2Vec implementations
    :param data: Data is a result from get_nonnumerical_data,
                dictionary of all columns in all tables.
    :return: Dictionary of embeddings, each column has its own embedding.
    """
    start = time.time()
    result = {}
    count = 1
    for key in data:
        print("Processing column: " + key + " " + str(round((count / len(data)) * 100, 2)) + "%")
        result[key] = function(
            data[key],
            trained_model.get_module(),
            key,
        )
        count += 1
    end = time.time()
    print(f"ELAPSED TIME :{end - start}")
    return result


def get_clusters(
    vectors_to_cluster: pd.DataFrame,
    n_clusters: int,
) -> list[list[str]]:
    """
    Creates clusters by KMeans for given vectors.

    :param vectors_to_cluster: Embeddings for all column
    :param n_clusters: number of clusters we want
    :return: List, for each cluster number it contains a list of column names
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)  # Change n_clusters as needed
    list_of_vectors = np.array(list(vectors_to_cluster.values()))
    kmeans.fit(list_of_vectors)

    clusters = [[]] * n_clusters
    for i in range(n_clusters):
        names = []
        for cluster, name in zip(
            kmeans.labels_,
            vectors_to_cluster.keys(),
        ):
            if cluster == i:
                names.append(name)
        clusters[i] = names

    return clusters


def plot_clusters(vectors_to_plot: pd.DataFrame, title: str):
    """
    From vectors creates clusters by Kmeans then it transforms clusters
     by TSNE(t-distributed Stochastic Neighbor Embedding).
     It plots de graphics, and it saves the plot as file
    :param vectors_to_plot: dataframe
    :param title: title of plot containing name of function
    """
    n_clusters = 12
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)  # Change n_clusters as needed
    list_of_vectors = np.array(list(vectors_to_plot.values()))
    kmeans.fit(list_of_vectors)

    tsne = TSNE(n_components=2, random_state=0)
    reduced_vectors = tsne.fit_transform(list_of_vectors)

    df = pd.DataFrame(reduced_vectors, columns=["x", "y"])
    df["names"] = vectors_to_plot.keys()
    # The cluster labels are returned in kmeans.labels_
    df["cluster"] = kmeans.labels_

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="cluster",
        hover_data=["names"],
    )
    fig.update_layout(title=title)
    fig.write_html(title.replace(" ", "_") + ".html")
    fig.show()


def compute_distances(vectors: dict):
    """
    Compute distance for each pair of vectors.

    :param vectors: Dictionary of embedding vectors
    :return: matrix with distances
    """
    res = {}
    for key1, vec1 in vectors.items():
        res[key1] = {}
        for key2, vec2 in vectors.items():
            res[key1][key2] = 1 - cosine_sim(vec1, vec2)
    return res
