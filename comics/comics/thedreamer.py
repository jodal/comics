from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Dreamer"
    language = "en"
    url = "http://thedreamercomic.com/"
    rights = "Lora Innes"


class Crawler(CrawlerBase):
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        page = self.parse_page("http://thedreamercomic.com/comic.php")
        url = page.src('img[src*="issues/"]')
        title = page.alt('img[src*="issues/"]')
        return CrawlerImage(url, title)
