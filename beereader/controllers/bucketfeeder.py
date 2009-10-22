import logging

from datetime import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.lib.base import BaseController, render
from beereader.lib.reader import tidy_entry
from beereader.lib.util import atomize_response
from beereader.model import context as ctx
from melkman.db.bucket import NewsBucket, NewsItem, view_entries_by_timestamp
from melk.util.dibject import Dibject

log = logging.getLogger(__name__)

DEFAULT_FEED_SIZE = 25
MAX_FEED_SIZE = 50

__controller__ = 'BucketFeederController'

class BucketFeederController(BaseController):

    def atom(self, id):
        atomize_response()
        return render('/feeder/atom.mako', {'feed': get_feed_info(id)})


def get_feed_info(id):
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

    feed.entries = _bucket_latest_items_batch(bucket, limit=limit)
    return feed


def _bucket_latest_items_batch(bucket, limit=DEFAULT_FEED_SIZE):
    limit = min(limit, MAX_FEED_SIZE)
    query = dict(
        limit=limit,
        startkey=[bucket.id, {}],
        endkey=[bucket.id],
        include_docs=True,
        descending=True,
        )
    entryids = [r.doc['item_id'] for r in view_entries_by_timestamp(ctx.db, **query)]
    return [tidy_entry(i) for i in NewsItem.get_by_ids(entryids, ctx)]


