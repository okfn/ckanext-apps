import logging
from datetime import datetime

from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import backref, relation


from ckan.lib.munge import munge_title_to_name
from ckan import model
from ckan.model import Session
from ckan.model.meta import Table, Column,types,ForeignKey,DateTime
from ckan.model.types import make_uuid
from ckan.model.core import metadata, mapper
from ckan.model.domain_object import DomainObject
from ckan.model.tag import Tag, tag_table

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
        define_apps_tables()
        log.debug('Apps tables defined in memory')

    if model.repo.are_tables_created():
        if not application_table.exists():

            # Create each table individually rather than
            # using metadata.create_all()
            application_table.create()
            application_tag_table.create()
            application_image_table.create()
            idea_table.create()
            idea_tag_table.create()

            log.debug('Apps tables created')
        else:
            log.debug('Apps tables already exist')
            from ckan.model.meta import engine
            # Check if existing tables need to be updated
            inspector = Inspector.from_engine(engine)
            columns = inspector.get_columns('application_tag')
            if not 'id' in [column['name'] for column in columns]:
                log.debug('Apps tables need to be updated')
                migrate_v2()


    else:
        log.debug('Apps table creation deferred')

    #import pdb; pdb.set_trace()
    #if application_table is None:
        #create_apps_tables()
    #metadata.create_all()

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

    def update_tags(self, tags):
        tags = [t.strip(',').strip() for t in tags]
        for app_tag in self.tags:
            if app_tag.tag.name in tags:
                tags.remove(app_tag.tag.name)
            else:
                app_tag.delete()
        for tag_name in tags:
            tag = Tag.by_name(tag_name)
            if not tag:
                tag = Tag(name=tag_name)
            app_tag = ApplicationTag(application=self, tag=tag)
            app_tag.add()
            self.tags.append(app_tag)

    @property
    def tags(self):
        app_tags = Session.query(ApplicationTag) \
               .join(Application) \
               .filter(Application.id==self.id) \
               .all()

        return app_tags



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

    def update_tags(self, tags):
        tags = [t.strip(',').strip() for t in tags]
        for idea_tag in self.tags:
            if idea_tag.tag.name in tags:
                tags.remove(idea_tag.tag.name)
            else:
                idea_tag.delete()
        for tag_name in tags:
            tag = Tag.by_name(tag_name)
            if not tag:
                tag = Tag(name=tag_name)
            idea_tag = IdeaTag(idea=self, tag=tag)
            idea_tag.add()
            self.tags.append(idea_tag)

    @property
    def tags(self):
        idea_tags = Session.query(IdeaTag) \
               .join(Idea) \
               .filter(Idea.id==self.id) \
               .all()

        return idea_tags

class IdeaTag(AppsDomainObject):

    @classmethod
    def by_tag(cls, idea, tag):
        match = Session.query(cls).\
            filter(and_(cls.tag_id==tag.id,
                        cls.idea_id==idea.id)).first()
        return match or cls(idea=idea, tag=tag)


def define_apps_tables():
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
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('application_id', types.UnicodeText,
            ForeignKey('application.id')),
        Column('tag_id', types.UnicodeText,
            ForeignKey('tag.id'))
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
        Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
        Column('idea_id', types.UnicodeText, ForeignKey('idea.id')),
        Column('tag_id', types.UnicodeText, ForeignKey('tag.id'))
        )

    mapper(Application, application_table)

    mapper(ApplicationTag, application_tag_table, properties={
            'tag':relation(Tag),
            'application':relation(Application),
            }
        )

    mapper(ApplicationImage, application_image_table, properties={
            'application': relation(Application,
                primaryjoin=(application_table.c.id==application_image_table.c.application_id),
                backref=backref("images", lazy=True)),
            },
        )

    mapper(Idea, idea_table)

    mapper(IdeaTag, idea_tag_table, properties={
            'tag':relation(Tag),
            'idea':relation(Idea),
            }
        )

def migrate_v2():

    log.debug('Migrating apps tables to v2. This may take a while...')

    statements='''
        CREATE TABLE application_tag_temp AS SELECT * FROM application_tag;
        CREATE TABLE idea_tag_temp AS SELECT * FROM idea_tag;
        '''
    Session.execute(statements)
    Session.commit()

    application_tag_table.drop()
    idea_tag_table.drop()

    application_tag_table.create()
    idea_tag_table.create()
    Session.commit()
    apps_tags = Session.execute('SELECT application_id,tag_id from application_tag_temp')
    ideas_tags = Session.execute('SELECT idea_id,tag_id from idea_tag_temp')

    for app_tag in apps_tags:
        Session.execute('''INSERT INTO application_tag (id,application_id,tag_id) VALUES ('%s','%s','%s')''' %
                        (make_uuid(), app_tag[0],app_tag[1]))

    for idea_tag in ideas_tags:
        Session.execute('''INSERT INTO idea_tag (id,idea_id,tag_id) VALUES ('%s','%s','%s')''' %
                        (make_uuid(), idea_tag[0],idea_tag[1]))

    statements='''
        DROP TABLE application_tag_temp;
        DROP TABLE idea_tag_temp;
        '''
    Session.execute(statements)
    Session.commit()

    log.info('Apps tables migrated to v2')
