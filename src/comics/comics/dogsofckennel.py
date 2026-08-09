from comics.aggregator.crawler import CreatorsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Dogs of C-Kennel"
    language = "en"
    url = "https://www.creators.com/read/dogs-of-c-kennel"
    rights = "Mason Mastroianni, Mick Mastroianni, Johnny Hart"


class Crawler(CreatorsCrawlerBase):
    url_id = "179"
    history_capable_date = "2007-02-12"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Los_Angeles"
