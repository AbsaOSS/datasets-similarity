from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from similarity.Comparator import cosine_sim
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator
from similarity.Types import NONNUMERICAL


def get_data(files: list[str]) -> dict[str, Any]:
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


def get_clusters(vectors_to_cluster: pd.DataFrame, n_clusters: int) -> list[list[str]]:
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)  # Change n_clusters as needed
    list_of_vectors = np.array(list(vectors_to_cluster.values()))
    kmeans.fit(list_of_vectors)

    clusters = [[]] * n_clusters
    for i in range(n_clusters):
        names = []
        for cluster, name in zip(kmeans.labels_, vectors_to_cluster.keys()):
            if cluster == i:
                names.append(name)
        clusters[i] = names

    return clusters


def compute_distances(vectors: dict):
    res = {}
    for key1, vec1 in vectors.items():
        res[key1] = {}
        for key2, vec2 in vectors.items():
            res[key1][key2] = 1 - cosine_sim(vec1, vec2)
    return res
