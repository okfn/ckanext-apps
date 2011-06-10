from ckan.lib.navl.validators import ignore_missing, not_empty
from ckan.lib.navl.validators import empty, ignore, not_missing
from ckan.logic.schema import tag_string_convert

from ckanext.apps.model import Application

def application_id_exists(id):
    return Application.by_id(id) is not None

def application_schema():
    return {
        'id': [ignore_missing, unicode, application_id_exists],
        'name': [ignore_missing, unicode],
        'title': [not_empty, unicode],
        'url': [not_empty, unicode],
        'featured': [ignore_missing, bool],
        'submitter': [ignore_missing, unicode],
        'developer': [unicode],
        'developer_url': [ignore_missing, unicode],
        'license': [ignore_missing, unicode],
        'code_url': [ignore_missing, unicode],
        'api_url': [ignore_missing, unicode],
        'description': [not_empty, unicode],
        'tags': [ignore_missing, unicode],
        '__extras': [ignore],
        '__junk': [empty]
        }

def idea_id_exists(id):
    return Idea.by_id(id) is not None

def idea_schema():
    return {
        'id': [ignore_missing, unicode, idea_id_exists],
        'name': [ignore_missing, unicode],
        'title': [not_empty, unicode],
        'featured': [ignore_missing, bool],
        'submitter': [ignore_missing, unicode],
        'submitter_url': [ignore_missing, unicode],
        'description': [not_empty, unicode],
        'tags': [ignore_missing, unicode],
        '__extras': [ignore],
        '__junk': [empty]
        }

