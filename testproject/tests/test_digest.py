import re

from djangohttpdigest.digest import Digestor, parse_authorization_header

from djangosanetesting import UnitTestCase

class TestDigestor(UnitTestCase):
    """ Test digestor, our wrapping class for handling digests """
    
    def setUp(self):
        self.digestor = Digestor(realm='testrealm', method='GET', path='/testapi/simpleprotected/')
        self.auth_string = 'Digest username="rpgpedia", realm="extproject", nonce="1cc6ab869fca869c2c085d78a3729a66", uri="/extproject/project/fc8afe5e-da35-4fe2-a991-7b26c829cde5/user/rpgpedia/salt/", response="69ead146a246cd51bbd076244d2e455b", opaque="ToDoMoveThisToSettings", algorithm="MD5", qop=auth, nc=00000001, cnonce="a84f8e6cfcd50a75"'
    
    def _assertKeyEquals(self, key, value):
        parsed_header = self.digestor.parse_authorization_header(self.auth_string)
        self.assertTrue(parsed_header.has_key(key))
        self.assertEquals(value, parsed_header[key])
    
    def test_get_digest_challenge(self):
        challenge = self.digestor.get_digest_challenge()
        
        # check our challenge is compatible with urllib2's resolving
        if re.compile('(?:.*,)*[ \t]*([^ \t]+)[ \t]+realm="([^"]*)"', re.I).match(challenge):
            pass
        else:
            self.fail("Challenge %s does not match urllib2's regexp" % challenge)
    
    def test_proper_parsing_username(self):
        self._assertKeyEquals('username', 'rpgpedia')

    def test_proper_parsing_realm(self):
        self._assertKeyEquals('realm', 'extproject')

    def test_proper_parsing_nonce(self):
        self._assertKeyEquals('nonce', '1cc6ab869fca869c2c085d78a3729a66')

    def test_proper_parsing_uri(self):
        self._assertKeyEquals('uri', '/extproject/project/fc8afe5e-da35-4fe2-a991-7b26c829cde5/user/rpgpedia/salt/')

    def test_proper_parsing_response(self):
        self._assertKeyEquals('response', '69ead146a246cd51bbd076244d2e455b')

    def test_proper_parsing_opaque(self):
        self._assertKeyEquals('opaque', 'ToDoMoveThisToSettings')

    def test_proper_parsing_algorithm(self):
        self._assertKeyEquals('algorithm', 'MD5')

    def test_proper_parsing_qop(self):
        self._assertKeyEquals('qop', 'auth')

    def test_proper_parsing_nc(self):
        self._assertKeyEquals('nc', '00000001')

    def test_proper_parsing_cnonce(self):
        self._assertKeyEquals('cnonce', 'a84f8e6cfcd50a75')

    def test_bad_parsing_missing_digest(self):
        auth_string = 'username="rpgpedia", realm="extproject", nonce="1cc6ab869fca869c2c085d78a3729a66", uri="/extproject/project/fc8afe5e-da35-4fe2-a991-7b26c829cde5/user/rpgpedia/salt/", response="69ead146a246cd51bbd076244d2e455b", opaque="ToDoMoveThisToSettings", algorithm="MD5", qop=auth, nc=00000001, cnonce="a84f8e6cfcd50a75"'
        self.assertRaises(ValueError, lambda:self.digestor.parse_authorization_header(auth_string))
    
class TestSimpleDigest(UnitTestCase):
    
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
    
    def test_parse_authorization_header(self):
        """ Authorization header parsing, for various inputs """
        self.assertRaises(ValueError, lambda:parse_authorization_header(''))