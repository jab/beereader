"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import config, tmpl_context as c
from paste.request import construct_url
from paste.deploy.converters import asbool

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""

        # figure out where this application is mounted
        base_url = construct_url(environ, with_query_string=False, with_path_info=False)
        if base_url.endswith('/'):
            base_url = base_url[0:-1]
        # figure out where we are now...
        this_url = construct_url(environ, with_query_string=True, with_path_info=True)

        # transfer some info from configuration into the template context
        # and set up some additional template 'globals'
        c.site_url = base_url
        c.this_url = this_url
        c.site_title = config.get('beereader.site_title', 'Beereader')
        c.default_bucket_id = config.get('beereader.default_bucket_id', 'site_index')
        c.google_ajax_api_key = config.get('beereader.google_ajax_api_key', '')
        c.local_resources_only = asbool(config.get('beereader.local_resources_only', True))

        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)
