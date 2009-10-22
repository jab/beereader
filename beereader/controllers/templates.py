import logging

from mako.exceptions import TopLevelLookupException
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.lib.base import BaseController, render
from beereader.lib.util import atomize_response

log = logging.getLogger(__name__)

class TemplatesController(BaseController):
    """
    Requests that come in that don't match specifically mapped routes are
    magically sent to this controller, which tries to render a corresponding
    template in the templates/site directory.

    Templates ending with 'atom' are automatically served as atom.
    """
    def render(self, template):
        template = template.lstrip('/')
        if template.endswith('atom'):
            atomize_response()
        try:
            return render('site/%s.mako' % template).strip()
        except TopLevelLookupException:
            abort(404)
