from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Scandinavia and the World'
    language = 'en'
    url = 'http://www.satwcomic.com/'
    start_date = '2009-06-01'
    rights = 'Humon'

class Crawler(CrawlerBase):
    schedule = None
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/satwcomic')
        for entry in feed.all():
            url = entry.summary.src('img[src*="/art/"]')
            if url is not None:
                url = url.replace('/thumb', '')
            title = entry.title
            return CrawlerImage(url, title)
