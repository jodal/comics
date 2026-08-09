from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Mutts"
    language = "en"
    url = "http://www.mutts.com"
    start_date = "1994-01-01"
    rights = "Patrick McDonnell"


class Crawler(ComicsKingdomCrawlerBase):
    url_name = "mutts"
    history_start_date = "1994-09-11"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
