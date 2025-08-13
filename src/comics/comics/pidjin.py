from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Fredo & Pid'jin"
    language = "en"
    url = "http://www.pidjin.net/"
    start_date = "2006-02-19"
    rights = "Tudor Muscalu & Eugen Erhan"


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/Pidjin")
        for entry in feed.for_date(pub_date):
            urls = [
                url
                for url in entry.content0.srcs('img[src*="/wp-content/uploads/"]')
                if (
                    "ad-RSS" not in url
                    and "ad5RSS" not in url
                    and "reddit-txt" not in url
                    and "rss-box" not in url
                )
            ]
            return [
                CrawlerImage(url, None, entry.content0.alt('img[src="%s"]' % url))
                for url in urls
            ]
