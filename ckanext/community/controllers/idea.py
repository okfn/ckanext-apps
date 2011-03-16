import colander

from sqlalchemy import orm

from pylons.i18n import _

from ckan.model import System, Action
from ckan.authz import Authorizer
from ckan.lib.base import BaseController, c, g, request, h, \
                          response, session, render, config, abort

from ..model import Idea
from ..model.meta import Session

from ..dictization import idea_dict_from_form
from ..dictization import idea_details

class IdeaController(BaseController):
    authorizer = Authorizer()
    
    def index(self, format='html'):
        c.ideas = idea_details()              
        return render('ckanext/community/ideas.html')
    
    def create(self):
        try:
            auth_for_create = self.authorizer.am_authorized(c, Action.PACKAGE_CREATE, System())
            if not auth_for_create:
                abort(401, _('Unauthorized to create an idea'))
            idea_dict = idea_dict_from_form(request.params)
        except colander.Invalid, e:
            c.errors = e.asdict()
            c.params = request.params
            return render('ckanext/community/ideas_new.html')

        idea = Idea(**idea_dict)
        Session.add(idea)
        Session.commit()
        return h.redirect_to(h.url_for('idea', id=idea.name))
        
    def new(self, format='html'):
        c.auth_for_create = self.authorizer.am_authorized(c, Action.PACKAGE_CREATE, System())
        if not c.auth_for_create:
            abort(401, _('Unauthorized to create an idea'))

        c.params = request.params
        return render('ckanext/community/ideas_new.html')
        
    def update(self, id):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        if not c.auth_for_update:
            abort(401, _('Unauthorized to edit idea'))
        try:
            idea_dict = idea_dict_from_form(request.params)
            idea = Session.query(Idea).filter_by(name=id).one()
            idea.update(**idea_dict)
            Session.commit()
        except colander.Invalid, e:
            c.errors = e.asdict()
            c.params = dict(request.params)
            c.params['name'] = id
            return render('ckanext/community/ideas_new.html')
        except orm.exc.NoResultFound, e:
            abort(404)
        return h.redirect_to(h.url_for('idea', id=idea.name))
        
        
    def delete(self, id):
        c.auth_for_delete = self.authorizer.am_authorized(c, Action.PURGE, System())
        if not c.auth_for_delete:
            abort(401, _('Unauthorized to delete idea'))
        try:
            idea = Session.query(Idea).filter_by(name=id).one()
            Session.delete(idea)
            Session.commit()
        except orm.exc.NoResultFound, e:
            abort(404)
        return h.redirect_to(h.url_for('ideas'))
 
    def show(self, id, format='html'):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        c.auth_for_delete = self.authorizer.am_authorized(c, Action.PURGE, System())
        c.auth_for_update = True
        idea_name = id
        c.idea = idea_details(idea_name)
        if not c.idea:
            abort(404)
        return render('ckanext/community/ideas_show.html')
            
    def edit(self, id, format='html'):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        if not c.auth_for_update:
            abort(401, _('Unauthorized to edit idea'))
            
        idea_name = id
        c.params = idea_details(idea_name)
        if not c.params:
            abort(404)
        return render('ckanext/community/ideas_new.html')

