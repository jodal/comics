from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Romantically Apocalyptic'
    language = 'en'
    url = 'http://www.romanticallyapocalyptic.com/'
    rights = 'Vitaly S. Alexius'

class Crawler(CrawlerBase):
    history_capable_days = None
    schedule = None
    time_zone = -5

    def crawl(self, pub_date):
        page = self.parse_page('http://www.romanticallyapocalyptic.com/')
        urls = page.src('img[src*="/art/"]', allow_multiple=True)
        for url in urls:
            if 'thumb' not in url:
                return CrawlerImage(url)
