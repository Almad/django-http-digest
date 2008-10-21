from django.conf.urls.defaults import *

urlpatterns = patterns('testapi.views',
    url('simpleprotected', 'simpleprotected'),
)
