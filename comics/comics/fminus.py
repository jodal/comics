from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "F Minus"
    language = "en"
    url = "http://www.gocomics.com/fminus"
    start_date = "1999-09-01"
    rights = "Tony Carrillo"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2001-02-02"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Mountain"

    def crawl(self, pub_date):
        return self.crawl_helper("fminus", pub_date)
