from marshmallow import Schema, fields, validate

from apidoc.libs.common import contain_zh
from apidoc.settings import Config


class PaginateSchema(Schema):
    page = fields.Int(missing=1, location='query')
    per_page = fields.Int(missing=Config.API_DOC_PER_PAGE, location='query')


class NameSchema(Schema):
    name = fields.Str(required=True, validate=[validate.Length(min=1, error='名称不能为空'), contain_zh], location='json')
