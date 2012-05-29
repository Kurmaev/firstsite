from django import template
from event.models import Category
from lxml import etree
from StringIO import StringIO
register = template.Library()
from django.core.urlresolvers import reverse, resolve

@register.inclusion_tag('main/show_cat.html', takes_context=True)
def show_category(context):
    list_cat = Category.objects.all()
    return {'list_cat':list_cat, 'request':context['request']}


@register.simple_tag(takes_context=True)
def path_match(context, class_name, name_view):
    try:
        regexp = reverse(name_view)
    except:
        regexp = name_view

    if (regexp == context['request'].path_info):
        return u''.join((' class="',class_name,'"'))
    else:
        return ""

@register.filter(name='cut')
def cut(text, len_):
    """
    Cut text to allowed lenght
    """
    if len(text)>len_:
        parser = etree.HTMLParser()
        broken_html = '...'.join((text[:len_],''))
        tree = etree.parse(StringIO(broken_html), parser)
        str_t = etree.tostring(tree.getroot(), pretty_print=True, method="html")
        return str_t
    else:
        return text
