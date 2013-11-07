import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Pole Dancing Adventures'
    language = 'en'
    url = 'http://pole-dancing-adventures.blogspot.com/'
    start_date = '2010-01-28'
    rights = 'Leen Isabel'


class Crawler(CrawlerBase):
    history_capable_date = '2010-01-28'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/blogspot/zumUM')
        for entry in feed.for_date(pub_date):
            results = []

            for url in entry.summary.src('img', allow_multiple=True):
                # Look for NN-*.jpg to differentiate comics from other images
                if re.match('.*\/\d\d-.*\.jpg', url) is not None:
                    results.append(CrawlerImage(url))

            if results:
                results[0].title = entry.title
                return results
