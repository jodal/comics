import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sinfest"
    language = "en"
    url = "https://sinfest.xyz/"
    start_date = "2001-01-17"
    rights = "Tatsuya Ishida"


class Crawler(CrawlerBase):
    history_capable_date = "2001-01-17"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        url = f"https://sinfest.xyz/btphp/comics/{pub_date}.jpg"
        return CrawlerImage(url)
