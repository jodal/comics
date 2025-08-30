import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Questionable Content"
    language = "en"
    url = "https://questionablecontent.net/"
    start_date = "2003-08-01"
    rights = "Jeph Jacques"


class Crawler(CrawlerBase):
    history_capable_days = 0
    schedule = "Mo,Tu,We,Th,Fr"
    time_zone = "America/New_York"

    # Without User-Agent set, the server returns 403 Forbidden
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        page = self.parse_page("https://questionablecontent.net/")
        url = page.src("img[src*='/comics/']")
        title = None
        page.remove("#news p, #news script")
        text = page.text("#news")
        if text:
            text = re.sub(r"\s{2,}", "\n\n", text).strip()
        return CrawlerImage(url, title, text)
