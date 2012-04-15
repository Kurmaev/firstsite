from django import template
from event.models import Category

register = template.Library()

@register.inclusion_tag('main/show_cat.html')
def show_category():
    list_cat = Category.objects.all()
    return {'list_cat':list_cat}

