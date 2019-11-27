from apidoc.settings import Config
from marshmallow import Schema, fields


class PaginateSchema(Schema):
    page = fields.Int(missing=1, location='query')
    per_page = fields.Int(missing=Config.API_DOC_PER_PAGE, location='query')
