# Similarity Runner

`similarityRunner` is a Python package designed to simplify the computation of similarity between datasets.
It provides a streamlined pipeline for creating metadata and computing similarity metrics using various comparators. 
The package is highly modular, allowing users to customize and extend its functionality to suit their specific needs.

## Features

- **Metadata Creation**: Generate metadata for datasets, with different settings and configurations.
- **Similarity Computation**: Compute similarity metrics between datasets using different comparator implementations.
- **Integration with Other Tools**: Seamlessly integrates with other components in the project, such as `Comparator` and `ComparatorByColumns`.

## Structure

- **Folder `interfaces`**: Contains interface definitions for connectors, formaters and user interaction.
- **Folder `models`**: Contains all models used for interfaces.
- **Folder `formators`**: Contains formators for different data types.
- **Folder `connectors`**: Contains connectors for different data sources.
- **Folder `UI`**: Contains user interfaces for interacting with the similarity pipeline.

## Usage

To run the similarity pipeline, use the `run` function with appropriate settings. 
The pipeline can be configured to run in different modes, 
such as creating metadata only, computing similarity only, or both.

Or run the similarity pipeline, use the following command:

```bash
PYTHONPATH="./similarity:./similarityRunner:$PYTHONPATH" python similarityRunner/UI/run_similarity.py data all by_type 

```
