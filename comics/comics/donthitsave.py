from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Don't Hit Save"
    language = "en"
    url = "https://donthitsave.com/"
    start_date = "2015-09-18"
    rights = "Jeff Lofvers"


class Crawler(CrawlerBase):
    history_capable_days = 60
    schedule = "Tu,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://donthitsave.com/donthitsavefeed.xml")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comicimages/"]')
            title = entry.title
            return CrawlerImage(url, title)
