import abc
from typing import Any

from similarity_framework.src.impl.comparator.comparator_by_column import ComparatorByColumn
from similarity_framework.src.impl.comparator.comparator_by_type import ComparatorByType
from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.interfaces.comparator.comparator import Comparator
from similarity_framework.src.interfaces.metadata.MetadataCreator import MetadataCreator
from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_runner.src.interfaces.connector import ConnectorInterface
from similarity_framework.src.models.analysis import AnalysisSettings
from similarity_runner.src.models.connectors import ConnectorSettings, FSConnectorSettings, FileType
from similarity_runner.src.impl.filesystem_connector import FilesystemConnector


class UI(abc.ABC):
    @abc.abstractmethod
    def _load_user_input(self) -> Any:
        pass


    @abc.abstractmethod
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


    def run(self):
        something = self._load_user_input()
        metadata_input, comparator, metadata_creator, analysis_settings = self._parse_input(something)

        metadata = []
        for i in metadata_input:
            metadata.append(metadata_creator.get_metadata(i))

        result = []
        for first in metadata:
            for second in metadata:
                result.append(comparator.compare(first, second))
        # TODO: based on analysis settings get specified metadata objects
        print("Result: ", result)