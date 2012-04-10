from django.conf.urls import patterns, include, url
#from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationFormUniqueEmail 


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    url(r'^$', 'firstsite.views.home', name='home'),
    # url(r'^firstsite/', include('firstsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

#    url(r'^login/$', 'auth.views.login'), #!!!!!!!! research and delete!!!
#, name='registration_register'
    #url('', include('registration.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login_user/login.html', 'redirect_field_name':'login_user/login_sucsess.html'}),
    #(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'registration.views.register', {'backend': 'registration.backends.default.DefaultBackend', 'form_class': RegistrationFormUniqueEmail}),
    #url(r'^accounts/login/$', 'login_user.views.login_user'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login_user/logout.html'}),
    (r'^accounts/', include('registration.backends.default.urls')),

)
