import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Optipess"
    language = "en"
    url = "http://www.optipess.com/"
    start_date = "2008-12-01"
    rights = "Kristian Nygård"


class Crawler(CrawlerBase):
    history_start_date = "2008-12-01"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        # Find the post for the requested date
        archive_page = self.parse_page(
            f"https://www.optipess.com/archive/?archive_year={pub_date:%Y}"
        )
        date_string = pub_date.strftime("%b %-d")

        for row in archive_page.elements("tr"):
            if row.text("td.archive-date") != date_string:
                continue

            title = row.text("td.archive-title a")
            post_url = row.href("td.archive-title a")
            if post_url is None:
                return None

            # Fetch the actual post
            page = self.parse_page(post_url)
            # The image is sometimes wrapped in a link
            url = page.src("div#comic img", first=True)
            text = page.title("div#comic img", first=True)

            return CrawlerImage(url, title, text)

        return None
