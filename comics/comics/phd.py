from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Piled Higher and Deeper'
    language = 'en'
    url = 'http://www.phdcomics.com/'
    start_date = '1997-10-27'
    rights = 'Jorge Cham'

class Crawler(CrawlerBase):
    history_capable_date = '1997-10-27'
    schedule = None
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://www.phdcomics.com/gradfeed_justcomics.php')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img')
            title = entry.title.split("'")[1]
            return CrawlerImage(url, title)
