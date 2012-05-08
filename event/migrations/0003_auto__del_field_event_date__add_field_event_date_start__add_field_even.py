# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.date'
        db.delete_column('event_event', 'date')

        # Adding field 'Event.date_start'
        db.add_column('event_event', 'date_start',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 7, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.date_end'
        db.add_column('event_event', 'date_end',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 7, 0, 0), blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'Event.date'
        db.add_column('event_event', 'date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 5, 7, 0, 0)),
                      keep_default=False)

        # Deleting field 'Event.date_start'
        db.delete_column('event_event', 'date_start')

        # Deleting field 'Event.date_end'
        db.delete_column('event_event', 'date_end')

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
            'added_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['event.Category']"}),
            'changed': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '3072'})
        }
    }

    complete_apps = ['event']