import re
import urllib2

from django.test import TestCase
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest

from djangohttpdigest.digest import Digestor, check_credentials, parse_authorization_header

class TestDigestor(TestCase):
    """ Test digestor, our wrapping class for handling digests """
    
    def setUp(self):
        self.digestor = Digestor(realm='testrealm')
    
    def test_get_digest_challenge(self):
        challenge = self.digestor.get_digest_challenge()
        
        # check our challenge is compatible with urllib2's resolving
        if re.compile('(?:.*,)*[ \t]*([^ \t]+)[ \t]+realm="([^"]*)"', re.I).match(challenge):
            pass
        else:
            self.fail("Challenge %s does not match urllib2's regexp" % challenge)
    
class TestSimpleDigest(TestCase):
    
    environment = {
        'HTTP_COOKIE':       '',
        'PATH_INFO':         '/',
        'QUERY_STRING':      '',
        'REQUEST_METHOD':    'GET',
        'SCRIPT_NAME':       '',
        'SERVER_NAME':       'testserver',
        'SERVER_PORT':       '80',
        'SERVER_PROTOCOL':   'HTTP/1.1',
    }
    
    def test_check_credentials(self):
        """ Manually construct requests and check parse function behave correctly """
        request = WSGIRequest(self.__class__.environment)
        self.assertEquals(False, check_credentials(request))
        
        # bad authentication content
        request.META['AUTHENTICATION'] = ''
        
        self.assertEquals(False, check_credentials(request))
    
    def test_parse_authorization_header(self):
        """ Authorization header parsing, for various inputs """
        self.assertRaises(ValueError, lambda:parse_authorization_header(''))