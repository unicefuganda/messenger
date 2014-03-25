from django.conf.urls.defaults import url, patterns
from .views import summary, utl_summary, detail, network_traffic, monitor, new_data

urlpatterns = patterns('',
    url(r'^$', summary, name="summary"),
    url(r'^utl/$', utl_summary, name="utl-summary"),
    url(r'^(?P<backend>[a-z0-9]+)/(?P<project>[a-z]+)/', detail, {}, name="billing-detail"),
    url(r'^monitor/', monitor, name="monitor_all"),
    url(r'^new_data/', new_data, name="new_data"),
    url(r'^(?P<project>[a-z]+)/', network_traffic, {}, name="network-traffic"),
)
