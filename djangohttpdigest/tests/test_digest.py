import urllib2

from django.test import TestCase
from django.http import HttpRequest, HttpResponseBadRequest
from django.core.handlers.wsgi import WSGIRequest

from djangohttpdigest.digest import check_credentials, parse_authorization_header

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
        
        self.assertRaises(HttpResponseBadRequest, lambda:parse_authorization_header(''))