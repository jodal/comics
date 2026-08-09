from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Hägar the Horrible"
    language = "en"
    url = "https://www.comicskingdom.com/hagar-the-horrible"
    rights = "Chris Browne"


class Crawler(ComicsKingdomCrawlerBase):
    url_name = "hagar-the-horrible"
    history_capable_date = "1998-10-05"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
