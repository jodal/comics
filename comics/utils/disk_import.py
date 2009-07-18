"""Imports existing comic strips from disk"""

import datetime as dt
import logging
import os

from django.conf import settings

from comics.core.models import Comic, Release, Strip
from comics.utils.hash import sha256sum

logger = logging.getLogger('comics.utils.disk_import')

def do_disk_import(options):
    for comic in _get_comics(options):
        logger.info('>>> %s', comic)
        for year in _get_years(comic):
            logger.info('%s from %s...', comic, year)
            for strip_name in _get_strip_names(comic, year):
                _try_import_strip(comic, year, strip_name)

def _get_comics(options):
    if options.get('comics', None) is None or len(options['comics']) == 0:
        comics = Comic.objects.all()
    else:
        comics = []
        for comic_slug in options['comics']:
            comics.append(Comic.objects.get(slug=comic_slug))
    if len(comics) == 0:
        logger.error('No comics found in database')
    return comics

def _get_years(comic):
    return sorted(os.listdir('%s%s' % (settings.MEDIA_ROOT, comic.slug)))

def _get_strip_names(comic, year):
    return sorted(os.listdir('%s%s/%s' % (
        settings.MEDIA_ROOT, comic.slug, year)))

def _try_import_strip(comic, year, strip_name):
    try:
        logger.debug('Checking %s', strip_name)
        filename = _get_filename(comic, year, strip_name)
        checksum = _get_checksum(filename)
        Strip.objects.get(comic=comic, checksum=checksum)
        logger.debug('Strip with same checksum exists; skipping.')
    except Strip.DoesNotExist:
        _import_strip(comic, filename, checksum, _get_pub_date(strip_name))

def _get_filename(comic, year, strip_name):
    return '%s/%s/%s' % (comic.slug, year, strip_name)

def _get_checksum(filename):
    return sha256sum('%s%s' % (settings.MEDIA_ROOT, filename))

def _get_pub_date(strip_name):
    return dt.datetime.strptime(strip_name.split('.')[0], '%Y-%m-%d').date()

def _import_strip(comic, filename, checksum, pub_date):
    strip = Strip(
        comic=comic,
        filename=filename,
        checksum=checksum)
    strip.save()
    release = Release(
        comic=comic,
        pub_date=pub_date,
        strip=strip)
    release.save()
    logger.info('%s imported', release)
