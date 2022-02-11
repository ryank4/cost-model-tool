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
    # try:
    #     attribute = client.get_attribute_values(
    #         ServiceCode=service_code,
    #         AttributeName=attribute_name
    #     )
    #     return attribute
    # except Exception as e:
    #     return e
    paginator = client.get_paginator('get_attribute_values')

    response_iterator = paginator.paginate(
        ServiceCode=service_code,
        AttributeName=attribute_name,
        PaginationConfig={
            'PageSize': 100
        }
    )

    instance_types = []
    for response in response_iterator:
        for instance_type_value in response["AttributeValues"]:
            instance_types.append(instance_type_value)

    return instance_types

def get_products(region):
    paginator = client.get_paginator('get_products')

    response_iterator = paginator.paginate(
        ServiceCode="AmazonEC2",
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': region
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'instanceType',
                'Value': 'm5.large'
            }
        ],
        PaginationConfig={
            'PageSize': 100
        }
    )

    products = []
    for response in response_iterator:
        for priceItem in response["PriceList"]:
            priceItemJson = json.loads(priceItem)
            products.append(priceItemJson)

    print(products)

def test(service_code, attribute_name):
    paginator = client.get_paginator('get_attribute_values')

    response_iterator = paginator.paginate(
        ServiceCode=service_code,
        AttributeName=attribute_name,
        PaginationConfig={
            'PageSize': 100
        }
    )

    instance_types = []
    for response in response_iterator:
        for instance_type_value in response["AttributeValues"]:
            instance_types.append(instance_type_value)

    return instance_types
#aws = AWS_Services()
#test('AmazonEC2', 'instanceType')
#describe_service('AmazonS3')
#get_attribute_values('AmazonS3', 'toLocation')
#get_products('EU (Ireland)')
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
