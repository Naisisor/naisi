from flask.views import MethodView

from app.api.v1 import api_v1
from app.models import URL
from app.response import response


class DocsAPI(MethodView):
    def get(self, url_id):
        """ 获取项目下的项目集 """
        url = URL.query.get_or_404(url_id)
        docs = url.api_docs.all()
        return response(data={'docs': [doc.to_json() for doc in docs]})

    def post(self, url_id):
        """ 新建接口 """
        url = URL.query.get_or_404(url_id)
        return response()


class DocAPI(MethodView):
    def get(self, doc_id):
        return response()

    def delete(self, doc_id):
        return response()

    def put(self, doc_id):
        return response()

    def patch(self, doc_id):
        return response()


api_v1.add_url_rule('/urls/<int:url_id>/docs',
                    view_func=DocsAPI.as_view('docs'),
                    methods=['GET', 'POST'])

api_v1.add_url_rule('/docs/<int:doc_id>',
                    view_func=DocsAPI.as_view('doc'),
                    methods=['GET', 'POST'])
