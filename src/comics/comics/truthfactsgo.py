from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Truth Facts (gocomics.com)"
    language = "en"
    url = "http://www.gocomics.com/truth-facts"
    active = False
    rights = "Wulff & Morgenthaler"


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = "2014-06-16"
    schedule = "Mo,We,Fr"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass  # Comic no longer published
