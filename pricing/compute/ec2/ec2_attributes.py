import pricing.utility.aws_utility as aws_util
from pricing.utility import mapping


def get_ec2_operating_systems():
    data = aws_util.get_attribute_values('AmazonEC2', 'operatingSystem')

    attribute_values = data['AttributeValues']

    operating_systems = {}
    index = 1
    for value in attribute_values:
        operating_systems[index] = value['Value']
        index += 1

    return operating_systems


def get_ec2_instance_types():
    data = aws_util.get_attribute_values('AmazonEC2', 'instanceType')

    attribute_values = data['AttributeValues']

    instance_types = {}
    index = 1
    for value in attribute_values:
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

get_ec2_regions()
