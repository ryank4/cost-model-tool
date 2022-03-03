import pytest

import pricing.compute.ec2.data_transfer_costs as data_transfer_costs
import pricing.compute.ec2.ec2_attributes as ec2_attributes

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

def test_get_ec2_operating_systems():
    expected = dict.fromkeys((range(6)))
    actual = ec2_attributes.get_ec2_operating_systems()

    assert len(actual) == len(expected)

def test_get_ec2_regions():
    expected = dict.fromkeys((range(19)))
    actual = ec2_attributes.get_ec2_regions()

    assert len(actual) == len(expected)

def test_get_ec2_instance_types():
    expected = dict.fromkeys((range(562)))
    actual = ec2_attributes.get_ec2_instance_types()

    assert len(actual) == len(expected)
