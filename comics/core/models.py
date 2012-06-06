import datetime
import os

from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.utils import timezone

from comics.core.managers import ComicManager


class Comic(models.Model):
    LANGUAGES = (
        ('en', 'English'),
        ('no', 'Norwegian'),
    )

    # Required fields
    name = models.CharField(max_length=100,
        help_text='Name of the comic')
    slug = models.SlugField(max_length=100, unique=True,
        verbose_name='Short name',
        help_text='For file paths and URLs')
    language = models.CharField(max_length=2, choices=LANGUAGES,
        help_text='The language of the comic')

    # Optional fields
    url = models.URLField(verbose_name='URL', blank=True,
        help_text='URL to the official website')
    active = models.BooleanField(default=True,
        help_text='Wheter the comic is still being crawled')
    start_date = models.DateField(blank=True, null=True,
        help_text='First published at')
    end_date = models.DateField(blank=True, null=True,
        help_text='Last published at, if comic has been cancelled')
    rights = models.CharField(max_length=100, blank=True,
        help_text='Author, copyright, and/or licensing information')

    # Automatically populated fields (i.e. for denormalization)

    objects = ComicManager()

    class Meta:
        db_table = 'comics_comic'
        ordering = ['name']

    def __unicode__(self):
        return u'%s [%s]' % (self.name, self.language)

    def get_absolute_url(self):
        return reverse('comic_latest', kwargs={'comic_slug': self.slug})

    def get_redirect_url(self):
        return reverse('comic_website', kwargs={'comic_slug': self.slug})

    def is_new(self):
        first_release = self.release_set.all().order_by('fetched')[:1]
        if not first_release:
            return False
        first_release = first_release[0]
        some_time_ago = timezone.now() - datetime.timedelta(
            days=settings.COMICS_NUM_DAYS_COMIC_IS_NEW)
        return first_release.fetched > some_time_ago


class Release(models.Model):
    # Required fields
    comic = models.ForeignKey(Comic)
    pub_date = models.DateField(verbose_name='publication date')
    images = models.ManyToManyField('Image', related_name='releases')

    # Automatically populated fields
    fetched = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comics_release'
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return u'%s published %s' % (self.comic, self.pub_date)

    def get_absolute_url(self):
        return reverse('comic_day', kwargs={
            'comic_slug': self.comic.slug,
            'year': self.pub_date.year,
            'month': self.pub_date.month,
            'day': self.pub_date.day,
        })

    def get_images_first_release(self):
        key = 'release_images_first_release:%s' % self.id
        first = cache.get(key)

        if first is not None:
            return first

        try:
            first = self.images.all()[0].get_first_release()
        except IndexError:
            return

        cache.set(key, first)
        return first

    def set_ordered_images(self, images):
        self._ordered_images = images

    def get_ordered_images(self):
        if not getattr(self, '_ordered_images', []):
            self._ordered_images = list(self.images.order_by('id'))

        return self._ordered_images


# Let all created dirs and files be writable by the group
os.umask(0002)

image_storage = FileSystemStorage(
    location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)


def image_file_path(instance, filename):
    return u'%s/%s/%s' % (instance.comic.slug, filename[0], filename)


class Image(models.Model):
    # Required fields
    comic = models.ForeignKey(Comic)
    file = models.ImageField(storage=image_storage, upload_to=image_file_path,
        height_field='height', width_field='width')
    checksum = models.CharField(max_length=64, db_index=True)

    # Optional fields
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)

    # Automatically populated fields
    fetched = models.DateTimeField(auto_now_add=True)
    height = models.IntegerField()
    width = models.IntegerField()

    class Meta:
        db_table = 'comics_image'

    def __unicode__(self):
        return u'%s image %s' % (self.comic, self.checksum)

    def get_first_release(self):
        return self.releases.select_related('comic').order_by('pub_date')[0]
