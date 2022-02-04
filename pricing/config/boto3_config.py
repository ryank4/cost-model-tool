import boto3


class ConfigureClient:
    def __init__(self):
        self.client = boto3.client('pricing', aws_access_key_id='AKIAUZAPGFSBAY4EVNPG',
                                    aws_secret_access_key='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',
                                    region_name='us-east-1')


