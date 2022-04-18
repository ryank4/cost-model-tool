import pytest

from pricing.storage.s3.s3 import S3

s3 = S3()

def test_put_copy_post_list_requests_price():
    region = 'US East (Ohio)'
    requests = 1000000
    expected = 5.00

    actual = s3.put_copy_post_list_requests_price(region) * requests

    assert actual == expected


def test_get_select_requests_price():
    region = 'US East (Ohio)'
    requests = 1000000
    expected = 0.40

    actual = s3.get_select_requests_price(region) * requests

    assert round(actual, 2) == expected


def test_get_storage_prices():
    region = 'US East (Ohio)'
    amount = 500
    expected = 11.50

    actual = s3.get_storage_prices(region, amount)

    assert actual == expected


def test_get_data_returned_price():
    region = 'US East (Ohio)'
    amount = 1000
    expected = 0.70

    actual = s3.get_data_returned_price(region) * amount

    assert actual == expected


def test_get_data_scanned_price():
    region = 'US East (Ohio)'
    amount = 1000
    expected = 2.00

    actual = s3.get_data_scanned_price(region) * amount

    assert actual == expected
