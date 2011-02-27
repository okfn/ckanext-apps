from ..model import Application
from ..model.meta import Session
from ckan.lib.base import BaseController, c, g, request, \
                          response, session, render, config, abort
                          
class AppController(BaseController):
    def index(self, format='html'):
        return render('ckanext/community/apps.html')
    
    def create(self):
        return None
        
    def new(self, format='html'):
        return render('ckanext/community/apps_new.html')
        
    def update(self, id):
        pass
        
    def delete(self, id):
        pass

    def show(self, id, format='html'):
        pass
            
    def edit(self, id, format='html'):
        pass