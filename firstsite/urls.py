from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationFormUniqueEmail 


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'firstsite.views.home', name='home'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login_user/login.html', 'redirect_field_name':'login_user/login_sucsess.html'}),

    url(r'^accounts/register/$', 'registration.views.register', {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormUniqueEmail}),

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login_user/logout.html'}),
    (r'^accounts/', include('registration.backends.default.urls')),

)
