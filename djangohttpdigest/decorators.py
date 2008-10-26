from django.http import HttpResponseBadRequest

from http import HttpResponseNotAuthorized
from digest import Digestor, parse_authorization_header
from authentication import SimpleHardcodedAuthenticator, ModelAuthenticator

__all__ = ("protect_digest", "protect_digest_model")

def protect_digest(realm, username, password):
    def _innerDecorator(function):
        def _wrapper(request, *args, **kwargs):
            
            digestor = Digestor(method=request.method, path=request.path, realm=realm)
            
            if request.META.has_key('HTTP_AUTHORIZATION'):
                # successfull auth
                if request.META['AUTH_TYPE'].lower() != 'digest':
                    raise NotImplementedError("Only digest supported")
                
                try:
                    parsed_header = digestor.parse_authorization_header(request.META['HTTP_AUTHORIZATION'])
                except ValueError, err:
                    return HttpResponseBadRequest(err)

                authenticator = SimpleHardcodedAuthenticator(server_realm=realm, server_username=username, server_password=password)
                
                if authenticator.secret_passed(digestor):
                    return function(request, *args, **kwargs)
                
            # nothing received, return challenge
            response = HttpResponseNotAuthorized("Not Authorized")
            response['www-authenticate'] = digestor.get_digest_challenge()
            return response
        return _wrapper
    return _innerDecorator

def protect_digest_model(model, realm, realm_field='realm', username_field='username', secret_field='secret_field'):
    def _innerDecorator(function):
        def _wrapper(request, *args, **kwargs):
            
            digestor = Digestor(method=request.method, path=request.path, realm=realm)
            
            if request.META.has_key('HTTP_AUTHORIZATION'):
                # successfull auth
                if request.META['AUTH_TYPE'].lower() != 'digest':
                    raise NotImplementedError("Only digest supported")
                
                try:
                    parsed_header = digestor.parse_authorization_header(request.META['HTTP_AUTHORIZATION'])
                except ValueError, err:
                    return HttpResponseBadRequest(err)

                authenticator = ModelAuthenticator(model=model, realm=realm, realm_field=realm_field, username_field=username_field, secret_field=secret_field)

                if authenticator.secret_passed(digestor):
                    return function(request, *args, **kwargs)
                
            # nothing received, return challenge
            response = HttpResponseNotAuthorized("Not Authorized")
            response['www-authenticate'] = digestor.get_digest_challenge()
            return response
        return _wrapper
    return _innerDecorator

