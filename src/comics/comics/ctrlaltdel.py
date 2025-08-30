from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ctrl+Alt+Del"
    language = "en"
    url = "https://cad-comic.com/category/ctrl-alt-del/"
    start_date = "2002-10-23"
    rights = "Tim Buckley"


class Crawler(CrawlerBase):
    history_capable_days = 20
    schedule = "Mo,We,Fr"
    time_zone = "America/New_York"

    # Without User-Agent set, the server returns empty responses
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        feed = self.parse_feed("https://cad-comic.com/feed/")

        for entry in feed.for_date(pub_date):
            if "Ctrl Alt Del" not in entry.tags:
                continue
            page = self.parse_page(entry.link)
            url = page.src(".comicpage img[src*='/uploads/']")
            title = entry.title
            return CrawlerImage(url, title)
