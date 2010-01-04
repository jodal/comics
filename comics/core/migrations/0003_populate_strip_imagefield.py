from __future__ import with_statement
import os
import shutil

from django.conf import settings
from django.core.files import File
from comics.core.models import *

class Migration:
    no_dry_run = True

    def forwards(self, orm):
        total = orm.Strip.objects.count()
        for i, strip in enumerate(orm.Strip.objects.all()):
            print '%s %d/%d' % (strip.checksum, i + 1, total)
            filename = '%s.%s' % (strip.checksum, strip.filename.split('.')[-1])
            file_path = '%s/%s' % (settings.COMICS_MEDIA_ROOT, strip.filename)
            file_path = os.path.abspath(file_path)
            with open(file_path) as fh:
                strip.file.save(filename, File(fh))
                strip.save()

    def backwards(self, orm):
        total = orm.Strip.objects.count()
        for i, strip in enumerate(orm.Strip.objects.all()):
            print '%s %d/%d' % (strip.checksum, i + 1, total)
            first_release = orm.Release.objects.filter(
                strip=strip.pk).order_by('pub_date')[0]
            filename = '%(slug)s/%(year)s/%(date)s.%(ext)s' % {
                'slug': strip.comic.slug,
                'year': first_release.pub_date.year,
                'date': first_release.pub_date.strftime('%Y-%m-%d'),
                'ext': strip.file.name.split('.')[-1],
            }
            file_path = '%s/%s' % (settings.COMICS_MEDIA_ROOT, filename)
            file_path = os.path.abspath(file_path)
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError:
                pass
            shutil.copy(strip.file.path, file_path)
            strip.filename = filename
            strip.save()

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
            'filename': ('models.CharField', [], {'max_length': '100'}),
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
