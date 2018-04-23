from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['BUNDLE_ERRORS'] = True
    # app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

    from app.api import api_bp as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
