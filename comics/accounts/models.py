import uuid

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from comics.core.models import Comic


@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def make_secret_key():
    return uuid.uuid4().hex


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='comics_profile')
    secret_key = models.CharField(
        max_length=32, blank=False, default=make_secret_key,
        help_text='Secret key for feed and API access')
    comics = models.ManyToManyField(Comic, through='Subscription')

    class Meta:
        db_table = 'comics_user_profile'
        verbose_name = 'comics profile'

    def __unicode__(self):
        return u'Comics profile for %s' % self.user.email

    def generate_new_secret_key(self):
        self.secret_key = make_secret_key()


class Subscription(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic)

    class Meta:
        db_table = 'comics_user_profile_comics'

    def __unicode__(self):
        return u'Subscription for %s to %s' % (
            self.userprofile.user.email, self.comic.slug)
