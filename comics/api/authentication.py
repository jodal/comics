from django.contrib.auth.models import User

from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized


class SecretKeyAuthentication(Authentication):
    def extract_credentials(self, request):
        if request.META.get('HTTP_AUTHORIZATION', '').lower().startswith(
                'key '):
            (auth_type, secret_key) = request.META['HTTP_AUTHORIZATION'].split()

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
            user = User.objects.get(comics_profile__secret_key=secret_key,
                is_active=True)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return HttpUnauthorized()

        request.user = user
        return True

    def get_identifier(self, request):
        return self.extract_credentials(request)
