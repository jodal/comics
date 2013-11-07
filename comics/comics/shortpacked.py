from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Shortpacked'
    language = 'en'
    url = 'http://www.shortpacked.com/'
    start_date = '2005-01-17'
    rights = 'David Willis'


class Crawler(CrawlerBase):
    schedule = 'Mo,Tu,We,Th,Fr'
    history_capable_days = 32
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.shortpacked.com/rss.php')
        for entry in feed.for_date(pub_date):
            if 'blog.php' in entry.link:
                continue
            page = self.parse_page(entry.link)
            url = page.src('img#comic')
            title = entry.title.replace('Shortpacked! - ', '')
            text = page.title('img#comic')
            return CrawlerImage(url, title, text)
