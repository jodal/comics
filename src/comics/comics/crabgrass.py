from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Crabgrass"
    language = "en"
    url = "https://www.gocomics.com/crabgrass"
    rights = "Tauhid Bondia"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2019-04-05"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("crabgrass", pub_date)
