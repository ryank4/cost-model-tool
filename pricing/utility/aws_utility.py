import json

from pricing.config.boto3_config import ConfigureClient

client = ConfigureClient().client

def get_all_services():
    try:
        service_code_list = []
        data = client.describe_services()
        for value in data['Services']:
            service_code_list.append(json.dumps(value['ServiceCode']))
       # print(service_code_list)
        return service_code_list

    except Exception as e:
        return e

def describe_service(service_code):
    try:
        service = client.describe_services(ServiceCode=service_code)
        return service
    except Exception as e:
        return e

def get_attribute_values(service_code, attribute_name):
    try:
        attribute = client.get_attribute_values(
            ServiceCode=service_code,
            AttributeName=attribute_name,
        )
        return attribute
    except Exception as e:
        return e


#aws = AWS_Services()
'''
aws.get_all_services()
aws.describe_service('AmazonEC2')
aws.get_attribute_values('AmazonEC2', 'volumeType')
aws.get_attribute_values('AmazonEC2', 'volumeApiName')
aws.get_attribute_values('AmazonEC2', 'maxThroughputvolume')
aws.get_attribute_values('AmazonEC2', 'maxIopsvolume')
aws.get_attribute_values('AmazonEC2', 'maxVolumeSize')

aws.get_all_services()
aws.describe_service('AmazonEC2')
aws.get_attribute_values('AmazonEC2', 'operatingSystem')
aws.get_attribute_values('AmazonEC2', 'instanceType')
aws.get_attribute_values('AmazonEC2', 'location')
'''
