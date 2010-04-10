from haystack import indexes
from haystack import site

from comics.core.models import Image

class ImageIndex(indexes.SearchIndex):
    document = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(indexed=False, use_template=True)

    def get_updated_field(self):
        return 'fetched'

site.register(Image, ImageIndex)
