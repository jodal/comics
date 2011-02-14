# encoding: utf-8

from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Radio Gaga (pondus.no)'
    language = 'no'
    url = 'http://pondus.no/#CartoonGallery'
    rights = 'Øyvind Sagåsen'

class Crawler(PondusNoCrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Fr'

    def crawl(self, pub_date):
        return self.crawl_helper('Radio-Gaga', pub_date)


