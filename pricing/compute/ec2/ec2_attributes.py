import math

import boto3

import pricing.utility.aws_utility as aws_util
from pricing.utility import mapping


def get_ec2_operating_systems():
    data = aws_util.get_attribute_values('AmazonEC2', 'operatingSystem')

    operating_systems = {}
    index = 1
    for value in data:
        operating_systems[index] = value['Value']
        index += 1

    return operating_systems


def get_ec2_instance_types():
    data = aws_util.get_attribute_values('AmazonEC2', 'instanceType')

    instance_types = {}
    index = 1
    for value in data:
        instance_types[index] = value['Value']
        index += 1
    print(instance_types)

    return instance_types

def get_ec2_regions():
    data = mapping.region_mapping_dict

    regions = {}
    index = 1
    for value in data:
        regions[index] = value
        index += 1
    print(regions)

    return regions

def describe_instance_types(instance_type):
    client = boto3.client('ec2')
    response = client.describe_instance_types(InstanceTypes=[instance_type])
    info = response['InstanceTypes']
    instance_type_info = {}
    for i in info:
        instance_type_info['vCPUs'] = i['VCpuInfo']['DefaultVCpus']
        instance_type_info['Memory'] = math.floor(i['MemoryInfo']['SizeInMiB'] / 1000)
        instance_type_info['Network'] = i['NetworkInfo']['NetworkPerformance']
        try:
            gpu_info = i['GpuInfo']['Gpus']
            instance_type_info['GPUs'] = gpu_info[0]['Count']
        except KeyError:
            instance_type_info['GPUs'] = 'NA'

    return instance_type_info

