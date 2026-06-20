from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Luann"
    language = "en"
    url = "https://www.gocomics.com/luann"
    rights = "Greg Evans and Karen Evans"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "1985-03-17"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("luann", pub_date)
