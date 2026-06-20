from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Off the Mark"
    language = "en"
    url = "https://www.gocomics.com/offthemark"
    start_date = "2002-09-02"
    rights = "Mark Parisi"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2002-09-02"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("offthemark", pub_date)
