from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Free Range"
    language = "en"
    url = "https://www.gocomics.com/freerange"
    rights = "Bill Whitehead"


class Crawler(GoComicsCrawlerBase):
    url_name = "freerange"
    history_start_date = "2007-02-03"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
