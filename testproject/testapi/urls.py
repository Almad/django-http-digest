from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('testapi.views',
    url('simpleprotected', 'simpleprotected'),
    url('modelprotected', 'modelprotected'),
    url('modelcleartextprotected', 'modelcleartextprotected'),
)
