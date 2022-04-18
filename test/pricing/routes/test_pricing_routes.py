import json

import pytest

from app._app import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client


def test_ec2_price_success(test_client):
    response = test_client.post('/pricing/ec2',
                                data=json.dumps(dict(os='Linux',
                                                     instance_type='c5.large',
                                                     region='US East (Ohio)',
                                                     dataIntra='1',
                                                     dataOutTo='Internet',
                                                     dataOut='2')),
                                content_type='application/json')

    assert response.status_code == 200
    res = json.loads(response.data)
    assert res['price'] == 82.53


def test_ec2_price_fail(test_client):
    response = test_client.post('/pricing/ec2')

    assert response.status_code == 400


def test_s3_price_success(test_client):
    response = test_client.post('/pricing/s3',
                                data=json.dumps(dict(region='US East (Ohio)',
                                                     storage=1000,
                                                     requests1=1000000,
                                                     requests2=1000000,
                                                     dataReturned=50,
                                                     dataScanned=50,
                                                     dataOutTo='Internet',
                                                     dataOut=2)),
                                content_type='application/json')

    assert response.status_code == 200
    res = json.loads(response.data)
    assert res['price'] == 28.54


def test_ec2_price_fail(test_client):
    response = test_client.post('/pricing/s3')

    assert response.status_code == 500


def test_elb_price_success(test_client):
    response = test_client.post('/pricing/elb',
                                data=json.dumps(dict(region='US East (Ohio)',
                                                     tcpProcessedBytes=1,
                                                     tcpNewConnections=1,
                                                     tcpAvgConnectionDuration=30,
                                                     udpProcessedBytes=2,
                                                     udpNewConnections=1,
                                                     udpAvgConnectionDuration=60,
                                                     tlsProcessedBytes=1,
                                                     tlsNewConnections=2,
                                                     tlsAvgConnectionDuration=60)),
                                content_type='application/json')

    assert response.status_code == 200
    res = json.loads(response.data)
    assert res['price'] == 33.95


def test_elb_price_fail(test_client):
    response = test_client.post('/pricing/elb')

    assert response.status_code == 500


def test_rds_price_success(test_client):
    response = test_client.post('/pricing/rds',
                                data=json.dumps(dict(region='US East (Ohio)',
                                                     instanceType='db.m4.10xlarge',
                                                     deploymentOption='Single-AZ',
                                                     volumeType='General Purpose (SSD)',
                                                     storageAmount=100)),
                                content_type='application/json')

    assert response.status_code == 200
    res = json.loads(response.data)
    assert res['price'] == 2567.96


def test_rds_price_fail(test_client):
    response = test_client.post('/pricing/rds')

    assert response.status_code == 500


def test_cloudwatch_price_success(test_client):
    response = test_client.post('/pricing/cloudwatch',
                                data=json.dumps(dict(region='US East (Ohio)',
                                                     numMetrics=10,
                                                     getMetricData=10,
                                                     getMetricWidgetImage=10,
                                                     otherMetrics=10,
                                                     standardLogs=10,
                                                     logsDeliveredToCloudwatch=0,
                                                     logStorage='Yes',
                                                     logsDeliveredToS3=10,
                                                     parquetConversion='Enabled')),
                                content_type='application/json')

    assert response.status_code == 200
    res = json.loads(response.data)
    assert res['price'] == 10.90


def test_cloudwatch_price_fail(test_client):
    response = test_client.post('/pricing/cloudwatch')

    assert response.status_code == 500
