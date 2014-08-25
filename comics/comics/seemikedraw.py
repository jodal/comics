from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'seemikedraw'
    language = 'en'
    url = 'http://mikejacobsen.tumblr.com/'
    start_date = '2007-07-31'
    rights = 'Mike Jacobsen'


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = 'Australia/Sydney'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://mikejacobsen.tumblr.com/rss')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title
            return CrawlerImage(url, title)
