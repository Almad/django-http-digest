from django.http import HttpResponse
from djangohttpdigest.decorators import protect_digest, protect_digest_model

from testapi.models import ModelWithRealmSet

@protect_digest(realm='simple', username='username', password='password')
def simpleprotected(request):
    """
    This is example of far too simply protected value
    Required credentials are given as argument to decorator,
    view returns 401 on failure or for challenge, 200 with empty body
    on successfull authorization. 
    """
    return HttpResponse('')

@protect_digest_model(realm='simple',
      model=ModelWithRealmSet,
      realm_field='realm',
      username_field='username',
      secret_field='secret'
)
def modelprotected(request):
    """
    Example of model-protected site.
    """
    return HttpResponse('')
