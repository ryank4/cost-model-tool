from datetime import datetime

from flask import request, Blueprint, jsonify
from flask_cors import cross_origin

import db.cost_model_db as db

cost_model_routes = Blueprint('cost_model_routes', __name__)

@cost_model_routes.route('/pricing/save', methods=['POST'])
@cross_origin()
def save():
    request_data = request.get_json()
    cost_model = {}
    total_cost = 0
    service_details = {}

    count = 0

    try:
        for data in request_data:
            if data['index'] == 'name':
                cost_model['name'] = data['value']
            # find the number of services by counting ids
            if data['index'] == '_id':
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

        if db.check_document_exists(cost_model['name']):
            return {"response": "Cost Model Already Exists!"}

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

    except Exception as e:
        return jsonify(message=str(e)), 500

    return res

@cost_model_routes.route('/pricing/load_one', methods=['POST'])
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


@cost_model_routes.route('/pricing/load_all', methods=['GET'])
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
