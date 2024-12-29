from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Cyanide and Happiness"
    language = "en"
    url = "http://www.explosm.net/comics/"
    start_date = "2005-01-26"
    rights = "Kris Wilson, Rob DenBleyker, Matt Melvin, & Dave McElfatrick "


class Crawler(CrawlerBase):
    history_capable_days = 7
    schedule = "Mo,Tu,We,Fr,Sa,Su"
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        feed = self.parse_feed("http://feeds.feedburner.com/Explosm")
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src("img#main-comic")
            return CrawlerImage(url)
