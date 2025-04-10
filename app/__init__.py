from flask import Flask
from flask_cors import CORS
from .routes.health import search_bp
from .routes.despesas import despesas_bp
from .routes.operators import operators_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registrando rotas
    app.register_blueprint(operators_bp, url_prefix='/api')
    app.register_blueprint(despesas_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')

    return app
