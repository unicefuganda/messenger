from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from rapidsms_httprouter.urls import urlpatterns as router_urls
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    # RapidSMS core URLs
    (r'^account/', include('rapidsms.urls.login_logout')),
    url(r'^$', direct_to_template, {'template':'mtrack/dashboard.html'}, name='rapidsms-dashboard'),
    url('^accounts/login', 'rapidsms.views.login'),
    url('^accounts/logout', 'rapidsms.views.logout'),
    (r'^billing/', 'billing.views.summary'),
) + router_urls

if settings.DEBUG:
    urlpatterns += patterns('',
        # helper URLs file that automatically serves the 'static' folder in
        # INSTALLED_APPS via the Django static media server (NOT for use in
        # production)
        (r'^', include('rapidsms.urls.static_media')),
    )


