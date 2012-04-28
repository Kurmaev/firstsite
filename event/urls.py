from django.conf.urls import patterns, include, url

urlpatterns = patterns('event.views',

    url(r'^view/([a-z]{1,10})/$', 'view_events_from_cat', name='view_cat'),

    url(r'^view-next-day/$', 'view_next_day', name="view_next_day"),

    url(r'^view-next-week/$', 'view_next_week', name="view_next_week"),

    url(r'^view-all/$', 'viewall', name="view_all_cat"),

    url(r'^more/(?P<event_slug>[-_\w]+)/$', 'view_more_about_event',
	    name="view_more"),

    url(r'^add_event/$', 'add_event', name="add_event"),
    url(r'^search/$', 'search', name="search_event"),
)

