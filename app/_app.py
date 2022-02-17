import json
from datetime import datetime

from bson import json_util
from flask import Flask, request, jsonify
from pricing.compute.ec2.ec2 import EC2
import pricing.compute.ec2.ec2_attributes as ec2_attributes
from flask_cors import CORS, cross_origin
import db.cost_model_db as db
import pricing.compute.ec2.descibe_ec2_instances as describe_ec2
import pricing.compute.ec2.data_transfer_costs as data_cost
from pricing.utility import mapping

app = Flask(__name__)
cors = CORS(app, resources={r"http://localhost:3000/*": {"origins": "*"}})

@app.route('/pricing/ec2', methods=['POST'])
@cross_origin()
def ec2_price():
    # if key doesn't exist, returns None
   # request.headers.add('Access-Control-Allow-Origin', '*')
    request_data = request.get_json(force=True)
    #request_data = request.get_data()
    #request_data = request.json

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

    res = {}
    res['os'] = os
    res['instance_type'] = instance_type
    res['region'] = region

    if price == 0:
        res['price'] = 0
    else:
        res['price'] = float("{:.2f}".format(price)) + data_transfer_costs

    return res

@app.route('/attributes/ec2/os', methods=['GET'])
@cross_origin()
def ec2_os():
    os_list = ec2_attributes.get_ec2_operating_systems()

    return os_list

@app.route('/attributes/ec2/instancetype', methods=['GET'])
@cross_origin()
def ec2_instance_types():
    instance_types = ec2_attributes.get_ec2_instance_types()

    return instance_types

@app.route('/attributes/ec2/instancetypeinfo', methods=['POST'])
@cross_origin()
def ec2_instance_type_info():
    request_data = request.get_json()
    instance_type = request_data
    instance_type_info = ec2_attributes.describe_instance_types(instance_type)

    return instance_type_info

@app.route('/attributes/ec2/regions', methods=['GET'])
@cross_origin()
def ec2_regions():
    regions = ec2_attributes.get_ec2_regions()

    return regions

@app.route('/pricing/save', methods=['POST'])
@cross_origin()
def save():
    request_data = request.get_json()
    cost_model = {}
    total_cost = 0
    service_details = {}

    count = 0
    for data in request_data:
        if data['index'] == 'name':
            cost_model['name'] = data['value']
        # find the number of services by counting ids
        if data['index'] == 'id':
            # create new dict for each service
            service = service_details[str(count)] = {}
            key = data['index']
            service[key] = data['value']
            count += 1
        else:
            # add values
            key = data['index']
            service[key] = data['value']
            if data['index'] == 'price':
                total_cost += data['value']

    cost_model['serviceDetails'] = service_details
    cost_model['time'] = datetime.now()
    cost_model['total cost'] = total_cost

    save_doc = db.save_cost_model(cost_model)

    if save_doc:
        res = {
            "response": "Cost Model Saved Successfully"
        }
    else:
        res = {
            "response": "Error Saving Cost Model"
        }

    return res

@app.route('/pricing/load_one', methods=['POST'])
@cross_origin()
def load_one():
    cost_model_name = request.get_json()
    load_doc = db.load_cost_model_by_name(cost_model_name)

    if load_doc is not False:
        cost_model_data = {
            "name": load_doc['name'],
            "serviceDetails": load_doc['serviceDetails'],
            "totalCost": load_doc['total cost']
        }
        return cost_model_data
    else:
        return {
            "response": "Error Loading Cost Model"
        }


@app.route('/pricing/load_all', methods=['GET'])
@cross_origin()
def load_all():
    loaded_docs = db.load_all_cost_models()
    cost_models = {}
    index = 0
    for document in loaded_docs:
        cost_models[index] = document['name']
        index += 1
    print(loaded_docs)
    return cost_models

@app.route('/ec2/describe', methods=['GET'])
@cross_origin()
def ec2_describe_instance_type():
    request_data = request.get_json()

    instance_type = request_data['instanceType']

    instance_type_info = describe_ec2.describe_instance_types(instance_type)

    return instance_type_info




@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)



# GET requests will be blocked
@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)



if __name__ == '__main__':
    app.run(debug=True)
