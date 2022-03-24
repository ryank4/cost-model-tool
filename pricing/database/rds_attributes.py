import pricing.utils.aws_utility as aws_util


def get_rds_instance_types():
    data = aws_util.get_attribute_values('AmazonRDS', 'instanceType')

    instance_types = {}
    index = 1
    for value in data:
        instance_types[index] = value['Value']
        index += 1

    return instance_types
