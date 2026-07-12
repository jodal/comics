from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Not Invented Here"
    language = "en"
    url = "https://www.notinventedhere.com/"
    start_date = "2009-09-21"
    end_date = "2015-12-31"
    rights = "Bill Barnes and Paul Southworth"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2009-09-21"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        url = (
            "https://s3.amazonaws.com/thiswas.notinventedhe.re/on/%s"
            % pub_date.strftime("%Y-%m-%d")
        )
        return CrawlerImage(url)
