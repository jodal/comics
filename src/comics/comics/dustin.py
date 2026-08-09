from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Dustin"
    language = "en"
    url = "https://www.comicskingdom.com/dustin"
    start_date = "2010-01-04"
    rights = "Steve Kelley & Jeff Parker"


class Crawler(ComicsKingdomCrawlerBase):
    url_name = "dustin"
    history_capable_date = "2010-01-04"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
