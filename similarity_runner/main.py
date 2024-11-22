from similarity_runner.src.impl.filesystem_connector import FilesystemConnector
from similarity_runner.src.models.connectors import FileType, FSConnectorSettings

data = FilesystemConnector().get_data(
    settings=FSConnectorSettings(files_paths=["../tests/data/autoscout24-germany-dataset.csv"], directory_paths=["../tests/data"], filetypes=(FileType.CSV,))
)
