from south.db import db
from django.db import models
from comics.core.models import *

class Migration:
    def forwards(self, orm):
        # Adding model 'Comic'
        db.create_table('comics_comic', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=100)),
            ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Short name')),
            ('language', models.CharField(max_length=2)),
            ('url', models.URLField(verbose_name='URL', blank=True)),
            ('start_date', models.DateField(null=True, blank=True)),
            ('end_date', models.DateField(null=True, blank=True)),
            ('rights', models.CharField(max_length=100, blank=True)),
            ('number_of_sets', models.PositiveIntegerField(default=0)),
        ))
        db.send_create_signal('core', ['Comic'])

        # Adding model 'Strip'
        db.create_table('comics_strip', (
            ('id', models.AutoField(primary_key=True)),
            ('comic', models.ForeignKey(orm.Comic)),
            ('fetched', models.DateTimeField(auto_now_add=True)),
            ('filename', models.CharField(max_length=100)),
            ('checksum', models.CharField(max_length=64, db_index=True)),
            ('title', models.CharField(max_length=255, blank=True)),
            ('text', models.TextField(blank=True)),
        ))
        db.send_create_signal('core', ['Strip'])

        # Adding model 'Release'
        db.create_table('comics_release', (
            ('id', models.AutoField(primary_key=True)),
            ('comic', models.ForeignKey(orm.Comic)),
            ('pub_date', models.DateField(verbose_name='publication date')),
            ('strip', models.ForeignKey(orm.Strip, related_name='releases')),
        ))
        db.send_create_signal('core', ['Release'])

    def backwards(self, orm):
        # Deleting model 'Comic'
        db.delete_table('comics_comic')

        # Deleting model 'Strip'
        db.delete_table('comics_strip')

        # Deleting model 'Release'
        db.delete_table('comics_release')

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
            'filename': ('models.CharField', [], {'max_length': '100'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'text': ('models.TextField', [], {'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255', 'blank': 'True'})
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
