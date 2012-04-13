# -*- coding: utf-8 -*-

from django.template.response import TemplateResponse
from event.models import Event, Category

def viewevents(request, sort, template_name='main/events.html'):
    try:
        p = Category.objects.get(shortname=sort)
    except Category.DoesNotExist:
        id_category = 0
    else:
        id_category = p.id

    if id_category:    
        list_events = Event.objects.filter(category=id_category)
    else:
        list_events = ""
    return TemplateResponse(request,template_name, {'list_events':list_events})
