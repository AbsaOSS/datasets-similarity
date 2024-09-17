"""Configuration module."""

# add configuration
# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage

import os
import certifi


def configure():
    print("Configuring.")
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
    os.environ["CURL_CA_BUNDLE"] = certifi.where()
    print(f"Environment configured. {certifi.where()}")


class Configuration: ...
