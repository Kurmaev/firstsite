from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.contrib.auth.views import login
from registration.forms import RegistrationFormUniqueEmail 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('django.contrib.auth.views',

    url(r'^accounts/login/$', login, 
        {'template_name': 'login_user/login.html',}, 
        name="user_login"),

    url(r'^accounts/logout/$', 'logout', 
        {'template_name': 'login_user/logout.html',},  
        name="user_logout"),
)

urlpatterns += patterns('',
    url(r'^profiles/', include('profiles.urls')),
    url(r'^accounts/register/$', 'registration.views.register', 
        {'backend': 'registration.backends.default.DefaultBackend', 
        'form_class': RegistrationFormUniqueEmail},
        name="registration_unique_mail"),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^view-rand/$', 'firstsite.views.randpage', {},'randpage'),

    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_PIC}),

    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^events/', include('event.urls')),
    (r'^', include('event.urls')),
)

urlpatterns += staticfiles_urlpatterns()

