from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Colleges Roomies from Hell"
    language = "en"
    url = "http://www.crfh.net/"
    start_date = "1999-01-01"
    rights = "Maritza Campos"


class Crawler(CrawlerBase):
    history_capable_date = "1999-01-01"
    time_zone = "America/Merida"

    def crawl(self, pub_date):
        page_url = "http://www.crfh.net/d/%s.html" % (
            pub_date.strftime("%Y%m%d"),
        )
        page = self.parse_page(page_url)
        url = page.src('img[src*="crfh%s"]' % pub_date.strftime("%Y%m%d"))
        url = url.replace("\n", "")
        return CrawlerImage(url)
