from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Real Life"
    language = "en"
    url = "http://www.reallifecomics.com/"
    start_date = "1999-11-15"
    rights = "Greg Dean"


class Crawler(CrawlerBase):
    history_capable_days = 30
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://reallifecomics.com/rss.php?feed=rss2")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            return CrawlerImage(url)
