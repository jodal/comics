from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "seemikedraw"
    language = "en"
    url = "http://mikejacobsen.tumblr.com/"
    start_date = "2007-07-31"
    end_date = "2017-04-06"
    rights = "Mike Jacobsen"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2014-05-06"
    time_zone = "Australia/Sydney"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://mikejacobsen.tumblr.com/rss")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            title = entry.title
            return CrawlerImage(url, title)
