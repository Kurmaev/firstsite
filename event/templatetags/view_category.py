from django import template
from event.models import Category

register = template.Library()
from django.core.urlresolvers import reverse, resolve

@register.inclusion_tag('main/show_cat.html', takes_context=True)
def show_category(context):
    list_cat = Category.objects.all()
    return {'list_cat':list_cat, 'request':context['request']}


class PathMatchNode(template.Node):
    def __init__(self, class_name, name_view):
        self.class_name = class_name
        self.name_view = name_view

    def render(self, context):
        try:
            regexp = reverse(self.name_view)
        except:
            regexp = template.Variable(self.name_view).resolve(context)

        if (regexp == context['request'].path_info):
            return u''.join((' class="',self.class_name,'"'))
        else:
            return ""

@register.tag('path_match')
def do_path_match(parser, token):
    try:
        tag_name, class_name, name_view = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
"%r tag requires a class name and name view or URL as arguments. \
Token is %s" % (token.contents.split()[0], token.contents)
    
    if name_view[0] in ( '"', "'" ):
        if not (name_view[0] == name_view[-1]):
            raise template.TemplateSyntaxError, \
        "%r tag requires right name view as argument" % tag_name
        else:
            name_view = name_view[1:-1]
    else:
        if name_view[-1] in ( '"', "'" ):
            raise template.TemplateSyntaxError, \
        "%r tag requires right name view as argument" % tag_name

    return PathMatchNode(class_name, name_view)
