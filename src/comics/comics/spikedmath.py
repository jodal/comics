from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Spiked Math"
    language = "en"
    url = "http://www.spikedmath.com/"
    start_date = "2009-08-24"
    rights = "Mike, CC BY-NC-SA 2.5"


class Crawler(CrawlerBase):
    history_capable_days = 20
    time_zone = "America/Denver"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/SpikedMath")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            urls = page.srcs('div.asset-body img[src*="/comics/"]')
            result = [
                CrawlerImage(url, title=(entry.title if i == 0 else None))
                for i, url in enumerate(urls)
            ]
            return result
