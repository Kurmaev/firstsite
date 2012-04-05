# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('event_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('event', ['Event'])

    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('event_event')

    models = {
        'event.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['event']