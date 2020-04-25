from comics.aggregator.crawler import CreatorsCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Liberty Meadows"
    language = "en"
    url = "http://www.creators.com/comics/liberty-meadows.html"
    start_date = "1997-03-30"
    end_date = "2001-12-31"
    rights = "Frank Cho"


class Crawler(CreatorsCrawlerBase):
    history_capable_date = "2006-11-21"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Pacific"

    def crawl(self, pub_date):
        return self.crawl_helper("153", pub_date)
