from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase
from comics.core.models import Release

class Meta(MetaBase):
    name = 'The Dreamer'
    language = 'en'
    url = 'http://thedreamercomic.com/'
    rights = 'Lora Innes'

class Crawler(CrawlerBase):
    schedule = 'Fr'
    multiple_releases_per_day = True

    def crawl(self, pub_date):
        page = self.parse_page('http://thedreamercomic.com/comic.php')
        url = page.src('img[src*="issues/"]')
        title = page.alt('img[src*="issues/"]')
        return CrawlerImage(url, title)
