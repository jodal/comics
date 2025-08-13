from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Exiern"
    language = "en"
    url = "http://www.exiern.com/"
    start_date = "2005-09-06"
    rights = "Dan Standing"


class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = "Tu,Th"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://www.exiern.com/?feed=rss2")
        for entry in feed.for_date(pub_date):
            urls = entry.summary.srcs("img")
            if not urls:
                continue
            url = urls[0].replace("comics-rss", "comics")
            title = entry.title
            return CrawlerImage(url, title)
