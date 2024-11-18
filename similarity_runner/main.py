from pprint import pprint

import pandas as pd

from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.impl.comparator.comparator_by_column import ComparatorByColumn
from similarity_framework.src.models.metadata import MetadataCreatorInput

from similarity_runner.src.impl.filesystem_connector import FilesystemConnector
from similarity_runner.src.models.connectors import FileType, FSConnectorSettings

data = FilesystemConnector().get_data(
    settings=FSConnectorSettings(
        files_paths=["../tests/data/autoscout24-germany-dataset.csv"],
        directory_paths=["../tests/data"],
        filetypes=(FileType.CSV,)
    )
)

