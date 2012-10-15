from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = "Fredo & Pid'jin"
    language = 'en'
    url = 'http://www.pidjin.net/'
    start_date = '2006-02-19'
    rights = 'Tudor Muscalu & Eugen Erhan'

class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/Pidjin')
        for entry in feed.for_date(pub_date):
            result = []
            urls = entry.content0.src('img[src*="/wp-content/uploads/"]',
                allow_multiple=True)
            for url in urls:
                result.append(CrawlerImage(url))
            return result
