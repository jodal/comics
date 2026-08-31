import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Anleggsplassen"
    language = "no"
    url = "https://www.at.no/emne/tegneserie/"
    rights = "Trond J. Stavås"


class Crawler(CrawlerBase):
    history_length_days = 100
    schedule = "Fr"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        page = self.parse_page("https://www.at.no/emne/tegneserie")
        articles = page.hrefs('article[data-section="tegneserie"] > div > a')
        for article in articles:
            article_page = self.parse_page(article)
            title = article_page.content('meta[name="title"]')
            text = article_page.content('meta[name="description"]')

            date_string = article_page.content(
                'meta[property="article:published_time"]'
            )
            if date_string is None:
                continue

            date = dt.date.fromisoformat(date_string[:10])
            if date != pub_date:
                continue

            # The comic image has no title, so select it by its container.
            # The page offers several widths, the widest one first.
            url = article_page.attr(
                "srcset", ".bodytext figure.column picture source", first=True
            )
            if url is None:
                continue

            return CrawlerImage(url, title, text)
        return None
