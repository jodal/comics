# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.comics.pondus import ComicData as PondusData


class ComicData(PondusData):
    name = "Pondus (bt.no)"
    url = "https://www.bt.no/kultur/tegneserier/"


class Crawler(CrawlerBase):
    history_capable_date = "2008-07-01"
    schedule = "Mo,Tu,We,Th,Fr,Sa"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        url = "https://cartoon-prod.schibsted.tech/pondus/%s.gif" % (
            pub_date.strftime("%d%m%y"),
        )
        return CrawlerImage(url)
