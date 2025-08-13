from datetime import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Anleggsplassen"
    language = "no"
    url = "https://www.at.no/emne/tegneserie/"
    rights = "Trond J. Stavås"


class Crawler(CrawlerBase):
    history_capable_days = 100
    schedule = "Fr"
    time_zone = "Europe/Oslo"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    }

    def crawl(self, pub_date):
        page = self.parse_page("https://www.at.no/emne/tegneserie")
        articles = page.root.xpath('.//article[@data-section="tegneserie"]/div/a/@href')
        for article in articles:
            article_page = self.parse_page(article)
            title = article_page.content('meta[name="title"]')
            text = article_page.content('meta[name="description"]')

            date_string = article_page.content(
                'meta[property="article:published_time"]'
            )
            if date_string is None:
                continue

            date = datetime.strptime(date_string[:10], "%Y-%m-%d").date()
            if date != pub_date:
                continue

            img = article_page.root.xpath('//img[@title="%s"]/@src' % title)
            url = str(img[0])

            return CrawlerImage(url, title, text)
