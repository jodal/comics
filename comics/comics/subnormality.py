import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Subnormality"
    language = "en"
    url = "http://www.viruscomix.com/subnormality.html"
    start_date = "2007-01-01"
    end_date = '2019-06-07'
    rights = "Winston Rowntree"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2008-11-25"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.viruscomix.com/rss.xml")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            elements = [
                el
                for el in page.root.find("body").findall("img")
                if el.attrib["src"].endswith(".jpg")
            ]
            elements.sort(
                key=lambda el: int(
                    re.match(r".*top:\s*(\d+).*", el.attrib["style"]).group(1)
                )
            )
            result = [
                CrawlerImage(
                    el.attrib["src"], None, el.attrib.get("title", None)
                )
                for el in elements
            ]
            if result:
                result[0].title = page.text("title")
            return result
