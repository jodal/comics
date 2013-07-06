from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Twenty Pixels'
    language = 'en'
    url = 'http://20px.com/'
    start_date = '2011-02-11'
    rights = 'Angela'


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/20px')
        for entry in feed.for_date(pub_date):
            if 'Comic' not in entry.tags:
                continue
            url = entry.summary.src('img[src$="_20px.jpg"]')
            title = entry.title
            text = entry.summary.alt('img[src$="_20px.jpg"]')
            return CrawlerImage(url, title, text)
