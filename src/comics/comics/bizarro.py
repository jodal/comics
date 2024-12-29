from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Bizarro"
    language = "en"
    url = "https://www.comicskingdom.com/bizarro"
    start_date = "1985-01-01"
    rights = "Dan Piraro"


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_date = "2004-03-09"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("bizarro", pub_date)
