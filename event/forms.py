# -*- coding: utf-8 -*-
from firstsite.settings import STATIC_URL
from django.forms import ModelForm, Textarea, DateInput, DateField, TextInput
from event.models import Event
from django.contrib.admin.widgets import AdminDateWidget


#class CalendarWidget(TextInput):
#    class Media:
#        js = ('/admin/jsi18n/',
#              STATIC_URL + 'admin/js/core.js',
#              STATIC_URL + "admin/js/calendar.js",
#              STATIC_URL + "admin/js/admin/DateTimeShortcuts.js")
#        css = {
#            'all': (
#                STATIC_URL + 'admin/css/forms.css',
#                STATIC_URL + 'admin/css/base.css',
#                STATIC_URL + 'admin/css/widgets.css',)
#        }
#
#    def __init__(self, attrs={}):
#        super(CalendarWidget, self).__init__(attrs={'class': 'vDateField', 'size': '13'})
#
# Create the form class.
class EventForm(ModelForm):

#    date = DateField(widget=CalendarWidget, required=True)
    
    class Meta:
        model = Event
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20}),
            #'date': AdminDateWidget(),
#error_messages={'required': 'Please enter your name'}
        }

