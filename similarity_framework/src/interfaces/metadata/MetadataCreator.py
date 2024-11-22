from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from similarity_framework.src.models.settings import AnalysisSettings
from similarity_framework.src.models.metadata import Metadata, MetadataCreatorInput


class MetadataCreator(ABC):
    @dataclass
    class __FunctionsParams:
        func: callable
        args: tuple
        kwargs: dict

        def __hash__(self):
            return hash(self.func) + hash(self.args) + hash(str(self.kwargs))

    @staticmethod
    def buildermethod(func):
        def inner1(*args, **kwargs):
            if not args[0].create:
                args[0].__dict__['_MetadataCreator__functions_to_run'].add(MetadataCreator.__FunctionsParams(func=func, args=args, kwargs=kwargs))
                return args[0]
            else:
                func(*args, **kwargs)
                return args[0]
        return inner1

    def __init__(self):
        self.dataframe: Optional[pd.DataFrame] = None
        self.__functions_to_run = set()
        self.create = False
        self.metadata: Optional[Metadata] = None

    @abstractmethod
    def _get_metadata_impl(self):
        pass

    def get_metadata(self, input_: MetadataCreatorInput) -> Metadata:
        self.dataframe = input_.dataframe
        self.metadata = Metadata()

        self._get_metadata_impl()
        self.create = True
        for fun in self.__functions_to_run:
            fun.func(*fun.args, **fun.kwargs)
        self.__functions_to_run = set()
        self.create = False
        return self.metadata

    @staticmethod
    @abstractmethod
    def from_settings(settings: AnalysisSettings) -> "MetadataCreator":
        pass