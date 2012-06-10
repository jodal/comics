from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Misfile'
    language = 'en'
    url = 'http://www.misfile.com/'
    start_date = '2004-03-01'
    rights = 'Chris Hazelton'

class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.misfile.com/misfileRSS.php')
        for entry in feed.for_date(pub_date):
            url = entry.link
            url = url.replace('?', 'overlay.php?')
            url = url.replace('page', 'pageCalled')
            return CrawlerImage(url)
