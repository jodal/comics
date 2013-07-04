from django.db import models
from django.utils import timezone

from comics.core.models import Comic


class Set(models.Model):
    name = models.SlugField(
        max_length=100, unique=True,
        help_text='The set identifier')
    add_new_comics = models.BooleanField(
        default=False,
        help_text='Automatically add new comics to the set')
    hide_empty_comics = models.BooleanField(
        default=False,
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
