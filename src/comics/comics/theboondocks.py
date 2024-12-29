from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Boondocks"
    language = "en"
    url = "http://www.gocomics.com/boondocks"
    start_date = "1999-04-19"
    rights = "Aaron McGruder"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "1999-04-19"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date):
        return self.crawl_helper("boondocks", pub_date)
