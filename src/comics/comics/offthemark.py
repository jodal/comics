from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Off the Mark"
    language = "en"
    url = "https://www.gocomics.com/offthemark"
    start_date = "2002-09-02"
    rights = "Mark Parisi"


class Crawler(GoComicsCrawlerBase):
    url_name = "offthemark"
    history_capable_date = "2002-09-02"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
