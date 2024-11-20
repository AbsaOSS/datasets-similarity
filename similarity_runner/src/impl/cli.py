import abc
from typing import Any

from similarity_framework.src.impl.comparator.comparator_by_column import ComparatorByColumn
from similarity_framework.src.impl.comparator.comparator_by_type import ComparatorByType
from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.interfaces.comparator.comparator import Comparator
from similarity_framework.src.interfaces.metadata.MetadataCreator import MetadataCreator
from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_framework.src.models.similarity import SimilarityOutput
from similarity_runner.src.interfaces.connector import ConnectorInterface
from similarity_framework.src.models.analysis import AnalysisSettings
from similarity_runner.src.interfaces.ui import UI
from similarity_runner.src.models.connectors import ConnectorSettings, FSConnectorSettings, FileType
from similarity_runner.src.impl.filesystem_connector import FilesystemConnector


class CLI(UI):
    def show(self, result: list[SimilarityOutput], settings: AnalysisSettings):
        pass

    def _load_user_input(self) -> Any:
        pass


    def _parse_input(self, data: Any) -> tuple[list[MetadataCreatorInput], Comparator, MetadataCreator, AnalysisSettings]:
        # TODO: parse user input and return connector, connector_settings, comparator, analysis_settings
        analysis_settings: AnalysisSettings = AnalysisSettings()

        match data.comparator:
            case "by_column":
                comparator = ComparatorByColumn.from_settings(analysis_settings)
            case "by_type":
                comparator = ComparatorByType.from_settings(analysis_settings)
            case _:
                raise ValueError("Invalid comparator")
        match data.metadata_creator:
            case "type":
                metadata_creator = TypeMetadataCreator.from_settings(analysis_settings)
            case _:
                raise ValueError("Invalid metadata creator")

        connector_settings = FSConnectorSettings(filetypes=data.filetypes, directory_paths=data.directory_paths)

        return (FilesystemConnector().get_data(connector_settings),
                comparator,
                metadata_creator,
                analysis_settings)
