import cgi
from datetime import datetime
from dateutil.tz import tzutc

from melk.feedparser import find_best_permalink
from melk.util.dibject import Dibject

from beereader.model import model, ObjectNotFoundError


__all__ = ['tidy_item']

# 
# helper functions to clean up item 
# details for templates 
#

HTML_TYPES = ['text/html', 'application/xhtml+xml']

def tidy_item(details):

    # prepare data for the template ...
    entry = Dibject()
    entry['id'] = details.melk_id
    entry['timestamp'] = _find_entry_timestamp(details)
    entry['permalink'] = find_best_permalink(details)
    entry['title'] = _find_entry_title(details)
    entry['author_name'] = _find_entry_author(details)
    entry['content'] = _find_entry_content(details)
    entry['tags'] = _find_entry_tags(details)

    source = _find_entry_source(details)
    if source is not None:
        source_details = source.details
        entry['source_name'] = _find_source_name(source_details)
        entry['source_url'] = _find_source_url(source_details)
    else:
        entry['source_name'] = ''
        entry['source_url'] = ''
    
    return entry

def _find_entry_title(entry):
    return _as_html(entry.get('title_detail', None))

def _find_entry_tags(entry):
    """
    find all the tags in an entry
    """
    tags = []
    for t in entry.get('tags', []):
        tag = None
        if 'label' in t and t.label:
            tags.append(t.label)
        elif 'term' in t and t.term:
            tags.append(t.term)

    return [cgi.escape(tag) for tag in tags]

def _find_entry_author(entry):
    if 'author_detail' in entry and 'name' in entry.author_detail and entry.author_detail.name:
        return entry.author_detail.name.title()
    elif 'author' in entry and entry.author:
        return cgi.escape(entry.author.title())
    else:
        return ''

def _find_entry_content(entry):
    content = entry.get('content', [None])[0]
    if content is None:
        content = entry.get('summary_detail', None)
    return _as_html(content)

def _find_entry_source(entry):
    feed_uri = entry.get('feed_uri', None)
    if feed_uri is None:
        return None
    try:
        return model.get_news_source_by_uri(feed_uri)
    except ObjectNotFoundError:
        return None
        
def _find_source_name(news_source):
    return _as_html(news_source.get('title_detail', None))
  
def _find_source_url(news_source):
    for link in news_source.get('links', []):
        if link.rel == 'alternate':
            return link.href
    return ''

def _find_entry_timestamp(entry):
    date_tuple = entry.get('updated_parsed', None)
    if date_tuple is None:
        date_tuple = entry.get('published_parsed', None)
    if date_tuple is None:
        return None
    return datetime(*date_tuple[0:6], **{'tzinfo': tzutc()})

def _as_html(content):
    if content is None:
        return ''

    if content.type in HTML_TYPES:
        return content.value
    else:
        return cgi.escape(content.value)