from marshmallow import Schema, fields, validate

from apidoc.libs.common import contain_zh
from apidoc.settings import Config


class PaginateSchema(Schema):
    page = fields.Int(missing=1, location='query')
    per_page = fields.Int(missing=Config.API_DOC_PER_PAGE, location='query')


class NameSchema(Schema):
    name = fields.Str(required=True, validate=[validate.Length(min=1, error='名称不能为空'), contain_zh], location='json')


class PASysSchema(Schema):
    """ Project & System 参数校验 """
    name = fields.Str(required=True, validate=validate.Length(min=1, error='名称不能为空'), location='json')
    desc = fields.Str(missing='', validate=validate.Length(max=255, error='名称不能为空'), location='json')
    domains = fields.Str(missing='[]', location='json')
    # TODO 以下参数后续逐步删除
    supporter_id = fields.Int(missing=0)  # 维护者 id 创建项目或者系统时，用 g.current_user.id 支持 method patch 修改用户及项目 id
    project_id = fields.Int(missing=0)
