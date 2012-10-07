from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Garfield minus Garfield'
    language = 'en'
    url = 'http://garfieldminusgarfield.tumblr.com/'
    rights = 'Travors'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = None
    time_zone = 'Europe/London'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://garfieldminusgarfield.tumblr.com/rss')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            return CrawlerImage(url)
