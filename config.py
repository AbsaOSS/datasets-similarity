# add configuration
# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage
import logging
import os
from typing import Optional

import certifi
from sentence_transformers import SentenceTransformer


def configure():
    print("Configuring.")
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
    os.environ['CURL_CA_BUNDLE'] = certifi.where()
    print(f"Environment configured. {certifi.where()}")


class Configuration:
    def __init__(self, log_level: Optional[int] = logging.INFO,
                 cache_file: str = "cache.txt", cache_save_persistently: bool = False):
        self.log_level: Optional[int] = log_level
        self.cache_file: str = cache_file
        self.cache_save_persistently: bool = cache_save_persistently
        configure()
