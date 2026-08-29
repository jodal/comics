import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Penny Arcade"
    language = "en"
    url = "https://penny-arcade.com/"
    start_date = "1998-11-18"
    rights = "Mike Krahulik & Jerry Holkins"


class Crawler(CrawlerBase):
    history_start_date = "1998-11-18"
    schedule = "Mo,We,Fr"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        page_url = f"https://penny-arcade.com/comic/{pub_date:%Y/%m/%d}"
        page = self.parse_page(page_url)
        title = page.content('meta[property="og:title"]', default="")
        title = title.replace(" - Penny Arcade", "")
        url = page.content('meta[property="og:image"]', default="")
        # The site gives a 404 page without a real 404 code
        if title == "Not Found (#404)":
            return None
        return CrawlerImage(url, title)
