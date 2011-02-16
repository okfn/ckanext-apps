import uuid

from meta import *

__all__ = ['application_table', 'application_tag_table',
           'Application', 'ApplicationTag'
          ]
          
APPLICATION_NAME_MAX_LENGTH = 100

application_table = Table('ckanext_community_application', metadata,
        Column('id', types.UnicodeText, primary_key=True, default=unicode(uuid.uuid4())),
        Column('name', types.Unicode(APPLICATION_NAME_MAX_LENGTH),
               nullable=False, unique=True),
        Column('description', types.UnicodeText),
        Column('url', types.UnicodeText),
        Column('developed_by', types.UnicodeText),
        Column('submitter', types.UnicodeText),
        Column('submitter_email', types.UnicodeText),
        )

application_tag_table = Table('ckanext_community_application_tag', metadata,
        Column('id', types.UnicodeText, primary_key=True),
        Column('application_id', types.UnicodeText, \
                ForeignKey('ckanext_community_application.id')),
        Column('tag_id', types.UnicodeText) # this will use a primaryjoin
        )

class Application(object):
    pass
                    
class ApplicationTag(object):
    def __init__(self, application=None, tag=None, state=None, **kwargs):
        self.application = application
        self.tag = tag
        self.state = state
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<ApplicationTag application=%s tag=%s>' % (self.application.name, self.tag.name)

    @classmethod
    def by_name(self, application_name, tag_name, autoflush=True):
        q = Session.query(self).autoflush(autoflush).\
            join('application').filter(Application.name==application_name).\
            join('tag').filter(Tag.name==tag_name)
        assert q.count() <= 1, q.all()
        return q.first()
            
mapper(Application, application_table, properties={
        'tags':relation(ApplicationTag, secondary=application_tag_table,
            cascade='all, delete, delete-orphan',
            primaryjoin=application_table.c.id==application_tag_table.c.application_id)
        },
    )

mapper(ApplicationTag, application_tag_table, properties={
    },
    order_by=application_tag_table.c.id,
    )