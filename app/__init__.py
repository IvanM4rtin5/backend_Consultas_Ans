from flask import Flask
from flask_cors import CORS
from .routes.health import search_bp
from .routes.expenses import expenses_bp
from .routes.operators import operators_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registrando rotas
    app.register_blueprint(operators_bp, url_prefix='/api')
    app.register_blueprint(expenses_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')

    return app
