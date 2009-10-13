"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from datetime import datetime, timedelta
from dateutil.tz import tzlocal, tzutc
import re

from routes import url_for

def iso8601_date(timestamp):
    """
    return the date specified in the format:
    """
    # YYYY-MM-DDTHH:MM:SS+ZZ:ZZ
    fmt = r"%Y-%m-%dT%H:%M:%S+%Z"
    lt = timestamp.astimezone(tzlocal())
    datestr = lt.strftime(fmt)
    pat = re.compile(r"\+(\d\d)(\d\d)$")
    return pat.sub(r'+\1:\2', datestr)

def pretty_date(timestamp):
    """
    return a human readable date for the UTC time 
    tuple specified
    """
    lt = timestamp.astimezone(tzlocal())
    tdiff = datetime.now(tzlocal()) - lt

    if tdiff < timedelta(days=1):
        fmt = "Today at %I%M%p %Z"
    elif tdiff < timedelta(days=2):
        fmt = "Yesterday at %I%M%p %Z"
    else:
        fmt = "%a, %b %d %Y at %I:%M%p %Z"
    
    return lt.strftime(fmt)