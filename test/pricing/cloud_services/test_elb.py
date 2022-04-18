import pytest

from pricing.network.elb_pricing import ELB

elb = ELB()
region = 'US East (Ohio)'

def test_get_price_per_nlb_hour():
    expected = 0.0225
    actual = elb.get_price_per_nlb_hour(region)

    actual = float(actual['NLB-hour'][0])

    assert actual == expected


def test_calc_nlb_charge():
    expected = 16.43
    actual = elb.get_price_per_nlb_hour(region)

    actual = float(actual['NLB-hour'][0]) * 730

    assert round(actual, 2) == expected


def test_calc_tcp_traffic():
    bytes_processe = 1
    new_connection = 1
    connection_duration = 30

    expected = 4.38

    actual = elb.calc_tcp_traffic(region, bytes_processe, new_connection, connection_duration)

    assert round(actual, 2) == expected


def test_calc_udp_traffic():
    bytes_processe = 2
    new_connection = 1
    connection_duration = 60

    expected = 8.76

    actual = elb.calc_udp_traffic(region, bytes_processe, new_connection, connection_duration)

    assert round(actual, 2) == expected


def test_calc_tls_traffic():
    bytes_processe = 3
    new_connection = 2
    connection_duration = 120

    expected = 13.14

    actual = elb.calc_tls_traffic(region, bytes_processe, new_connection, connection_duration)

    assert round(actual, 2) == expected

def test_calc_total_nlcu_charge():
    expected = 26.28
    actual = elb.calc_total_nlcu_charge(4.38, 8.76, 13.14)

    assert actual == expected


def test_calc_total_monthly_cost():
    expected = 42.71
    actual = elb.calc_total_monthly_cost(16.43, 26.28)

    assert actual == expected

