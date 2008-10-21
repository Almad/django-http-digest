from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^testapi/', include('testapi.urls')),
)
