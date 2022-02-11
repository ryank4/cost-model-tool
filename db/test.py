from pymongo.errors import WriteError

from db.db_config import db

test = db.costmodels

def save_cost_model(cost_model):
    try:
        test.insert_one(cost_model)
        return True
    except WriteError:
        return False

def load_cost_model(cost_model):
    try:
        return test.find_one({"name": cost_model})
    except WriteError:
        return False

# test_doc = {
#       "name": "Test Cost Model 3",
#       "service details": [
#         {
#             "service": "EC2",
#             "instance_type": "a1.2xlarge",
#             "os": "Linux",
#             "region": "us-east-2",
#             "price": 148.92
#         },
#           {
#             "service": "EC2",
#             "instance_type": "a1.medium",
#             "os": "Linux",
#             "region": "us-east-2",
#             "price": 18.615,
#           }
#     ],
#         "total cost": 167.535
# }
#
# test.insert_one(test_doc)