from flask import request, Blueprint

import pricing.compute.ec2.ec2_attributes as ec2_attributes
from flask_cors import cross_origin

ec2_routes = Blueprint('ec2_routes', __name__)

@ec2_routes.route('/ec2/attributes/os', methods=['GET'])
@cross_origin()
def ec2_os():
    os_list = ec2_attributes.get_ec2_operating_systems()

    return os_list

@ec2_routes.route('/ec2/attributes/instancetype', methods=['GET'])
@cross_origin()
def ec2_instance_types():
    instance_types = ec2_attributes.get_ec2_instance_types()

    return instance_types

@ec2_routes.route('/ec2/attributes/instancetypeinfo', methods=['POST'])
@cross_origin()
def ec2_instance_type_info():
    request_data = request.get_json()
    instance_type = request_data
    instance_type_info = ec2_attributes.describe_instance_types(instance_type)

    return instance_type_info

@ec2_routes.route('/ec2/attributes/regions', methods=['GET'])
@cross_origin()
def ec2_regions():
    regions = ec2_attributes.get_ec2_regions()

    return regions

