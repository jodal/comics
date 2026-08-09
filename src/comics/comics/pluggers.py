from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Pluggers"
    language = "en"
    url = "http://www.gocomics.com/pluggers"
    start_date = "2001-04-08"
    rights = "Gary Brookins"


class Crawler(GoComicsCrawlerBase):
    url_name = "pluggers"
    history_capable_date = "2001-04-08"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
