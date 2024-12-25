from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "User Friendly"
    language = "en"
    url = "http://www.userfriendly.org/"
    start_date = "1997-11-17"
    rights = 'J.D. "Illiad" Frazer'


class Crawler(CrawlerBase):
    has_rerun_releases = True
    history_capable_date = "1997-11-17"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Vancouver"

    def crawl(self, pub_date):
        page_url = "http://ars.userfriendly.org/cartoons/?id={}".format(
            pub_date.strftime("%Y%m%d"),
        )
        page = self.parse_page(page_url)
        url = page.src('img[alt^="Strip for"]')
        if not url:  # Old releases
            url = page.src('img[src^="http://www.userfriendly.org/cartoons/archives/"]')
        return CrawlerImage(url)
