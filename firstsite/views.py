from django.template.response import TemplateResponse
from event.models import Event
import datetime

def home(request):
    today = datetime.date.today()
    list_events = Event.objects.order_by("-created","date").filter(date__gte=today)[:10]
    list_events_today = []
    list_events_future = []
    for i in list_events:
        if i.date==today:
            list_events_today.append(i)
        else:
            list_events_future.append(i)
    list_events_future.sort(key=lambda event: event.date)
    return TemplateResponse(request,'main/home.html',{'list_events_today':list_events_today,'list_events_future':list_events_future,})
