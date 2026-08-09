from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Pickles"
    language = "en"
    url = "https://www.gocomics.com/pickles"
    start_date = "2003-10-01"
    rights = "Brian Crane"


class Crawler(GoComicsCrawlerBase):
    url_name = "pickles"
    history_capable_date = "2003-10-01"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/Denver"
