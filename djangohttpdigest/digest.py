"""
Helper functions and algorithms for computing HTTP digest thingies.
"""
from time import time
import urllib2
from md5 import md5
#from sha import sha

class Digestor(object):
    """ Main class for handling digest algorithms as described in RFC 2617 """
    
    # map string representation of algorithm to hash function
    algorithm_implementation_map = {
        'md5' : md5,
#        'sha' : sha,
    }
    
    def __init__(self, realm=None, qop=None, opaque=None, algorithm=None):
        object.__init__(self)
        
        self.algorithm = algorithm or 'md5'
        self.opaque = opaque or 'ToDoMoveThisToSettings'
        self.qop = qop or 'auth'
        self.realm = realm or None
        
        assert self.algorithm in self.algorithm_implementation_map
    
    def get_digest_challenge(self):
        """ Return HTTP digest challenge, which has to be placed into www-authenticate header"""
        
        nonce = self.algorithm_implementation_map[self.algorithm]("%s:%s" % (time(), self.realm)).hexdigest()
        
        return 'Digest realm="%(realm)s", qop="%(qop)s", nonce="%(nonce)s", opaque="%(opaque)s"' % {
            'realm' : self.realm,
            'qop' : self.qop,
            'nonce' : nonce,
            'opaque' : self.opaque
        }

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
    