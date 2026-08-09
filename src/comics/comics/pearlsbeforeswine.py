from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Pearls Before Swine"
    language = "en"
    url = "https://www.gocomics.com/pearlsbeforeswine"
    start_date = "2001-12-30"
    rights = "Stephan Pastis"


class Crawler(GoComicsCrawlerBase):
    url_name = "pearlsbeforeswine"
    history_capable_date = "2002-01-06"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
