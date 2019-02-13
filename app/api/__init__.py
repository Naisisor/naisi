from flask import Blueprint

from app.api import auth, users, projects, systems, uri, api_docs, protocols, methods


def create_blueprint():
    bp_api = Blueprint('api', __name__, url_prefix='/api')
    auth.api.register(bp_api)
    users.api.register(bp_api)
    projects.api.register(bp_api)
    systems.api.register(bp_api)
    uri.api.register(bp_api)
    api_docs.api.register(bp_api)
    protocols.api.register(bp_api)
    methods.api.register(bp_api)
    return bp_api
