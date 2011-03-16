import colander

from sqlalchemy import orm

from pylons.i18n import _

from ckan.model import System, Action
from ckan.authz import Authorizer
from ckan.lib.base import BaseController, c, g, request, h, \
                          response, session, render, config, abort

from ..model import Application
from ..model.meta import Session

from ..dictization import application_dict_from_form
from ..dictization import application_details

class AppController(BaseController):
    authorizer = Authorizer()
    
    def index(self, format='html'):
        c.apps = application_details()              
        return render('ckanext/community/apps.html')
    
    def create(self):
        try:
            auth_for_create = self.authorizer.am_authorized(c, Action.PACKAGE_CREATE, System())
            if not auth_for_create:
                abort(401, _('Unauthorized to create an application'))
            application_dict = application_dict_from_form(request.params)
        except colander.Invalid, e:
            c.errors = e.asdict()
            c.params = request.params
            return render('ckanext/community/apps_new.html')

        app = Application(**application_dict)
        Session.add(app)
        Session.commit()
        return h.redirect_to(h.url_for('app', id=app.name))
        
    def new(self, format='html'):
        c.auth_for_create = self.authorizer.am_authorized(c, Action.PACKAGE_CREATE, System())
        if not c.auth_for_create:
            abort(401, _('Unauthorized to create an application'))

        c.params = request.params
        return render('ckanext/community/apps_new.html')
        
    def update(self, id):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        if not c.auth_for_update:
            abort(401, _('Unauthorized to edit application'))
        try:
            application_dict = application_dict_from_form(request.params)
            app = Session.query(Application).filter_by(name=id).one()
            app.update(**application_dict)
            Session.commit()
        except colander.Invalid, e:
            c.errors = e.asdict()
            c.params = dict(request.params)
            c.params['name'] = id
            return render('ckanext/community/apps_new.html')
        except orm.exc.NoResultFound, e:
            abort(404)
        return h.redirect_to(h.url_for('app', id=app.name))
        
        
    def delete(self, id):
        c.auth_for_delete = self.authorizer.am_authorized(c, Action.PURGE, System())
        if not c.auth_for_delete:
            abort(401, _('Unauthorized to delete application'))
        try:
            app = Session.query(Application).filter_by(name=id).one()
            Session.delete(app)
            Session.commit()
        except orm.exc.NoResultFound, e:
            abort(404)
        return h.redirect_to(h.url_for('apps'))
 
    def show(self, id, format='html'):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        c.auth_for_delete = self.authorizer.am_authorized(c, Action.PURGE, System())
        application_name = id
        c.app = application_details(application_name)
        if not c.app:
            abort(404)
        return render('ckanext/community/apps_show.html')
            
    def edit(self, id, format='html'):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        if not c.auth_for_update:
            abort(401, _('Unauthorized to edit application'))
            
        application_name = id
        c.params = application_details(application_name)
        if not c.params:
            abort(404)
        return render('ckanext/community/apps_new.html')

