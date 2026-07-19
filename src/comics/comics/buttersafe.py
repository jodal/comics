import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Buttersafe"
    language = "en"
    url = "http://buttersafe.com/"
    start_date = "2007-04-03"
    rights = "Alex Culang & Raynato Castro"


class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = "Th"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        date_page_url = f"https://www.buttersafe.com/{pub_date:%Y/%m/%d/}"
        date_page = self.parse_page(date_page_url)
        page_url = date_page.href(f"a[href^='{date_page_url}']")
        if not page_url:
            return None
        page = self.parse_page(page_url)
        url = page.src(".comic img")
        if not url:
            return None
        title = page.alt(".comic img")
        return CrawlerImage(url, title)
