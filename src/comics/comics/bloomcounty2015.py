from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Bloom County 2015"
    language = "en"
    url = "http://www.gocomics.com/bloom-county/"
    start_date = "2015-07-20"
    end_date = "2020-06-08"
    rights = "Berkeley Breathed"
    active = False


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2015-07-20"
    schedule = "Mo,Tu,We,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        pass  # Comic no longer published
