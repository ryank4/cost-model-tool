from pymongo.errors import WriteError

from db.db_config import db

cost_model_col = db.costmodels

def save_cost_model(cost_model):
    try:
        cost_model_col.insert_one(cost_model)
        return True
    except WriteError:
        return False

def load_all_cost_models():
    try:
        return cost_model_col.find({})
    except WriteError:
        return False

def load_cost_model_by_name(cost_model_name):
    try:
        return cost_model_col.find_one({"name": cost_model_name})
    except WriteError:
        return False

def check_document_exists(cost_model_name):
    if cost_model_col.count_documents({'name': cost_model_name}, limit=1):
        return True
    else:
        return False
