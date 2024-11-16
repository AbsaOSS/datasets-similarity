import boto3

from interfaces.ConnectorInterface import ConnectorInterface
from models.connector_models import ConnectorOutput, Output, S3ConnectorSettings


class S3Connector(ConnectorInterface):
    def __init__(self, config):
        self.config = config

    def _connect_and_load_data_source(self, settings: S3ConnectorSettings) -> ConnectorOutput:
        # https://www.gormanalysis.com/blog/connecting-to-aws-s3-with-python/
        s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-2',
            aws_access_key_id='mykey',
            aws_secret_access_key='mysecretkey'
        )

    def _format_data(self, data: ConnectorOutput) -> Output:
        pass

    def close(self):
        pass