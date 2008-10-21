from django.test import TestCase
from djangohttpdigest.client import HttpDigestClient

class TestSimpleDigest(TestCase):
    
    def test_simple_authorization(self):
        """ Test view protected by simple realm-username-password decorator """
        path = '/testapi/simpleprotected/'
        
        # first test that using normal client, path is protected and returns 401
        response = self.client.get(path)
        self.assertEquals(401, response.status_code)