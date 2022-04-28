from marshmallow import Schema
from webargs import fields

# Disclaimer: note I am actually not using Schemas properly... that requires a bit more effort...

class SSchema(Schema):
  string = fields.Str()
class JSON(Schema):
  json = fields.List(fields.Dict())
class HTML(Schema):
    html = fields.Str()