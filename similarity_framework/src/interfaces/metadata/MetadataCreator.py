from abc import ABC, abstractmethod
from dataclasses import dataclass

from similarity_framework.src.models.metadata import Metadata, MetadataCreatorInput


class MetadataCreator(ABC):
    @dataclass
    class __FunctionsParams:
        func: callable
        args: tuple
        kwargs: dict

    @staticmethod
    def buildermethod(func):
        def inner1(*args, **kwargs):
            if not args[0].create:
                args[0].functions_to_run.append(MetadataCreator.__FunctionsParams(func=func, args=args, kwargs=kwargs))
                return args[0]
            else:
                func(*args, **kwargs)
                return args[0]
        return inner1

    def __init__(self, input_: MetadataCreatorInput):
        self.dataframe = input_.dataframe
        self.functions_to_run = list()
        self.create = False
        self.metadata = Metadata()

    @abstractmethod
    def _get_metadata_impl(self):
        pass

    def get_metadata(self) -> Metadata:
        self._get_metadata_impl()
        self.create = True
        for fun in self.functions_to_run:
            fun.func(*fun.args, **fun.kwargs)
        self.functions_to_run = set()
        self.functions_to_run = list()
        return self.metadata
