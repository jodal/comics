from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ctrl+Alt+Del Sillies"
    language = "en"
    url = "http://www.cad-comic.com/sillies/"
    start_date = "2008-06-27"
    rights = "Tim Buckley"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass
