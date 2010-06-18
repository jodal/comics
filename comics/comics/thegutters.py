from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase
from comics.core.models import Release

class Meta(MetaBase):
    name = 'The Gutters'
    language = 'en'
    url = 'http://thedreamercomic.com/'
    rights = 'Blind Ferret Entertainment'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page = self.parse_page('http://the-gutters.com')
        url = page.src('img[class="img_comic"]')
        return CrawlerImage(url)
