from flask import request, Blueprint
from flask_cors import cross_origin

from pricing.compute.ec2.ec2_pricing import EC2
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


