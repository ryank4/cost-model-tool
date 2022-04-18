import pytest

import pricing.database.rds_attributes as rds_attributes
from pricing.database.rds_pricing import RDS

rds = RDS()

def test_get_rds_instance_types():
    actual = rds_attributes.get_rds_instance_types()

    assert type(actual) == dict


def test_get_db_instance_price():
    region = "US East (Ohio)"
    instance_type = "db.m4.10xlarge"
    deployment_option = "Single-AZ"

    expected = 3.502

    actual = float(rds.get_db_instance_price(region, instance_type, deployment_option))

    assert actual == expected


def test_get_storage_price():
    region = "US East (Ohio)"
    volume_type = "General Purpose (SSD)"
    deployment_option = "Single-AZ"
    storage_amount = 100

    expected = 11.50

    actual = rds.get_storage_price(region, volume_type, deployment_option, storage_amount)

    assert actual == expected


def test_calc_total_cost():
    expected = 2567.96
    actual = rds.calc_total_cost(3.502, 11.50)

    assert actual == expected