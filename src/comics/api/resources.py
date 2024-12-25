from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from comics.accounts.models import Subscription
from comics.api.authentication import MultiAuthentication, SecretKeyAuthentication
from comics.core.models import Comic, Image, Release


class UsersAuthorization(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(pk=bundle.request.user.pk)


class UsersResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ["email", "date_joined", "last_login"]
        resource_name = "users"
        authentication = MultiAuthentication(
            BasicAuthentication(realm="Comics API"), SecretKeyAuthentication()
        )
        authorization = UsersAuthorization()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]

    def dehydrate(self, bundle):
        bundle.data["secret_key"] = bundle.request.user.comics_profile.secret_key
        return bundle


class ComicsAuthorization(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        if bundle.request.GET.get("subscribed") == "true":
            return object_list.filter(userprofile__user=bundle.request.user)
        elif bundle.request.GET.get("subscribed") == "false":
            return object_list.exclude(userprofile__user=bundle.request.user)
        else:
            return object_list


class ComicsResource(ModelResource):
    class Meta:
        queryset = Comic.objects.all()
        resource_name = "comics"
        authentication = SecretKeyAuthentication()
        authorization = ComicsAuthorization()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]
        filtering = {
            "active": "exact",
            "language": "exact",
            "name": ALL,
            "slug": ALL,
        }


class ImagesResource(ModelResource):
    class Meta:
        queryset = Image.objects.all()
        resource_name = "images"
        authentication = SecretKeyAuthentication()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]
        filtering = {
            "fetched": ALL,
            "title": ALL,
            "text": ALL,
            "height": ALL,
            "width": ALL,
        }


class ReleasesAuthorization(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        if bundle.request.GET.get("subscribed") == "true":
            return object_list.filter(comic__userprofile__user=bundle.request.user)
        elif bundle.request.GET.get("subscribed") == "false":
            return object_list.exclude(comic__userprofile__user=bundle.request.user)
        else:
            return object_list


class ReleasesResource(ModelResource):
    comic = fields.ToOneField(ComicsResource, "comic")
    images = fields.ToManyField(ImagesResource, "images", full=True)

    class Meta:
        queryset = Release.objects.select_related().order_by("-fetched")
        resource_name = "releases"
        authentication = SecretKeyAuthentication()
        authorization = ReleasesAuthorization()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]
        filtering = {
            "comic": ALL_WITH_RELATIONS,
            "images": ALL_WITH_RELATIONS,
            "pub_date": ALL,
            "fetched": ALL,
        }


class SubscriptionAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(userprofile__user=bundle.request.user)


class SubscriptionsResource(ModelResource):
    comic = fields.ToOneField(ComicsResource, "comic")

    class Meta:
        queryset = Subscription.objects.all()
        resource_name = "subscriptions"
        authentication = SecretKeyAuthentication()
        authorization = SubscriptionAuthorization()
        list_allowed_methods = ["get", "post", "patch"]
        detail_allowed_methods = ["get", "delete", "put"]
        filtering = {
            "comic": ALL_WITH_RELATIONS,
        }

    def obj_create(self, bundle, **kwargs):
        return super().obj_create(
            bundle, userprofile=bundle.request.user.comics_profile
        )
