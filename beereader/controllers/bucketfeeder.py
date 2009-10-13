import logging

from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.lib.base import BaseController, render
from beereader.lib.tidyitem import tidy_item
from beereader.model import model, ObjectNotFoundError

from melk.util.dibject import Dibject

log = logging.getLogger(__name__)

DEFAULT_FEED_SIZE = 25
MAX_FEED_SIZE = 50

__controller__ = 'BucketFeederController'

class BucketFeederController(BaseController):

    def atom(self, id):
        return render('/feeder/atom.mako', feed=get_feed_info(id))


def get_feed_info(id):
    try:
        bucket = model.get_news_bucket_by_uri(id)
    except ObjectNotFoundError:
        abort(404)

    feed = Dibject()

    feed.id = id
    feed.title = bucket.title
    feed.timestamp = bucket.last_modification or datetime.utcnow()

    count = int(request.params.get('count', DEFAULT_FEED_SIZE))
    if count > MAX_FEED_SIZE:
        count = MAX_FEED_SIZE

    feed.entries = []
    for item in bucket.get_latest_news_items(count):
        feed.entries.append(tidy_item(item.details))
        
    return feed