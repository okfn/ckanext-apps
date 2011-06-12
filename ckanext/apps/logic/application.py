
from ckan.logic import ValidationError
from ckan.lib.navl.dictization_functions import DataError, validate
from ckan.lib.base import abort
from ckan.logic.action.update import prettify
from ckan.model import Session, Tag

from ckanext.apps.schema import application_schema
from ckanext.apps.model import Application, ApplicationImage, ApplicationTag

def all_applications():
    return Session.query(Application)

def applications_by_tag(tag_name):
    q = Session.query(Application)
    q = q.join(ApplicationTag)
    q = q.join(Tag)
    q = q.filter(Tag.name==tag_name)
    return q

def featured_applications():
    q = Session.query(Application)
    q = q.filter(Application.featured==True)
    return q

def error_summary(errors):
    error_summary = {}
    for key, error in errors.iteritems():
        error_summary[prettify(key)] = error[0]
    return error_summary

def create_application(data_dict, image):
    if 'image' in data_dict:
        del data_dict['image']
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
            license=data.get('license'),
            code_url=data.get('code_url'),
            api_url=data.get('api_url'),
        )

    for tag in data.get('tags', '').split(' '):
        application.add_tag_by_name(tag)

    if image and image.filename and image.file:
        image = ApplicationImage(name=image.filename, 
            data=image.file.read())
        application.images = [image]
    application.save()
    return application

def edit_application(application, data_dict, image, keep_images):
    if 'image' in data_dict:
        del data_dict['image']
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
    application.license = data.get('license')
    application.code_url = data.get('code_url')
    application.api_url = data.get('api_url')

    for tag in data.get('tags', '').split(' '):
        application.add_tag_by_name(tag)

    for _image in application.images:
        if _image.id not in keep_images:
            _image.delete()

    if image is not None and hasattr(image, 'file'):
        image = ApplicationImage(name=image.filename, 
            data=image.file.read(),
            application=application)
        image.save()

    application.save()
    return application

def delete_application(application_name):
    application = Application.by_name(application_name)
    if not application_name:
        abort(404)
    application.delete()
    Session.commit()

