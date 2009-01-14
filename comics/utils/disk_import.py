"""Imports existing comic strips from disk"""

import datetime as dt
import optparse

def get_option_group(parser):
    """Create an optparse option group for the module"""

    option_group = optparse.OptionGroup(parser, 'Disk Import')
    option_group.add_option('-I', '--import',
        action='store_const', const='disk_import', dest='action',
        help='Import comic strips from disk')
    option_group.add_option('-i', '--icomic',
        action='append', dest='comics', metavar='COMIC',
        help='Comic to import, repeat for multiple [default: all]')
    return option_group

def do_disk_import(options):
    """Execute a disk import of comics from one or more comics"""

    import os
    import sys

    from django.conf import settings

    from comics.common.models import Comic, Strip
    from comics.utils.hash import sha256sum

    verbose = False
    if options.get('verbose', 1) == 2:
        verbose = True

    if options.get('comics', None) is None or len(options['comics']) == 0:
        comics = Comic.objects.all()
    else:
        comics = []
        for comic_slug in options['comics']:
            comics.append(Comic.objects.get(slug=comic_slug))

    if len(comics) == 0:
        print 'No comics found in database'

    for comic in comics:
        print '>>> %s' % comic

        years = os.listdir(settings.MEDIA_ROOT + comic.slug)
        years.sort()

        for year in years:
            print 'Import %s from %s ' % (comic, year),

            strips = os.listdir(settings.MEDIA_ROOT
                                + comic.slug
                                + '/'
                                + year)
            strips.sort()

            for stripname in strips:
                filename = '%s/%s/%s' % (comic.slug, year, stripname)
                checksum = sha256sum(settings.MEDIA_ROOT + filename)

                if verbose:
                    print 'Importing %s:' % (stripname),

                try:
                    Strip.objects.get(comic=comic, checksum=checksum)
                    if verbose:
                        print 'Strip with same checksum exists; skipping.'
                    else:
                        sys.stdout.write('.')
                        sys.stdout.flush()
                    continue
                except Strip.DoesNotExist:
                    pass

                pub_date = dt.datetime.strptime(
                    stripname.split('.')[0], '%Y-%m-%d').date()
                strip = Strip(comic=comic,
                              pub_date=pub_date,
                              filename=filename,
                              checksum=checksum)
                strip.save()

                if verbose:
                    print '%s saved' % strip
                else:
                    sys.stdout.write('N')
                    sys.stdout.flush()
            print ' OK'
        print '%s complete' % comic
