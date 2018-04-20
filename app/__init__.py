from flask import Flask
from flask_restful import Api


def create_app(config_name):
    app = Flask(__name__)
    app.config['BUNDLE_ERRORS'] = True
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

    from app.api import api_bp as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app
