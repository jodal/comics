from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Baby Blues"
    language = "en"
    url = "https://www.gocomics.com/babyblues"
    start_date = "1990-01-01"
    rights = "Rick Kirkman and Jerry Scott"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2011-11-26"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        return self.crawl_helper("babyblues", pub_date)
