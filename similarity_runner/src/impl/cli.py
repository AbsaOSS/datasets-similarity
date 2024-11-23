import argparse
from typing import Any

from logging_ import logger
from similarity_framework.src.impl.comparator.comparator_by_column import ComparatorByColumn
from similarity_framework.src.impl.comparator.comparator_by_type import ComparatorByType
from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.interfaces.comparator.comparator import Comparator
from similarity_framework.src.interfaces.metadata.metadata_creator import MetadataCreator
from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_framework.src.models.similarity import SimilarityOutput
from similarity_framework.src.models.settings import AnalysisSettings, Settings
from similarity_runner.src.interfaces.ui import UI
from similarity_runner.src.impl.filesystem_connector import FilesystemConnector


class CLI(UI):

    REGISTERED_CONNECTORS = {
        FilesystemConnector,
    }

    def show(self, result: dict[tuple[str, str], SimilarityOutput], settings: AnalysisSettings):
        for tables, res in result.items():
            print(f"{tables[0]}, {tables[1]}: {res.distance}\n")

    def _load_user_input(self) -> Any:
        parser = argparse.ArgumentParser(
            prog="SimilarityRunner CLI",
            description="This is a CLI for interaction with similarity-framework, which is a framework for comparing data",
        )
        parser.add_argument("-c", "--config", help="Configuration file for configure analyses settings", required=False, default=".config")
        subparsers = parser.add_subparsers(
            title="Connectors",
            description=f"Available connectors: {', '.join([item.get_name() for item in self.REGISTERED_CONNECTORS])}",
            dest="connector",
            required=True,
        )

        for connector in self.REGISTERED_CONNECTORS:
            connector_parser = subparsers.add_parser(connector.get_name(), help=f"{connector.get_name().capitalize()} connector")
            for field, description in connector.get_settings_class().required_fields():
                connector_parser.add_argument(f"--{field}", help=description, required=True)
            for field, description in connector.get_settings_class().optional_fields():
                connector_parser.add_argument(f"--{field}", help=description, required=False)
        return parser.parse_args()

    def _parse_input(self, data: Any) -> tuple[list[MetadataCreatorInput], Comparator, MetadataCreator, AnalysisSettings]:
        # TODO: Add file path validation, for this we may want to use pydantic validation methods or just create method called .validate() on analysis settings
        #  and ConnectorSettings
        # TODO: Add proper exception handling, for example when invalid settings is provided to config creation it can raise Error

        # TODO: Consider adding this, this would allow using only CLI or using CLI and config file !
        #   https://docs.pydantic.dev/latest/concepts/pydantic_settings/#command-line-support
        settings: Settings = Settings.load(data.config)
        for connector_class in self.REGISTERED_CONNECTORS:
            if data.connector == connector_class.get_name():
                connector_settings = connector_class.get_settings_class()(**data.__dict__)
                break
        connector = connector_class()

        match settings.comparator:
            case "by_column":
                comparator = ComparatorByColumn.from_settings(settings.analysis_settings)
            case "by_type":
                comparator = ComparatorByType.from_settings(settings.analysis_settings)
            case _:
                raise ValueError("Invalid comparator")
        match settings.metadata_creator:
            case "type":
                metadata_creator = TypeMetadataCreator.from_settings(settings.analysis_settings)
            case _:
                raise ValueError("Invalid metadata creator")
        logger.info(f"Using {comparator.__class__.__name__} and {metadata_creator.__class__.__name__}")
        return (connector.get_data(connector_settings), comparator, metadata_creator, settings.analysis_settings)
