from flask_restx import Api
from flask import Blueprint, current_app
from mic_serv_uf_chile.adapters.web.controllers.uf import api as uf_ns


blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title=current_app.ms_actions.config['info']['name'],
          version=current_app.ms_actions.config['info']['version'],
          description=current_app.ms_actions.config['info']['description'],
          prefix='/'
          )

api.add_namespace(uf_ns, path='/uf')
