import pytest

from pricing.management.cloudwatch_pricing import CloudWatch

cw = CloudWatch()
region = "US East (Ohio)"

def test_get_metric_price():
    num_metrics = 10
    expected = 3
    actual = cw.get_metric_price(region, num_metrics)

    assert actual == expected


def test_api_get_metric_data():
    num_metrics = 1000000
    expected = 10
    actual = cw.api_get_metric_data(region, num_metrics)
    assert actual == expected


def test_api_get_metric_widget_image():
    num_metrics = 1000000
    expected = 20
    actual = cw.api_get_metric_widget_image(region, num_metrics)
    assert actual == expected


def test_standard_log_ingested():
    log_amount = 10
    expected = 5
    actual = cw.standard_log_ingested(region, log_amount)
    assert actual == expected


def test_log_storage():
    num_standard_logs = 10
    num_vended_logs = 5
    expected = 0.0675
    actual = cw.log_storage(region, num_standard_logs, num_vended_logs)

    assert round(actual, 4) == expected


def test_logs_delivered_cloudwatch():
    destination = "Amazon CloudWatch Logs"
    amount = 20
    expected = 10
    actual = cw.logs_delivered(region, destination, amount)

    assert actual == expected


def test_logs_delivered_s3():
    destination = "Amazon S3"
    amount = 20
    expected = 5
    actual = cw.logs_delivered(region, destination, amount)

    assert actual == expected


def test_parquet_conversion():
    num_logs = 20
    expected = 0.70
    actual = cw.parquet_conversion(region, num_logs)
    assert actual == expected
