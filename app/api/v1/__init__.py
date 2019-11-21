from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)

CORS(api_v1)

from app.api.v1 import projects, systems, urls, docs
