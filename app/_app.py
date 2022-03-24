from flask import Flask
from flask_cors import CORS

from app.routes.ec2_routes import ec2_routes
from app.routes.price_routes import price_routes
from app.routes.cost_model_routes import cost_model_routes
from app.routes.rds_routes import rds_routes

app = Flask(__name__)

app.register_blueprint(ec2_routes)
app.register_blueprint(rds_routes)
app.register_blueprint(price_routes)
app.register_blueprint(cost_model_routes)

cors = CORS(app, resources={r"http://localhost:3000/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
