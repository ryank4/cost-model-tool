from flask import Flask
from flask_cors import CORS

from routes.ec2_routes import ec2_routes
from routes.price_routes import price_routes
from routes.cost_model_routes import cost_model_routes
from routes.rds_routes import rds_routes

def create_app():
    app = Flask(__name__)

    app.register_blueprint(ec2_routes)
    app.register_blueprint(rds_routes)
    app.register_blueprint(price_routes)
    app.register_blueprint(cost_model_routes)

    cors = CORS(app, resources={r"http://localhost:3000/*": {"origins": "*"}})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
