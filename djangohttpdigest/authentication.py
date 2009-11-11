"""
Various authentication cases, used by decorators.
"""

__all__ = ("SimpleHardcodedAuthenticator", "ModelAuthenticator", "ClearTextModelAuthenticator")

from hashlib import md5

class Authenticator(object):
    """ Authenticator """
    
    def __init__(self):
        object.__init__(self)
        
        self.server_secret = None
        self.a1 = None
        self.a2 = None
    
    def get_a1(self, *args, **kwargs):
        """ Get server's a1 hash for later comparison """
        raise NotImplementedError("This (sub)class does not support this method, see another one.")
    
    def secret_passed(self, digestor):
        """ Compare computed secret to secret from authentication backend.
        If get_a1 was not called before, it's called with digestor as an argument.
        Return bool whether it matches.
        """
        if not self.a1:
            try:
                self.get_a1(digestor=digestor)
            except ValueError:
                return False
        
        assert self.a1 is not None
        
        client_secret = digestor.get_client_secret()
        server_secret = digestor.get_server_secret(a1=self.a1)
        return client_secret == server_secret

def check_hardcoded_authentication(parsed_header, method, path, params, realm, username, password):
    """ Do information sent in header authenticates against given credentials? """
    
    return parsed_header['response'] == result_secret 

class SimpleHardcodedAuthenticator(Authenticator):
    """ Compares secret to explicitly given credentials """
    
    def __init__(self, server_realm, server_username, server_password):
        Authenticator.__init__(self)
        
        self.server_realm = server_realm
        self.server_username = server_username
        self.server_password = server_password

    def get_a1(self, digestor):
        self.a1 = digestor.get_a1(realm=self.server_realm, username=self.server_username, password=self.server_password)
        return self.a1 
    

class ModelAuthenticator(Authenticator):
    def __init__(self, model, realm, realm_field, username_field, secret_field):
        Authenticator.__init__(self)
        
        self.model = model
        self.realm = realm
        self.realm_field = realm_field
        self.username_field = username_field
        self.secret_field = secret_field
    
    
    def get_a1(self, digestor):
        try:
            inst = self.model.objects.get(**{
                self.realm_field : self.realm,
                self.username_field : digestor.get_client_username()
            })
            self.a1 = getattr(inst, self.secret_field)
            return self.a1
        
        except self.model.DoesNotExist:
            raise ValueError()

class ClearTextModelAuthenticator(Authenticator):
    def __init__(self, model, realm, realm_field, username_field, password_field):
        Authenticator.__init__(self)

        self.model = model
        self.realm = realm
        self.realm_field = realm_field
        self.username_field = username_field
        self.password_field = password_field


    def get_a1(self, digestor):
        try:
            username = digestor.get_client_username()
            inst = self.model.objects.get(**{
                self.realm_field : self.realm,
                self.username_field : username
            })
            password = getattr(inst, self.password_field)
            self.a1 = md5("%s:%s:%s" % (username, self.realm, password)).hexdigest()
            return self.a1

        except self.model.DoesNotExist:
            raise ValueError()
