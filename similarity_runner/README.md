# Similarity Runner

`similarity_runner` is a Python package designed to simplify the computation of similarity between datasets.
It provides a streamlined pipeline for creating metadata and computing similarity metrics using various comparators. 
The package is highly modular, allowing users to customize and extend its functionality to suit their specific needs.

## Features

- **Metadata Creation**: Generate metadata for datasets, with different settings and configurations.
- **Similarity Computation**: Compute similarity metrics between datasets using different comparator implementations.
- **Integration with Other Tools**: Seamlessly integrates with other components in the project, such as `Comparator` and `ComparatorByColumns`.

## Structure

- **Folder `interfaces`**: Contains interface definitions for connectors and user interaction.
- **Folder `models`**: Contains connector models explicitly FSConnectorSettings
- **Folder `impl`**: Contains file system connector implementation and implementation of user interfaces for interacting with the similarity pipeline.

## Usage


run the similarity pipeline, use the following command:

```bash
python main.py --config <path_to_config_file>

```
