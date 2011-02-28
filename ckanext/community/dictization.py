from model import Application
from model.meta import Session

from schema import ApplicationSchema

def application_dict_from_form(params):
    return ApplicationSchema().deserialize(params)
    
def application_details(application_name):
    app = Session.query(Application).filter_by(name=application_name).one()
    if app:
        return dict(
            id=app.id,
            name=app.name,
            description=app.description,
            url=app.url,
            developed_by=app.developed_by,
            submitter=app.submitter,
            extras=app.extras,
            tags=[tag.name for tag in app.tags]
        )