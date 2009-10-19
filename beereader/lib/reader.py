import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.lib.base import BaseController, render
from beereader.model import context as ctx
from melkman.db.bucket import NewsItem

log = logging.getLogger(__name__)


__all__ = ['BaseReader', 'init_reader_from_batch', 'render_items_html']

class BaseReader(BaseController):

    def item_html(self, id):
        """
        Renders a news item in HTML
        """
        item = NewsItemRef.get(id, ctx)
        if item is None:
            abort(404)
        return render('reader/hentry.mako', {'entry': item})

def init_reader_from_batch(bucketid, batch):
    c.bucketid = bucketid
    c.reader_batch = batch
    c.reader_initial_entries = batch.entries

def render_items_html(items):
    return [render('reader/hentry.mako', {'entry': i}) for i in items]
