import urllib2
import logging
from django.test import TestCase

from djangohttpdigest.client import HttpDigestClient

from module_test import LiveServerTestCase

class TestSimpleDigest(LiveServerTestCase):
    path = '/testapi/simpleprotected/'
    url = 'http://localhost:8000'
    
    def test_simple_autentization(self):
        """ Test view protected by simple realm-username-password decorator """
        
        
        # first test that using normal client, path is protected and returns 401
        response = self.client.get(self.path)
        self.assertEquals(401, response.status_code)
        
        # and that challenge is returned
        assert len(response['www-authenticate']) > 0
        assert 'nonce' in response['www-authenticate']
        
        #Now use our client ant autentize
#        client = HttpDigestClient()
#        client.set_http_authentication(username='username', password='password', path=self.path)
#        response = client.get(self.path)
#        self.assertEquals(200, response.status_code)
        

    def test_autentization_compatible(self):
        """ Check our server-side autentization is compatible with standard (urllib2) one """
        
        auth_handler = urllib2.HTTPDigestAuthHandler()
        auth_handler.add_password('simple', self.url, 'username', 'password')
        opener = urllib2.build_opener(auth_handler)
        
        request = urllib2.Request(self.url+self.path)
        try:
            response = opener.open(request)
        except urllib2.HTTPError, err:
            if err.fp:
                error = ": %s" % err.fp.read()
            else:
                error = ''
            logging.error("Error occured while opening HTTP %s" % error)
            raise
        self.assertEquals(200, response.code)
        response.close()

