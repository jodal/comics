from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Hjalmar (bt.no)"
    language = "no"
    url = "https://www.bt.no/kultur/tegneserier/"
    rights = "Nils Axle Kanten"


class Crawler(CrawlerBase):
    history_capable_date = "2013-01-15"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"

    def crawl(self, pub_date):
        url = "https://cartoon-prod.schibsted.tech/rocky/%s.gif" % (
            pub_date.strftime("%d%m%y"),
        )
        return CrawlerImage(url)
