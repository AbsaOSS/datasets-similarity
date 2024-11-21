import abc
import sys
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
from similarity_runner.src.models.connectors import ConnectorSettings, FSConnectorSettings, FileType
from similarity_runner.src.impl.filesystem_connector import FilesystemConnector


class UI(abc.ABC):
    @abc.abstractmethod
    def _load_user_input(self) -> Any:
        pass

    @abc.abstractmethod
    def _parse_input(self, data: Any) -> tuple[list[MetadataCreatorInput], Comparator, MetadataCreator, AnalysisSettings]:
        pass

    @abc.abstractmethod
    def show(self, result: list[SimilarityOutput], settings: AnalysisSettings):
        pass


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
        self.show(result, analysis_settings)
