from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Gunnerkrigg Court"
    language = "en"
    url = "http://www.gunnerkrigg.com/"
    start_date = "2005-08-13"
    rights = "Tom Siddell"


class Crawler(CrawlerBase):
    schedule = "Mo,We,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        page = self.parse_page("http://www.gunnerkrigg.com/index2.php")
        url = page.src('img[src*="/comics/"]')
        title = page.alt('img[src*="/comics/"]')
        text = ""
        for content in page.text('table[cellpadding="5"] td', allow_multiple=True):
            text += content + "\n\n"
        text = text.strip()
        return CrawlerImage(url, title, text)
