from datetime import datetime
from ckan.lib.munge import munge_title_to_name
from ckan.model.tag import Tag, tag_table
from ckan.model.types import JsonDictType, make_uuid
from meta import *

__all__ = ['idea_table', 'idea_tag_table',
           'Idea', 'IdeaTag'
          ]
          
IDEA_NAME_MAX_LENGTH = 100

idea_table = Table('ckanext_community_idea', metadata,
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('name', types.Unicode(IDEA_NAME_MAX_LENGTH),
               nullable=False, unique=True),
        Column('title', types.Unicode(IDEA_NAME_MAX_LENGTH),
              nullable=False, unique=False),
        Column('description', types.UnicodeText),
        Column('submitter', types.UnicodeText),
        Column('created', DateTime, default=datetime.now),
        Column('extras', JsonDictType)
        )

idea_tag_table = Table('ckanext_community_idea_tag', metadata,
        Column('id', types.UnicodeText, primary_key=True),
        Column('idea_id', types.UnicodeText, \
                ForeignKey('ckanext_community_idea.id')),
        Column('tag_id', types.UnicodeText) # this will use a primaryjoin
        )

class Idea(object):
    def __init__(self, description=u'', submitter=u'', title=u'',
                 extras=None, **kwargs):
        self.title = title
        self.name = self.gen_name(self.title)
        self.description = description
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
        taken = [idea.name for idea in query]
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
            
        idea_tag = IdeaTag.by_tag(self, tag)
        if not idea_tag in self.tags:
            self.tags.append(idea_tag)

    def update(self, description=u'',
               submitter=u'', title=u'',
               extras=None, **kwargs):
        if not title == self.title:
            self.title = title
            self.name = self.gen_name(self.title)
        self.description = description
        self.submitter = submitter
        self.extras = extras or {}

        tags = kwargs.get('tags')
        for tag in tags.split(' '):
            pass
            
class IdeaTag(object):
    def __init__(self, idea=None, tag=None, state=None, **kwargs):
        self.idea = idea
        self.tag = tag
        self.state = state
        for k,v in kwargs.items():
            setattr(self, k, v)
    
    @classmethod
    def by_tag(cls, idea, tag):
        match = Session.query(cls).filter(cls.tag_id==tag.id).first()
        if match:
            return match
        else:
            return cls(idea, tag)

    def __repr__(self):
        return '<IdeaTag idea=%s tag=%s>' % (self.idea.name, self.tag.name)

    @classmethod
    def by_name(self, idea_name, tag_name, autoflush=True):
        q = Session.query(self).autoflush(autoflush).\
            join('idea').filter(Idea.name==idea_name).\
            join('tag').filter(Tag.name==tag_name)
        assert q.count() <= 1, q.all()
        return q.first()
            
mapper(Idea, idea_table, properties={
        'tags':relation(IdeaTag, secondary=idea_tag_table,
            cascade='all, delete',
            primaryjoin=idea_table.c.id==idea_tag_table.c.idea_id,
            secondaryjoin='tag.id'==idea_tag_table.c.tag_id),
        },
    )

mapper(IdeaTag, idea_tag_table, properties={
        'tag':relation(Tag,
            primaryjoin=idea_tag_table.c.tag_id==tag_table.c.id,
            foreign_keys=idea_tag_table.c.tag_id),
        }
    )