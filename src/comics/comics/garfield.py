from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Garfield"
    language = "en"
    url = "https://www.gocomics.com/garfield"
    start_date = "1978-06-19"
    rights = "Jim Davis"


class Crawler(GoComicsCrawlerBase):
    url_name = "garfield"
    history_capable_date = "1978-06-19"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
