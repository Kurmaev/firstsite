# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Category.rusname'
        db.add_column('event_category', 'rusname',
                      self.gf('django.db.models.fields.CharField')(default=0, unique=True, max_length=10),
                      keep_default=False)

        # Adding unique constraint on 'Category', fields ['shortname']
        db.create_unique('event_category', ['shortname'])

    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['shortname']
        db.delete_unique('event_category', ['shortname'])

        # Deleting field 'Category.rusname'
        db.delete_column('event_category', 'rusname')

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
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['event']