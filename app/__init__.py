from flask_restplus import Api
from flask import Blueprint
from flask_restplus.apidoc import apidoc
from .main.controller.samba_controller import api as samba_ns

URL_PREFIX = '/api'
apidoc.url_prefix = URL_PREFIX
blueprint = Blueprint('api', __name__, url_prefix=URL_PREFIX)
api = Api(blueprint,
          title='DLDS REST API BOILER-PLATE',
          version='1.0',
          description='a boilerplate for dlds web service',
          doc='/doc/')

api.add_namespace(samba_ns, path='/samba')
