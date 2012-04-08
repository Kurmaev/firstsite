# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.category'
        db.add_column('event_event', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['event.Category']),
                      keep_default=False)

        # Removing M2M table for field category on 'Event'
        db.delete_table('event_event_category')

    def backwards(self, orm):
        # Deleting field 'Event.category'
        db.delete_column('event_event', 'category_id')

        # Adding M2M table for field category on 'Event'
        db.create_table('event_event_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['event.event'], null=False)),
            ('category', models.ForeignKey(orm['event.category'], null=False))
        ))
        db.create_unique('event_event_category', ['event_id', 'category_id'])

    models = {
        'event.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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