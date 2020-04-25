from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Three Panel Soul"
    language = "en"
    url = "http://www.threepanelsoul.com/"
    start_date = "2006-11-05"
    rights = "Ian McConville & Matt Boyd"


class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = "Mo"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.threepanelsoul.com/rss.php")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src("img#cc-comic")
            if url is None:
                continue
            title = page.text("#comictitle")
            return CrawlerImage(url, title)
