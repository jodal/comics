from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Garfield"
    language = "en"
    url = "http://www.garfield.com/"
    start_date = "1978-06-19"
    rights = "Jim Davis"


class Crawler(CrawlerBase):
    history_capable_days = 100
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "US/Eastern"

    def crawl(self, pub_date):
        if pub_date.weekday() == 6:
            url = "http://picayune.uclick.com/comics/ga/%s.jpg" % (
                pub_date.strftime("%Y/ga%y%m%d"),
            )
        else:
            url = "http://images.ucomics.com/comics/ga/%s.gif" % (
                pub_date.strftime("%Y/ga%y%m%d"),
            )
        return CrawlerImage(url)
