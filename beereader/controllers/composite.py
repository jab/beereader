from couchdb import ResourceConflict, ResourceNotFound

from pylons import response
from pylons.controllers.util import abort

from beereader.lib.base import BaseController, render
from beereader.lib.util import get_posted_data, opmlize_response
from beereader.model import context as ctx
from melkman.db.composite import Composite
from melkman.db.remotefeed import RemoteFeed
from melkman.green import sleep
from melk.util.opml import dump_opml, feeds_in_opml

import logging
log = logging.getLogger(__name__)

class CompositeController(BaseController):

    def opml(self, id):
        composite = Composite.get(id, ctx)
        if composite is None:
            abort(404)

        feeds = []
        feed_titles = {}
        for sub_info in composite.subscriptions.itervalues():
            feed_url = sub_info.url
            feeds.append(feed_url)
            title = sub_info.title
            if title:
                feed_titles[feed_url] = title

        opmlize_response()
        return dump_opml(feeds, feed_titles=feed_titles)

    def set_opml(self, id):
        composite = Composite.get(id, ctx)
        if composite is None:
            abort(404)

        opml_data = get_posted_data()
        try:
            feeds = set(feeds_in_opml(opml_data))
        except: 
            import traceback
            log.error(traceback.format_exc())
            abort(400)
        
        oldfeeds = set(i.url for i in composite.subscriptions.itervalues())
        remove = oldfeeds - feeds
        for url in remove:
            try:
                feed = RemoteFeed.get_by_url(url, ctx)
                if feed is not None:
                    composite.unsubscribe(feed)
                    log.debug('Unsubscribed composite "%s" from %s' % (id, url))
                else:
                    raise ResourceNotFound('Could not get RemoteFeed for %s' % url)
            except ResourceNotFound, e:
                log.warn(e)

        for url in feeds:
            feed = RemoteFeed.get_by_url(url, ctx)
            if feed is None:
                # XXX would be nice to have a get_or_create method
                try:
                    feed = RemoteFeed.create_from_url(url, ctx)
                    feed.save()
                    log.debug('Created RemoteFeed for %s' % url)
                except ResourceConflict:
                    feed = RemoteFeed.get_by_url(url, ctx)
                    if feed is None:
                        log.error('Could not get or create feed for %s' % url)
                        raise

            if url not in oldfeeds:
                composite.subscribe(feed)
                log.debug('Subscribed composite "%s" to %s' % (id, url))

        composite.save()
        log.debug('Composite "%s" has been saved' % id)
