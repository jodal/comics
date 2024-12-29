# noqa: N999

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Twenty Pixels"
    language = "en"
    url = "http://20px.com/"
    start_date = "2011-02-11"
    rights = "Angela"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/20px")
        for entry in feed.for_date(pub_date):
            if "Comic" not in entry.tags:
                continue
            selector = 'img[src*="/wp-content/uploads/"]:not(img[src$="_sq.jpg"])'
            results = []

            for url in entry.content0.src(selector, allow_multiple=True):
                results.append(CrawlerImage(url))

            if results:
                results[0].title = entry.title
                results[0].text = entry.content0.alt(selector, allow_multiple=True)[0]
                return results
