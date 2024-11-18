import abc
from typing import Any

from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.interfaces.comparator.comparator import Comparator
from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_runner.src.interfaces.connector import ConnectorInterface
from similarity_runner.src.models.analysis import AnalysisSettings
from similarity_runner.src.models.connectors import ConnectorSettings


class UI(abc.ABC):
    @abc.abstractmethod
    def _load_user_input(self) -> Any:
        pass

    @abc.abstractmethod
    def _parse_input(self, data: Any) -> tuple[ConnectorInterface, ConnectorSettings, Comparator, AnalysisSettings]:
        pass

    def run(self):
        something = self._load_user_input()
        connector, connector_settings, comparator, analysis_settings = self._parse_input(something)

        metadata_input: list[MetadataCreatorInput] = connector.get_data(connector_settings)
        metadata = []
        for i in metadata_input:
            metadata.append(
                # TODO: call specific methods on connector based on analysis settings
                TypeMetadataCreator(i)
                    .compute_basic_types()
                    .get_metadata()
            )
        # TODO: call specific methods on comparator
        # TODO: based on analysis settings get specified metadata objects
        result = comparator.compare(..., ...)
        print("Result: ", result)