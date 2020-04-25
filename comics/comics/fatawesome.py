from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Fatawesome"
    language = "en"
    url = "http://www.fatawesome.com/"
    start_date = "2014-09-16"
    rights = "James Craig"


class Crawler(CrawlerBase):
    history_capable_date = "2014-09-16"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.fatawesome.com/feed/")
        for entry in feed.for_date(pub_date):
            if "Comics" not in entry.tags:
                continue
            url = entry.content0.src("img")
            title = entry.title
            text = entry.content0.alt("img")
            return CrawlerImage(url, title, text)
