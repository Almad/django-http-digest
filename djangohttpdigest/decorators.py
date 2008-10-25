from http import HttpResponseNotAuthorized

from digest import get_digest_challenge

def protect_digest(realm, username, password):
    def _innerDecorator(function):
        def _wrapper(request, *args, **kwargs):
            if request.META.has_key('HTTP_AUTHORIZATION'):
                # successfull auth
                if request.META['AUTH_TYPE'].lower() != 'digest':
                    raise NotImplementedError("Only digest supported")
                #return function(request, *args, **kwargs)
            response = HttpResponseNotAuthorized("Not Authorized")
            response['www-authenticate'] = get_digest_challenge(realm)
            return response
        return _wrapper
    return _innerDecorator

