from django.contrib.auth.models import User

from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized


class SecretKeyAuthentication(Authentication):
    def extract_credentials(self, request):
        if request.META.get('HTTP_AUTHORIZATION', '').lower().startswith(
                'key '):
            (auth_type, secret_key) = (
                request.META['HTTP_AUTHORIZATION'].split())

            if auth_type.lower() != 'key':
                raise ValueError("Incorrect authorization header.")
        else:
            secret_key = request.GET.get('key') or request.POST.get('key')

        return secret_key

    def is_authenticated(self, request, **kwargs):
        try:
            secret_key = self.extract_credentials(request)
        except ValueError:
            return HttpUnauthorized()

        if not secret_key:
            return HttpUnauthorized()

        try:
            user = User.objects.get(
                comics_profile__secret_key=secret_key, is_active=True)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return HttpUnauthorized()

        request.user = user
        return True

    def get_identifier(self, request):
        return self.extract_credentials(request)


class MultiAuthentication(object):
    """
    An authentication backend that tries a number of backends in order.

    This class have been copied from the Tastypie source code. It can hopefully
    be removed with the release of Tastypie 0.9.12.
    """
    def __init__(self, *backends, **kwargs):
        super(MultiAuthentication, self).__init__(**kwargs)
        self.backends = backends

    def is_authenticated(self, request, **kwargs):
        """
        Identifies if the user is authenticated to continue or not.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        unauthorized = False

        for backend in self.backends:
            check = backend.is_authenticated(request, **kwargs)

            if check:
                if isinstance(check, HttpUnauthorized):
                    unauthorized = unauthorized or check
                else:
                    request._authentication_backend = backend
                    return check

        return unauthorized

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.

        This implementation returns a combination of IP address and hostname.
        """
        try:
            return request._authentication_backend.get_identifier(request)
        except AttributeError:
            return 'nouser'
