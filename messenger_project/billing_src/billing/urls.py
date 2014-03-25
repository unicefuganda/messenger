from django.conf.urls.defaults import url, patterns
from .views import summary, utl_summary, detail, network_traffic, monitor

urlpatterns = patterns('',
    url(r'^$', summary, name="summary"),
    url(r'^utl/$', utl_summary, name="utl-summary"),
    url(r'^(?P<backend>[a-z0-9]+)/(?P<project>[a-z]+)/', detail, {}, name="billing-detail"),
    url(r'^monitor/', monitor , name="monitor_all"),
    url(r'^(?P<project>[a-z]+)/', network_traffic, {}, name="network-traffic"),
)
