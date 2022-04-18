import pytest

import pricing.compute.ec2.data_transfer_costs as data_transfer_costs
import pricing.compute.ec2.ec2_attributes as ec2_attributes
from pricing.compute.ec2.ec2_pricing import EC2

def test_ec2_price():
    os = "Linux"
    instance_type = "c5.large"
    region = "us-east-1"

    ec2 = EC2()
    expected_price = 62.05
    actual_price = ec2.get_instance_price(os, instance_type, region)
    actual_price = float(actual_price) * 730
    assert round(actual_price, 2) == expected_price


def test_calculate_outbound_to_internet_data_cost():
    to = 'internet'
    amount = 10
    expected = 921.60
    actual = data_transfer_costs.calculate_outbound_data_cost(to, amount)
    assert round(actual, 2) == expected


def test_calculate_outbound_to_region_data_cost():
    to = 'other regions'
    amount = 10
    expected = 204.80
    actual = data_transfer_costs.calculate_outbound_data_cost(to, amount)
    assert round(actual, 2) == expected


def test_calculate_intra_region_data_cost():
    amount = 2
    expected = 40.96
    actual = data_transfer_costs.calculate_intra_region_data_cost(amount)
    assert round(actual, 2) == expected


def test_describe_instance_types():
    instance_type = "a1.2xlarge"
    expected = {
        "vCPUs": 8,
        "Memory(GiB)": 16,
        "Network": "Up to 10 Gigabit",
        "GPUs": "NA"
    }
    actual = ec2_attributes.describe_instance_types(instance_type)

    assert actual == expected


'''The following tests should return a dict
   Since the dict content is constantly changing,
   the exact contents and size will be unknown'''


def test_get_ec2_operating_systems():
    actual = ec2_attributes.get_ec2_operating_systems()

    assert type(actual) == dict


def test_get_ec2_regions():
    actual = ec2_attributes.get_ec2_regions()

    assert type(actual) == dict


def test_get_ec2_instance_types():
    actual = ec2_attributes.get_ec2_instance_types()

    assert type(actual) == dict

