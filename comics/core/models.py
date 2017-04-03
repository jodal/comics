import datetime
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from comics.core.managers import ComicManager


class Comic(models.Model):
    LANGUAGES = (
        ('en', 'English'),
        ('no', 'Norwegian'),
    )

    # Required fields
    name = models.CharField(
        max_length=100,
        help_text='Name of the comic')
    slug = models.SlugField(
        max_length=100, unique=True,
        verbose_name='Short name',
        help_text='For file paths and URLs')
    language = models.CharField(
        max_length=2, choices=LANGUAGES,
        help_text='The language of the comic')

    # Optional fields
    url = models.URLField(
        verbose_name='URL', blank=True,
        help_text='URL to the official website')
    active = models.BooleanField(
        default=True,
        help_text='Wheter the comic is still being crawled')
    start_date = models.DateField(
        blank=True, null=True,
        help_text='First published at')
    end_date = models.DateField(
        blank=True, null=True,
        help_text='Last published at, if comic has been cancelled')
    rights = models.CharField(
        max_length=100, blank=True,
        help_text='Author, copyright, and/or licensing information')

    # Automatically populated fields
    added = models.DateTimeField(
        auto_now_add=True,
        help_text='Time the comic was added to the site')

    objects = ComicManager()

    class Meta:
        db_table = 'comics_comic'
        ordering = ['name']

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('comic_latest', kwargs={'comic_slug': self.slug})

    def get_redirect_url(self):
        return reverse('comic_website', kwargs={'comic_slug': self.slug})

    def is_new(self):
        some_time_ago = timezone.now() - datetime.timedelta(
            days=settings.COMICS_NUM_DAYS_COMIC_IS_NEW)
        return self.added > some_time_ago


class Release(models.Model):
    # Required fields
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    pub_date = models.DateField(verbose_name='publication date', db_index=True)
    images = models.ManyToManyField('Image', related_name='releases')

    # Automatically populated fields
    fetched = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'comics_release'
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return u'Release %s/%s' % (self.comic.slug, self.pub_date)

    def get_absolute_url(self):
        return reverse('comic_day', kwargs={
            'comic_slug': self.comic.slug,
            'year': self.pub_date.year,
            'month': self.pub_date.month,
            'day': self.pub_date.day,
        })

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
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    file = models.ImageField(
        storage=image_storage, upload_to=image_file_path,
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
        return u'Image %s/%s...' % (self.comic.slug, self.checksum[:8])
