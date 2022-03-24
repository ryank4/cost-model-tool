from flask import request, Blueprint
from flask_cors import cross_origin

from pricing.compute.ec2.ec2_pricing import EC2
from pricing.database.rds_pricing import RDS
from pricing.management.cloudwatch_pricing import CloudWatch
from pricing.network.elb_pricing import ELB
from pricing.storage.s3.s3 import S3

from pricing.utils import mapping
import pricing.compute.ec2.data_transfer_costs as data_cost


price_routes = Blueprint('price_routes', __name__)

@price_routes.route('/pricing/ec2', methods=['POST'])
@cross_origin()
def ec2_price():
    request_data = request.get_json(force=True)

    os = request_data['os']
    instance_type = request_data['instance_type']

    all_regions = mapping.region_mapping_dict
    provided_region = request_data['region']

    for index, value in all_regions.items():
        if value == provided_region:
            region = index

    ec2 = EC2()
    value = ec2.get_instance_price(os, instance_type, region)
    price = float(value) * 730

    data_intra = float(request_data['dataIntra'])
    data_intra_cost = data_cost.calculate_intra_region_data_cost(data_intra)

    to = request_data['dataOutTo']
    data_out = float(request_data['dataOut'])
    data_out_cost = data_cost.calculate_outbound_data_cost(to, data_out)

    data_transfer_costs = data_out_cost + data_intra_cost

    res = {'os': os, 'instance_type': instance_type, 'region': region}

    if price == 0:
        res['price'] = 0
    else:
        res['price'] = round(price + data_transfer_costs, 2)

    return res

@price_routes.route('/pricing/s3', methods=['POST'])
@cross_origin()
def s3_price():
    request_data = request.get_json()

    region = request_data['region']

    storage = request_data['storage']
    requests1 = request_data['requests1']
    requests2 = request_data['requests2']
    data_returned = request_data['dataReturned']
    data_scanned = request_data['dataScanned']

    s3 = S3()

    storage_price = s3.get_storage_prices(region, storage)
    requests1_price = s3.put_copy_post_list_requests_price(region) * int(requests1)
    requests2_price = s3.get_select_requests_price(region) * int(requests2)
    data_returned_price = s3.get_data_returned_price(region) * int(data_returned)
    data_scanned_price = s3.get_data_scanned_price(region) * int(data_scanned)

    to = request_data['dataOutTo']
    data_out = float(request_data['dataOut'])
    data_out_cost = data_cost.calculate_outbound_data_cost(to, data_out)

    price = storage_price + requests1_price + requests2_price + data_returned_price + data_scanned_price + data_out_cost

    return {"price": round(price, 2)}


@price_routes.route('/pricing/elb', methods=['POST'])
@cross_origin()
def elb_price():
    request_data = request.get_json()

    region = request_data['region']

    tcp_processed_bytes = int(request_data['tcpProcessedBytes'])
    tcp_new_connections = int(request_data['tcpNewConnections'])
    tcp_avg_connection_duration = int(request_data['tcpAvgConnectionDuration'])

    udp_processed_bytes = int(request_data['udpProcessedBytes'])
    udp_new_connections = int(request_data['udpNewConnections'])
    udp_avg_connection_duration = int(request_data['udpAvgConnectionDuration'])

    tls_processed_bytes = int(request_data['tlsProcessedBytes'])
    tls_new_connections = int(request_data['tlsNewConnections'])
    tls_avg_connection_duration = int(request_data['tlsAvgConnectionDuration'])

    elb = ELB()

    tcp_price = elb.calc_tcp_traffic(region, tcp_processed_bytes, tcp_new_connections, tcp_avg_connection_duration)
    udp_price = elb.calc_udp_traffic(region, udp_processed_bytes, udp_new_connections, udp_avg_connection_duration)
    tls_price = elb.calc_tls_traffic(region, tls_processed_bytes, tls_new_connections, tls_avg_connection_duration)

    nlb_price = elb.calc_nlb_charge(region)
    nlcu_price = elb.calc_total_nlcu_charge(tcp_price, udp_price, tls_price)

    price = elb.calc_total_monthly_cost(nlb_price, nlcu_price)

    return {"price": price}

@price_routes.route('/pricing/rds', methods=['POST'])
@cross_origin()
def rds_price():
    request_data = request.get_json()

    region = request_data['region']

    instance_type = request_data['instanceType']
    deployment_option = request_data['deploymentOption']
    volume_type = request_data['volumeType']
    storage_amount = float(request_data['storageAmount'])

    rds = RDS()

    instance_cost = rds.get_db_instance_price(region, instance_type, deployment_option)
    storage_cost = rds.get_storage_price(region, volume_type, deployment_option, storage_amount)

    price = rds.calc_total_cost(instance_cost, storage_cost)

    return {"price": price}

@price_routes.route('/pricing/cloudwatch', methods=['POST'])
@cross_origin()
def cloudwatch_price():
    request_data = request.get_json()

    region = request_data['region']

    num_metrics = request_data['numMetrics']
    get_metric_data = request_data['getMetricData']
    get_metric_widget_image = request_data['getMetricWidgetImage']
    other_metric_requests = request_data['otherMetrics']
    standard_logs = request_data['standardLogs']
    logs_delivered_cloudwatch = request_data['logsDeliveredToCloudwatch']
    log_storage = request_data['logStorage']
    logs_delivered_s3 = request_data['logsDeliveredToS3']
    parquet_conversion = request_data['parquetConversion']

    cw = CloudWatch()
    num_metrics_price = cw.get_metric_price(region, num_metrics)
    get_metric_data_price = cw.api_get_metric_data(region, get_metric_data)
    get_metric_widget_image_price = cw.api_get_metric_widget_image(region, get_metric_widget_image)
    other_metric_requests_price = cw.api_get_metric_data(region, other_metric_requests)
    standard_logs_price = cw.standard_log_ingested(region, standard_logs)
    logs_delivered_cloudwatch_price = cw.logs_delivered(region, 'Amazon CloudWatch Logs', logs_delivered_cloudwatch)
    logs_delivered_s3_price = cw.logs_delivered(region, 'Amazon S3', logs_delivered_s3)

    if log_storage == "Yes":
        log_storage_price = cw.log_storage(region, standard_logs, logs_delivered_cloudwatch)
    else:
        log_storage_price = 0

    if parquet_conversion == "Enabled":
        parquet_conversion_price = cw.parquet_conversion(region, logs_delivered_s3)
    else:
        parquet_conversion_price = 0

    price = num_metrics_price + get_metric_data_price + get_metric_widget_image_price + other_metric_requests_price + \
            standard_logs_price + logs_delivered_cloudwatch_price + logs_delivered_s3_price + log_storage_price + \
            parquet_conversion_price

    return {"price": round(price, 2)}
