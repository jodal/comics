import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals

from comics.core.models import Comic

class NamedSet(models.Model):
    name = models.SlugField(max_length=100, unique=True,
        help_text='The set identifier')
    add_new_comics = models.BooleanField(default=False,
        help_text='Automatically add new comics to the set')
    hide_empty_comics = models.BooleanField(default=False,
        help_text='Hide comics without matching releases from view')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField()
    last_loaded = models.DateTimeField()
    comics = models.ManyToManyField(Comic)

    class Meta:
        db_table = 'comics_namedset'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('namedset-latest', kwargs={'namedset': self.name})

    def get_feed_url(self):
        return reverse('namedset-feed', kwargs={'namedset': self.name})

    def get_slug(self):
        return self.name
    def set_slug(self, slug):
        self.name = slug
    slug = property(get_slug, set_slug)

    def set_loaded(self):
        self.last_loaded = datetime.datetime.now()
        self.save()


class UserSet(models.Model):
    user = models.ForeignKey(User)
    add_new_comics = models.BooleanField(default=False,
        help_text='Automatically add new comics to the set')
    hide_empty_comics = models.BooleanField(default=False,
        help_text='Hide comics without matching releases from view')
    last_modified = models.DateTimeField()
    last_loaded = models.DateTimeField()
    comics = models.ManyToManyField(Comic)

    class Meta:
        db_table = 'comics_user_set'

    def __unicode__(self):
        return u'Comic set for %s' % self.user

    def set_loaded(self):
        self.last_loaded = datetime.datetime.now()
        self.save()


def create_user_set_for_new_users_callback(sender, **kwargs):
    if sender == User and kwargs['created']:
        user_set = UserSet(user=kwargs['instance'])
        user_set.save()

signals.post_save.connect(create_user_set_for_new_users_callback, sender=User)


def add_new_comic_to_user_sets_callback(sender, **kwargs):
    if sender == Comic and kwargs['created']:
        # Add new comic to all sets with add_new_comics=True
        for user_set in UserSet.objects.filter(add_new_comics=True):
            user_set.comics.add(kwargs['instance'])
        # Update number_of_sets on the new comic
        kwargs['instance'].number_of_sets = UserSet.objects.filter(
            add_new_comics=True).count()
        kwargs['instance'].save()

signals.post_save.connect(add_new_comic_to_user_sets_callback, sender=Comic)
