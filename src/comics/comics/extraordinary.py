from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Extra Ordinary"
    language = "en"
    url = "https://www.exocomics.com/"
    start_date = "2009-12-14"
    rights = "Li Chen"


class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = "We"
    time_zone = "Pacific/Auckland"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://www.exocomics.com/index.xml")
        for entry in feed.for_date(pub_date):
            url = entry.content0.src("img")
            title = entry.title
            text = "\n\n".join(entry.summary.texts("p"))
            return CrawlerImage(url, title, text)
