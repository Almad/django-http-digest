"""
Helper functions and algorithms for computing HTTP digest thingies.
"""
import time
import urllib2
from md5 import md5

def parse_authorization_header(header):
    """ Parse requests authorization header into list.
    Raise ValueError if some problem occurs. """
    # digest is marked as part of header and causes problem
    # parsing, so remove its
    
    if header.startswith('Digest '):
        header = header[len('Digest '):]
    
    # Convert the auth params to a dict
    items = urllib2.parse_http_list(header)
    params = urllib2.parse_keqv_list(items)
    
    required = ["username", "realm", "nonce", "uri", "response"]

    for field in required:
        if not params.has_key(field):
            raise ValueError("Required field %s not found" % field)

    # check for qop companions
    # (RFC 2617, sect. 3.2.2)
    if params.has_key("qop") and not params.has_key("cnonce") and params.has_key("cn"):
        raise ValueError("qop sent without cnonce and cn")

    return params

def get_digest_challenge(realm):
    """ Return HTTP digest challenge, which has to be placed into www-authenticate header"""
    
    algorithm = 'md5'
    qop = 'auth'
    opaque = 'ToDoMoveThisToSettings'
    
    nonce = md5("%s:%s" % (time.time(), realm)).hexdigest()
    
    return 'Digest realm="%(realm)s", qop="%(qop)s", nonce="%(nonce)s", opaque="%(opaque)s"' % {
        'realm' : realm,
        'qop' : qop,
        'nonce' : nonce,
        'opaque' : opaque
    }

def check_credentials(request):
    """
    Check if request contains credentials.
    Raise HttpResponseBadRequest if malformed header was send.
    """
    if request.META.has_key('AUTHORIZATION'):
        header = parse_authorization_header(request.meta['AUTHORIZATION'])
    else:
        return False
    
def check_hardcoded_authentication(parsed_header, method, path, params, realm, username, password):
    """ Do information sent in header authenticates against given credentials? """
    assert parsed_header['qop'] == 'auth'
    
    # compute A1 according to RFC 2617, section 3.2.2.2
    a1 = md5("%s:%s:%s" % (username, realm, password)).hexdigest()
    # A2, according to section 3.2.2.3
    a2 = md5("%s:%s" % (method,path)).hexdigest()

    request = "%s:%s:%s:%s:%s" % (
            parsed_header["nonce"],
            parsed_header["nc"],
            parsed_header["cnonce"],
            parsed_header["qop"],
            a2
    )
    

    result_secret = md5("%s:%s" % (a1, request)).hexdigest()
    
    return parsed_header['response'] == result_secret 
    