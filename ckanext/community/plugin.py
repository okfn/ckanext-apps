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
        map.resource('app', 'apps', controller='ckanext.community.controllers.application:AppController')
        map.resource('idea', 'ideas', contorller='ckanext.community.controllers.idea:IdeaController')
        
        map.connect('app_api', '/api/2/util/apps/{action}',
            conditions=dict(method=['GET']),
            controller='ckanext.community.controllers.api:ApiController')
                
        map.connect('app_api_resource', '/api/2/util/apps/{action}/:id',
            conditions=dict(method=['GET']),
            controller='ckanext.community.controllers.api:ApiController')
            
        return map

    def update_config(self, config):
        """We use update_config here to get the main config from the
        application and create our extensions engine and metadata as well as
        test our templates and public folders for the extension.
        """
        engine = engine_from_config(config, 'sqlalchemy.', pool_threadlocal=True)
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

