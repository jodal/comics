import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Wumo"
    language = "en"
    url = "http://wumo.com/wumo/"
    start_date = "2001-01-01"
    rights = "Mikael Wulff & Anders Morgenthaler"


class Crawler(CrawlerBase):
    history_capable_date = "2013-01-15"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "Europe/Copenhagen"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        page_url = f"http://wumo.com/wumo/{pub_date:%Y/%m/%d}"
        page = self.parse_page(page_url)
        urls = page.srcs(f'img[src*="/img/wumo/{pub_date:%Y/%m}"]')
        if not urls:
            return None
        return CrawlerImage(urls[0])
