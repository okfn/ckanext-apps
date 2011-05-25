import os
from logging import getLogger

from sqlalchemy import engine_from_config

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes, IConfigurer

from ckanext.community.model import init_model

log = getLogger(__name__)
    
class Community(SingletonPlugin):
    
    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)
        
    def before_map(self, map):
        app_controller = 'ckanext.community.controllers.application:AppController'
        map.redirect("/apps", "/app")
        map.redirect("/apps/{url:.*}", "/app/{url}")
        map.connect('/app/{action}', controller=app_controller,
        requirements=dict(action='|'.join([
                        'create',
                        'new',
                        'update',
                        'edit',
                        'delete',
                        'show',
                        ]))
                    )
        map.connect('/app/{id}', controller=app_controller, action='show')
        map.connect('/app', controller=app_controller, action='index')

        idea_controller = 'ckanext.community.controllers.idea:IdeaController'
        map.redirect("/ideas", "/idea")
        map.redirect("/ideas/{url:.*}", "/idea/{url}")
        map.connect('/idea/{action}', controller=idea_controller,
        requirements=dict(action='|'.join([
                        'create',
                        'new',
                        'update',
                        'edit',
                        'delete',
                        'show',
                        ]))
                    )
        map.connect('/idea/{id}', controller=idea_controller, action='show')
        map.connect('/idea', controller=idea_controller, action='index')
        
        map.connect('app_api', '/api/2/util/apps/{action}',
            conditions=dict(method=['GET']),
            controller='ckanext.community.controllers.api:AppApiController')
                
        map.connect('app_api_resource', '/api/2/util/apps/{action}/:id',
            conditions=dict(method=['GET']),
            controller='ckanext.community.controllers.api:AppApiController')
                
        map.connect('idea_api', '/api/2/util/ideas/{action}',
            conditions=dict(method=['GET']),
            controller='ckanext.community.controllers.api:IdeaApiController')
        
        map.connect('idea_api_resource', '/api/2/util/ideas/{action}/:id',
            conditions=dict(method=['GET']),
            controller='ckanext.community.controllers.api:IdeaApiController')
        return map

    def update_config(self, config):
        """We use update_config here to get the main config from the
        application and create our extensions engine and metadata as well as
        test our templates and public folders for the extension.
        """
        engine = engine_from_config(config, 'sqlalchemy.', strategy="threadlocal", pool_threadlocal=True)
        init_model(engine)
         
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))

        template_dir = os.path.join(rootdir, 'templates')
        public_dir = os.path.join(rootdir, 'public')
        
        if config.get('extra_template_paths'):
            config['extra_template_paths'] += ','+template_dir
        else:
            config['extra_template_paths'] = template_dir
        if config.get('extra_public_paths'):
            config['extra_public_paths'] += ','+public_dir
        else:
            config['extra_public_paths'] = public_dir

