from django.http import HttpResponse

def simpleprotected(request):
    """
    This is example of far too simply protected value
    Required credentials are given as argument to decorator,
    view returns 401 on failure or for challenge, 200 with empty body
    on successfull authorization. 
    """
    
    return HttpResponse('')