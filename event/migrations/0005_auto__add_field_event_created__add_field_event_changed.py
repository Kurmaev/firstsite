# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.created'
        db.add_column('event_event', 'created',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.date.today(), blank=True),
                      keep_default=False)

        # Adding field 'Event.changed'
        db.add_column('event_event', 'changed',
                      self.gf('django.db.models.fields.DateField')(auto_now=True, default=datetime.date.today(), blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Event.created'
        db.delete_column('event_event', 'created')

        # Deleting field 'Event.changed'
        db.delete_column('event_event', 'changed')

    models = {
        'event.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rusname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'shortname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'event.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['event.Category']"}),
            'changed': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['event']
