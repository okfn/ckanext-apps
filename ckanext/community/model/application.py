from datetime import datetime
from ckan.lib.munge import munge_title_to_name
from ckan.model.tag import Tag, tag_table
from ckan.model.types import JsonDictType, make_uuid
from meta import *

__all__ = ['application_table', 'application_tag_table',
           'Application', 'ApplicationTag'
          ]
          
APPLICATION_NAME_MAX_LENGTH = 100

application_table = Table('ckanext_community_application', metadata,
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('name', types.Unicode(APPLICATION_NAME_MAX_LENGTH),
               nullable=False, unique=True),
        Column('title', types.Unicode(APPLICATION_NAME_MAX_LENGTH),
              nullable=False, unique=False),
        Column('description', types.UnicodeText),
        Column('url', types.UnicodeText),
        Column('developed_by', types.UnicodeText),
        Column('submitter', types.UnicodeText),
        Column('created', DateTime, default=datetime.now),
        Column('extras', JsonDictType)
        )

application_tag_table = Table('ckanext_community_application_tag', metadata,
        Column('id', types.UnicodeText, primary_key=True),
        Column('application_id', types.UnicodeText, \
                ForeignKey('ckanext_community_application.id')),
        Column('tag_id', types.UnicodeText) # this will use a primaryjoin
        )

class Application(object):
    def __init__(self, url=u'', description=u'',
                 developed_by=u'', submitter=u'', title=u'',
                 extras=None,
                 **kwargs):
        self.title = title
        self.name = self.gen_name(self.title)
        self.url = url
        self.description = description
        self.developed_by = developed_by
        self.submitter = submitter
        self.extras = extras or {}
        
        tags = kwargs.get('tags')
        for tag in tags.split(' '):
            pass

    @classmethod          
    def gen_name(cls, title):
        name = munge_title_to_name(title).replace('_', '-')
        while '--' in name:
            name = name.replace('--', '-')
        like_q = u"%s%%" % name
        query = Session.query(cls).filter(cls.name.ilike(like_q)).limit(100)
        taken = [app.name for app in query]
        if name not in taken:
            return name
        else:
            counter = 1
            while counter < 101:
                if name+str(counter) not in taken:
                    return name+str(counter)
                counter+=1 
            return None

    def add_tag_by_name(self, tagname, autoflush=True):
        if not tagname:
            return
        
        tag = Tag.by_name(tagname, autoflush=autoflush)
        if not tag:
            tag = Tag(name=tagname)
            
        app_tag = ApplicationTag.by_tag(self, tag)
        if not app_tag in self.tags:
            self.tags.append(app_tag)

    def update(self, url=u'', description=u'',
               developed_by=u'', submitter=u'', title=u'',
               extras=None, **kwargs):
        if not title == self.title:
            self.title = title
            self.name = self.gen_name(self.title)
        self.url = url
        self.description = description
        self.developed_by = developed_by
        self.submitter = submitter
        self.extras = extras or {}

        tags = kwargs.get('tags')
        for tag in tags.split(' '):
            pass
class ApplicationTag(object):
    def __init__(self, application=None, tag=None, state=None, **kwargs):
        self.application = application
        self.tag = tag
        self.state = state
        for k,v in kwargs.items():
            setattr(self, k, v)
    
    @classmethod
    def by_tag(cls, app, tag):
        match = Session.query(cls).filter(cls.tag_id==tag.id).first()
        if match:
            return match
        else:
            return cls(app, tag)

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
            cascade='all, delete',
            primaryjoin=application_table.c.id==application_tag_table.c.application_id,
            secondaryjoin='tag.id'==application_tag_table.c.tag_id),
        },
    )

mapper(ApplicationTag, application_tag_table, properties={
        'tag':relation(Tag,
            primaryjoin=application_tag_table.c.tag_id==tag_table.c.id,
            foreign_keys=application_tag_table.c.tag_id),
        }
    )