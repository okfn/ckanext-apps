import colander

class ExtraSchema(colander.MappingSchema):
    key = colander.SchemaNode(colander.String())
    value = colander.SchemaNode(colander.String())
    
class ExtrasSchema(colander.MappingSchema):
    extra = ExtraSchema()

class ApplicationSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), validator=colander.Length(min=1))
    description = colander.SchemaNode(colander.String(), missing=u'')
    url = colander.SchemaNode(colander.String(), validator=colander.Length(min=1))
    developed_by = colander.SchemaNode(colander.String(), missing=u'')
    submitter = colander.SchemaNode(colander.String(), validator=colander.Length(min=1))
    tags = colander.SchemaNode(colander.String(), missing=u'')
    extras = ExtrasSchema(missing={})
    
class IdeaSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String(), validator=colander.Length(min=1))
    description = colander.SchemaNode(colander.String())
    submitter = colander.SchemaNode(colander.String())
    tags = colander.SchemaNode(colander.String(), missing=u'')
    extras = ExtrasSchema(missing={})