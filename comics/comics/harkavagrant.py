from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Hark, A Vagrant!"
    language = "en"
    url = "http://www.harkavagrant.com/"
    start_date = "2008-05-01"
    rights = "Kate Beaton"


class Crawler(CrawlerBase):
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        page = self.parse_page("http://www.harkavagrant.com/")
        url = page.src(".rss-content img")
        title = page.title(".rss-content img")
        return CrawlerImage(url, title)
