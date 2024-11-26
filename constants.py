"""
This file contains constants
"""

from sentence_transformers import (
    SentenceTransformer,
)

from similarity_framework.config import configure


class TrainedModel:
    """
    Class encapsulating trained module
    """

    configure()
    __model = SentenceTransformer(
        "paraphrase-multilingual-mpnet-base-v2",
        tokenizer_kwargs={
            "clean_up_tokenization_spaces": True,
        },
    )

    def set_module(self, model: SentenceTransformer):
        """
        Sets __model
        :param model: to be set
        """
        self.__model = model

    def get_module(self) -> SentenceTransformer:
        """
        :return: __module
        """
        return self.__model


trained_model = TrainedModel()
