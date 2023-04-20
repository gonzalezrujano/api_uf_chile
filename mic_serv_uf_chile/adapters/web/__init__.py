import logging
from flask import Flask
from mic_serv_uf_chile.core.exceptions import NoConfigFile


def create_app(config=None, actions=None):
    if config is None:
        logging.critical('config not defined')
        raise NoConfigFile
    logging.info('creating web app')
    app = Flask(__name__, instance_relative_config=True)
    for k, v in config.items():
        app.config[k] = v
    app.ms_actions = actions

    with app.app_context():
        from mic_serv_uf_chile.adapters.web.controllers import blueprint
        app.register_blueprint(blueprint)

    return app
