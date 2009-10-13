import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from beereader.lib.tidyitem import tidy_item

from beereader.lib.base import BaseController, render
from beereader.model import model, ObjectNotFoundError

log = logging.getLogger(__name__)


__all__ = ['BaseReader', 'init_reader_from_batch', 'render_items_html']

class BaseReader(BaseController):

    def item_html(self, id):
        """
        Renders a news item in HTML
        """
        try:
            news_item = model.get_news_item_by_uri(id)
        except ObjectNotFoundError:
            abort(404)

        return render('reader/hentry.mako', {'entry': tidy_item(news_item.details)})

def init_reader_from_batch(batch):
    # prepare the batch to be rendered immediately...
    silo = model.get_silo()
    item_details = silo.item_detail(batch.entries)
    entries = []
    for iid in batch.entries:
        details = item_details.get(iid, None)
        if details:
            entries.append(tidy_item(details))

    c.reader_batch = batch
    c.reader_initial_entries = entries

def render_items_html(ids):
    """
    renders the html for each item specified by id in
    the list 'ids'.
    
    returns a map from item id to rendered html.  
    
    No mapping is produced for items that cannot be found.
    """
    silo = model.get_silo()
    item_details = silo.item_detail(ids)
    html = {}
    for iid in ids:
        details = item_details.get(iid, None)
        if details:
            html[iid] = render('reader/hentry.mako', {'entry': tidy_item(details)})
    return html
