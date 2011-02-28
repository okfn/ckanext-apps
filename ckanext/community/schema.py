import colander

class ExtraSchema(colander.MappingSchema):
    key = colander.SchemaNode(colander.String())
    value = colander.SchemaNode(colander.String())
    
class ExtrasSchema(colander.MappingSchema):
    extra = ExtraSchema()

class ApplicationSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String(), validator=colander.Length(min=1))
    description = colander.SchemaNode(colander.String(), missing=u'')
    url = colander.SchemaNode(colander.String(), validator=colander.Length(min=1))
    developed_by = colander.SchemaNode(colander.String(), missing=u'')
    submitter = colander.SchemaNode(colander.String(), validator=colander.Length(min=1))
    extras = ExtrasSchema(missing={})
    
class IdeaSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String())
    url = colander.SchemaNode(colander.String())
    developer_by = colander.SchemaNode(colander.String())
    submitter = colander.SchemaNode(colander.String())
    extras = ExtrasSchema()