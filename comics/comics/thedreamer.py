from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase
from comics.core.models import Release

class Meta(MetaBase):
    name = 'The Dreamer'
    language = 'en'
    url = 'http://thedreamercomic.com'
    rights = 'Lora Innes, Innes Art LLC. All rights reserved.'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        next_id = Release.objects.filter(comic__name='The Dreamer').count() + 1
        url = 'http://thedreamercomic.com/comic.php?id=%s' % next_id
        print url
        page = self.parse_page(url)
        img_url = page.src('img[src*="issues/"]')
        img_alt = page.alt('img[src*="issues/"]')
        return CrawlerImage(img_url, img_alt)
