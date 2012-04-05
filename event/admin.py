from django.contrib import admin
from event.models import Category, Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'get_category',)
    list_filter = ('category',)
    date_hierarchy = 'date'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'description',)

admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoryAdmin)
