import datetime

from south.db import db
from django.db import models
from comics.core.models import *

class Migration:
    def forwards(self, orm):
        # Adding field 'Release.fetched'
        db.add_column('comics_release', 'fetched', models.DateTimeField(auto_now_add=True, default=datetime.datetime.now), keep_default=False)
        # Fix for South bug #316 in sqlite3 backend
        if hasattr(db, '_populate_current_structure'):
            db._populate_current_structure('comics_release', force=True)

    def backwards(self, orm):
        # Deleting field 'Release.fetched'
        db.delete_column('comics_release', 'fetched')

    models = {
        'core.comic': {
            'Meta': {'db_table': "'comics_comic'"},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number_of_sets': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'core.image': {
            'Meta': {'db_table': "'comics_image'"},
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
            'Meta': {'db_table': "'comics_release'"},
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Comic']"}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['core.Image']"}),
            'pub_date': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['core']
