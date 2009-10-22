import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.lib.base import BaseController, render
from beereader.model import context as ctx
from melkman.db.bucket import NewsItem
from melk.util.dibject import Dibject

log = logging.getLogger(__name__)


__all__ = ['BaseReader', 'init_reader_from_batch', 'render_entries_html']

class BaseReader(BaseController):

    def entry_html(self, id):
        """
        Renders a news entry in HTML
        """
        entry = NewsItem.get(id, ctx)
        if item is None:
            abort(404)
        return render('reader/hentry.mako', {'entry': tidy_entry(entry)})

def init_reader_from_batch(bucketid, batch):
    c.bucketid = bucketid
    c.reader_batch = batch
    c.reader_initial_entries = batch.entries

def render_entries_html(entries):
    return [render('reader/hentry.mako', {'entry': tidy_entry(i)}) for i in entries]

def tidy_entry(entry):
    tidied = Dibject()
    for attr in ('item_id', 'title', 'timestamp', 'author', 'link', 'summary', 'content',
            'source_title', 'source_url'):
        tidied[attr] = getattr(entry, attr, '')
    tidied.tags = [tag.get('term') for tag in entry.details.get('tags', ())]
    return tidied
