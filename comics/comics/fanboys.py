from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "F@NB0Y$"
    language = "en"
    url = "http://www.fanboys-online.com/"
    start_date = "2006-04-19"
    rights = "Scott Dewitt"


class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = "Mo,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.fanboys-online.com/rss.php")
        for entry in feed.for_date(pub_date):
            title = entry.title.replace("Fanboys - ", "")
            page = self.parse_page(entry.link)
            url = page.src("img#comic")
            if not url:
                continue
            url = url.replace(" ", "%20")
            return CrawlerImage(url, title)
