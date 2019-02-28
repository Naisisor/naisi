from app.api import errors, auth, users, projects, systems, urls, api_docs, protocols, methods


def register_blueprint(app):
    app.register_blueprint(errors.api)
    app.register_blueprint(auth.api, url_prefix='/api/auth')
    app.register_blueprint(users.api, url_prefix='/api/users')
    app.register_blueprint(projects.api, url_prefix='/api/projects')
    app.register_blueprint(systems.api, url_prefix='/api/systems')
    app.register_blueprint(urls.api, url_prefix='/api/uri')
    app.register_blueprint(api_docs.api, url_prefix='/api/docs')
    app.register_blueprint(protocols.api, url_prefix='/api/protocols')
    app.register_blueprint(methods.api, url_prefix='/api/methods')
