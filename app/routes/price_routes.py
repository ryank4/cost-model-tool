from flask import request, Blueprint
from flask_cors import cross_origin

from pricing.compute.ec2.ec2_pricing import EC2
from pricing.storage.s3.s3 import S3

from pricing.utility import mapping
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
        res['price'] = float("{:.2f}".format(price)) + data_transfer_costs

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

    return {"price": price}





