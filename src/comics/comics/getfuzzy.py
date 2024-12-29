from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Get Fuzzy"
    language = "en"
    url = "http://www.gocomics.com/getfuzzy/"
    start_date = "1999-09-01"
    rights = "Darby Conley"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2009-05-26"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date):
        return self.crawl_helper("getfuzzy", pub_date)
