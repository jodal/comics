import datetime as dt
import re

from lxml.html import HtmlElement

from comics.aggregator.crawler import CrawlerBase, CrawlerImage, CrawlerResult
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Subnormality"
    language = "en"
    url = "http://www.viruscomix.com/subnormality.html"
    start_date = "2007-01-01"
    end_date = "2019-06-07"
    rights = "Winston Rowntree"
    active = False


class Crawler(CrawlerBase):
    history_capable_date = "2008-11-25"
    time_zone = "America/New_York"

    def crawl(self, pub_date: dt.date) -> CrawlerResult:
        feed = self.parse_feed("http://www.viruscomix.com/rss.xml")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            body = page.root.find("body")
            assert body is not None
            elements = [
                el for el in body.findall("img") if el.attrib["src"].endswith(".jpg")
            ]

            def sort_key(el: HtmlElement) -> int:
                match = re.match(r".*top:\s*(\d+).*", el.attrib["style"])
                assert match is not None
                return int(match.group(1))

            elements.sort(key=sort_key)
            result = [
                CrawlerImage(el.attrib["src"], None, el.attrib.get("title", None))
                for el in elements
            ]
            if result:
                result[0].title = page.text("title")
            return result
        return None
