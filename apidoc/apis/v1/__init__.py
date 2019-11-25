from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)

CORS(api_v1)

from apidoc.apis.v1 import projects, systems, urls, docs, protocols, methods, users  # noqa
