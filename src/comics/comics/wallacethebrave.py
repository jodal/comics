from comics.aggregator.crawler import GoComicsCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Wallace the Brave"
    language = "en"
    url = "https://www.gocomics.com/wallace-the-brave"
    rights = "Will Henry"


class Crawler(GoComicsCrawlerBase):
    url_name = "wallace-the-brave"
    history_start_date = "2015-06-29"
    schedule = "Mo,Tu,We,Th,Fr,Sa,Su"
    time_zone = "America/New_York"
