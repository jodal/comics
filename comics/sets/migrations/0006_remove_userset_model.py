# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserSet'
        db.delete_table('comics_userset')

        # Removing M2M table for field comics on 'UserSet'
        db.delete_table('comics_userset_comics')

    def backwards(self, orm):
        # Adding model 'UserSet'
        db.create_table('comics_userset', (
            ('hide_empty_comics', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('add_new_comics', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('sets', ['UserSet'])

        # Adding M2M table for field comics on 'UserSet'
        db.create_table('comics_userset_comics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userset', models.ForeignKey(orm['sets.userset'], null=False)),
            ('comic', models.ForeignKey(orm['core.comic'], null=False))
        ))
        db.create_unique('comics_userset_comics', ['userset_id', 'comic_id'])

    models = {
        'core.comic': {
            'Meta': {'ordering': "['name']", 'object_name': 'Comic', 'db_table': "'comics_comic'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number_of_sets': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'sets.set': {
            'Meta': {'ordering': "['name']", 'object_name': 'Set', 'db_table': "'comics_set'"},
            'add_new_comics': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Comic']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hide_empty_comics': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_loaded': ('django.db.models.fields.DateTimeField', [], {}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['sets']