from ckan.model.types import JsonDictType, make_uuid

from meta import *

__all__ = ['idea_table', 'idea_tag_table',
           'Idea', 'IdeaTag'
          ]

idea_table = Table('ckanext_community_idea', metadata,
      Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
      Column('extras', JsonDictType),
      )
   
idea_tag_table = Table('ckanext_community_idea_tag', metadata,
      Column('id', types.UnicodeText, primary_key=True),
      Column('idea_id', types.UnicodeText, \
              ForeignKey('ckanext_community_idea.id')),
      Column('tag_id', types.UnicodeText) # this will use a primaryjoin
      )
                              
class Idea(object):
    pass
    
class IdeaTag(object):
    pass