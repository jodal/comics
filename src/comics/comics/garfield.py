from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Garfield"
    language = "en"
    url = "https://www.gocomics.com/garfield/"
    start_date = "1978-06-19"
    rights = "Jim Davis"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "1978-06-19"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("garfield", pub_date)
