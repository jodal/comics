from django.template.loader import get_template
from django.template import Context

from haystack import indexes
from haystack import site

from comics.core.models import Image

class ImageIndex(indexes.SearchIndex):
    document = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(indexed=False)

    def get_updated_field(self):
        return 'fetched'

    def prepare_rendered(self, obj):
        template = get_template('search/results.html')
        context = Context({'release': obj.get_first_release()})
        return template.render(context)

site.register(Image, ImageIndex)
