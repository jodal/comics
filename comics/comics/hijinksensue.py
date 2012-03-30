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
    schedule = None
    time_zone = -6

    def crawl(self, pub_date):
        feed_url = 'http://feeds.feedburner.com/hijinksensue'
        feed = self.parse_feed(feed_url)
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/comics/%s"]' %
                pub_date.strftime('%Y'))
            title = entry.title
            # Weed out the blog posts without images
            if url is not None:
                return CrawlerImage(url, title)
