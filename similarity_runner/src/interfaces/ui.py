import abc
import json
from typing import Any

from logging_ import logger
from similarity_framework.src.interfaces.comparator.comparator import Comparator
from similarity_framework.src.interfaces.metadata.metadata_creator import MetadataCreator
from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_framework.src.models.similarity import SimilarityOutput
from similarity_framework.src.models.settings import AnalysisSettings


class UI(abc.ABC):
    @abc.abstractmethod
    def _load_user_input(self) -> Any:
        pass

    @abc.abstractmethod
    def _parse_input(self, data: Any) -> tuple[list[MetadataCreatorInput], Comparator, MetadataCreator, AnalysisSettings]:
        pass

    @abc.abstractmethod
    def show(self, result:  dict[tuple[str, str], SimilarityOutput], settings: AnalysisSettings):
        pass

    def run(self):
        something = self._load_user_input()
        metadata_input, comparator, metadata_creator, analysis_settings = self._parse_input(something)
        logger.debug("Analysis settings: ")
        logger.debug(json.dumps(analysis_settings.model_dump(), indent=4))
        logger.info(f"Metadata input has {len(metadata_input)} elements")
        metadata = []
        for i in metadata_input:
            metadata.append(metadata_creator.get_metadata(i))
        logger.info(f"Loaded metadata with size {len(metadata)}")

        result = dict()
        for first in metadata:
            for second in metadata:
                result[(first.name, second.name)] = comparator.compare(first, second, analysis_settings)
        # TODO: based on analysis settings get specified metadata objects
        self.show(result, analysis_settings)
