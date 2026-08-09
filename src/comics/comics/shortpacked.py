from comics.aggregator.crawler import ComicControlCrawlerBase
from comics.core.metadata import MetadataBase


class Metadata(MetadataBase):
    name = "Shortpacked"
    language = "en"
    url = "http://www.shortpacked.com/"
    start_date = "2005-01-17"
    rights = "David Willis"


class Crawler(ComicControlCrawlerBase):
    base_url = Metadata.url
    schedule = "Mo,We,Fr"
    history_capable_days = 32
    time_zone = "America/New_York"
