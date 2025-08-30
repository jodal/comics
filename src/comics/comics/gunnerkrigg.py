from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Gunnerkrigg Court"
    language = "en"
    url = "https://www.gunnerkrigg.com/"
    start_date = "2005-08-13"
    rights = "Tom Siddell"


class Crawler(CrawlerBase):
    schedule = "Mo,We,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        page = self.parse_page("https://www.gunnerkrigg.com/")
        url = page.src('img[src*="/comics/"]')
        title = page.alt('img[src*="/comics/"]')
        text = "\n\n".join(page.texts('table[cellpadding="5"] td')).strip()
        return CrawlerImage(url, title, text)
