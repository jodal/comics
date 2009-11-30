import datetime as dt
import time
import os

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

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
    url = models.URLField(verbose_name='URL', blank=True,
        help_text='URL to the official website')

    # Optional fields
    start_date = models.DateField(blank=True, null=True,
        help_text='First published at')
    end_date = models.DateField(blank=True, null=True,
        help_text='Last published at, if comic has been cancelled')
    history_capable_date = models.DateField(blank=True, null=True,
        help_text='Date of oldest release available for crawling')
    history_capable_days = models.PositiveIntegerField(blank=True, null=True,
        help_text='Number of days a release is available for crawling')
    has_reruns = models.BooleanField(default=False,
        help_text='Check to add reruns as new releases')
    schedule = models.CharField(max_length=20, blank=True,
        help_text='On what weekdays the comic is published')
    time_zone = models.IntegerField(blank=True, null=True,
        help_text='In what approximate time zone, in whole hours, '
            + 'relative to UTC, the comic is published')
    rights = models.CharField(max_length=100, blank=True,
        help_text='Author, copyright, and/or licensing information')

    # Automatically populated fields (i.e. for denormalization)
    number_of_sets = models.PositiveIntegerField(default=0,
        help_text='Number of sets the comic is in (automatically updated)')

    objects = ComicManager()

    class Meta:
        db_table = 'comics_comic'
        ordering = ['name']

    def __unicode__(self):
        return u'%s [%s]' % (self.name, self.language)

    def get_absolute_url(self):
        return reverse('comic-latest', kwargs={
            'comic': self.slug,
        })

    def get_feed_url(self):
        return reverse('feeds', kwargs={
            'url': 'c/%s' % self.slug,
        })

    def history_capable(self):
        if self.history_capable_date is not None:
            return self.history_capable_date
        elif self.history_capable_days is not None:
            return (dt.date.today() - dt.timedelta(self.history_capable_days))
        else:
            return dt.date.today()

    def schedule_as_isoweekday(self):
        weekday_mapping = {'Mo': 1, 'Tu': 2, 'We': 3,
            'Th': 4, 'Fr': 5, 'Sa': 6, 'Su': 7}
        iso_schedule = []
        for weekday in self.schedule.split(','):
            iso_schedule.append(weekday_mapping[weekday])
        return iso_schedule

    def datetime_in_time_zone(self):
        if self.time_zone is None:
            return None
        local_time_zone = - time.timezone // 3600
        hour_diff = local_time_zone - self.time_zone
        return dt.datetime.now() - dt.timedelta(hours=hour_diff)


class Release(models.Model):
    # XXX An index ranging over all three fields of this class is CRITICAL for
    # any performance. For PostreSQL use:
    #
    #     CREATE INDEX "comics_release_comic_id_pub_date_strip_id"
    #         ON "comics_release" ("comic_id", "pub_date", "strip_id");

    # Required fields
    comic = models.ForeignKey(Comic)
    pub_date = models.DateField(verbose_name='publication date')
    strip = models.ForeignKey('Strip', related_name='releases')

    class Meta:
        db_table = 'comics_release'
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return u'%s published %s' % (self.comic, self.pub_date)

    def get_absolute_url(self):
        return reverse('comic-date', kwargs={
            'comic': self.comic.slug,
            'year': self.pub_date.year,
            'month': self.pub_date.month,
            'day': self.pub_date.day,
        })


class Strip(models.Model):
    # Required fields
    comic = models.ForeignKey(Comic)
    fetched = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=100)
    checksum = models.CharField(max_length=64, db_index=True)

    # Optional fields
    title = models.CharField(max_length=100, blank=True)
    text = models.TextField(blank=True)

    class Meta:
        db_table = 'comics_strip'
        get_latest_by = 'pub_date'

    def delete(self, *args, **kwargs):
        super(Strip, self).delete(*args, **kwargs)
        os.remove('%s%s' % (settings.COMICS_MEDIA_ROOT, self.filename))

    def __unicode__(self):
        return u'%s strip %s' % (self.comic, self.checksum)

    def get_image_url(self):
        return '%s%s' % (settings.COMICS_MEDIA_URL, self.filename)

    def get_first_release(self):
        return self.releases.order_by('pub_date')[0]
