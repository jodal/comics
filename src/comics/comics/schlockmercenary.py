from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Schlock Mercenary"
    language = "en"
    url = "http://www.schlockmercenary.com/"
    start_date = "2000-06-12"
    rights = "Howard Tayler"


class Crawler(CrawlerBase):
    history_capable_date = "2000-06-12"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"

    def crawl(self, pub_date):
        page_url = "http://www.schlockmercenary.com/%s" % pub_date.strftime("%Y-%m-%d")
        page = self.parse_page(page_url)
        return [CrawlerImage(url) for url in page.srcs("#comic img")]
