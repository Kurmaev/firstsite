from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.contrib.auth.views import login
from registration.forms import RegistrationFormUniqueEmail 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from event.models import Event
from django.shortcuts import get_object_or_404

urlpatterns = patterns('django.contrib.auth.views',

    url(r'^accounts/login/$', login, 
        {'template_name': 'login_user/login.html',}, 
        name="user_login"),

    url(r'^accounts/logout/$', 'logout', 
        {'template_name': 'login_user/logout.html',},  
        name="user_logout"),
)

urlpatterns += patterns('',

    url(r'^accounts/register/$', 'registration.views.register', 
    {'backend': 'registration.backends.default.DefaultBackend', 
    'form_class': RegistrationFormUniqueEmail},
    name="registration_unique_mail"),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'firstsite.views.home', name='home'),

    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', 
	{'document_root': settings.MEDIA_ROOT}),

    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', 
	{'document_root': settings.MEDIA_PIC}),

    (r'^accounts/', include('registration.backends.default.urls')),
)

urlpatterns += patterns('event.views',

    url(r'^view/([a-z]{1,10})/$', 'viewevents', 
        {'template_name': 'main/events.html',}),

    url(r'^viewall/$', 'viewall', {'template_name': 'main/events.html',},
    name="view_all_cat"),
	url(r'^events/(?P<event_slug>[-_\w]+)/$', 'view_more_about_event',
	{'template_name': 'main/view_events.html',},
	name="view_more"),
)

urlpatterns += staticfiles_urlpatterns()

