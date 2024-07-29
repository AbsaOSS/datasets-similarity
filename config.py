# add configuration
# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#usage
import logging
import os
import certifi


def configure():
    print("Configuring.")
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
    os.environ['CURL_CA_BUNDLE'] = certifi.where()
    # os.environ['REQUESTS_CA_BUNDLE'] = r"/etc/ssl/cert.pem"
    # os.environ['REQUESTS_CA_BUNDLE'] = r"/etc/ssl/openssl.cnf"
    print(f"Environment configured. {certifi.where()}")

class Configuration():
    ...
