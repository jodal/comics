from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Manly Guys Doing Manly Things"
    language = "en"
    url = "http://thepunchlineismachismo.com/"
    start_date = "2005-05-29"
    rights = "Kelly Turnbull, CC BY-NC-SA 3.0"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 60
    schedule = "Mo"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://thepunchlineismachismo.com/feed")
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/wp-content/uploads/"]')
            if url is not None:
                url = url.replace("-150x150", "")
                title = entry.title
                return CrawlerImage(url, title)
