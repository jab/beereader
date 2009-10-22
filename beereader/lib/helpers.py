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
    lt = timestamp.replace(tzinfo=tzutc()).astimezone(tzlocal())
    datestr = lt.strftime(fmt)
    pat = re.compile(r"\+(\d\d)(\d\d)$")
    return pat.sub(r'+\1:\2', datestr)

def pretty_date(timestamp):
    """
    return a human readable date for the UTC time 
    tuple specified
    """
    lt = timestamp.replace(tzinfo=tzutc()).astimezone(tzlocal())
    lnow = datetime.now(tzlocal())
    tdiff = lnow - lt

    time = lt.strftime("%I:%M%p")
    time = time.lstrip('0').replace(':00', '')

    if tdiff < timedelta(days=1) and lt.day == lnow.day:
        return time

    yesterday = lnow - timedelta(days=1)
    if tdiff < timedelta(days=2) and lt.day == yesterday.day:
        return 'yesterday at ' + time

    if tdiff < timedelta(days=7):
        return lt.strftime('%A at ') + time

    if lt.year == lnow.year:
        return lt.strftime('%a, %b %d at ') + time

    return lt.strftime('%a, %b %d %Y at ') + time
