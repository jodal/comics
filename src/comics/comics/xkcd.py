from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "xkcd"
    language = "en"
    url = "http://www.xkcd.com/"
    start_date = "2005-05-29"
    rights = "Randall Munroe, CC BY-NC 2.5"


class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = "Mo,We,Fr"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.xkcd.com/rss.xml")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)
