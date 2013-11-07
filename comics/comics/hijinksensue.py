from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'HijiNKS Ensue'
    language = 'en'
    url = 'http://hijinksensue.com/'
    start_date = '2007-05-11'
    rights = 'Joel Watson'


class Crawler(CrawlerBase):
    history_capable_days = 28
    time_zone = 'US/Central'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/hijinksensue')
        for entry in feed.for_date(pub_date):
            if 'Comics' not in entry.tags:
                continue
            url = entry.summary.src('img[src*="/comics-rss/"]')
            if url is None:
                continue
            url = url.replace('/comics-rss/', '/comics/')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics-rss/"]')
            return CrawlerImage(url, title, text)
