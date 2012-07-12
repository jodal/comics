from tastypie.constants import ALL
from tastypie.resources import ModelResource

from comics.api.authentication import SecretKeyAuthentication
from comics.core.models import Comic


class ComicResource(ModelResource):
    class Meta:
        queryset = Comic.objects.all()
        resource_name = 'comic'
        authentication = SecretKeyAuthentication()
        filtering = {
            'active': 'exact',
            'language': 'exact',
            'name': ALL,
            'slug': ALL,
        }
