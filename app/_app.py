from flask import Flask, request, jsonify
from pricing.compute.ec2.ec2 import EC2
import pricing.compute.ec2.ec2_attributes as ec2_attributes
from flask_cors import CORS, cross_origin

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
    region = request_data['region']

    ec2 = EC2()
    value = ec2.get_instance_price(os, instance_type, region)
    price = float(value) * 730
    res = {}
    res['os'] = os
    res['instance_type'] = instance_type
    res['region'] = region
    res['price'] = price

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

@app.route('/attributes/ec2/regions', methods=['GET'])
@cross_origin()
def ec2_regions():
    regions = ec2_attributes.get_ec2_regions()

    return regions
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
