import uuid

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    secret_key = models.CharField(max_length=32, blank=False,
        help_text='Secret key for feed and API access')

    class Meta:
        db_table = 'comics_user_profile'

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        if self.secret_key is None:
            self.generate_new_secret_key()

    def __unicode__(self):
        return u'User profile for %s' % self.user

    def generate_new_secret_key(self):
        self.secret_key = uuid.uuid4().hex
