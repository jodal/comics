from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.aggregator.exceptions import CrawlerError
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Sinfest"
    language = "en"
    url = "https://sinfest.xyz/"
    start_date = "2001-01-17"
    rights = "Tatsuya Ishida"


class Crawler(CrawlerBase):
    history_capable_date = "2001-01-17"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        try:
            url = "https://sinfest.xyz/btphp/comics/{}.jpg".format(
                pub_date.strftime("%Y-%m-%d"),
            )
            return CrawlerImage(url)
        except CrawlerError:  # Some releases use gif
            url = "https://sinfest.xyz/btphp/comics/{}.gif".format(
                pub_date.strftime("%Y-%m-%d"),
            )
            return CrawlerImage(url)
