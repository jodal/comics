from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Rose Is Rose"
    language = "en"
    url = "http://www.gocomics.com/roseisrose/"
    start_date = "1984-10-02"
    rights = "Pat Brady"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "1995-10-09"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("roseisrose", pub_date)
