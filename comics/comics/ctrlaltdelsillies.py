from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ctrl+Alt+Del Sillies"
    language = "en"
    url = "http://www.cad-comic.com/sillies/"
    start_date = "2008-06-27"
    rights = "Tim Buckley"


class Crawler(CrawlerBase):
    history_capable_date = "2008-06-27"
    schedule = None
    time_zone = "US/Eastern"

    # Without User-Agent set, the server returns empty responses
    headers = {"User-Agent": "Mozilla/4.0"}

    def crawl(self, pub_date):
        page = self.parse_page(
            "http://www.cad-comic.com/sillies/%s" % pub_date.strftime("%Y%m%d")
        )
        url = page.src('img[src*="/comics/"]')
        return CrawlerImage(url)
