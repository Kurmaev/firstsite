from django import template
from event.models import Event
import datetime
register = template.Library()

@register.inclusion_tag('main/show_events.html',takes_context=True)
def show_last_event(context):
    today = datetime.date.today()
    list_events = Event.objects.order_by("-created","date").filter(date__gte=today)[0:9]
    list_events_today = []
    list_events_future = []
    for i in list_events:
        if i.date==today:
            list_events_today.append(i)
        else:
            list_events_future.append(i)
    
    return {'list_events_today':list_events_today,
            'list_events_future':list_events_future,
            'STATIC_URL':context["STATIC_URL"]}



