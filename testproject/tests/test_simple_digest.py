import urllib2
import logging
from md5 import md5
from djangohttpdigest.client import HttpDigestClient

from django.db import transaction

from djangosanetesting import HttpTestCase

from testapi.models import ModelWithRealmSet, ClearTextModel, ClearTextModelWithDefaultRealm

class TestSimpleDigest(HttpTestCase):
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
        
    
    def _check_authentication_compatibility(self, path):
        
        # first handle bad path
        
        auth_handler = urllib2.HTTPDigestAuthHandler()
        auth_handler.add_password('simple', self.url, 'username', 'badpassword')
        opener = urllib2.build_opener(auth_handler)
        
        request = urllib2.Request(self.url+path)
        try:
            response = opener.open(request)
            self.fail("Exception expected to be raised")
        except urllib2.HTTPError, err:
            if err.code != 401 and err.fp:
                logging.error(err.fp.read())
            self.assertEquals(401, err.code)
            if err.fp:
                err.fp.close()

        # then happy path
        
        auth_handler = urllib2.HTTPDigestAuthHandler()
        auth_handler.add_password('simple', self.url, 'username', 'password')
        opener = urllib2.build_opener(auth_handler)
        
        request = urllib2.Request(self.url+path)
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
    
    def test_autentization_compatible_simple(self):
        """ Check our server-side autentizations is compatible with standard (urllib2) one """
        self._check_authentication_compatibility(path='/testapi/simpleprotected/')
        
    def test_autentization_compatible_model(self):
        # add something to test agains
        secret = md5("%s:%s:%s" % ("username", "simple", "password")).hexdigest()
        ModelWithRealmSet.objects.create(realm='simple', username='username', secret=secret)

        transaction.commit()
        
        self._check_authentication_compatibility(path='/testapi/modelprotected/')

    def test_autentization_compatible_model_with_cleartext_field(self):
        # add something to test agains
        secret = md5("%s:%s:%s" % ("username", "simple", "password")).hexdigest()

        ClearTextModel.objects.create(realm='simple', username='username', password='password')
        transaction.commit()

        self._check_authentication_compatibility(path='/testapi/modelcleartextprotected/')

    def test_autentization_compatible_model_with_cleartext_field_without_realm(self):
        # add something to test agains
        ClearTextModelWithDefaultRealm.objects.create(username='username', password='password')

        transaction.commit()

        self._check_authentication_compatibility(path='/testapi/modelcleartextprotectedwithdefaultrealm/')

