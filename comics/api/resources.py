from django.contrib.auth.models import User

from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from comics.api.authentication import SecretKeyAuthentication
from comics.core.models import Comic, Release, Image


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['email', 'date_joined', 'last_login']
        resource_name = 'user'
        authentication = SecretKeyAuthentication()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(pk=request.user.pk)

    def dehydrate(self, bundle):
        bundle.data['secret_key'] = \
            bundle.request.user.comics_profile.secret_key
        return bundle


class ComicsResource(ModelResource):
    class Meta:
        queryset = Comic.objects.all()
        resource_name = 'comics'
        authentication = SecretKeyAuthentication()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'active': 'exact',
            'language': 'exact',
            'name': ALL,
            'slug': ALL,
        }


class ImagesResource(ModelResource):
    class Meta:
        queryset = Image.objects.all()
        resource_name = 'images'
        authentication = SecretKeyAuthentication()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'fetched': ALL,
            'title': ALL,
            'text': ALL,
            'height': ALL,
            'width': ALL,
        }


class ReleasesResource(ModelResource):
    comic = fields.ToOneField(ComicsResource, 'comic')
    images = fields.ToManyField(ImagesResource, 'images', full=True)

    class Meta:
        queryset = Release.objects.select_related(depth=1
            ).order_by('-fetched')
        resource_name = 'releases'
        authentication = SecretKeyAuthentication()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'comic': ALL_WITH_RELATIONS,
            'images': ALL_WITH_RELATIONS,
            'pub_date': ALL,
            'fetched': ALL,
        }


class MyComicsResource(ComicsResource):
    class Meta(ComicsResource.Meta):
        resource_name = 'mycomics'

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(userprofile__user=request.user)


class MyReleasesResource(ReleasesResource):
    class Meta(ReleasesResource.Meta):
        resource_name = 'myreleases'

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(comic__userprofile__user=request.user)
