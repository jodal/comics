from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Magpie Luck'
    language = 'en'
    url = 'http://magpieluck.com/'
    start_date = '2009-07-30'
    rights = 'Katie Sekelsky, CC BY-NC-SA 3.0'

class Crawler(CrawlerBase):
    history_capable_days = 32
    schedule = None
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/MagpieLuckComic')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/wp-content/"]')
            title = entry.title.split('- ', 1)[-1]
            text = entry.content0.alt('img[src*="/wp-content/"]')
            return CrawlerImage(url, title, text)
