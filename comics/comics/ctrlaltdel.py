from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ctrl+Alt+Del"
    language = "en"
    url = "https://cad-comic.com/category/ctrl-alt-del/"
    start_date = "2002-10-23"
    rights = "Tim Buckley"


class Crawler(CrawlerBase):
    # history_capable_date = "2002-10-23"
    history_capable_days = 20
    schedule = "Mo,We,Fr"
    time_zone = "US/Eastern"

    # Without User-Agent set, the server returns empty responses
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("https://cad-comic.com/feed/")

        for entry in feed.for_date(pub_date):
            url = entry.summary.src("img")
            title = entry.title
            return CrawlerImage(url, title)
