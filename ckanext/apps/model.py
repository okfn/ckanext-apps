import logging
from datetime import datetime

from ckan.lib.munge import munge_title_to_name
from ckan.model.meta import *
from ckan.model.types import make_uuid
from ckan.model.core import *
from ckan.model.domain_object import DomainObject
from ckan.model.tag import Tag, tag_table

from sqlalchemy.orm import backref, relation
log = logging.getLogger(__name__)

__all__ = [
    'Application', 'application_table',
    'ApplicationTag', 'application_tag_table',
    'ApplicationImage', 'application_image_table',
    'Idea', 'idea_table',
    'IdeaTag', 'idea_tag_table',
]


application_table = None
application_tag_table = None
application_image_table = None
idea_table = None
idea_tag_table = None

def setup():
    if application_table is None:
        create_apps_tables()
    metadata.create_all()

def _generate_name(cls, title):
    name = munge_title_to_name(title).replace('_', '-')
    while '--' in name:
        name = name.replace('--', '-')
    like_q = u"%s%%" % name
    query = Session.query(cls).filter(cls.name.ilike(like_q)).limit(100)
    taken = [do.name for do in query]
    if name not in taken:
        return name
    else:
        counter = 1
        while counter < 101:
            if name+str(counter) not in taken:
                return name+str(counter)
            counter+=1 

class AppsDomainObject(DomainObject):

    @classmethod
    def by_id(cls, id, autoflush=True):
        obj = Session.query(cls).autoflush(autoflush)\
              .filter_by(id=id).first()
        return obj


class Application(AppsDomainObject):

    @classmethod
    def generate_name(cls, title):
        return _generate_name(cls, title)

    def add_tag_by_name(self, tagname, autoflush=True):
        tag = Tag.by_name(tagname, autoflush=autoflush)
        if not tag:
            tag = Tag(name=tagname)
        app_tag = ApplicationTag.by_tag(self, tag)
        if not app_tag in self.tags:
            self.tags.append(app_tag)

class ApplicationTag(AppsDomainObject):

    @classmethod
    def by_tag(cls, app, tag):
        match = Session.query(cls).\
            filter(and_(cls.tag_id==tag.id,
                        cls.application_id==app.id)).first()
        return match or cls(application=app, tag=tag)

class ApplicationImage(AppsDomainObject):
    pass

class Idea(AppsDomainObject):

    @classmethod
    def generate_name(cls, title):
        return _generate_name(cls, title)

    def add_tag_by_name(self, tagname, autoflush=True):
        tag = Tag.by_name(tagname, autoflush=autoflush)
        if not tag:
            tag = Tag(name=tagname)
        idea_tag = IdeaTag.by_tag(self, tag)
        if not idea_tag in self.tags:
            self.tags.append(idea_tag)

class IdeaTag(AppsDomainObject):

    @classmethod
    def by_tag(cls, idea, tag):
        match = Session.query(cls).\
            filter(and_(cls.tag_id==tag.id,
                        cls.idea_id==idea.id)).first()
        return match or cls(idea=idea, tag=tag)


def create_apps_tables():
    global application_table
    global application_tag_table
    global application_image_table
    global idea_table
    global idea_tag_table

    application_table = Table('application', metadata,
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('name', types.Unicode(), nullable=False, unique=True),
        Column('title', types.Unicode(), nullable=False),
        Column('featured', types.Boolean(), default=False),
        Column('description', types.UnicodeText),
        Column('url', types.UnicodeText),
        Column('developer', types.UnicodeText),
        Column('developer_url', types.UnicodeText),
        Column('submitter', types.UnicodeText),
        Column('license', types.UnicodeText),
        Column('code_url', types.UnicodeText),
        Column('api_url', types.UnicodeText),
        Column('created', DateTime, default=datetime.now),
        Column('updated', DateTime, default=datetime.now, onupdate=datetime.now),
        )
    
    application_image_table = Table('application_image', metadata,
        Column('application_id', types.UnicodeText,
            ForeignKey('application.id')),
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('name', types.Unicode(), nullable=False),
        Column('data', types.LargeBinary(), nullable=False),
        Column('created', DateTime, default=datetime.now),
        )

    application_tag_table = Table('application_tag', metadata,
        Column('application_id', types.UnicodeText,
            ForeignKey('application.id')),
        Column('tag_id', types.UnicodeText,
            ForeignKey(tag_table.c.id))
        )

    idea_table = Table('idea', metadata,
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('name', types.Unicode(), nullable=False, unique=True),
        Column('title', types.Unicode(), nullable=False),
        Column('featured', types.Boolean(), default=False),
        Column('description', types.UnicodeText),
        Column('submitter', types.UnicodeText),
        Column('submitter_url', types.UnicodeText),
        Column('created', DateTime, default=datetime.now),
        Column('updated', DateTime, default=datetime.now, onupdate=datetime.now),
        )

    idea_tag_table = Table('idea_tag', metadata,
        Column('idea_id', types.UnicodeText, ForeignKey('idea.id')),
        Column('tag_id', types.UnicodeText, ForeignKey(tag_table.c.id))
        )

    mapper(Application, application_table, properties={
            'tags':relation(ApplicationTag, secondary=application_tag_table, viewonly=True,
                cascade='all, delete',
                primaryjoin=application_table.c.id==application_tag_table.c.application_id,
                secondaryjoin=tag_table.c.id==application_tag_table.c.tag_id,
            )
            }
        )

    mapper(ApplicationTag, application_tag_table, properties={
            'tag':relation(Tag),
            'application':relation(Application),
            },
            primary_key=[
                application_tag_table.c.tag_id,
                application_tag_table.c.application_id
            ]
        )

    mapper(ApplicationImage, application_image_table, properties={
            'application': relation(Application,
                primaryjoin=application_table.c.id==application_image_table.c.application_id,
                backref=backref("images", lazy=True)),
            },
        )

    mapper(Idea, idea_table, properties={
            'tags':relation(IdeaTag, secondary=idea_tag_table, viewonly=True,
                cascade='all, delete',
                primaryjoin=idea_table.c.id==idea_tag_table.c.idea_id,
                secondaryjoin=tag_table.c.id==idea_tag_table.c.tag_id),
            },
        )
        
    mapper(IdeaTag, idea_tag_table, properties={
            'tag':relation(Tag),
            'idea':relation(Idea),
            },
            primary_key=[
                idea_tag_table.c.tag_id,
                idea_tag_table.c.idea_id
            ]
        )


