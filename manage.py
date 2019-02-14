import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User, Project, System, URL, APIDoc, Protocol, \
    Method, SystemCollect, URLCollect, ProjectCollect

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Role=Role,
        User=User,
        Project=Project,
        System=System,
        URL=URL,
        APIDoc=APIDoc,
        Protocol=Protocol,
        Method=Method,
        ProjectCollect=ProjectCollect,
        SystemCollect=SystemCollect,
        URLCollect=URLCollect
    )
