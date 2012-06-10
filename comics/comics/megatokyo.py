from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'MegaTokyo'
    language = 'en'
    url = 'http://www.megatokyo.com/'
    start_date = '2000-08-14'
    rights = 'Fred Gallagher & Rodney Caston'

class Crawler(CrawlerBase):
    history_capable_days = 30
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.megatokyo.com/rss/megatokyo.xml')
        for entry in feed.for_date(pub_date):
            if entry.title.startswith('Comic ['):
                title = entry.title.split('"')[1]
                page = self.parse_page(entry.link)
                url = page.src('img[src*="/strips/"]')
                return CrawlerImage(url, title)
