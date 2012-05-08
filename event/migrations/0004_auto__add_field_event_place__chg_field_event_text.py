# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.place'
        db.add_column('event_event', 'place',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True),
                      keep_default=False)


        # Changing field 'Event.text'
        db.alter_column('event_event', 'text', self.gf('django.db.models.fields.CharField')(max_length=5000))
    def backwards(self, orm):
        # Deleting field 'Event.place'
        db.delete_column('event_event', 'place')


        # Changing field 'Event.text'
        db.alter_column('event_event', 'text', self.gf('django.db.models.fields.CharField')(max_length=3072))
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
            'place': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        }
    }

    complete_apps = ['event']