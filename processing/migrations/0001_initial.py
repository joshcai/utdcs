# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table(u'processing_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_str', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'processing', ['Post'])


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table(u'processing_post')


    models = {
        u'processing.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'date_str': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['processing']