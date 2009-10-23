from paste.deploy.converters import asbool
from pylons import request
from pylons.controllers.util import abort
from routes import url_for

from melk.util.dibject import Dibject, json_sleep, json_wake
from beereader.lib.base import BaseController, render
from beereader.lib.reader import BaseReader, init_reader_from_batch, render_entries_html, tidy_entry
from beereader.lib.util import json_response, is_ajax_request
from beereader.model import context as ctx
from melkman.db.bucket import NewsBucket, NewsItem, NewsItemRef, view_entries_by_timestamp

import logging
log = logging.getLogger(__name__)

DEFAULT_BATCH_SIZE = 25
MAX_BATCH_SIZE = 50

class BucketreaderController(BaseReader):

    def view(self, id):
        initial_batch = get_initial_batch(id)
        return self._show_batch(initial_batch)

    def _show_batch(self, id, batch):
        init_reader_from_batch(id, batch)
        #return render('/reader/standalone.mako')
        return render('/examples/standalone_reader.mako')
        
    def get_batch(self, id):
        bucket = NewsBucket.get(id, ctx)
        if bucket is None:
            abort(404)

        batch_args = _get_batch_args()
        entries, next = _bucket_latest_entries_batch(bucket, **batch_args)
        batch = Dibject(next=next)

        if is_ajax_request():
            # this html section can be optionally omitted by specifying 
            # the query argument no_html=True
            if not asbool(request.params.get('no_html', False)):
                batch.html = render_entries_html(entries)
            batch.entries = [i.item_id for i in entries]
            return json_response(batch)
        else:
            batch.entries = entries
            return self._show_batch(id, batch)


def get_initial_batch(id):
    bucket = NewsBucket.get(id, ctx)
    if bucket is None:
        abort(404)
    batch_args = _get_batch_args()
    entries, next = _bucket_latest_entries_batch(bucket, **batch_args)
    return Dibject(entries=entries, next=next)


def _bucket_latest_entries_batch(bucket, limit=DEFAULT_BATCH_SIZE, startkey=None, startkey_docid=None):
    limit = min(limit, MAX_BATCH_SIZE)
    query = dict(
        limit=limit + 1, # request 1 more than limit to see if there's a next batch
        startkey=[bucket.id, {}], # initial batch; overridden for subsequent batches below
        endkey=[bucket.id],
        include_docs=True,
        descending=True,
        )
    if startkey is not None: # subsequent batches
        assert startkey_docid is not None, 'startkey given with no startkey_docid'
        query.update(startkey=startkey, startkey_docid=startkey_docid)

    rows = list(view_entries_by_timestamp(ctx.db, **query))
    if len(rows) > limit: # there's another batch after this one
        lastrow = rows.pop()
        next = url_for('bucket_latest_entries',
            bucket=bucket,
            startkey=json_sleep(lastrow.key),
            startkey_docid=lastrow.id,
            )
    else:
        next = None

    #entries = [tidy_entry(NewsItemRef.from_doc(r.doc, ctx)) for r in rows]
    entryids = [r.doc['item_id'] for r in rows]
    entries = [tidy_entry(i) for i in NewsItem.get_by_ids(entryids, ctx)]
    return (entries, next)


def _get_batch_args():
    try:
        limit = int(request.params.get('limit', DEFAULT_BATCH_SIZE))
    except:
        limit = DEFAULT_BATCH_SIZE
    try:
        startkey = json_wake(request.params.get('startkey', 'null'))
    except:
        startkey = None
    try:
        startkey_docid = request.params.get('startkey_docid', None)
    except:
        startkey_docid = None
    return dict(limit=limit, startkey=startkey, startkey_docid=startkey_docid)
