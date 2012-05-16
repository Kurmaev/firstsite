# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, DateInput, DateField, TextInput
from event.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20,'class':'wysiwyg'}),
            'date_start': DateInput(attrs={'class':'date-pick'}),
            'date_end': DateInput(attrs={'class':'date-pick'}),
        }

