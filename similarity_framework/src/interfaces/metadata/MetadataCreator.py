from abc import ABC

from src.models.metadata import Metadata


class MetadataCreator(ABC):
    def get_metadata(self) -> Metadata:
        pass
