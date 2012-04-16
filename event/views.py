# -*- coding: utf-8 -*-

from django.template.response import TemplateResponse
from event.models import Event, Category
from django.shortcuts import get_object_or_404

def viewevents(request, sort, template_name='main/events.html'):
    p = get_object_or_404(Category, shortname=sort)
    id_category = p.id
    list_events = Event.objects.filter(category=id_category)
    return TemplateResponse(request,template_name, {'list_events':list_events})

def viewall(request, template_name='main/events.html'):
    list_events = Event.objects.order_by('date')[0:10]
    return TemplateResponse(request,template_name, {'list_events':list_events})

def view_more_about_event(request, event_slug, template_name='main/view_events.html'):
    p = get_object_or_404(Event, slug=event_slug)
    return TemplateResponse(request,template_name, {'event':p})
