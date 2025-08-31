from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Unsounded"
    language = "en"
    url = "https://unsoundedupdates.tumblr.com/"
    start_date = "2009-10-25"
    rights = "Ashley Cope"


class Crawler(CrawlerBase):
    history_capable_days = 50
    schedule = "Tu,Th,Su"
    time_zone = "America/New_York"

    def crawl(self, pub_date):
        feed = self.parse_feed("https://unsoundedupdates.tumblr.com/rss")
        for entry in feed.for_date(pub_date):
            page_url = entry.summary.href('a[href*="/comic/"]')
            if not page_url:
                continue
            page_url = page_url.replace("https://href.li/?", "")
            page = self.parse_page(page_url)
            url = page.src("#comic img")
            title = entry.title
            return CrawlerImage(url, title)
