from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The DaneMen"
    language = "en"
    url = "http://www.webtoons.com/en/comedy/the-danemen/list?title_no=395"
    start_date = "2015-03-02"
    rights = "David Danemen"
    active = False


class Crawler(CrawlerBase):
    has_rerun_releases = True  # Not really, but reuses same image in a release
    history_capable_date = "2017-08-26"
    schedule = "Mo,Sa"
    time_zone = "America/Los_Angeles"

    headers = {
        "Referer": "http://www.webtoons.com/",
    }

    def crawl(self, pub_date):
        feed = self.parse_feed(
            "http://www.webtoons.com/en/comedy/the-danemen/rss?title_no=395"
        )
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            urls = page._get("data-url", "#_imageList img", allow_multiple=True)
            images = [CrawlerImage(url) for url in urls]
            if images:
                images.pop(0)  # Remove The DaneMen logo
                images.pop()  # Remove Web Toon logo
            if images:
                images[0].title = entry.title
                return images
