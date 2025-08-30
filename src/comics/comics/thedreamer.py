from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Dreamer"
    language = "en"
    url = "https://thedreamercomic.com/"
    rights = "Lora Innes"
    active = False


class Crawler(CrawlerBase):
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        page = self.parse_page("https://thedreamercomic.com/comic.php")
        url = page.src('img[src*="issues/"]')
        title = page.alt('img[src*="issues/"]')
        return CrawlerImage(url, title)
