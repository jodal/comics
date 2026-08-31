import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Wumo"
    language = "en"
    url = "http://wumo.com/wumo/"
    start_date = "2001-01-01"
    rights = "Mikael Wulff & Anders Morgenthaler"


class Crawler(CrawlerBase):
    history_start_date = "2013-01-15"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "Europe/Copenhagen"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        page_url = f"http://wumo.com/wumo/{pub_date:%Y/%m/%d}"
        page = self.parse_page(page_url)
        url = page.src(f'img[src*="/img/wumo/{pub_date:%Y/%m}"]', first=True)
        if url is None:
            return None
        return CrawlerImage(url)
