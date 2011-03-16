import json
from ckan.lib.base import BaseController, c, g, request, \
                          response, session, render, config, abort
from ..dictization import *

class AppApiController(BaseController):
                
    def application_details(self, id=None):
        return json.dumps(application_information(application_name=id))


class IdeaApiController(BaseController):

    def idea_details(self, id=None):
        return json.dumps(idea_information(idea_name=id))
