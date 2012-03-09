
from ckan.logic import ValidationError
from ckan.lib.navl.dictization_functions import DataError, validate
from ckan.lib.base import abort
from ckan.logic.action.update import prettify
from ckan.model import Session, Tag

from ckanext.apps.schema import idea_schema
from ckanext.apps.model import Idea, IdeaTag

def all_ideas():
    return Session.query(Idea)

def ideas_by_tag(tag_name):
    q = Session.query(Idea)
    q = q.join(IdeaTag)
    q = q.join(Tag)
    q = q.filter(Tag.name==tag_name)
    return q

def featured_ideas():
    q = Session.query(Idea)
    q = q.filter(Idea.featured==True)
    return q

def error_summary(errors):
    error_summary = {}
    for key, error in errors.iteritems():
        error_summary[prettify(key)] = error[0]
    return error_summary

def create_idea(data_dict):
    data, errors = validate(data_dict, idea_schema())
    if errors:
        raise ValidationError(errors, error_summary(errors))

    idea = Idea(
            name=Idea.generate_name(data.get('title')),
            title=data.get('title'),
            description=data.get('description'),
            featured=data.get('featured'),
            submitter=data.get('submitter'),
            submitter_url=data.get('submitter_url'),
        )

    tags = data.get('tags', '').split(' ')
    idea.update_tags(tags)

    idea.save()
    return idea

def edit_idea(idea, data_dict):
    data, errors = validate(data_dict, idea_schema())
    if errors:
        raise ValidationError(errors, error_summary(errors))

    idea.title = data.get('title')
    idea.description = data.get('description')
    idea.featured = data.get('featured')
    idea.submitter = data.get('submitter')
    idea.submitter_url = data.get('submitter_url')

    tags = data.get('tags', '').split(' ')
    idea.update_tags(tags)
    idea.save()
    return idea

def delete_idea(idea_name):
    idea = Idea.by_name(idea_name)
    if not idea_name:
        abort(404)
    idea_tags = Session.query(IdeaTag) \
        .filter(IdeaTag.idea_id==idea.id) \
        .all()
    for idea_tag in idea_tags:
        idea_tag.delete()

    idea.delete()
    Session.commit()


