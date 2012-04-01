from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.utils import timezone

from comics.core.models import Comic


class Set(models.Model):
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
        db_table = 'comics_set'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_slug(self):
        return self.name

    def set_slug(self, slug):
        self.name = slug

    slug = property(get_slug, set_slug)

    def set_loaded(self):
        self.last_loaded = timezone.now()
        self.save()


class UserSet(models.Model):
    user = models.ForeignKey(User)
    add_new_comics = models.BooleanField(default=False,
        help_text='Automatically add new comics to the set')
    hide_empty_comics = models.BooleanField(default=False,
        help_text='Hide comics without matching releases from view')
    comics = models.ManyToManyField(Comic)

    class Meta:
        db_table = 'comics_userset'

    def __unicode__(self):
        return u'Comic set for %s' % self.user

    def get_absolute_url(self):
        return reverse('userset-latest')

    def get_feed_url(self):
        return reverse('userset-feed')


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
