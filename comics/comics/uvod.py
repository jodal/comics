from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "The Unspeakable Vault (of Doom)"
    language = "en"
    url = "http://www.goominet.com/unspeakable-vault/"
    rights = "Francois Launet"


class Crawler(CrawlerBase):
    history_capable_days = 180
    time_zone = "Europe/Paris"

    def crawl(self, pub_date):
        feed = self.parse_feed(
            "http://www.goominet.com/unspeakable-vault/"
            "?type=103&ecorss[clear_cache]=1"
        )
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/tx_cenostripviewer/"]')
            title = entry.title
            return CrawlerImage(url, title)
