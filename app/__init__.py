from flask import Flask
import logging
from config import config
from common import defaults as df


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['BUNDLE_ERRORS'] = True
    # app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

    handler = logging.FileHandler(df.LOG_PATH, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter(df.LOG_FORMAT)
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    from app.api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
