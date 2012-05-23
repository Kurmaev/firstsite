# -*- coding: utf-8 -*-
import datetime
from django.template.response import TemplateResponse
from event.models import Event, Category
from django.shortcuts import get_object_or_404
from event.forms import EventForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from event.utils import getPage
from django.db.models import Q

today = datetime.date.today()

def view_events_from_cat(request, sort, template_name='main/events.html'):
    p = get_object_or_404(Category, shortname=sort)
    list_events = Event.objects.filter(category=p).filter(date_end__gte=today)

    return TemplateResponse(request,template_name, 
        {'list_events':getPage(request, list_events, 6), 
        'state':' '.join((u"Категория ", p.rusname))})

def viewall(request, template_name='main/events.html'):
    list_events = Event.objects.order_by('date_start').filter(date_end__gte=today)

    return TemplateResponse(request,template_name, 
        {'list_events':getPage(request, list_events, 3), 'state':'Все события'})

def view_more_about_event(request, event_slug, 
                            template_name='main/view_full_event.html'):
    p = get_object_or_404(Event, slug=event_slug)
    return TemplateResponse(request,template_name, {'event':p})

def view_next_day(request, template_name='main/events.html'):
    next_day = today + datetime.timedelta(1)
    list_events = Event.objects.filter(date_start__lte=next_day)
    list_events = list_events.filter(date_end__gte=next_day)

    return TemplateResponse(request,template_name, 
        {'list_events':getPage(request, list_events, 6), 
        'state':"События на завтра",})

def view_today(request, template_name='main/events.html'):
    list_events = Event.objects.filter(date_start__lte=today)
    list_events = list_events.filter(date_end__gte=today)
    zz = getPage(request, list_events, 6)
    return TemplateResponse(request,template_name, 
        {'list_events':zz, 
        'state':"Сегодня можно посетить",})

def view_next_week(request, template_name='main/events.html'):
    next_week = today + datetime.timedelta(7)
    list_events = Event.objects.filter(Q(date_start__range=(today,next_week))|\
Q(date_end__gte=next_week))

    return TemplateResponse(request,template_name, 
    {'list_events':getPage(request, list_events, 6),
    'state':"События на неделю",})

def search(request, template_name='main/search.html'):
    if 'query' in request.GET and request.GET['query']:
        q = request.GET['query']
        try:
            from sphinx import sphinxapi
        except:
            return TemplateResponse(request,'main/disable_search.html', 
                {'query': q,})
        
        sphinx = sphinxapi.SphinxClient()
        sphinx.SetServer('', 3312)
        sphinx.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED)
        sphinx.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
        sphinx.SetFieldWeights({'name':20, 'text':10})
        
        results = sphinx.Query(q)

        if results:
            ids = [m['id'] for m in results['matches']]

            # ?
            events = ids and Event.objects.filter(id__in=ids)

            #сортировка по весам
            events3 = dict((o.pk, o) for o in events)
            events3 = [events3[id] for id in ids]

            return TemplateResponse(request,template_name, 
                {'events': events3, 'query': q})
        else:
            return TemplateResponse(request,'main/disable_search.html', 
                {'query': q,})
    else:
        return HttpResponseRedirect(reverse('homepage'))

@login_required()
def add_event(request, template_name='main/add_event.html'):
    state = ''
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid(): 
            form.instance.added_by = request.user
            form.save()
            return HttpResponseRedirect(reverse('view_more', 
                                                args=[form.instance.slug]))
    else:
        form = EventForm()

    return TemplateResponse(request, template_name,     
                            {'form': form,'state':state,})
