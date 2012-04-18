from django import template
from event.models import Event
import datetime
register = template.Library()

@register.inclusion_tag('main/show_short_event.html',takes_context=True)
def show_short_event(context, list_):
    return {'list_events':list_,'STATIC_URL':context["STATIC_URL"]}



