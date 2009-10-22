from pylons import config, request, response
from pylons.controllers.util import abort, redirect_to

try:
    import json
except ImportError:
    import simplejson as json

def is_ajax_request():
    return ('x-requested-with' in request.headers and
            request.headers['x-requested-with'].lower() == 'xmlhttprequest')

def direct_redirect(url):
    stuff_session()
    abort(303, headers=[('Content-Type', 'text/html'), ('Location', url)])

def redirect_to_referer():
    ref = request.headers.get('referer', c.site_url)
    return direct_redirect(ref)


###
# helpers for inspecting / checking the request
###

def method_in(methods):
    methods = [x.upper() for x in methods]
    if request.environ['REQUEST_METHOD'].upper() in methods:
        return True
    return False
        
def assert_method(methods): 
    if not method_in(methods):
        abort(405, headers=[('Allow',', '.join(methods))])

def get_content_type(ct=None):
    if ct is None:
        ct = request.environ.get('CONTENT_TYPE', None).strip()
    if ';' in ct:
        ct = ct[0:ct.find(';')].strip()
    return ct

def assert_content_type(content_types):
    ct = get_content_type()

    if not ct in content_types:
        abort(415)    

POSTY_METHODS = ['POST', 'PUT']

def get_posted_data(content_types=None, methods=None):
    """
    get data that came with the request

    if content_types is specified, assert that the content type specified 
    for the data is one of the types listed.

    if methods is specified, assert that the method is one of the 
    methods given. if not specified, only POST and PUT are permitted.
    """

    if methods is None:
        methods = POSTY_METHODS

    assert_method(methods)

    if not 'CONTENT_LENGTH' in request.environ:
        abort(411)
            
    if content_types is not None:
        assert_content_type(content_types)

    length = int(request.environ['CONTENT_LENGTH'])
    return request.environ['wsgi.input'].read(length)

def has_posted_data(content_types=None, methods=None):
    """
    check if the request posted data. 

    if content_types is specified, only returns True
    when the content type of the request was one of the 
    content types given. 

    if methods specified, only returns true if the method
    of the request was one of the methods given. Otherwise
    only returns true if the method is POST or PUT
    """
    if methods is None:
        methods = POSTY_METHODS

    if not method_in(methods):
        return False

    if content_types is None:
        return True

    ct = get_content_type()
    
    for content_type in content_types:
        if ct.startswith(content_type):
            return True
    
    return False
        

FORM_CONTENT_TYPES = ['application/x-www-form-urlencoded', 'multipart/form-data']
def has_posted_formdata(methods=None):
    return has_posted_data(content_types=FORM_CONTENT_TYPES, methods=methods)

####
# json specific helpers 
####

JSON_CONTENT_TYPES = ['application/json']

def has_posted_json(methods=None):
    return has_posted_data(content_types=JSON_CONTENT_TYPES, methods=methods)

def get_posted_json(methods=None):
    json = get_posted_data(content_types=JSON_CONTENT_TYPES, methods=methods)
        
    try:
        envelope = json_wake(json)
        return envelope["content"]
    except: # ValueError, KeyError
        abort(400)

def json_response(content=None, errors=None):
    # send it back in an object envelope.
    envelope = {}
    envelope['content'] = content
    if errors is not None:
        envelope['errors'] = errors

    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return json.dumps(envelope)

def iframe_json_response(*args, **kwargs):
    value = json_response(*args, **kwargs)
    value = value.replace("&", "&amp;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")

    # send it back in an object envelope... in an html envelope.
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return '<html><body>%s</body></html>' % value

def atomize_response():
    response.headers['Content-Type'] = 'application/atom+xml; charset=utf-8'
