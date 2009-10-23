"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def bucket_expand(kw):
    bucket = kw.get('bucket', None)
    if bucket:
        del kw['bucket']
        kw['id'] = bucket.id
    return kw

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    # map.connect('front_page', '/',
    #             controller='bucketreader', action='view',
    #             id=config.get('beereader.default_bucket_id', 'site_index'))

    map.connect('front_page', '/', controller='templates', action='render', 
        template='index')
    
    map.connect('bucket_latest_entries', '/api/bucket/*(id)/entries/by_date',
        controller='bucketreader', action='get_batch', _filter=bucket_expand)

    map.connect('bucket_latest_entries_atom', '/api/bucket/*(id)/entries/by_date/atom',
        controller='bucketfeeder', action='atom', _filter=bucket_expand)

    map.connect('composite_opml', '/api/composite/*(id)/opml', conditions=dict(
        method=['GET']), controller='composite', action='opml', _filter=bucket_expand)

    map.connect('composite_set_opml', '/api/composite/*(id)/opml', conditions=dict(
        method=['PUT']), controller='composite', action='set_opml', _filter=bucket_expand)

    map.connect('entry_html', '/api/entry/{id}/html', controller='bucketreader', action='entry_html')

    map.connect('template', '*(template)', controller='templates', action='render')

    # map.connect('/{controller}/{action}')
    # map.connect('/{controller}/{action}/{id}')

    return map
