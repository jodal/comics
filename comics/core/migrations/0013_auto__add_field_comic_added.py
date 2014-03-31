# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.utils.timezone import utc


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Comic.added'
        default = datetime.datetime(1, 1, 1, 0, 0).replace(tzinfo=utc)
        db.add_column('comics_comic', 'added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=default, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Comic.added'
        db.delete_column('comics_comic', 'added')


    models = {
        'core.comic': {
            'Meta': {'ordering': "['name']", 'object_name': 'Comic', 'db_table': "'comics_comic'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'core.image': {
            'Meta': {'object_name': 'Image', 'db_table': "'comics_image'"},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Comic']"}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.release': {
            'Meta': {'object_name': 'Release', 'db_table': "'comics_release'"},
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Comic']"}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'releases'", 'symmetrical': 'False', 'to': "orm['core.Image']"}),
            'pub_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['core']
