# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('event_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shortname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('rusname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('event', ['Category'])

        # Adding model 'Event'
        db.create_table('event_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Category'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('changed', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('event', ['Event'])

    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('event_category')

        # Deleting model 'Event'
        db.delete_table('event_event')

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
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['event']