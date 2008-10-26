from django.http import HttpResponseBadRequest

from http import HttpResponseNotAuthorized
from digest import get_digest_challenge, parse_authorization_header, check_hardcoded_authentication

def protect_digest(realm, username, password):
    def _innerDecorator(function):
        def _wrapper(request, *args, **kwargs):
            if request.META.has_key('HTTP_AUTHORIZATION'):
                # successfull auth
                if request.META['AUTH_TYPE'].lower() != 'digest':
                    raise NotImplementedError("Only digest supported")
                try:
                    parsed_header = parse_authorization_header(request.META['HTTP_AUTHORIZATION'])
                except ValueError, err:
                    return HttpResponseBadRequest(err)
                
                if check_hardcoded_authentication(parsed_header, request.method, request.path, request.GET.urlencode(), realm, username, password):
                    return function(request, *args, **kwargs)
            
            # nothing received, return challenge
            response = HttpResponseNotAuthorized("Not Authorized")
            response['www-authenticate'] = get_digest_challenge(realm)
            return response
        return _wrapper
    return _innerDecorator

