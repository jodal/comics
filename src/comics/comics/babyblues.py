from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Baby Blues"
    language = "en"
    url = "https://www.gocomics.com/babyblues"
    start_date = "1990-01-01"
    rights = "Rick Kirkman and Jerry Scott"


class Crawler(GoComicsCrawlerBase):
    url_name = "babyblues"
    history_capable_date = "2011-11-26"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
