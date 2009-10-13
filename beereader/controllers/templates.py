import logging

from mako.exceptions import TopLevelLookupException
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.lib.base import BaseController, render

log = logging.getLogger(__name__)

class TemplatesController(BaseController):

    def render(self, template):
        try:
            return render('site/%s.mako' % template)
        except TopLevelLookupException:
            abort(404)
