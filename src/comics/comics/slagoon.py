from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sherman's Lagoon"
    language = "en"
    url = "http://shermanslagoon.com/"
    start_date = "1991-05-13"
    rights = "Jim Toomey"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2003-12-29"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        return self.crawl_helper("shermanslagoon", pub_date)
