from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Peanuts"
    language = "en"
    url = "https://www.gocomics.com/peanuts"
    start_date = "1950-10-02"
    end_date = "2000-02-13"
    rights = "Charles M. Schulz"


class Crawler(GoComicsCrawlerBase):
    url_name = "peanuts"
    history_capable_date = "1950-10-02"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
