from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Nerd Rage"
    language = "en"
    url = "http://www.nerdragecomic.com/"
    start_date = "2010-09-28"
    end_date = "2017-11-17"
    rights = "Andy Kluthe"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
