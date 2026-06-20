from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Perry Bible Fellowship"
    language = "en"
    url = "https://www.pbfcomics.com/"
    start_date = "2001-01-01"
    rights = "Nicholas Gurewitch"


class Crawler(CrawlerBase):
    history_capable_date = "2019-06-12"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://pbfcomics.com/feed/")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            urls = [
                img.attrib["data-src"]
                for img in page.root.findall('.//div[@id="comic"]/img')
            ]
            return [CrawlerImage(url, entry.title) for url in urls]
