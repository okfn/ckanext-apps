import sys, rfc822
import Image, ImageOps
from hashlib import sha1
from StringIO import StringIO
from pylons.controllers.util import etag_cache
from pylons.decorators.cache import beaker_cache
from pylons.i18n import _

from ckan.model import System, Action
from ckan.authz import Authorizer
from ckan.lib.helpers import Page
from ckan.lib.base import BaseController, c, g, request, h, \
                          response, session, render, config, abort
from ckan.lib.navl.dictization_functions import DataError, validate
from ckan.logic import ValidationError

from ckanext.apps.model import Application, ApplicationImage
from ckanext.apps.logic.application import all_applications, \
    applications_by_tag, delete_application, create_application, \
    edit_application

class AppController(BaseController):
    authz = Authorizer()

    def _render_index(self, apps):
        c.auth_for_create = self.authz.am_authorized(c, Action.PACKAGE_CREATE, System())
        c.page = Page(
            collection=apps,
            page=int(request.params.get('page', 1)),
            items_per_page=10)
        return render('app/index.html')

    def index(self):
        return self._render_index(all_applications())

    def tag(self, tag):
        c.tag_name = tag
        return self._render_index(applications_by_tag(tag))

    def new(self, data={}, errors={}, error_summary={}):
        if not self.authz.am_authorized(c, Action.PACKAGE_CREATE, System()):
            abort(401, _('Unauthorized to create an application'))
        if request.method == 'POST' and not errors:
            try:
                image = request.POST.get('image')
                data_dict = dict(request.params)
                app = create_application(data_dict, image)
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

    def read_image(self, id, x=None, y=None):
        etag_cache(sha1(str(id)+str(x)+str(y)).hexdigest())
        image = ApplicationImage.by_id(id)
        handle = Image.open(StringIO(image.data))
        if not image:
            abort(404)
        response.content_type = 'image/png'
        outfh = StringIO()
        try:
            if x is not None and y is not None:
                size = (int(x), int(y))
                handle = ImageOps.fit(handle, size, Image.ANTIALIAS, 0.01, (0.0, 0.0))
        except ValueError, e:
            pass
        handle.save(outfh, 'PNG')
        response.pragma = None 
        response.cache_control = 'public; max-age: 84600'
        response.cache_expires(seconds=84600)
        return outfh.getvalue()

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
        data['images'] = c.app.images
        data['tags'] = [t.tag.name for t in c.app.tags]
        if request.method == 'POST' and not errors:
            try:
                data_dict = dict(request.params)
                app = edit_application(c.app, data_dict,
                        request.POST.get('image'),
                        request.POST.getall('keep_images'))
                h.redirect_to(action='read', id=app.name)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.edit(data_dict, errors, error_summary)
        c.form = render('app/form.html', extra_vars={'data': data,
                                                     'errors': errors,
                                                     'error_summary': error_summary})
        return render('app/edit.html')

