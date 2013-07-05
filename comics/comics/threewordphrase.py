from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Three Word Phrase'
    language = 'en'
    url = 'http://www.threewordphrase.com/'
    start_date = '2010-07-13'
    rights = 'Ryan Pequin'


class Crawler(CrawlerBase):
    history_capable_days = 0
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
         # Thee feed has broken dates, so we fetch only the latest one
        feed = self.parse_feed('http://www.threewordphrase.com/rss.xml')
        if feed.all():
            entry = feed.all()[0]
            url = entry.link.replace('.htm', '.gif')
            title = entry.title
            text = entry.summary.root.text
            return CrawlerImage(url, title, text)
