import colander

from sqlalchemy import orm

from pylons.i18n import _

from ckan.model import System, Action
from ckan.authz import Authorizer
from ckan.lib.base import BaseController, c, g, request, h, \
                          response, session, render, config, abort
from ckan.lib.navl.dictization_functions import DataError, validate
from ckan.logic import ValidationError

from ckanext.apps.model import Application
from ckanext.apps.logic import all_applications, applications_by_tag, \
    delete_application, create_application, edit_application

class AppController(BaseController):
    authz = Authorizer()

    def index(self, format='html'):
        c.apps = all_applications()
        return render('app/index.html')

    def tag(self, tag):
        c.tag_name = tag
        c.apps = applications_by_tag(tag)
        return render('app/index.html')

    def new(self, data={}, errors={}, error_summary={}):
        if not self.authz.am_authorized(c, Action.PACKAGE_CREATE, System()):
            abort(401, _('Unauthorized to create an application'))
        if request.method == 'POST' and not errors:
            try:
                data_dict = dict(request.params)
                app = create_application(data_dict)
                h.redirect_to(action='read', id=app.name)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.new(data_dict, errors, error_summary)
        c.form = render('app/form.html', extra_vars={'data': data,
                                                     'errors': errors,
                                                     'error_summary': error_summary})
        return render('app/new.html')

    def read(self, id):
        c.auth_for_update = self.authz.am_authorized(c, Action.CHANGE_STATE, System())
        c.auth_for_delete = self.authz.am_authorized(c, Action.PURGE, System())
        c.app = Application.by_name(id)
        if not c.app:
            abort(404)
        return render('app/read.html')

    def delete(self, id):
        if not self.authz.am_authorized(c, Action.PURGE, System()):
            abort(401, _('Unauthorized to delete application'))
        delete_application(id)
        return h.redirect_to(h.url_for('apps'))

    def edit(self, id, data={}, errors={}, error_summary={}):
        c.auth_for_update = self.authorizer.am_authorized(c, Action.CHANGE_STATE, System())
        if not c.auth_for_update:
            abort(401, _('Unauthorized to edit application'))
        c.app = Application.by_name(id)
        if c.app is None:
            abort(404)
        data = c.app.as_dict()
        data['tags'] = [t.tag.name for t in c.app.tags]
        if request.method == 'POST' and not errors:
            try:
                data_dict = dict(request.params)
                app = edit_application(c.app, data_dict)
                h.redirect_to(action='read', id=app.name)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.edit(data_dict, errors, error_summary)
        c.form = render('app/form.html', extra_vars={'data': data,
                                                     'errors': errors,
                                                     'error_summary': error_summary})
        return render('app/edit.html')

