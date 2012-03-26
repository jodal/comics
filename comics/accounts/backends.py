# Based on https://bitbucket.org/jokull/django-email-login/

import re
from uuid import uuid4

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite, Site

from registration import signals
from registration.backends.default import DefaultBackend
from registration.models import RegistrationProfile

from forms import RegistrationForm

class RegistrationBackend(DefaultBackend):
    """
    Does not require the user to pick a username. Sets the username to a random
    string behind the scenes.

    """

    def register(self, request, **kwargs):
        email, password = kwargs['email'], kwargs['password1']

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(
            uuid4().get_hex()[:10], email, password, site)
        signals.user_registered.send(
            sender=self.__class__, user=new_user, request=request)
        return new_user

    def get_form_class(self, request):
        """
        Return the default form class used for user registration.

        """
        return RegistrationForm

email_re = re.compile(
    # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|'
    r'\\[\001-\011\013\014\016-\177])*"'
    # domain
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)

class AuthBackend(ModelBackend):
    """Authenticate using email only"""
    def authenticate(self, email=None, password=None):
        if email_re.search(email):
            user = User.objects.filter(email__iexact=email)
            if user.count() > 0:
                user = user[0]
                if user.check_password(password):
                    return user
        return None
