from django.http import HttpResponse
from djangohttpdigest import protect_digest

@protect_digest(realm='simple', username='username', password='password')
def simpleprotected(request):
    """
    This is example of far too simply protected value
    Required credentials are given as argument to decorator,
    view returns 401 on failure or for challenge, 200 with empty body
    on successfull authorization. 
    """
    raise ValueError()
    return HttpResponse('')