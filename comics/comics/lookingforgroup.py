from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Looking For Group"
    language = "en"
    url = "http://www.lfgcomic.com/"
    start_date = "2006-11-06"
    rights = "Ryan Sohmer & Lar deSouza"


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = "Mo,Th"
    time_zone = "America/Montreal"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/LookingForGroup")
        for entry in feed.for_date(pub_date):
            if not entry.title.isdigit():
                continue
            page = self.parse_page(entry.link)
            if not page.text("title").startswith("Looking For Group"):
                continue
            url = page.src("#comic img")
            title = entry.title
            return CrawlerImage(url, title)
