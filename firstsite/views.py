from django.template.response import TemplateResponse
from event.models import Event
import datetime

def home(request):
    #FIXME: Rewrite this
    today = datetime.date.today()
    list_events = Event.objects.order_by("created").filter(date_end__gte=today)[:10]
    return TemplateResponse(request,'main/home.html',{'list_events':list_events,})
