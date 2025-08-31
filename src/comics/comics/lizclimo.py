from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Hi, I'm Liz"
    language = "en"
    url = "https://lizclimo.tumblr.com/"
    start_date = "2011-12-15"
    rights = "Liz Climo"


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://lizclimo.tumblr.com/rss")
        for entry in feed.for_date(pub_date):
            if "comics" not in entry.tags:
                continue
            page = self.parse_page(entry.link)
            url = page.src(".post_media_photo")
            return CrawlerImage(url)
