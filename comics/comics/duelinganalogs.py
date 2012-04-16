from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Dueling Analogs'
    language = 'en'
    url = 'http://www.duelinganalogs.com/'
    start_date = '2005-11-17'
    rights = 'Steve Napierski'

class Crawler(CrawlerBase):
    history_capable_days = 35
    schedule = 'Mo,Th'
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/DuelingAnalogs')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
