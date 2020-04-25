from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Super Effective"
    language = "en"
    url = "http://www.vgcats.com/super/"
    start_date = "2008-04-23"
    rights = "Scott Ramsoomair"


class Crawler(CrawlerBase):
    history_capable_date = "2008-04-23"
    time_zone = "US/Eastern"

    # Without User-Agent set, the server returns empty responses
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        url = "http://www.vgcats.com/super/images/%s.gif" % (
            pub_date.strftime("%y%m%d"),
        )
        return CrawlerImage(url)
