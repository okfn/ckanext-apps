from pylons.controllers.util import etag_cache
from pylons.i18n import _

from ckan.model import System, Action
from ckan.authz import Authorizer
from ckan.lib.helpers import Page
from ckan.lib.base import BaseController, c, g, request, h, \
                          response, session, render, config, abort
from ckan.lib.navl.dictization_functions import DataError, validate
from ckan.logic import ValidationError

from ckanext.apps.model import Idea
from ckanext.apps.logic.idea import all_ideas, \
    ideas_by_tag, delete_idea, create_idea, \
    edit_idea

class IdeaController(BaseController):
    authz = Authorizer()
    
    def _render_index(self, ideas):
        c.auth_for_create = self.authz.am_authorized(c, Action.PACKAGE_CREATE, System())
        c.page = Page(
            collection=ideas,
            page=int(request.params.get('page', 1)),
            items_per_page=10)
        return render('idea/index.html')

    def index(self):
        return self._render_index(all_ideas())

    def tag(self, tag):
        c.tag_name = tag
        return self._render_index(ideas_by_tag(tag))

    def new(self, data={}, errors={}, error_summary={}):
        if not self.authz.am_authorized(c, Action.PACKAGE_CREATE, System()):
            abort(401, _('Unauthorized to create an application'))
        if request.method == 'POST' and not errors:
            try:
                data_dict = dict(request.params)
                idea = create_idea(data_dict)
                h.redirect_to(action='read', id=idea.name)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.new(data_dict, errors, error_summary)
        c.form = render('idea/form.html', extra_vars={'data': data,
                                                      'errors': errors,
                                                      'error_summary': error_summary})
        return render('idea/new.html')

    def read(self, id):
        c.auth_for_update = self.authz.am_authorized(c, Action.CHANGE_STATE, System())
        c.auth_for_delete = self.authz.am_authorized(c, Action.PURGE, System())
        c.idea = Idea.by_name(id)
        if not c.idea:
            abort(404)
        return render('idea/read.html')

    def delete(self, id):
        if not self.authz.am_authorized(c, Action.PURGE, System()):
            abort(401, _('Unauthorized to delete idea'))
        delete_idea(id)
        return h.redirect_to(h.url_for('ideas'))

    def edit(self, id, data={}, errors={}, error_summary={}):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        if not c.auth_for_update:
            abort(401, _('Unauthorized to edit application'))
        c.idea = Idea.by_name(id)
        if c.idea is None:
            abort(404)
        data = c.idea.as_dict()
        data['tags'] = [t.tag.name for t in c.idea.tags]
        if request.method == 'POST' and not errors:
            try:
                data_dict = dict(request.params)
                idea = edit_idea(c.idea, data_dict)
                h.redirect_to(action='read', id=idea.name)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.edit(data_dict, errors, error_summary)
        c.form = render('idea/form.html', extra_vars={'data': data,
                                                      'errors': errors,
                                                      'error_summary': error_summary})
        return render('idea/edit.html')


