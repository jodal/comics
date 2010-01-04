from south.db import db
from django.db import models
from comics.core.models import *

class Migration:
    def forwards(self, orm):
        # Deleting field 'Strip.filename'
        db.delete_column('comics_strip', 'filename')

    def backwards(self, orm):
        # Adding field 'Strip.filename'
        db.add_column('comics_strip', 'filename', models.CharField(max_length=100, default=''), keep_default=False)

    models = {
        'core.comic': {
            'Meta': {'ordering': "['name']", 'db_table': "'comics_comic'"},
            'end_date': ('models.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'language': ('models.CharField', [], {'max_length': '2'}),
            'name': ('models.CharField', [], {'max_length': '100'}),
            'number_of_sets': ('models.PositiveIntegerField', [], {'default': '0'}),
            'rights': ('models.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '100', 'verbose_name': "'Short name'"}),
            'start_date': ('models.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('models.URLField', [], {'verbose_name': "'URL'", 'blank': 'True'})
        },
        'core.strip': {
            'Meta': {'db_table': "'comics_strip'", 'get_latest_by': "'pub_date'"},
            'checksum': ('models.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'comic': ('models.ForeignKey', ['Comic'], {}),
            'fetched': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'file': ('models.ImageField', [], {'height_field': "'height'", 'upload_to': 'image_file_path', 'width_field': "'width'", 'storage': 'image_storage'}),
            'height': ('models.IntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'text': ('models.TextField', [], {'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'width': ('models.IntegerField', [], {})
        },
        'core.release': {
            'Meta': {'db_table': "'comics_release'", 'get_latest_by': "'pub_date'"},
            'comic': ('models.ForeignKey', ['Comic'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('models.DateField', [], {'verbose_name': "'publication date'"}),
            'strip': ('models.ForeignKey', ["'Strip'"], {'related_name': "'releases'"})
        }
    }

    complete_apps = ['core']
