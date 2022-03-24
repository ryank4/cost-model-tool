from flask import Blueprint

from flask_cors import cross_origin

from pricing.database.rds_attributes import get_rds_instance_types

rds_routes = Blueprint('rds_routes', __name__)


@rds_routes.route('/rds/attributes/instancetype', methods=['GET'])
@cross_origin()
def rds_instance_types():
    instance_types = get_rds_instance_types()

    return instance_types
