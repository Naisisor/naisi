from app.libs.api_doc_blueprint import APIDocBlueprint
from app.models import Project
from app.response import response

api = APIDocBlueprint('projects')


@api.route('/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get_or_404(id)
    return response(data={'project': project.to_json()})


@api.route('/', methods=['POST'])
def new_project():
    return response()
