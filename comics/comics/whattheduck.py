from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'What the Duck'
    language = 'en'
    url = 'http://www.whattheduck.net/'
    start_date = '2006-07-01'
    rights = 'Aaron Johnson'

class Crawler(CrawlerBase):
    history_capable_days = 7
    schedule = 'We'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.whattheduck.net/strip/rss.xml')
        for entry in feed.for_date(pub_date):
            if (entry.enclosures[0].type.startswith('image')
                    and entry.title.startswith('WTD')):
                url = entry.enclosures[0].href
                title = entry.title
                return CrawlerImage(url, title)
