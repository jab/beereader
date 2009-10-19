import logging

from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.controllers.bucketreader import _bucket_latest_items_batch # XXX
from beereader.lib.base import BaseController, render
from beereader.model import context as ctx
from melkman.db.bucket import NewsBucket

from melk.util.dibject import Dibject

log = logging.getLogger(__name__)

DEFAULT_FEED_SIZE = 25
MAX_FEED_SIZE = 50

__controller__ = 'BucketFeederController'

class BucketFeederController(BaseController):

    def atom(self, id):
        return render('/feeder/atom.mako', {'feed': get_feed(id)})


def get_feed(id):
    bucket = NewsBucket.get(id, ctx)
    if bucket is None:
        abort(404)

    feed = Dibject()
    feed.id = id
    feed.title = bucket.title
    feed.timestamp = bucket.last_modification_date or datetime.utcnow()

    try:
        limit = int(request.params.get('limit', DEFAULT_FEED_SIZE))
    except:
        limit = DEFAULT_FEED_SIZE
    limit = min(limit, MAX_FEED_SIZE)

    batch = _bucket_latest_items_batch(bucket, limit=limit)
    feed.entries = batch.entries

    return feed
