from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

from registration.forms import RegistrationFormUniqueEmail 


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'firstsite.views.home', name='home'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login_user/login.html',}),

    url(r'^accounts/register/$', 'registration.views.register', {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormUniqueEmail}),

    url(r'^view/([a-z]{1,10})/$', 'event.views.viewevents', {'template_name': 'main/events.html',}),

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login_user/logout.html'}),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
