from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Completely Serious Comics'
    language = 'en'
    url = 'http://completelyseriouscomics.com/'
    start_date = '2010-12-30'
    rights = 'Jesse'


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://completelyseriouscomics.com/?feed=rss2')
        for entry in feed.for_date(pub_date):
            if 'Comic' not in entry.tags:
                continue
            url = entry.summary.src('img')
            url = url.replace('comics-rss', 'comics')
            title = entry.title
            text = entry.summary.title('img')
            return CrawlerImage(url, title, text)
