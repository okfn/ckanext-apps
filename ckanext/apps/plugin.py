import os
from logging import getLogger

from genshi.input import HTML
from genshi.filters import Transformer

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes, IConfigurer, IConfigurable, IGenshiStreamFilter

from ckanext.apps.model import setup
from ckanext.apps.menu import MENU_LINKS

log = getLogger(__name__)

class Apps(SingletonPlugin):

    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)
    implements(IConfigurable, inherit=True)
    implements(IGenshiStreamFilter, inherit=True)

    def before_map(self, map):
        app_controller = 'ckanext.apps.controllers.application:AppController'
        map.redirect("/apps", "/app")
        map.redirect("/apps/{url:.*}", "/app/{url}")
        map.connect('apps', '/app', controller=app_controller, action='index')
        map.connect('/app/new', controller=app_controller, action='new')
        map.connect('/app/tag/:tag', controller=app_controller, action='tag') 
        map.connect('/app/edit/:id', controller=app_controller, action='edit') 
        map.connect('/app/image/{id}@{x}x{y}', controller=app_controller,
                action='read_image') 
        map.connect('/app/image/:id', controller=app_controller,
                action='read_image') 
        map.connect('/app/delete/:id',controller=app_controller, action='delete')
        map.connect('app', '/app/:id', controller=app_controller, action='read')

        idea_controller = 'ckanext.apps.controllers.idea:IdeaController'
        map.redirect("/ideas", "/idea")
        map.redirect("/ideas/{url:.*}", "/idea/{url}")
        map.connect('ideas', '/idea', controller=idea_controller, action='index')
        map.connect('/idea/new', controller=idea_controller, action='new')
        map.connect('/idea/tag/:tag', controller=idea_controller, action='tag') 
        map.connect('/idea/edit/:id', controller=idea_controller, action='edit') 
        map.connect('/idea/delete/:id',controller=idea_controller, action='delete')
        map.connect('/idea/:id', controller=idea_controller, action='read')
        return map

    def configure(self, config):
        setup()

    def update_config(self, config):
        here = os.path.dirname(__file__)
        template_dir = os.path.join(here, 'theme', 'templates')
        public_dir = os.path.join(here, 'theme', 'public')
        if config.get('extra_template_paths'):
            config['extra_template_paths'] += ','+template_dir
        else:
            config['extra_template_paths'] = template_dir
        if config.get('extra_public_paths'):
            config['extra_public_paths'] += ','+public_dir
        else:
            config['extra_public_paths'] = public_dir

    def filter(self, stream):
        stream = stream | Transformer('body//div[@id="mainmenu"]')\
                .append(HTML(MENU_LINKS))
        return stream


