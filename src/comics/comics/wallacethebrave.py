from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Wallace the Brave"
    language = "en"
    url = "https://www.gocomics.com/wallace-the-brave"
    rights = "Will Henry"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2015-06-29"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("wallace-the-brave", pub_date)
