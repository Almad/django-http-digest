from http import HttpResponseNotAuthorized
def protect_digest(realm, username, password):
    def _innerDecorator(f):
        def _wrapper(*args, **kwargs):
            return HttpResponseNotAuthorized("Not Authorized")
        return _wrapper
    return _innerDecorator

