from django.conf.urls.defaults import *
from .views import summary, utl_summary, detail

urlpatterns = patterns('',
    url(r'^$', summary, name="summary"),
    url(r'^utl/$', utl_summary, name="utl-summary"),
    url(r'^(?P<backend>[a-z0-9]+)/(?P<project>[a-z]+)/', detail, {}, name="billing-detail"),
)
