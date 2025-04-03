from flask import Flask
from flask_cors import CORS
from .routes.despesas import despesas_bp
from .routes.health import health_bp
from .routes.xmls import xmls_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registrando rotas
    app.register_blueprint(despesas_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(xmls_bp, url_prefix='/api')

    return app
