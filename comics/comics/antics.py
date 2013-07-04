from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Antics'
    language = 'en'
    url = 'http://www.anticscomic.com/'
    start_date = '2008-10-25'
    rights = 'Fletcher'


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Fr'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.anticscomic.com/?feed=rss2')
        for entry in feed.for_date(pub_date):
            if 'comic' not in entry.tags:
                continue
            image_url = pub_date.strftime('/comics/%Y-%m-%d.jpg')
            url = entry.content0.src('img[src$="%s"]' % image_url)
            title = entry.title
            text = entry.content0.title('img[src*="%s"]' % image_url)
            return CrawlerImage(url, title, text)
