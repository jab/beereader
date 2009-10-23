from collections import defaultdict
from pylons import response
from pylons.controllers.util import abort
from beereader.lib.base import BaseController, render
from beereader.lib.util import get_posted_data, json_response, opmlize_response
from beereader.model import context as ctx
from melkman.db.composite import Composite
from melkman.db.remotefeed import RemoteFeed, get_or_immediate_create_by_url
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
        
        result = defaultdict(list)
        oldfeeds = set(i.url for i in composite.subscriptions.itervalues())
        remove = oldfeeds - feeds
        for url in remove:
            feed = RemoteFeed.get_by_url(url, ctx)
            if feed is not None:
                composite.unsubscribe(feed)
                result['unsubscribed'].append(url)
                log.debug('Unsubscribed composite "%s" from %s' % (id, url))
            else:
                result['unsubscribe_failed'].append(url)
                log.error('Expected composite "%s" to have RemoteFeed for %s' % (id, url))

        for url in feeds:
            if url not in oldfeeds:
                feed = get_or_immediate_create_by_url(url, ctx)
                if feed is None:
                    result['subscribe_failed'].append(url)
                    log.warn('Could not get or create feed for %s' % url)
                    continue
                composite.subscribe(feed)
                result['subscribed'].append(url)
                log.debug('Subscribed composite "%s" to %s' % (id, url))
            else:
                result['unchanged'].append(url)

        composite.save()
        log.debug('Composite "%s" saved' % id)
        return json_response(result)
