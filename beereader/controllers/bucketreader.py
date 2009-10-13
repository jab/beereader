import logging
import time
from datetime import datetime

from paste.deploy.converters import asbool
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from routes import url_for

from melk.util.dibject import Dibject

from beereader.lib.base import BaseController, render
from beereader.lib.reader import BaseReader, init_reader_from_batch, render_items_html
from beereader.lib.util import json_response, is_ajax_request
from beereader.model import model, ObjectNotFoundError

log = logging.getLogger(__name__)

DEFAULT_BATCH_SIZE = 25
MAX_BATCH_SIZE = 50

class BucketreaderController(BaseReader):

    def view(self, id):
        initial_batch = get_initial_batch(id)
        return self._show_batch(initial_batch)

    def _show_batch(self, batch):
        init_reader_from_batch(batch)
        return render('/reader/standalone.mako')
        
    def get_batch(self, id):

        try:
            bucket = model.get_news_bucket_by_uri(id)
        except ObjectNotFoundError:
            abort(404)

        batch_args = _get_batch_offset()
        batch = _bucket_latest_items_batch(bucket, **batch_args)

        if is_ajax_request():
            # this html section can be optionally ommitted by specifying 
            # the query argument no_html=True
            if not asbool(request.params.get('no_html', False)):
                batch['html'] = render_items_html(batch.entries)

            return json_response(batch)
        else:
            return self._show_batch(batch)


def get_initial_batch(id):
    try:
        bucket = model.get_news_bucket_by_uri(id)
    except ObjectNotFoundError:
        abort(404)

    # grab the initial batch of items...
    batch_args = _get_batch_offset()
    return _bucket_latest_items_batch(bucket, **batch_args)

    
def _bucket_latest_items_batch(bucket, count, date=None, skip=0):
    if count > MAX_BATCH_SIZE:
        count = MAX_BATCH_SIZE

    # grab one extra item to figure out the next batch
    items = bucket.get_latest_news_items(count + 1, start=date, skip=skip, reverse=False)

    batch = Dibject()
    
    # only take the first count items
    batch.entries = [item.uri for item in items[0:count]]

    batch.next = _next_batch(bucket, items, count, date, skip)

    return batch

def _next_batch(bucket, items, count, date, skip):
    """
    generate the batch of items following a certain offset
    """
    
    # if there was no extra item, there is no next batch
    if len(items) != count + 1:
        return None

    # scan the items, use the latest timestamp and minimum skip
    next_start = date
    next_skip = skip
    for item in items:
        if item.timestamp == next_start:
            next_skip += 1
        else:
            next_start = item.timestamp
            next_skip = 0

    bargs = dict(bucket=bucket, count=count)
    if next_skip > 0:
        bargs['skip'] = next_skip
    if next_start:
        bargs['date'] = time.mktime(next_start.timetuple())
    
    return url_for('bucket_latest_items', **bargs)


def _get_batch_offset():
    try:
        count = int(request.params.get('count', DEFAULT_BATCH_SIZE))
    except:
        count = DEFAULT_BATCH_SIZE

    try:
        date = datetime.fromtimestamp(float(request.params.get('date', None)))
    except:
        date = None

    try:
        skip = int(request.params.get('skip', None))
    except:
        skip = 0

    return dict(count=count, date=date, skip=skip)