# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Lunch (dn.no)"
    language = "no"
    url = "https://www.dn.no/topic/Lunch/"
    active = True
    rights = "Børge Lund"


class Crawler(CrawlerBase):
    history_capable_days = 21  # 3 weeks
    schedule = "Fr"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        page = self.parse_page(ComicData.url)
        page_url = page.root.xpath(
            '//time[@datetime="%s"]/../a/@href' % pub_date.strftime("%Y-%m-%d")
        )
        if not page_url:
            return

        release_page = self.parse_page(page_url[0])
        image = release_page.root.xpath('//meta[@itemprop="image"]')
        if not image:
            return
        url = image[0].get("content")

        return CrawlerImage(url)
