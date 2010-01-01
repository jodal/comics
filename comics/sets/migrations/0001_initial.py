from south.db import db
from django.db import models
from comics.sets.models import *

class Migration:
    depends_on = (
        ('core', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'Set'
        db.create_table('comics_set', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.SlugField(unique=True, max_length=100)),
            ('add_new_comics', models.BooleanField(default=False)),
            ('hide_empty_comics', models.BooleanField(default=False)),
            ('created', models.DateTimeField(auto_now_add=True)),
            ('last_modified', models.DateTimeField()),
            ('last_loaded', models.DateTimeField()),
        ))
        db.send_create_signal('sets', ['Set'])

        # Adding ManyToManyField 'Set.comics'
        db.create_table('comics_set_comics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('set', models.ForeignKey(Set, null=False)),
            ('comic', models.ForeignKey(Comic, null=False))
        ))

    def backwards(self, orm):
        # Deleting model 'Set'
        db.delete_table('comics_set')

        # Dropping ManyToManyField 'Set.comics'
        db.delete_table('comics_set_comics')

    models = {
        'sets.set': {
            'Meta': {'ordering': "['name']", 'db_table': "'comics_set'"},
            'add_new_comics': ('models.BooleanField', [], {'default': 'False'}),
            'comics': ('models.ManyToManyField', ['Comic'], {}),
            'created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'hide_empty_comics': ('models.BooleanField', [], {'default': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'last_loaded': ('models.DateTimeField', [], {}),
            'last_modified': ('models.DateTimeField', [], {}),
            'name': ('models.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'core.comic': {
            'Meta': {'ordering': "['name']", 'db_table': "'comics_comic'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['sets']
