from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Nerd Rage"
    language = "en"
    url = "http://www.nerdragecomic.com/"
    start_date = "2010-09-28"
    rights = "Andy Kluthe"


class Crawler(CrawlerBase):
    history_capable_date = "2010-09-28"
    time_zone = "US/Central"

    def crawl(self, pub_date):
        page = self.parse_page(
            pub_date.strftime("http://www.nerdragecomic.com/?date=%Y-%m-%d")
        )
        url = page.src('img[src*="/strips/"]')
        title = page.alt('img[src*="/strips/"]')
        return CrawlerImage(url, title)
