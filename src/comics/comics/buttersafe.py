from comics.aggregator.crawler import CrawlerBase, CrawlerImage
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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }

    def crawl(self, pub_date):
        date_page_url = f"https://www.buttersafe.com/{pub_date:%Y/%m/%d/}"
        date_page = self.parse_page(date_page_url)
        page_url = date_page.href(f"a[href^='{date_page_url}']")
        if not page_url:
            return
        page = self.parse_page(page_url)
        url = page.src(".comic img")
        if not url:
            return
        title = page.alt(".comic img")
        return CrawlerImage(url, title)
