from pylons import response
from pylons.controllers.util import abort

from beereader.lib.base import BaseController, render
from beereader.lib.util import get_posted_data
from beereader.model import context as ctx
from melkman.db.composite import Composite
from melkman.db.remotefeed import RemoteFeed
from melkman.fetch import request_feed_index
from melkman.green import sleep
from melk.util.opml import dump_opml, feeds_in_opml

import logging
log = logging.getLogger(__name__)

class CompositeController(BaseController):

    def opml(self, id):
        composite = Composite.get(id, ctx)
        if composite is None:
            abort(404)
        response.headers['Content-Type'] = 'application/xml;charset=utf-8'
        feeds = []
        feed_titles = {}
        for sub_info in composite.subscriptions.itervalues():
            feed_url = sub_info.url
            feeds.append(feed_url)
            title = sub_info.title
            if title:
                feed_titles[feed_url] = title
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
            feed = RemoteFeed.get_by_url(url, ctx)
            if feed is not None:
                log.debug('Unsubscribing %s from %s' % (id, url))
                composite.unsubscribe(feed)
            else:
                log.warn('Could not get RemoteFeed for %s' % url)

        for url in feeds:
            request_feed_index(url, ctx)
            sleep(.1)
            feed = RemoteFeed.get_by_url(url, ctx)
            if feed is None:
                log.warn('Could not get RemoteFeed for %s' % url)
                continue
            if url not in oldfeeds:
                log.debug('Subscribing %s to %s' % (id, url))
                composite.subscribe(feed)
        composite.save()
