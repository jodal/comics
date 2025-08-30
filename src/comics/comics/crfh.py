from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Colleges Roomies from Hell"
    language = "en"
    url = "https://www.maritzacampos.com/crfh/"
    start_date = "1999-01-01"
    end_date = "2025-02-24"
    rights = "Maritza Campos"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "1999-01-01"
    time_zone = "America/Merida"

    def crawl(self, pub_date):
        pass  # Comic no longer published
