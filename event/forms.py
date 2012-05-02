# -*- coding: utf-8 -*-
from firstsite.settings import STATIC_URL
from django.forms import ModelForm, Textarea, DateInput, DateField, TextInput
from event.models import Event
from django.contrib.admin.widgets import AdminDateWidget

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20}),
            'date': DateInput(attrs={'class':'date-pick'}),
        }

