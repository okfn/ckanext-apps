
from ckan.logic import ValidationError
from ckan.lib.navl.dictization_functions import DataError, validate
from ckan.lib.base import abort
from ckan.logic.action.update import prettify
from ckan.model import Session, Tag

from ckanext.apps.schema import application_schema
from ckanext.apps.model import Application, ApplicationImage, ApplicationTag
from ckanext.apps.model import Idea, IdeaTag

def all_applications():
    return Session.query(Application)

def applications_by_tag(tag_name):
    q = Session.query(Application)
    q = q.join(ApplicationTag)
    q = q.join(Tag)
    q = q.filter(Tag.name==tag_name)
    return q

def error_summary(errors):
    error_summary = {}
    for key, error in errors.iteritems():
        error_summary[prettify(key)] = error[0]
    return error_summary

def create_application(data_dict):
    data, errors = validate(data_dict, application_schema())
    if errors:
        raise ValidationError(errors, error_summary(errors))

    application = Application(
            name=Application.generate_name(data.get('title')),
            title=data.get('title'),
            url=data.get('url'),
            description=data.get('description'),
            featured=data.get('featured'),
            submitter=data.get('submitter'),
            developer=data.get('developer'),
            developer_url=data.get('developer_url'),
        )
    for tag in data.get('tags', '').split(' '):
        application.add_tag_by_name(tag)
    application.save()
    return application

def edit_application(application, data_dict):
    data, errors = validate(data_dict, application_schema())
    if errors:
        raise ValidationError(errors, error_summary(errors))

    application.title = data.get('title')
    application.url = data.get('url')
    application.description = data.get('description')
    application.featured = data.get('featured')
    application.submitter = data.get('submitter')
    application.developer = data.get('developer')
    application.developer_url = data.get('developer_url')
    for tag in data.get('tags', '').split(' '):
        application.add_tag_by_name(tag)
    application.save()
    return application

def delete_application(application_name):
    application = Application.by_name(application_name)
    if not application_name:
        abort(404)
    application.delete()
    Session.commit()

