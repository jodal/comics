import re
from datetime import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Anleggsplassen"
    language = "no"
    url = "https://www.at.no"
    rights = "Trond J. Stavås"


class Crawler(CrawlerBase):
    history_capable_days = 7 * 9
    schedule = "Fr"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        page = self.parse_page(ComicData.url)
        div = page.root.xpath('//h5[.="Anleggsplassen"]/..')
        articles = div[0].xpath(".//ul/li/a/@href")
        for article in articles:
            article_page = self.parse_page(article)
            title = article_page.content('meta[name="title"]')
            text = article_page.content('meta[name="description"]')

            date_string = article_page.content(
                'meta[property="article:published_time"]'
            )
            date = datetime.strptime(date_string[:10], "%Y-%m-%d").date()
            if date != pub_date:
                continue

            url = re.sub(
                r"(http.+imageId=\d+).+",
                r"\1&x=0&y=0&cropw=100&croph=100&width=1037&height=396",
                article_page.content('meta[property="og:image"]'),
            )

            return CrawlerImage(url, title, text)
