import colander

from ckan.lib.base import BaseController, c, g, request, h, \
                          response, session, render, config, abort

from ..model import Application
from ..model.meta import Session

from ..dictization import application_dict_from_form
from ..dictization import application_details

class AppController(BaseController):
    def index(self, format='html'):
        c.apps = application_details()              
        return render('ckanext/community/apps.html')
    
    def create(self):
        try:
            application_dict = application_dict_from_form(request.params)
        except colander.Invalid, e:
            c.errors = e.asdict()
            return render('ckanext/community/apps_new.html')

        app = Application(**application_dict)
        Session.add(app)
        Session.flush()
        Session.commit()
        return h.redirect_to(h.url_for('app', id=app.name))
        
    def new(self, format='html'):
        return render('ckanext/community/apps_new.html')
        
    def update(self, id):
        pass
        
    def delete(self, id):
        pass

    def show(self, id, format='html'):
        application_name = id
        c.app = application_details(application_name)
        if not c.app:
            abort(404)
        return render('ckanext/community/apps_show.html')
            
    def edit(self, id, format='html'):
        pass

