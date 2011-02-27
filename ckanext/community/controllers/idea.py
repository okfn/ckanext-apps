from ..model import Idea
from ..model.meta import Session
from ckan.lib.base import BaseController, c, g, request, \
                          response, session, render, config, abort
                          
class IdeaController(BaseController):
    def index(self, format='html'):
        return render('ckanext/community/ideas.html')
    
    def create(self):
        pass
        
    def new(self, format='html'):
        pass
        
    def update(self, id):
        pass
        
    def delete(self, id):
        pass

    def show(self, id, format='html'):
        pass
            
    def edit(self, id, format='html'):
        pass