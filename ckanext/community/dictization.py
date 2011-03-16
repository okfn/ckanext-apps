from sqlalchemy import orm
from model import Application
from model import Idea
from model.meta import Session

from schema import ApplicationSchema
from schema import IdeaSchema

def idea_dict_from_form(params):
    return IdeaSchema().deserialize(params)

def idea_to_python(idea):
    return dict(
        id=idea.id,
        title=idea.title,
        name=idea.name,
        description=idea.description,
        submitter=idea.submitter,
        extras=idea.extras,
        tags=[dict(
                id=idea_tag.tag.id,
                name=idea_tag.tag.name
              ) for idea_tag in idea.tags],
        created=idea.created.strftime('%c'),
    )
    
def idea_details(idea_name=None):
    ideas = Session.query(Idea)
    if idea_name:
        try:
            idea = ideas.filter_by(name=idea_name).one()
            return idea_to_python(idea)
        except orm.exc.NoResultFound, e:
            return []
    else:
        return [idea_to_python(idea) for idea in ideas]
            
def application_dict_from_form(params):
    return ApplicationSchema().deserialize(params)
        
def application_to_python(application):
    return dict(
        id=application.id,
        title=application.title,
        name=application.name,
        description=application.description,
        url=application.url,
        developed_by=application.developed_by,
        submitter=application.submitter,
        extras=application.extras,
        tags=[dict(
                id=app_tag.tag.id,
                name=app_tag.tag.name
              ) for app_tag in application.tags],
        created=application.created.strftime('%c'),
    )

def application_details(application_name=None):
    apps = Session.query(Application)
    if application_name:
        try:
            app = apps.filter_by(name=application_name).one()
            return application_to_python(app)
        except orm.exc.NoResultFound, e:
            return []
    else:
        return [application_to_python(app) for app in apps]