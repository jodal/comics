# Based on https://bitbucket.org/jokull/django-email-login/

import re

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


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
    def authenticate(self, username=None, password=None, email=None):
        if email is None:
            email = username
        if email_re.search(email):
            user = User.objects.filter(email__iexact=email)
            if user.count() > 0:
                user = user[0]
                if user.check_password(password):
                    return user
        return None
