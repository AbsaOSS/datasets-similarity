from abc import ABC
from similarity_framework.src.models.metadata import Metadata, MetadataCreatorInput


class MetadataCreator(ABC):
    def __init__(self, input_: MetadataCreatorInput):
        self.dataframe = input_.dataframe

    def get_metadata(self) -> Metadata:
        pass
