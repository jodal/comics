from tastypie.resources import ModelResource
from comics.core.models import Comic


class ComicResource(ModelResource):
    class Meta:
        queryset = Comic.objects.all()
        resource_name = 'comic'
