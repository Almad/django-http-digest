"""
Helper functions and algorithms for computing HTTP digest thingies.
"""
import time
from md5 import md5
from django.http import HttpResponseBadRequest

def parse_authorization_header(header):
    #auth_scheme, auth_params  = credentials.split(" ", 1)
    pass

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
    
    