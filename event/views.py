# -*- coding: utf-8 -*-
import datetime
from django.template.response import TemplateResponse
from event.models import Event, Category
from django.shortcuts import get_object_or_404
from event.forms import EventForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

today = datetime.date.today()

def view_events_from_cat(request, sort, template_name='main/events.html'):
    p = get_object_or_404(Category, shortname=sort)
    list_events = Event.objects.filter(category=p).filter(date__gte=today)
    return TemplateResponse(request,template_name, {'list_events':list_events,
                                'state': ' '.join((u"Категория ", p.rusname))})

def viewall(request, template_name='main/events.html'):
    list_events = Event.objects.order_by('date').filter(date__gte=today)
    return TemplateResponse(request,template_name, {'list_events':list_events,
                                                        'state':'Все события'})

def view_more_about_event(request, event_slug, 
                            template_name='main/view_full_event.html'):
    p = get_object_or_404(Event, slug=event_slug)
    return TemplateResponse(request,template_name, {'event':p})

def view_next_day(request, template_name='main/events.html'):
    list_events = Event.objects.filter(date=datetime.date.today() +\
        datetime.timedelta(1))
    return TemplateResponse(request,template_name, {'list_events':list_events, 
                                                'state':"События на завтра",
                                                    })

def view_next_week(request, template_name='main/events.html'):
    list_events = Event.objects.filter(date__gte=today).filter(date__lte= today +\
        datetime.timedelta(7)).order_by("date")
    return TemplateResponse(request,template_name, {'list_events':list_events,
                                                 'state':"События на неделю",
                                                    })



@login_required()
def add_event(request, template_name='main/add_event.html'):
    state = ''
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid(): 
            form.instance.added_by = request.user
            form.save()
            state = u"Событие успешно добавлено!"
            return HttpResponseRedirect(reverse('view_more', args=[form.instance.slug]))
    else:
        form = EventForm()

    return TemplateResponse(request, template_name, 
                            {'form': form,'state':state,})
